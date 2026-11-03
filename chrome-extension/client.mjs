import { endpoint, pairingToken, authAnswer, micFrame, MAX_BUFFERED } from './protocol.mjs';

// One connection owns one approval. Any fault closes it; never auto-reconnect/key.
export class TabClient {
  constructor({ changed = () => {}, ended = () => {}, socket = url => new WebSocket(url, 'hermitsdr-control.v1'),
                now = () => performance.now() } = {}) {
    Object.assign(this, { changed, ended, socket, now });
    this.state = { phase: 'disconnected', allowed: false, error: '', peak: 0, sent: 0 };
    this.pending = new Map(); this.nextId = 1;
  }
  publish(update) { Object.assign(this.state, update); this.changed({ ...this.state }); }
  async connect({ host, code, clientId }) {
    if (this.ws) throw new Error('Disconnect before pairing again.');
    const token = pairingToken(code), url = endpoint(host);
    const hello = JSON.stringify({ t: 'hello', apiVersion: 1, clientId,
      name: 'HermitSDR Tab Audio', platform: 'chrome-extension', features: ['control'] });
    this.publish({ phase: 'connecting', allowed: false, error: '', sent: 0 });
    const ws = this.ws = this.socket(url);
    ws.binaryType = 'arraybuffer';
    return new Promise((resolve, reject) => {
      let stage = 'challenge';
      const timer = setTimeout(() => this.fail('Pairing timed out. Check host, certificate and pairing code.'), 8000);
      this.connectReject = reject;
      this.connectTimer = timer;
      ws.onopen = () => { if (this.ws === ws) ws.send(hello); };
      ws.onerror = () => { if (this.ws === ws) this.fail('Cannot reach HermitSDR. Check TLS certificate trust and Local Network permission.'); };
      ws.onclose = () => { if (this.ws === ws) this.fail('Station disconnected. Pair and approve again.'); };
      ws.onmessage = async event => {
        if (this.ws !== ws || typeof event.data !== 'string') return;
        try {
          const m = JSON.parse(event.data);
          if (m.t === 'error' || m.t === 'bye') throw new Error(m.message || m.reason || m.code || 'Station refused the request.');
          if (stage === 'challenge') {
            stage = 'auth';
            const answer = await authAnswer(token, hello, event.data);
            token.fill(0);
            if (this.ws === ws) ws.send(JSON.stringify({ t: 'auth', answer }));
          } else if (stage === 'auth') {
            if (m.t !== 'welcome' || m.apiVersion !== 1 || m.apiRevision < 3 || !m.granted?.includes('control')) {
              throw new Error('HermitSDR Control API revision 3 and the Control grant are required.');
            }
            if (m.radio?.txCapable !== true) throw new Error('This station session is receive-only. Connect to a TX-capable live radio.');
            stage = 'paired'; clearTimeout(timer); this.connectReject = null;
            this.publish({ phase: 'paired', allowed: false }); resolve();
            this.heartbeat = setInterval(() => {
              if (this.state.phase === 'paired') this.request({ t: 'ping', ts: Date.now() }).catch(e => this.fail(e.message));
            }, 10000);
          } else if (m.t === 'txPermission') {
            this.publish({ allowed: m.allowed === true });
            if (!m.allowed && ['capturing', 'starting', 'transmitting'].includes(this.state.phase)) this.fail('TX permission was removed at the station.');
          } else if (m.t === 'ack' || m.t === 'pong') {
            const p = this.pending.get(m.id);
            if (p) { this.pending.delete(m.id); clearTimeout(p.timer); p.resolve(m); }
          }
        } catch (e) { if (this.ws === ws) this.fail(e.message); }
      };
    });
  }
  request(message, timeout = 1500) {
    if (!this.ws || this.ws.readyState !== 1) return Promise.reject(new Error('Station is disconnected.'));
    if (this.ws.bufferedAmount >= MAX_BUFFERED) return Promise.reject(new Error('Network backlog: transmission stopped.'));
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => { this.pending.delete(id); reject(new Error('Station acknowledgement timed out.')); }, timeout);
      this.pending.set(id, { resolve, reject, timer });
      try { this.ws.send(JSON.stringify({ ...message, id })); }
      catch (e) { this.pending.delete(id); clearTimeout(timer); reject(e); }
    });
  }
  async begin() {
    if (!['paired', 'capturing'].includes(this.state.phase) || !this.state.allowed) throw new Error('ARM locally and allow TX for this connected session first.');
    this.publish({ phase: 'starting', sent: 0 });
    await this.request({ t: 'micConfig', sampleRate: 48000, channels: 1, sampleCount: 480, codec: 'pcm16' });
    if (this.state.phase !== 'starting') throw new Error('Start cancelled.');
    await this.request({ t: 'ptt', down: true }, 250);
    if (this.state.phase !== 'starting') throw new Error('Start cancelled.');
    this.sequence = 0;
    this.lastTick = this.lastAudio = this.now();
    this.publish({ phase: 'transmitting' });
    this.lease = setInterval(() => {
      const now = this.now();
      if (now - this.lastTick > 250 || now - this.lastAudio > 120) return this.fail('Audio or lease clock stalled. Pair and approve again.');
      this.lastTick = now;
      this.request({ t: 'txLease' }, 250).catch(e => this.fail(e.message));
    }, 100);
  }
  audio(pcm, peak = 0) {
    if (this.state.phase !== 'transmitting') return;
    try {
      if (!this.ws || this.ws.readyState !== 1 || this.ws.bufferedAmount >= MAX_BUFFERED || this.now() - this.lastAudio > 120) {
        throw new Error('Audio/network backlog: transmission stopped.');
      }
      this.ws.send(micFrame(pcm, this.sequence++)); this.lastAudio = this.now();
      this.state.sent += pcm.byteLength; this.state.peak = peak;
    } catch (e) { this.fail(e.message); }
  }
  stop(reason = 'Stopped. Pair and approve to transmit again.') {
    // Close even if PTT-up cannot get through: the host lease also expires.
    const ws = this.ws; this.ws = null;
    clearTimeout(this.connectTimer); clearInterval(this.heartbeat); clearInterval(this.lease);
    for (const p of this.pending.values()) { clearTimeout(p.timer); p.reject(new Error(reason)); }
    this.pending.clear();
    this.connectReject?.(new Error(reason)); this.connectReject = null;
    if (ws) {
      try { if (ws.readyState === 1) ws.send(JSON.stringify({ t: 'ptt', down: false })); } catch {}
      try { ws.close(1000, 'stopped'); } catch {}
    }
    this.publish({ phase: 'disconnected', allowed: false, peak: 0, error: reason }); this.ended();
  }
  fail(reason) { if (this.ws) this.stop(reason); }
}
