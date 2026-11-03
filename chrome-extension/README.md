# HermitSDR Tab Audio → Radio

Capture the selected Chrome tab (including sites you are signed into), key
HermitSDR on another computer on your LAN, and stream the tab's audio into its
existing TX chain. There is **no transmission-duration limit** in the extension
or HermitSDR's streaming Control API. Silence does not end a stream while its
audio clock remains healthy.

## Install and pair

1. Install the matching HermitSDR release on the shack Mac. Enable **Settings →
   Control API → Thin-client server** during a live radio session. Note its
   port (default **4996**), pairing code and certificate fingerprint.
2. Download the **HermitSDR-Tab-Audio-<version>.zip** asset from the HermitSDR
   release and extract it on the browser computer. Requires **Chrome 116+**.
3. Open `chrome://extensions`, enable **Developer mode**, choose **Load
   unpacked**, and select the extracted `HermitSDR-Tab-Audio` folder (or this
   `chrome-extension` source directory). Pin the extension.
4. Open the extension and enter the shack's LAN **host:port**. Use the Control
   API port, not the web console/overlay or Hermit Remote ports. Allow Local
   Network access for Chrome and HermitSDR if the browser or macOS requests it.
5. On first contact click **Certificate…**. In Chrome's certificate viewer,
   compare the SHA-256 fingerprint with HermitSDR's Settings before accepting
   the self-signed certificate for that host. Return to your audio tab and
   reopen the extension. TLS is mandatory; there is no `ws://` option.
6. Enter the pairing code and click **Pair with station**. The pairing code
   is used only for HMAC challenge/response and is never saved. Host, gain,
   monitor preference and a random client ID are stored locally. Nothing
   goes to a relay or cloud service.
7. At the shack, ARM using the normal TX Controls, then enable **Allow TX this
   session** beside **HermitSDR Tab Audio** in **Settings → Control API**.
   The paired client also needs its normal **Control** permission.

## Transmit

Play the desired audio, select that tab, open the extension, and click
**Transmit this tab**. Capture is limited to the explicitly selected HTTP(S)
tab; there is no microphone or whole-computer capture. Audio from all tab
channels is averaged to mono at 48 kHz and sent as 480-sample/10 ms PCM frames.
The native TX profile, gain, EQ, limiter and protection remain authoritative.

**Gain** scales the captured program (0–300%, including true zero). The peak
meter reports captured audio after this gain; it is not an RF/ALC meter. Watch
the native TX meters at the shack. **Keep playing audio locally** monitors the
original tab independently of transmitted gain. The `TX` badge/status indicates
the extension's active stream, not independent proof of emitted RF.

Closing the popup keeps streaming. **Stop / disconnect** ends capture and
releases PTT. Local PTT termination, disarm, protection, session revocation,
Kick, server shutdown, captured-tab closure, socket loss, stale audio or
backpressure also stop the stream. No automatic reconnect or re-key occurs.
Reconnects require fresh local session approval. There is no timed cutoff or
VOX/silence-duration cutoff.

The existing 450 ms host lease watchdog is renewed every 100 ms; it protects
against a vanished browser and never limits how long a healthy stream can run.
The client closes on excessive queueing or capture stalls rather than replaying
old audio. The host still rejects stale/replayed/malformed frames and enforces
exclusive TX ownership, local ARM, mode/policy and hardware protection. Remote
ARM is unavailable. The existing explicitly bounded TUNE test-tone command is
separate from continuous tab streaming; this extension never sends it.

## Checks and scope

In the development checkout, `node --test chrome-extension/tests/client.test.mjs` exercises the protocol,
worklet, cancellation and failure handling. `python3 tools/chrome-extension-smoke.py`
uses the real TLS server and remote TX controller with synthetic PCM and fake
coordinator ports on loopback. With current Chrome installed it also loads the
actual unpacked extension, captures a local tone-generating tab through
`tabCapture`, and checks gain and Stop cleanup. Neither command connects to a
physical radio. Cross-computer capture and dummy-load RF acceptance remain operator
checks; automated fixtures are not hardware validation.

The capture architecture follows Chrome's [offscreen tab-capture guidance](https://developer.chrome.com/docs/extensions/how-to/web-platform/screen-capture).
RigGPT's tab-audio extension supplied the feature reference; HermitSDR uses its
own authenticated Control API instead of RigGPT's plaintext streaming endpoint.
