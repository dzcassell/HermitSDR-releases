import { TabClient } from './client.mjs';
let ctx, stream, source, worklet, monitorNode;
let generation = 0, preparing = false, capturedTabId = null;
const client = new TabClient({
  changed: state => chrome.runtime.sendMessage({ target: 'background', type: 'state', state }).catch(() => {}),
  ended: () => teardown(),
});
function teardown() {
  generation++; preparing = false; capturedTabId = null;
  if (worklet) { worklet.port.onmessage = null; worklet.disconnect(); }
  source?.disconnect(); monitorNode?.disconnect();
  stream?.getTracks().forEach(track => { track.onended = null; track.stop(); });
  ctx?.close().catch(() => {});
  ctx = stream = source = worklet = monitorNode = null;
}
async function capture(msg) {
  if (preparing || ctx) throw new Error('Tab capture is already starting or active.');
  if (client.state.phase !== 'paired' || !client.state.allowed) throw new Error('Allow TX this session at the station first.');
  preparing = true; capturedTabId = msg.tabId;
  client.publish({ phase: 'capturing' });
  const epoch = ++generation;
  const timeout = setTimeout(() => { if (epoch === generation) client.fail('Tab audio did not start.'); }, 5000);
  try {
    const captured = await navigator.mediaDevices.getUserMedia({ audio: {
      mandatory: { chromeMediaSource: 'tab', chromeMediaSourceId: msg.streamId } }, video: false });
    if (epoch !== generation) { captured.getTracks().forEach(t => t.stop()); return; }
    stream = captured;
    stream.getTracks().forEach(t => { t.onended = () => {
      if (epoch === generation) client.fail('Captured tab closed or capture ended.');
    }; });
    ctx = new AudioContext({ sampleRate: 48000 });
    if (ctx.sampleRate !== 48000) throw new Error('48 kHz capture is required.');
    await ctx.audioWorklet.addModule('pcm-worklet.js');
    if (epoch !== generation) return;
    source = ctx.createMediaStreamSource(stream);
    monitorNode = ctx.createGain(); monitorNode.gain.value = msg.monitor ? 1 : 0;
    source.connect(monitorNode).connect(ctx.destination);
    worklet = new AudioWorkletNode(ctx, 'hermit-pcm', { outputChannelCount: [1] });
    worklet.parameters.get('gain').value = msg.gain / 100;
    source.connect(worklet).connect(ctx.destination);
    let prime = [], keying = false;
    worklet.port.onmessage = async ({ data }) => {
      if (epoch !== generation) return;
      if (ctx.currentTime - data.time > 0.06) return client.fail('Queued audio expired. Pair and approve again.');
      if (client.state.phase === 'transmitting') return client.audio(data.pcm, data.peak);
      // Establish flowing audio BEFORE asking for a key, and bound pending PCM.
      prime.push(data);
      if (prime.length > 10) return client.fail('Station did not start in time.');
      if (prime.length >= 3 && !keying) {
        keying = true;
        try {
          await client.begin();
          if (epoch !== generation) return;
          clearTimeout(timeout); preparing = false;
          // Only the newest 30 ms may prime the host, never replay startup delay.
          for (const frame of prime.slice(-3)) client.audio(frame.pcm, frame.peak);
          prime = [];
        } catch (e) { if (epoch === generation) client.fail(e.message); }
      }
    };
    await ctx.resume();
  } catch (e) { if (epoch === generation) client.fail('Tab capture failed: ' + e.message); throw e; }
  finally { if (epoch !== generation) clearTimeout(timeout); }
}
chrome.runtime.onMessage.addListener((msg, sender, reply) => {
  if (sender.id !== chrome.runtime.id || msg?.target !== 'offscreen') return;
  (async () => {
    switch (msg.type) {
      case 'connect': await client.connect(msg); break;
      case 'start': await capture(msg); break;
      case 'stop': client.stop(); break;
      case 'status': return { ok: true, state: { ...client.state, tabId: capturedTabId } };
      case 'gain': if (worklet) worklet.parameters.get('gain').value = Math.max(0, Math.min(3, msg.gain / 100)); break;
      case 'monitor': if (monitorNode) monitorNode.gain.value = msg.on ? 1 : 0; break;
      default: throw new Error('Unknown request.');
    }
    return { ok: true };
  })().then(reply, e => reply({ ok: false, error: e.message }));
  return true;
});
