// Control API revision 3. No radio access, capture, or persistent credentials here.
export const FRAME_SAMPLES = 480;
export const MAX_BUFFERED = 976 * 5; // Fail closed at 50 ms, never replay a backlog.
export function endpoint(host) {
  const input = host.includes('://') ? host : `wss://${host}`;
  const url = new URL(input);
  if (url.protocol !== 'wss:' || !url.hostname || url.username || url.password ||
      url.search || url.hash || !['', '/', '/control/v1'].includes(url.pathname)) {
    throw new Error('Use a host:port or wss://host:port/control/v1 (TLS required).');
  }
  // URL canonicalization removes an explicit :443. Preserve that choice.
  const explicit443 = /^wss:\/\/[^/?#]+:443(?:\/|$)/i.test(input);
  if (!url.port && !explicit443) url.port = '4996';
  url.pathname = '/control/v1';
  return url.href;
}
export function pairingToken(code) {
  const clean = code.toUpperCase().replace(/[-\s]/g, '');
  if (!/^[A-Z2-7]{32}$/.test(clean)) throw new Error('Enter the 32-character Control API pairing code.');
  const out = new Uint8Array(20);
  let bits = 0, value = 0, pos = 0;
  for (const c of clean) {
    value = (value << 5) | 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'.indexOf(c);
    bits += 5;
    if (bits >= 8) { bits -= 8; out[pos++] = (value >>> bits) & 255; }
  }
  return out;
}
export async function authAnswer(token, hello, challengeText) {
  const challenge = JSON.parse(challengeText);
  if (challenge.t !== 'challenge' || challenge.apiVersion !== 1 || challenge.minApiVersion > 1) {
    throw new Error('Unsupported Control API challenge.');
  }
  const nonce = Uint8Array.from(atob(challenge.nonce), c => c.charCodeAt(0));
  if (nonce.length !== 32) throw new Error('Invalid authentication nonce.');
  const hash = new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(hello + '\n' + challengeText)));
  const bytes = new Uint8Array(64); bytes.set(nonce); bytes.set(hash, 32);
  const key = await crypto.subtle.importKey('raw', token, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const answer = new Uint8Array(await crypto.subtle.sign('HMAC', key, bytes));
  return btoa(String.fromCharCode(...answer));
}
export function micFrame(pcm, sequence) {
  if (!(pcm instanceof ArrayBuffer) || pcm.byteLength !== 960) throw new Error('Invalid 10 ms audio frame.');
  const out = new ArrayBuffer(976), view = new DataView(out);
  view.setUint8(0, 0x10);
  view.setUint32(4, sequence >>> 0, true);
  view.setUint32(8, 48000, true);
  view.setUint16(12, 1, true);
  view.setUint16(14, FRAME_SAMPLES, true);
  new Uint8Array(out, 16).set(new Uint8Array(pcm));
  return out;
}
