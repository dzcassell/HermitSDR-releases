import { endpoint } from './protocol.mjs';
const $ = id => document.getElementById(id);
const send = msg => chrome.runtime.sendMessage({ ...msg, target: 'background' });
let operating = false, error = '';
async function refresh() {
  try {
    const r = await send({ type: 'status' });
    if (!r?.ok) throw new Error(r?.error || 'Extension unavailable.');
    const s = r.state, connected = s.phase !== 'disconnected';
    $('host').disabled = $('code').disabled = connected || operating;
    $('connect').disabled = connected || operating;
    $('start').disabled = s.phase !== 'paired' || !s.allowed || operating;
    $('stop').disabled = !connected && !operating;
    $('meter').value = s.peak || 0;
    const label = { disconnected: 'Disconnected', connecting: 'Pairing…', paired: s.allowed ? 'Approved · ready to transmit the selected tab' : 'Paired · waiting for local TX approval',
      capturing: 'Capturing tab audio…', starting: 'Starting tab audio…', transmitting: 'Streaming tab audio · TX requested at station' }[s.phase];
    $('status').textContent = error || s.error || label;
    if (s.phase === 'transmitting') $('status').textContent += `\n${Math.floor((s.sent || 0) / 1024)} KiB sent`;
  } catch (e) { $('status').textContent = e.message; }
}
async function action(task) {
  operating = true; error = ''; await refresh();
  try { const r = await task(); if (!r?.ok) throw new Error(r?.error || 'Request failed.'); }
  catch (e) { error = e.message; }
  finally { operating = false; await refresh(); }
}
$('connect').onclick = () => action(async () => {
  const host = $('host').value.trim(); endpoint(host);
  await chrome.storage.local.set({ host });
  const code = $('code').value; $('code').value = '';
  return send({ type: 'connect', host, code });
});
$('start').onclick = () => action(() => send({ type: 'start' }));
$('stop').onclick = () => action(() => send({ type: 'stop' }));
$('certificate').onclick = async () => {
  try {
    const url = new URL(endpoint($('host').value.trim()));
    url.protocol = 'https:'; url.pathname = '/';
    await chrome.tabs.create({ url: url.href });
  } catch (e) { error = e.message; await refresh(); }
};
$('gain').oninput = async () => {
  const gain = Number($('gain').value); $('gain-value').textContent = gain + '%';
  await chrome.storage.local.set({ gain }); await send({ type: 'gain', gain });
};
$('monitor').onchange = async () => {
  const on = $('monitor').checked;
  await chrome.storage.local.set({ monitor: on }); await send({ type: 'monitor', on });
};
const settings = await chrome.storage.local.get({ host: '', gain: 100, monitor: true });
$('host').value = settings.host; $('gain').value = settings.gain;
$('gain-value').textContent = settings.gain + '%'; $('monitor').checked = settings.monitor;
await refresh();
setInterval(refresh, 300);
