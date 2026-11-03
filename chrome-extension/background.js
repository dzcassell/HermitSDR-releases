// The offscreen document owns the live socket/audio; worker restarts never re-key.
let creating;
async function ensureOffscreen() {
  if (creating) return creating;
  creating = (async () => {
    if ((await chrome.runtime.getContexts({ contextTypes: ['OFFSCREEN_DOCUMENT'] })).length) return;
    await chrome.offscreen.createDocument({ url: 'offscreen.html', reasons: ['USER_MEDIA'],
      justification: 'Capture selected tab audio and stream it to the paired HermitSDR station.' });
  })();
  try { await creating; } finally { creating = null; }
}
const relay = msg => chrome.runtime.sendMessage({ ...msg, target: 'offscreen' });
async function status() {
  const contexts = await chrome.runtime.getContexts({ contextTypes: ['OFFSCREEN_DOCUMENT'] });
  if (!contexts.length) return { ok: true, state: { phase: 'disconnected', allowed: false, error: '', sent: 0, peak: 0 } };
  return relay({ type: 'status' });
}
let busy = false;
chrome.runtime.onMessage.addListener((msg, sender, reply) => {
  if (sender.id !== chrome.runtime.id || msg?.target !== 'background') return;
  (async () => {
    if (msg.type === 'state') {
      const state = msg.state;
      await chrome.action.setBadgeText({ text: state.phase === 'transmitting' ? 'TX' : state.phase === 'paired' ? 'LINK' : '' });
      await chrome.action.setBadgeBackgroundColor({ color: state.phase === 'transmitting' ? '#e44757' : '#007c9c' });
      return { ok: true };
    }
    if (msg.type === 'status') return status();
    if (msg.type === 'stop') return relay({ type: 'stop' }).catch(() => ({ ok: true }));
    if (msg.type === 'gain' || msg.type === 'monitor') return relay(msg).catch(() => ({ ok: true }));
    if (busy) throw new Error('An operation is already in progress.');
    busy = true;
    try {
      if (msg.type === 'connect') {
        await ensureOffscreen();
        const stored = await chrome.storage.local.get({ clientId: '' });
        const clientId = stored.clientId || crypto.randomUUID();
        if (!stored.clientId) await chrome.storage.local.set({ clientId });
        return await relay({ type: 'connect', host: msg.host, code: msg.code, clientId });
      }
      if (msg.type === 'start') {
        const current = await status();
        if (current.state?.phase !== 'paired' || !current.state.allowed) throw new Error('ARM locally and allow TX for this session first.');
        const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
        if (!tab?.id || !/^https?:/.test(tab.url || '')) throw new Error('Select an HTTP(S) tab playing audio.');
        const streamId = await chrome.tabCapture.getMediaStreamId({ targetTabId: tab.id });
        const settings = await chrome.storage.local.get({ gain: 100, monitor: true });
        return await relay({ type: 'start', streamId, tabId: tab.id, gain: settings.gain, monitor: settings.monitor });
      }
      throw new Error('Unknown request.');
    } finally { busy = false; }
  })().then(reply, e => reply({ ok: false, error: e.message }));
  return true;
});

// Independent fallback if a browser version delays the MediaStream ended event.
// Query the offscreen owner so worker suspension cannot lose the captured tab.
chrome.tabs.onRemoved.addListener(async tabId => {
  const live = await status().catch(() => null);
  if (live?.state?.tabId === tabId) await relay({ type: 'stop' }).catch(() => {});
});
