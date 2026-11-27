# Web console — listen and tune from a browser

Issue #154 (public web receiver), the first browser slice of #91 (responsive
remote console) and the answer to #201 (control the HL2 from a car's
browser). One static page, served by HermitSDR itself, that shows the shack
receiver — panadapter, waterfall, S-meter, dial — plays its audio and
operates its receive side: click or tap the spectrum, step buttons and arrow
keys, mode, filter presets and custom width/shift, band, AGC, VFO A/B, and (since #201) RF gain and
the step attenuator, NR / NB / ANF, squelch, the shack's own volume and
mute, RIT, split and the shack's tuning step. **Receive only.** The page has
no transmit control of any kind. Control API TX remains a separate, default-off
local approval for an authenticated session (`docs/ControlAPI.md` § 5.6); the
console never implements or requests those commands.

It is **off by default** and stays off until the operator turns it on.

## What it is made of

The console is two existing services and one file:

| Piece | Where | Role |
| --- | --- | --- |
| `HermitSDR/Resources/WebConsole/console.html` | app bundle | The page. Plain HTML/CSS/JS, no build step, no CDN, no cookies, no libraries (the WebGL2 waterfall is written out in the page). |
| OBS overlay HTTP server (#148) | port 4997, `Station ▸ Audio & Streaming ▸ OBS Studio` | Serves `GET /console` (the page) and `GET /console/config.json` (Control API port, TLS fingerprint, policy, station name, waterfall palette). Loopback unless its **Allow LAN** switch is on. |
| Control API (#122) | port 4996, `Settings ▸ Control API` | The WebSocket the page pairs with. State, meters, spectrum rows and 12 kHz PCM audio down; RX commands up. |

The browser loads the page over HTTP from the overlay server, reads
`config.json`, then opens `wss://<same host>:<Control API port>/control/v1`
exactly like any other Control API client. Nothing is proxied: the overlay
server never sees the pairing handshake or the radio traffic.

## Enable it

1. **Settings ▸ Control API**: turn on the thin-client server. It binds while
   a radio session, a file replay or Demo Mode is active; its pairing code
   and certificate fingerprint appear then.
2. **Settings ▸ Web console**: turn on *Browser console*. The status line
   says what is still missing and offers the one-click fix (turn on the
   overlay server), then shows the URL.
3. **On this Mac:** open the URL (`http://127.0.0.1:4997/console`), paste the
   pairing code, Connect.
4. **From a phone or tablet:** in `Station ▸ OBS Studio` turn on the overlay
   server's **Allow LAN**; Settings then shows the LAN URL
   (`http://192.168.x.y:4997/console`). *Copy link with pairing code* puts
   the code in the URL fragment so the phone needs one tap.
5. **The certificate, once per browser.** The Control API presents the
   shack's self-signed certificate (the one Hermit Remote uses). A browser
   has no fingerprint-pinning API, so the first time it will refuse the
   `wss://` connection. The page then shows the fingerprint from
   `config.json` and a link to `https://<host>:4996/`: open it, compare the
   fingerprint the browser shows with the one on the page (and with
   `Settings ▸ Control API`), accept it, then Connect again. Safari and
   Chrome remember the decision per host.

   After that the page pairs in well under a second and audio starts on
   the **Listen** button (browsers require a tap before they play sound).

## Install and open the shell offline

On a supported secure origin, the page provides a manifest and local icons for
standalone installation. Use **Install console** when the browser offers it, or
the browser's own Install / Add to Home Screen / Add to Dock action. Availability
varies by browser. The in-page status reports whether the offline shell is ready.

The current local server uses HTTP. `http://127.0.0.1:4997/console` on this Mac is
a trustworthy loopback origin. Ordinary `http://192.168…/console` LAN pages keep
working online, but cannot register this service worker or offer the same PWA
install behavior. HTTPS hosting, if already supplied by the operator, must serve
the `/console` page and its `/console/*` resources at the same origin, preserving
the static page’s `X-Hermit-Console-Shell: 1` response header. This change
does not configure a proxy, relay, firewall or a new listener. Browser requirements:
[MDN installability](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)
and [service workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers).

Only one marked static HTML shell is kept in the browser's Cache Storage.
Other HTML, including an unmarked proxy login page, is never stored there. Config,
certificate fingerprints, pairing responses, receiver snapshots, meters, audio
and spectrum are never cached. The existing explicit **remember the code**
setting remains separate browser-local storage. No radio recording is created.
An offline launch clears receiver indications and imagery and leaves receive
editors disabled. Return to the station's network and **Connect** to pair again.

When a worker update is ready, **Update console** disconnects this browser and
reloads it. A waiting update does not interrupt a current receiver session.
Normal online navigation uses the network; an online disabled-console response
remains a refusal instead of falling back to an old page. Successful online
navigation can replenish an evicted shell without making storage availability a
condition for using the online console.

**Remove offline copy** unregisters the worker and removes its shell cache. The
choice persists for this browser; **Enable offline copy** enables it again.
Other applications' caches and the optional remembered pairing code are retained.
To remove remembered credentials, uncheck **remember the code** and connect, or
clear this site's browser data. Device-level installation/uninstallation remains
in the browser or operating system. Actual iOS/Android and hostile-route acceptance
remains in #91; automated Chrome checks establish the software behavior only.

## Tablets and phones: the touch layout (#468)

On an iPad, an Android tablet or a phone the console arranges itself for
fingers: a large frequency readout and S-meter, the panadapter and waterfall,
a tuning ring, and pads for the step, band and mode. Nothing is installed on
the tablet; it is the same page, the same pairing and the same receive-only
command set as on a desktop.

### Open it on an iPad

1. On the Mac: **Settings ▸ Control API** on, **Settings ▸ Web console** on,
   and **Allow LAN** on for the overlay server (see *Enable it* above). The
   iPad must be on the same network as the Mac.
2. On the Mac press *Copy link with pairing code* and send the link to the
   iPad (AirDrop, Messages, Universal Clipboard), or type the LAN URL
   (`http://192.168.x.y:4997/console`) into Safari and paste the pairing code.
3. The first time, Safari refuses the shack's self-signed certificate. Tap
   the *open the Control API port once* link the page shows, compare the
   fingerprint, accept it, go back and tap **Connect**.
4. Tap **Listen** for audio (a browser plays nothing until it is tapped).

### Add it to the Home Screen

In Safari: **Share ▸ Add to Home Screen**. The console then opens full screen
with its own icon, without Safari's bars, inside the safe areas of the
display, and without the rubber-band bounce at the edges. The pairing code is
kept only if **remember the code on this device** is ticked; a Home Screen
web app has its own storage, so tick it there once. The icon is a 180 px PNG
served by the Mac at `/console/apple-touch-icon.png`; the manifest and its
SVG icons are the ones the console already had.

### Which layout

The touch layout is chosen automatically when the device's main pointer is
coarse (a finger: `pointer: coarse`), and the pointer layout otherwise. The
**Auto** button in the header changes it by hand: Auto → Touch → Pointer →
Auto, remembered on that device. `?layout=touch` or `?layout=pointer` on the
URL forces one for that visit. The pointer layout is unchanged from earlier
releases.

The touch layout has four arrangements: a tablet in landscape (scope on the
left, ring and pads on the right, all on the first screen), a tablet in
portrait (scope above, ring beside the pads), a phone in portrait (one
column) and a phone in landscape (ring beside the scope). The remaining
controls (filter, AGC, audio, RF gain, DSP, squelch, RIT, split, connection)
are below, a scroll away.

### Fingers

| Gesture | Where | What it does |
| --- | --- | --- |
| Spin | Tuning ring | Tunes: clockwise is up, 48 clicks a turn, each click one step. A flick keeps turning and slows down by itself; touching the ring stops it at once. At rest it never moves. |
| Tap a pad | Step | 10 Hz, 100 Hz, 500 Hz, 1 kHz, 5 kHz, 10 kHz, or **shack** (the shack's own step, through `tuneStep`). |
| Tap a pad | Band, Mode | The band and mode buttons, at finger size (`setBand`, `setMode`). |
| Drag sideways | Panadapter or waterfall | The dial follows the finger by the frequency it crosses. Nothing jumps when the finger lands. |
| Tap | Panadapter or waterfall | Tunes to the tapped frequency; if a signal stands at least 10 dB out within about a fingertip, lands on its peak. |
| Pinch | Panadapter or waterfall | Zooms this device's view, up to ×16, about the fingers. A **×N** chip appears; tap it for the whole span again. |
| Two fingers together | Panadapter or waterfall | Pans the zoomed view. |
| Swipe up or down | Anywhere, the spectrum included | Scrolls the page. It never tunes. |

Tuning from the ring and from a drag is sent at most 25 times a second and
always carries the newest target, so a fast spin does not queue behind
itself; the server's own coalescing does the rest.

Zoom and pan are local. The Control API sends the span the shack operator is
looking at, at up to 1024 bins; the tablet crops and stretches those rows.
Pinching does not change the shack's display, does not reach outside the
shack's span, and does not add resolution beyond those bins. At ×16 on a
96 kHz span a bin is about 94 Hz. When the view is zoomed and the ring tunes
the dial out of it, the view follows.

While the shack is on the air the ring, the pads, drag and tap are held like
every other tuning control, with the same reason shown.

### Apple Pencil

Safari reports a pencil as a pen pointer, and the console gives it the
precise tools. Fingers keep the gestures above.

| Pencil | Where | What it does |
| --- | --- | --- |
| Hover | Panadapter or waterfall | A cursor line with the frequency and level under the tip. Nothing is tuned. Needs an iPad and pencil that report hover; without hover the cursor shows while the tip is down. |
| Tap | Panadapter or waterfall | Tunes to the 10 Hz under the tip, with no snapping to a signal. |
| Drag a passband edge | Panadapter | Within 14 points of the shaded passband's edge the pencil takes that edge: the other edge stays, the width changes in the mode's own steps (`setFilter`, width and shift). The receiver follows while dragging. |
| Drag elsewhere | Panadapter | Sweeps a new passband: on lifting, the width becomes the swept width (`setFilter`) and the dial moves so the passband lies on the sweep (`tune`), with the shift it had. |
| Drag | Waterfall | The dial follows the tip in 10 Hz steps. |

Pinch first for fine filter work: at the full span of a wide receiver one
point is many tens of hertz. Edge drags and sweeps need the mode's announced
filter limits (the same condition as the Width and Shift fields).

**No notch drawing.** The page draws no notch with the pencil. Control API
revision 6 added RF notch commands (`addRFNotch`, `removeRFNotch`,
`clearRFNotches`, `setRFNotches`, see [ControlAPI.md](ControlAPI.md)), so
drawing one can now be built; it has not been.

### Screen stays awake while listening

While **Listen** is on and the console is paired, the page holds a screen
wake lock where the browser provides one, and releases it when Listen goes
off, the connection closes or the page is hidden. The side panel's **Screen**
line says which. Browsers offer the wake lock only to secure pages (HTTPS, or
the Mac's own loopback URL). The console is served to the LAN over plain
HTTP, so **on an iPad opened at `http://192.168…` the wake lock is not
available** and the page says so; set **Settings ▸ Display & Brightness ▸
Auto-Lock ▸ Never** on the iPad while it is the radio's display. Behind the
operator's own HTTPS front the lock works.

### Limits

* No memory or bookmark pads: the Control API carries no memories, so the
  console has none to show. Band pads restore each band's last frequency.
* No transmit control of any kind, as before.
* Same access rules as before: pairing code, the certificate, the per-client
  grants, the session cap and time limit. No command was added to the
  Control API for this; every gesture ends in `tune`, `tuneStep`, `setBand`,
  `setMode` or `setFilter`.
* No third-party script, font or request: the page, its icon and its
  manifest come from the Mac.
* The offline shell and browser "Install" prompt keep their secure-origin
  rule (above). **Add to Home Screen** on an iPad works over the plain LAN
  URL because it needs neither.
* A Home Screen web app keeps its own browser storage. If it refuses the
  connection after Safari had accepted the shack's certificate, accept the
  certificate again from inside it (the same link on the page), or open the
  console in Safari instead.
* Checked in headless Chrome with emulated touch and pen input against the
  production servers. Safari on a real iPad, the Home Screen web app and an
  Apple Pencil are the operator's check; see the list in #468.

Sidecar is a different thing: it makes the iPad a second Mac display that
shows the HermitSDR window itself (macOS **Displays ▸ Add Display**), with
the Mac's pointer and the pencil acting as a mouse. It needs no Web Console
and has none of these gestures.

## What the page does

* **Panadapter + waterfall** from the Control API spectrum downlink: the span
  the shack operator is looking at (their zoom and pan), 10 rows/s,
  peak-decimated to the canvas width (16–1024 bins; the page asks for the
  power of two above its pixel width and re-subscribes on resize). The
  floor and top track the row. VFO A is the red line, VFO B the dashed
  green one, the receive passband is shaded.
* **Waterfall on the GPU (#91).** The waterfall is a WebGL2 ring texture:
  every row the Control API delivers is uploaded once (`texSubImage2D`, 8-bit
  dB bins, no CPU colouring) into a bins × 512-row history texture, a write
  offset scrolls it, and the fragment shader maps each pixel through the
  page's floor / top (the same automatic range the panadapter shows) into a
  256-entry palette texture and draws the passband tint and VFO line — one
  upload and one triangle per row, no per-frame allocation, so a phone or
  tablet GPU draws it at display rate regardless of history depth. The
  palette is the shack's own: `config.json` carries the operator's static
  waterfall colormap (`palette: [[position, r, g, b], …]`, 2–16 stops,
  `WebConsolePalette`); a procedural colormap (Prism, Nebula) has no table,
  so the page keeps its embedded default, which is the app's **Classic**.
  Changing the colormap in the app reaches a browser on its next page load.
  When `webgl2` is unavailable, refused, or the GPU context is lost
  (`webglcontextlost`), the page draws the same rows from its CPU copy of
  the history with the 2D canvas — identical mapping and palette, nothing is
  lost — and returns to the GPU when the context is restored. The side panel's
  **Waterfall** line says which is in use (`#scopeCard[data-renderer]` for
  tooling); `?renderer=canvas2d` on the page URL forces the 2D canvas. The
  rows themselves are unchanged: ≤ 1024 bins at ≤ 10 rows/s from the API,
  so the renderer's headroom (up to 4096 bins) is for a later server slice.
  A mouse has click to tune and the wheel on both canvases; touch and pencil
  gestures are in the tablet section above. A pinched view crops the same
  history in the shader (and in the 2D fallback).
* **Dial, mode, filter, band, link, ON AIR** from the state stream;
  the receive footprint uses the native voice/data sideband offsets and RIT.
  **S-meter** from the 10 Hz meter messages (S-units and dBm, ADC overload).
* **Audio**: the 20 ms PCM frames are placed on the Web Audio clock as 12 kHz
  `AudioBuffer`s (the browser resamples), 90 ms of lead, late frames drop
  the backlog instead of drifting. Volume and mute on the page are local to
  that browser; the shack's own volume/mute still shape the downlink and
  the page says so when the shack is muted. Stopping or disconnecting cancels
  already queued audio. Stream gaps and excessive backlog cancel old sources
  before rescheduling, with bounded pending playback. Unsupported audio rates or
  frames outside the documented 12 kHz / at most 20 ms profile are ignored.
* **Tuning**: click/tap the panadapter or waterfall (100 Hz snap), ◀ ▶ with
  a step picker, ← → (step), ↑ ↓ (step × 10), scroll wheel, *MHz…* to type
  a frequency. The step picker's last entry, **shack step**, moves by the
  shack's own tuning step through `tuneStep` (the entry shows that step as
  the state reports it; detents add up under the server's coalescing).
  Mode buttons, the mode's filter presets (`radio.filters`, revision 1),
  band buttons, AGC, **A⇄B** (`swapVFO`) and **A→B** (`setVFOB`). Every
  command is a documented Control API message; the server coalesces bursts
  and rate-limits (50/s).
* **Custom filter**: Width and Shift fields use Hz. Width follows the current
  mode's announced minimum, maximum and step; the protocol accepts shift
  within ±5000 Hz and the shack applies its narrower mode range/quantum.
  **Apply** sends only edited fields through `setFilter`; **Revert** restores
  the latest received state. Enter submits the form. Native number validation
  and inline feedback reject blank, nonfinite, out-of-range and off-step
  widths before any command is sent. Unedited fields continue following the
  receiver while an edited field remains a draft; changing mode discards the
  old draft. A clamped/no-op write reconciles with the authoritative state
  even if it produces no delta. Disconnected/read-only clients and older
  servers without announced filter limits have disabled editors; presets
  continue to work as before. These are receive-filter controls and remain
  available during the existing dial hold.
* **Receiver controls (#201)**, all of them the shack's own settings,
  reflected from the state stream and lit when on:
  * **RF gain** slider bounded by the radio's announced range
    (`welcome.radio.rfGainMinDb…rfGainMaxDb`, −12…+48 on a Hermes-Lite 2,
    −31…0 on an ANAN) → `setRFGain`; **ATT** 0 / −10 / −20 / −30 chips →
    `setAttenuation`.
  * **NR**, **NB**, **ANF** toggles → `setDSP`.
  * **SQL** on/off and a level slider (−150…−30 dBm) → `setSquelch`.
  * **Shack** mute and volume → `setMute` / `setVolume`. These are the
    shack speaker and therefore shape the downlink every listener hears;
    the **Browser** row above them (Listen, Mute, volume) stays local to
    the device and sends nothing.
  * **RIT** on/off, −/+ 10 Hz, a typed offset (±9999 Hz) and **0** →
    `setRIT`.
  * **Split** → `setSplit`: arms split at the shack, where VFO B becomes
    the other frequency. It keys nothing and the page cannot.
  * Sliders send one command on release (the label follows the thumb); a
    control the user touched in the last second is not overwritten by the
    echo of its own command.
* **On-air hold.** While the state says the shack is keyed (`txKeyed`, also
  mirrored by the 10 Hz meter), the dial, step buttons, *MHz…*, mode, band
  and VFO A/B controls are greyed with the reason ("the shack is on the
  air — the dial is held until it returns to receive") and the page forms
  no tuning command; the server would refuse them anyway
  (`docs/ControlAPI.md` § 5.1). DSP, squelch, gain and shack audio stay
  live.
* **Phone layout**: below 860 px the side panel drops under the controls,
  buttons are ≥ 40 px tall, the page works as a home-screen web app. On a
  touch screen the touch layout above takes over.

Keyboard: `←` `→` step, `↑` `↓` step × 10, `M` mute (this browser), `N` /
`B` / `A` toggle NR / NB / ANF, `S` squelch, `R` RIT.

## Security model

Nothing on the server was loosened for the browser.

* **Same transport.** `wss://` to the Control API's TLS listener, same
  certificate, same subprotocol. There is no plaintext mode in the app
  (`WebConsoleTests` and `ControlAPITests` pin that no app source can reach
  the test-only plaintext server or set the config's scheme to `ws`).
* **Same pairing.** The page answers the HMAC-SHA256 challenge
  (`docs/ControlAPI.md` § 3.3) with SHA-256/HMAC implemented in the page
  itself — a plain-http LAN page is not a "secure context" and has no
  WebCrypto — pinned against the protocol's worked example and against the
  Swift implementation on random vectors. The pairing code never leaves
  the browser except as that answer. Three wrong codes from one address
  start the API's 60 s cool-down, as for any client.
* **Same grants.** The browser pairs with `platform: "browser"` and a
  `clientId` it keeps in the browser's local storage; it appears in
  `Settings ▸ Control API` like any client, with the same Control / Audio /
  Spectrum permissions, Kick, Revoke and Forget. Rotating the pairing code
  unpairs it. There is no per-command allow-list: the single **Control**
  grant covers every receive-side command (§ 5.1), so #201 needed no
  server change; `WebConsoleTests` pins that a browser session with Control
  reaches the radio with each command the page forms and that one without
  it is answered `forbidden` for each.
* **No transmit.** The page forms no transmit message (a test rejects the
  page if a reserved transmit name appears in it in any quoted form), the
  API refuses TX by default unless a separate session is locally approved, and
  the console’s `welcome.granted` never contains `transmit`. The page has no
  microphone uplink or TX command UI; its PWA shell adds none.
* **The pairing code in a link.** *Copy link with pairing code* appends
  `#code=…`. Browsers never send the fragment to any server; the page reads
  it once and removes it from the address bar. The link is therefore as
  secret as the code — share it the way you would share the code, and
  rotate the code if a link leaks. The page offers to remember the code
  in local storage; that is the browser's own storage on that device.
* **What the overlay server adds.** `/console` and `/console/config.json`
  are public to whoever can reach the overlay port (loopback by default;
  the LAN when the operator allows it). The page is static and the config
  carries the Control API port, the certificate fingerprint (public by
  definition), the station callsign and the policy — never the code.

### Honest limits

* A browser cannot pin a certificate fingerprint. The operator compares it
  by eye in the browser's certificate dialog on first contact; afterwards
  the browser's own stored decision is the pin. A new certificate (Hermit
  Remote identity rotated) means a new dialog.
* The console's own page arrives over plain HTTP from the overlay server.
  On a hostile LAN someone could serve a different page; the pairing code
  would then be typed into that page. Keep **Allow LAN** off outside your
  own network; for remote use, reach the shack through your own VPN —
  the same trust model as Hermit Remote. No relay or account exists.
* Volume and mute on the page are local; the downlink is the shack's
  speaker mix, so the operator's volume and mute apply to listeners too
  (`docs/ControlAPI.md` § 12).

## Limits and policy

* **Sessions**: at most *N* browser sessions paired at once (Settings ▸ Web
  console, 1–4, default 3). The Control API allows 4 clients in total, so
  the cap leaves room for native clients. A further browser `hello` is
  denied `busy` with "the web console allows N browser sessions at a time".
* **Time limit**: none, or 15 / 30 / 60 / 120 minutes per session. When it
  elapses the server sends `bye` (`kicked`, "web console session limit …
  reached — reconnect to continue") and closes; the page shows it and does
  not auto-reconnect after a kick.
* Both bounds key on `hello.platform == "browser"`. They are resource policy,
  not authentication: a hand-written client that says otherwise still faces
  the 4-client cap, the pairing code and the operator's grants. They are
  installed only while the Web console switch is on.
* Everything else is the Control API's: 50 commands/s with bursts of 100,
  ≤ 10 spectrum rows/s at ≤ 1024 bins, 0.5 s of audio in flight per
  client, slow consumers closed.

## Replay and Demo Mode

Since this feature the Control API also binds during a file replay and in
Demo Mode (`link: "replay"`, `txCapable: false`): the chain demodulates,
the analyzer runs and tuning works within the recorded span, so a browser
can listen to a recording or try the console against the demo band
without a radio. Before, only a live radio session bound the listener.

## Checks

* `swift test --filter WebConsoleTests` — routes, config, policy, the
  page's self-containment and transmit-free source, its pairing crypto
  run in JavaScriptCore against the documented vector and the Swift code,
  receive-footprint geometry checked against the native receiver in every mode,
  and (#201) that every `{t:'…'}` command the page forms parses as a
  protocol command and is granted to a browser session holding Control.
* `swift test --filter WebConsoleTests` also pins (#91) that the config's
  palette export is bounded and falls back to the default, that the page's
  embedded default is the same table and its LUT interpolates the stops the
  way the renderer does (run in JavaScriptCore), that the page refuses what
  the server would refuse, and that the WebGL2 path, the 2D fallback, the
  context-loss handlers and `data-renderer` are present with no dynamic code.
* `swift test --filter WebConsoleTouchTests` (#468) runs the page's touch
  and pencil maths in JavaScriptCore: layout choice, pen / touch / mouse
  routing, ring angle wrap-around and detents, step quantisation, inertia
  decay, stop-on-touch and no drift, pinch limits and focus, two-finger pan,
  drag versus scroll, tap-to-signal, and the pencil's filter geometry
  against the native receiver in every mode; plus the Home Screen icon.
  `tools/web-console-smoke.sh` then proves the pointer layout unchanged with
  a real mouse click and wheel, switches on touch emulation, and drives the
  ring, the spectrum gestures and the pencil tools with real touch and pen
  events into the fixture radio at tablet and phone sizes in both
  orientations.
* `tools/web-console-smoke.sh` — the production overlay server and Control
  API server on loopback; HTTP routes; the Python reference client as a
  browser (cap, native client unaffected, time limit, slot reuse); then
  headless Google Chrome loads the real page with the code in the fragment
  and, over the DevTools protocol, the page's own self-test must report
  paired + spectrum rows + audio frames, the waterfall must be on WebGL2 (a
  synthetic spectrum row injected into the page is read back from the GPU
  canvas with its spike where it belongs; a lost context must fall back to
  the 2D canvas with the history intact and a restored one take over again;
  a second tab with `?renderer=canvas2d` must draw with the 2D canvas), a
  tune and a mode change issued
  through the page must land in the fixture radio, an out-of-range tune
  must surface as an error, every #201 control clicked or dragged on the
  real page (NR/NB/ANF, squelch, RIT, split, shack mute and volume, ATT, RF
  gain, shack step) must land in the fixture radio and light the control,
  custom filter edits must honor bounds, preserve drafts/untouched fields,
  reconcile clamped no-ops and refuse invalid/read-only/disconnected edits;
  an injected keyed state must grey the dial with the reason, and a
  390 px-wide screenshot is written when `WEB_CONSOLE_SMOKE_SHOTS` names a
  folder. Runs twice: plaintext `ws`,
  then real TLS `wss` with a throwaway identity. Set
  `WEB_CONSOLE_SMOKE_BROWSER=0` to skip the browser phase.
* `tools/control-api-smoke.sh` — unchanged and still green; the browser
  policy does not touch non-browser clients.

## Not in this slice (#91 remains open)

Decoder panels (a separate later slice), sub-receiver audio, LAN discovery
from the browser, a relay or hostile-network route, and any transmit. (Touch
gestures and pencil tools arrived with #468; drawing a notch and memory pads
wait for Control API commands that do not exist yet.) Each is a Control API client-side addition or
a separately reviewed server change. (RF gain, attenuation, DSP, squelch,
shack audio, RIT, split and the shack step arrived with #201; the WebGL2
waterfall with its 2D-canvas fallback with this slice of #91.)

## Completion boundary for #201

The receive-only browser-control wish is implemented in the existing native
architecture: the Mac owns DSP and serves the page; the browser pairs with
existing grants and operates the receive controls listed above. Custom filter
editing completes the remaining basic filter-control gap. This is software
acceptance against the production servers and a synthetic receiver on loopback,
including throwaway TLS and phone/desktop layouts. It does not certify a Tesla
browser, iOS Safari, a car-to-shack VPN, or physical RF.
Cross-device/mobile and hostile-route acceptance stays in #91; relay/NAT work
stays in #181. Browser transmit remains outside this receive-only request.
