# Browser tab audio from another LAN computer

HermitSDR Tab Audio is a Chrome extension that sends a selected tab's audio to
the shack's existing transmit chain. **There is no elapsed transmission limit**
in the extension or streaming Control API. It uses TLS, the normal pairing code,
local ARM and explicit approval for each connected session.

Download the extension ZIP beside the DMG on the
[latest release](https://github.com/dzcassell/HermitSDR-releases/releases/latest).
Extract it, then in `chrome://extensions` enable Developer mode and Load unpacked.
Select the extracted `HermitSDR-Tab-Audio` folder. Chrome 116 or later is required.

The full [extension setup and operating guide](../chrome-extension/README.md)
covers certificate trust, pairing, selected-tab capture, gain, local monitoring
and stop behavior. The shack host is the LAN address of the Mac running
HermitSDR, with the Control API port (default 4996).

At the shack enable Settings → Control API during a live radio session. At the
browser, compare and trust that host's certificate, enter the pairing code and
Pair with station. At the shack ARM in TX Controls and enable Allow TX this
session beside HermitSDR Tab Audio. On the browser computer select the playing
tab, open the extension and Transmit this tab. Closing the popup keeps streaming;
Stop / disconnect ends it. Reconnects require fresh local approval.

A healthy stream can run indefinitely, including silent PCM. Connection/audio
watchdogs, explicit stop/disarm, ownership and transmitter protection still end
an unhealthy or revoked transmission. No automatic reconnect or re-key occurs.
See [Control API revision 3](ControlAPI.md#56-session-approved-transmit--revision-3)
for the wire contract. The existing receive-only [Web console](WebConsole.md)
remains a separate client and has no tab-capture or transmit controls.

Software checks include the real unpacked Chrome extension capturing a local
tone-generating tab, the production TLS server, and fake coordinator ports. Cross-computer
capture and physical dummy-load acceptance require an operator session; no RF
validation is implied by an app build or a test pass.
