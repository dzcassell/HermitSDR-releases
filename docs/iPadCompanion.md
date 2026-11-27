# iPad companion (second slice)

A native iPad screen for a HermitSDR running on a Mac on the same network:
it finds the Mac, pairs with it, shows the dial, mode, band, S-meter, a
panadapter and a Metal waterfall, plays the receiver's audio (with the
screen locked too), pans and zooms its own view of the spectrum, and
offers receive controls for fingers, Apple Pencil and a keyboard. It is the existing
**Hermit Location** companion made universal: on an iPhone the app is the
location sender exactly as before ([iPhoneLocation.md](iPhoneLocation.md));
on an iPad it opens on a **Radio** tab and keeps the location sender in a
**Location** tab.

This is the second slice of issue #469. It is an own-device build installed
from Xcode. There is no App Store or TestFlight build. **Nothing in it has
run on an iPad or in a simulator**: it is compiled for iOS and its logic is
tested on macOS (see "Verified, and not").

**It has no transmit controls.** There is no key, arm, tune-carrier or drive
control, and the client code has no message that could ask for one: the
Control API's transmit requests, split, VFO B and the A/B swap are on a list
the app refuses to send, and a test fails if one is ever added.

## What it does

- **Finds the Mac.** The Mac advertises its Control API by Bonjour
  (`_hermitsdr-ctl._tcp`) while that listener is running. The iPad lists
  what it finds, with the Control API version each one announces. You can
  also type the Mac's host name or address (`mac-mini.local`,
  `192.168.1.20`, `host:port`).
- **Pairs with the Control API's own rules.** Nothing about the Mac's
  security changes. On first contact the iPad shows the Mac's certificate
  fingerprint and sends nothing until you have compared it with the one on
  the Mac and typed the Mac's pairing code. The code is stored in the iPad's
  Keychain (this device only, not iCloud Keychain); the fingerprint and a
  label are ordinary preferences. Later connections go straight through,
  and a Mac presenting a different certificate is refused.
- **Shows** link status and round-trip time, frequency, mode, band, filter
  width, S-meter (S-units and dBm, overload flag), and a read-only "Shack is
  transmitting" marker when the Mac's own operator keys.
- **Plays the receiver's audio** on the iPad: **Listen**, a volume slider
  and a mute that belong to the iPad alone. See "Listening" below.
- **Draws** a panadapter line and a scrolling waterfall from the Control
  API's spectrum rows (512 points, ten rows a second). The waterfall is
  drawn with Metal. Until you pan or zoom it shows the span the operator
  has on the Mac's own panadapter.
- **Pans and zooms its own view.** Pinch to zoom, drag with two fingers to
  pan, or use the magnifier buttons, anywhere inside the span the radio is
  sampling. The Mac's own panadapter and other clients are not affected.
  See "This iPad's view".
- **Controls the receiver:** drag the spectrum sideways to tune (the signal
  follows your finger), tap a signal to land on it, step buttons for one and
  ten tuning steps (hold to repeat), band, mode, the mode's filter presets,
  and the shack's volume and mute.
- **Apple Pencil:** hover shows the frequency under the tip, a tap tunes
  exactly there, a drag tunes, a double tap on the barrel switches fine
  tuning, a squeeze opens a small palette. See "Apple Pencil".
- **Lock screen and keyboard:** Now Playing with play / pause and step
  tuning; arrow keys and a few letters on a hardware keyboard.
- **Reconnects by itself** when the Mac sleeps, its radio session ends, the
  network drops or the app returns from the background. It does not retry a
  refused pairing code (three failures start the Mac's one-minute
  cool-down), and it does not reconnect after the operator's **Kick** until
  you tap **Try again**.
- Keeps the screen awake while it is connected and in front.

## On the Mac

1. Open **Settings ▸ AI & APIs ▸ Control API** and switch it on. It is off
   by default. The listener, and so the Bonjour advertisement, exists only
   while it is on **and** a radio is connected (or Demo Mode or a replay is
   running).
2. Leave that pane open: it shows the **certificate fingerprint** and the
   **pairing code** you need on the iPad.
3. After the iPad pairs it appears in the client list there. **Control**,
   **Audio** and **Spectrum** are its permissions; untick **Audio** and the
   iPad's Listen button is disabled and says why. **Kick**, **Revoke** and
   **Rotate code** work as for any other Control API client
   ([ControlAPI.md](ControlAPI.md) § 9).
4. The iPad's own view of the spectrum needs a Mac with Control API
   revision 7 (the release after 2026.1127_002). With an older Mac the
   iPad still works and follows the Mac's span; the zoom buttons are hidden.

The advertisement carries a TXT record with public facts only: `app`, the
protocol version range (`v`, `minv`), the revision (`rev`) and the instance
name (`name`, the radio's name, which is also the Bonjour service name). It
never carries the pairing code, an address, a frequency or a client list.

## On the iPad

1. Open **Hermit Location**. Allow **Local Network** access when asked
   (without it the list stays empty; typing the address still works only if
   Local Network is allowed, because the Mac is on the local network).
2. Tap the Mac under **On this network**, or type its address and tap
   **Connect**.
3. The pairing sheet shows a certificate fingerprint. Check it against the
   Mac's, character for character. If it differs, cancel.
4. Type or paste the pairing code and tap **Pair**.

**Shack volume** and mute are the Mac's own speaker controls. They change
what is heard in the shack and nothing on the iPad.

## Listening

Tap **Listen**. The iPad asks the Mac for its receive audio (12 kHz mono,
the Control API's existing downlink: the same stream the Web Console and
the Python client play) and plays it.

- **The shack's mute and volume do not affect it.** The Mac takes this
  stream ahead of its own speaker volume and mute, so the shack can be
  silent while the iPad listens. (The Control API document used to say the
  opposite; it was wrong and is corrected. No Mac-side change was needed.)
  Squelch, AGC, noise controls and the filter are the receiver's and are
  heard on the iPad as in the shack. While the shack transmits, the
  receiver is muted by the radio and the iPad hears that silence (or the
  operator's monitor, if they have it on).
- **Volume and mute on the Listen row are the iPad's.** They are never sent
  to the Mac. The iPad's hardware volume buttons work as for any audio app.
- **It keeps playing with the screen locked or another app in front.** The
  link to the Mac stays up for it; the spectrum rows and the ten-a-second
  meter are stopped while the screen is not showing them and restart when
  you come back. If you are
  not listening, the link is closed in the background as before.
- **Lock screen and Control Centre** show the dial and mode ("7.074.000
  USB") and the radio's name. Play and pause start and stop listening.
  **Next** and **previous** tune up and down one tuning step, from the lock
  screen and from headphone buttons.
- **Calls and other audio.** A phone call, Siri or an alarm pauses the
  audio; it resumes by itself when the system says the interruption is
  over. If another app takes the audio for good, or the headphones or
  Bluetooth speaker you were listening on go away, it stays paused (it does
  not start playing from the iPad's speaker unasked) and the button reads
  **Resume**.
- **The delay.** A buffer of about a tenth of a second evens out Wi-Fi. The
  status line shows it ("Playing · 120 ms buffered") and counts dropouts.
  After a dropout the buffer is made 40 ms deeper, up to 0.4 s, and eases
  back after half a minute of clean reception. After a stall the backlog
  is skipped, so you hear the present, not the stall. Expect roughly
  0.15–0.25 s from the Mac's speaker to the iPad's on a good network.
- If the Mac sleeps or the network drops while you listen, the iPad keeps
  trying and audio returns with the link. In the background iOS allows
  this only while the audio session stays active, which it does.

The app has no microphone use: the audio session is playback-only, no
input is opened and there is no microphone permission string.

## This iPad's view

- **Pinch** to zoom about your fingers; **two-finger drag** to pan;
  **double tap** (one finger) to bring the dial back to the middle.
- The buttons at the bottom right of the spectrum: zoom out, zoom in,
  centre on the dial, and **Mac view** (go back to following the Mac's
  operator).
- The view is limited to what the radio is sampling (for example 96 kHz
  around the radio's centre at a 96 k sample rate) and to 2 kHz at the
  narrow end. Its resolution is the Mac's analyzer: zooming far in shows
  fewer, wider bins, not more detail.
- While you tune by dragging or with the step buttons, your view moves with
  the dial. A tap tunes without moving the view. If the dial leaves your
  view some other way (the operator tunes, a band change) the view is
  brought back to it.
- The waterfall responds at once: older rows are redrawn on their true
  frequencies as you move, and rows for the new view arrive about a tenth
  of a second later. Parts of older rows that the earlier view did not
  cover are black.

## Apple Pencil

- **Hover** over the spectrum: a cursor and the frequency under the tip,
  to the hertz. Nothing is tuned by hovering. (Needs an iPad and Pencil
  that support hover; the iPad Air M4 with Apple Pencil Pro does. A
  trackpad pointer shows the same cursor.)
- **Tap** with the tip: tune to that frequency, on the Mac's tuning step,
  or on the fine step in fine mode.
- **Drag** with the tip: tune. In **fine** mode the dial moves a tenth as
  far as the tip and lands on 10 Hz (on 1 Hz when the Mac's step is already
  10 Hz or less).
- **Double tap** on the Pencil's barrel: fine tuning on or off. A yellow
  **FINE** chip shows while it is on; tapping the chip also switches it off.
- **Squeeze** (Apple Pencil Pro): a palette at the tip with fine tuning,
  one step down and up, the mode's filter presets and the view buttons.
  Squeeze again or tap ✕ to close it.
- If double tap or squeeze is set to **Off** in **Settings ▸ Apple
  Pencil**, the app does nothing for it.

Fingers and Pencil do different things on purpose: one finger tunes
coarsely and two fingers move the view, so the Pencil can be the precise
tool. The Pencil has no action that keys, arms or sets up a transmitter.

## External keyboard

| Key | Action |
| --- | --- |
| ← → | One tuning step down / up |
| ↓ ↑ | Ten steps down / up |
| Space | Listen / stop |
| M | Mute this iPad |
| F | Fine tuning on / off |
| = and − | Zoom this iPad's view in / out |
| 0 | Follow the Mac's view |

To make the Mac forget the iPad, use **Revoke** or **Forget** on the Mac. To
make the iPad forget the Mac, disconnect and swipe it away under **Paired
Macs**; that deletes the code from the Keychain.

## Build and install on your own iPad

Requirements: Xcode with the iOS SDK, an Apple Development signing identity
in the team the project names, and the iPad (iPadOS 17 or later) registered
in that team. The app keeps the companion's bundle identifier
(`com.hermitsdr.location`), automatic signing and capabilities, so an iPad
is one more registered device, not a new app record. No entitlement was
added.

```sh
open Companion/HermitLocation.xcodeproj
```

1. Connect the iPad by cable (or pair it for network debugging) and trust
   the Mac on it. On the iPad switch on **Settings ▸ Privacy & Security ▸
   Developer Mode** and restart when asked.
2. In Xcode choose the **Hermit Location** scheme and the iPad as the run
   destination.
3. If Xcode reports that the device is not in the provisioning profile, let
   automatic signing register it (**Signing & Capabilities ▸ Try Again**).
4. **Product ▸ Run**. The first launch may need the developer certificate
   trusted under **Settings ▸ General ▸ VPN & Device Management**.

With a free Apple ID the install expires after seven days; with the paid
developer team it lasts until the profile expires (a year).

The app's capabilities did not change with audio: background audio is an
`Info.plist` background mode (`UIBackgroundModes` now lists `location` and
`audio`), not an entitlement, and needs no paid capability.

Compile checks without a device:

```sh
xcodebuild -project Companion/HermitLocation.xcodeproj \
  -scheme 'Hermit Location' -configuration Debug -sdk iphonesimulator \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath /private/tmp/hermit-companion-ios-build \
  CODE_SIGNING_ALLOWED=NO build
python3 tools/swiftpm.py test --filter HermitLink
```

## How it is built

- `Companion/HermitLinkKit/` is the client: plain Swift (Foundation,
  Network, CryptoKit, Security, and since this slice AVFAudio and Metal),
  no UIKit. It was written from
  [ControlAPI.md](ControlAPI.md) and shares no source with the server. The
  companion project compiles these files into the app; `Package.swift`
  compiles the same files as the `HermitLinkKit` target so the package tests
  run them on macOS.
  - `HermitLinkWire.swift`: pairing code, handshake answer, the receive-only
    command set, decoders for every server message and binary frame.
  - `HermitLinkDiscovery.swift`: Bonjour results and TXT parsing, typed
    addresses, the browser.
  - `HermitLinkTransport.swift`: one TLS WebSocket with the certificate pin.
  - `HermitLinkClient.swift`: handshake, state, commands, keep-alive and
    reconnection.
  - `HermitLinkReconnect.swift`: what to do after each kind of ending, and
    the spacing of dial commands during a drag.
  - `HermitLinkStore.swift`: pairings and the Keychain.
  - `HermitLinkSpectrum.swift`: waterfall history, panadapter trace, the
    touch- and pencil-to-frequency maths and the viewport (pan, zoom,
    clamping).
  - `HermitLinkAudio.swift`: the jitter buffer, its thread-safe wrapper and
    the play / pause rules for interruptions and lost outputs.
  - `HermitLinkAudioPlayer.swift`: an `AVAudioEngine` with one source node
    at 12 kHz mono. It can render into memory instead of a device, which
    is how the tests run it.
  - `HermitLinkWaterfallRenderer.swift`: the Metal waterfall. Plain Metal
    with its shader in the source, so the test renders it off screen on
    macOS.
- `Companion/HermitLocation/Console*.swift` are the SwiftUI views and a thin
  model around the client. `ConsoleAudio.swift` owns the audio session, Now
  Playing and the lock-screen commands; `ConsoleWaterfallView.swift` hosts
  the renderer in an `MTKView`; `ConsoleSpectrumSurface.swift` holds the
  gesture recognizers and the Pencil interaction. The location sender's
  files are unchanged.
- **Audio path.** Frames go from the connection's own queue straight into
  the jitter buffer, not through the main thread, so a busy screen adds no
  jitter. The audio thread pulls from the buffer under a short lock.
- **The Mac's waterfall renderer is not shared.** It is 2,700 lines bound
  to AppKit, MetalPerformanceShaders and the Mac app's scene and overlay
  state, and it draws from the full analyzer row, which the Control API
  does not send. The iPad has a small renderer of its own for what it does
  receive: each row is uploaded once into a ring texture, and every frame
  places each row by its own centre and span, so panning and zooming cost
  no re-upload. Zoomed out, a pixel shows the strongest bin under it.
- The connection is TLS 1.2 or later to the Mac's self-signed certificate,
  accepted only when its SHA-256 matches a fingerprint the user has paired
  with. There is no plaintext mode in the app (a test-only loopback mode
  exists in the kit and a test checks that the app never names it), and no
  App Transport Security exception.
- Nothing is sent anywhere except to the paired Mac. No analytics, no
  cloud, no account.

## Verified, and not

Verified by tests on macOS (`HermitLinkWireTests`, `HermitLinkLoopbackTests`,
`HermitLinkAudioTests`, `HermitLinkSpectrumWindowTests`, 52 tests):

- Every codec against the server's own and against the byte examples in
  ControlAPI.md.
- The client against the **production** Control API server on loopback:
  pairing, state, meters, tune, step, band, mode, filter preset, volume,
  mute, a refused tune while the shack is keyed, spectrum rows, a session
  without the Control permission, the server stopping and returning, a
  background pause and resume, Kick, a wrong code, and a missing code.
- **Audio**, same server: Listen subscribes and the receiver's audio tap is
  taken only then; a tone arrives in the jitter buffer at its own level;
  shack mute and zero volume do not stop it; in the background with audio
  the link stays and the spectrum stops; after the server stops and
  returns (also while "in the background"), listening resumes by itself
  and nothing stale is played; Stop
  releases the tap; a Mac that does not grant Audio is never asked.
- **The jitter buffer** against generated arrival patterns: a steady stream
  is played sample for sample; a lost frame is silence of its own length
  with no change of delay and no click; reordered and duplicate frames; a
  frame that arrives after its time; the sequence number wrapping; a 0.9 s
  stall followed by a burst (one dropout, the backlog skipped, the delay
  back near its target); twenty stalls in a row (the target stops at 0.4 s
  and eases back in calm); a restarted stream; ten minutes with the two
  clocks 0.1 % apart in each direction (no dropout, no skip, delay within
  0.04–0.20 s, speed correction within 2 %); frames arriving while nothing
  is played (bounded).
- **The player** rendering into memory (no device): a 1 kHz tone in is a
  1 kHz tone out at 48 kHz, the local volume scales it, local mute
  silences it while the stream keeps flowing. Its render callback is also
  called from a background thread, as the audio system will call it.
- **The play / pause rules** for interruptions, a lost output and an audio
  system reset.
- **The Mac's audio tap is ahead of shack volume and mute**: a test pins
  the three places in the Mac source that make it so (the app's engine is
  compiled by no package test, so this is a source check, not a run).
- **Own view**, production server: the iPad's window is served alongside a
  second client that follows the operator; a carrier the operator cannot
  see is where it should be; a burst of fifty window changes sends at most
  four requests and ends on the last; a window past the edge is slid back
  in; a window wider than the sampled span gets all of it; returning to
  the Mac's view. Pan, zoom and clamp maths, and the Pencil's hover and
  fine-drag maths, on their own.
- **The Metal waterfall**, rendered off screen on this Mac's GPU: newest
  row on top, each row on its own frequencies in three different views,
  black where a row has no data, a one-bin carrier kept when zoomed out,
  the slide-in between rows, the ring wrapping, clear.
- Real TLS on loopback with a throwaway certificate: an unknown certificate
  is reported and nothing is sent; after pairing the link works; a device
  pinned to another certificate refuses.
- A scripted fake server: silence treated as a lost link, a full server
  retried, a later protocol version not retried.
- A Bonjour advertisement with the Mac's TXT record, confined to the
  loopback interface, found by the app's browser and connected to by name.
- Receive only: the client can build no transmit, split, VFO B or A/B swap
  message; the send gate is now a list of the fourteen message types that
  may leave plus the list of those that never may; no source file names a
  transmit message or opens an audio input.
- The app compiles for the iOS Simulator SDK (universal, iPhone and iPad).

**Not verified. Nothing has run on an iPad or in a simulator**, and no
sound has been played by any of this, on any device:

- **Audio by ear**: that it sounds right, the real delay, behaviour on real
  Wi-Fi, the lock screen, Control Centre, AirPods and Bluetooth, a phone
  call arriving, unplugging headphones, the silent switch.
- **`ConsoleAudio.swift` as a whole** (the audio session, the notification
  handlers, Now Playing, the remote commands): compiled for iOS only. Its
  decisions come from the tested rules, but the wiring has never run.
- **Background behaviour**: that iOS keeps the app and its link alive with
  the screen locked for as long as audio plays, and what happens when the
  link drops in the background for minutes.
- **The Metal view on iPadOS**: the renderer was drawn off screen on macOS;
  the same shader source is compiled at run time on the iPad and has not
  been. The 60 Hz drawing, its power use and its look are unseen.
- **Every gesture and the Pencil**: the recognizers, hover, barrel double
  tap and squeeze are compiled for iOS only. Whether one-finger drag,
  two-finger pan and pinch stay out of each other's way has not been felt.
- **External keyboard shortcuts**: compiled only. Plain letter and arrow
  shortcuts may be taken by the system when a text field has focus.
- The screen itself: layout at 11 inches in both orientations with the new
  Listen row, touch targets, Dynamic Type, VoiceOver, colours.
- Discovery across a real network between two devices, the iPadOS Local
  Network prompt, and the Mac's real Keychain TLS identity (the tests use a
  throwaway certificate and the loopback interface).
- TLS and a Bonjour-name connection together (each is tested separately).
- The iPad Keychain (tests use an in-memory stand-in).
- That the iPhone location sender is unchanged in use. Its source files are
  untouched and the app still opens on it on an iPhone, but it was not run.

Checklist for the first run on the iPad (iPad Air 11-inch M4 with Pencil):

1. Build and run from Xcode; the Mac appears under **On this network**;
   pair. Frequency, mode, band and S-meter follow the Mac.
2. Tap **Listen**. You hear the receiver within a second. The status line
   reads "Playing · … ms buffered".
3. Mute the Mac's speaker (on the Mac, and with the iPad's shack mute
   button). **The iPad keeps playing.** Move the iPad's own slider and
   mute: only the iPad changes.
4. Lock the iPad. Audio continues. The lock screen shows the frequency
   and mode; pause and play work; next / previous move the dial one step.
5. Open another app for a minute, then come back: audio never stopped and
   the waterfall restarts.
6. Walk to the edge of Wi-Fi range and back: after a dropout the audio
   returns and is not noticeably later than before.
7. Call the iPad (FaceTime) or trigger Siri while listening: audio pauses
   and resumes. With headphones, unplug or switch them off: audio pauses
   and does not come out of the speaker.
8. Pinch the spectrum, drag it with two fingers, use the magnifier
   buttons: the waterfall moves at once, the Mac's own panadapter does
   not. **Mac view** returns to the operator's span.
9. Drag with one finger to tune: the signal follows the finger and your
   zoomed view moves with the dial. Tap a signal: it tunes there.
10. Pencil: hover shows a cursor and a frequency; tap tunes exactly;
    double-tap the barrel shows **FINE** and a drag then moves a tenth as
    far; squeeze opens the palette at the tip.
11. With a keyboard: arrows tune, Space starts and stops listening.
12. Switch the Control API off and on at the Mac while listening: the iPad
    says why it is reconnecting, comes back by itself and audio resumes.
13. Key the shack transmitter on a dummy load (with the operator's usual
    approval): the iPad shows "Shack is transmitting", refuses to tune and
    says why.
14. On the iPhone, the app is still the location sender and still shares.

## Known limits of this slice

- **Audio is the shack's one receiver mix**, mono, 12 kHz, uncompressed
  (192 kbit/s). There is no separate receiver for the iPad: it hears what
  the main receiver is tuned to, with the shack's filter, AGC, squelch and
  noise controls. No Opus yet (the Control API reserves it).
- **The delay is not adjustable** from the screen; the buffer sizes itself.
- **Loss concealment is silence** with a short fade, not interpolation.
- **The view cannot leave the sampled span** and its resolution is the
  Mac's analyzer. Rows older than a change of view cover only what that
  earlier view covered.
- The waterfall's colours and range are fixed (70 dB above a tracked noise
  floor). No passband overlay, no filter-edge dragging, no tuning ring.
- **Pencil pressure and tilt are not used.** Hover uses position only.
- No spots, decoder text, memories or second-screen panes.
- No widget and no Shortcuts actions. Lock-screen control is play / pause
  and one step up or down.
- One Mac at a time. The shack volume and mute buttons are the shack's.
- The tuning step is the Mac's current step; the Control API has no command
  to change it.
- With a Mac older than Control API revision 7 there is no own view (the
  rest works).

## Next slices

1. **A tuning ring**, a passband overlay with draggable filter edges, and
   memories and spots as panes. Decoder text needs a Control API addition.
2. **Opus audio** on the Control API for use away from the LAN, and an
   adjustable delay.
3. **A second, independent receiver for the iPad** (its own frequency and
   mode). The Mac has sub and independent receivers; exposing one per
   client is Mac-side work beyond the Control API server.
4. A widget, Shortcuts actions, and a larger lock-screen surface.
5. Transmit from the tablet is separate, reviewed transmit-path work with a
   dummy-load session. Nothing in this slice prepares for it.

## Decisions for the owner

- **Own device or public?** This slice assumes own device. A public app
  needs App Store review, privacy declarations, support, and a plan for a
  newer iPad app meeting an older Mac (the handshake already carries the
  version and revision).
- **Name and bundle identifier.** The app is still called Hermit Location
  with the identifier `com.hermitsdr.location`, so signing did not change.
  A name that fits both jobs would change the label under the icon on the
  iPhone too; a new identifier would mean a new provisioning profile.
- **Should the iPhone get the Radio tab?** It is iPad-only so the iPhone app
  stays as it was. The code is not iPad-specific, but the layout is.
- **Shack volume and mute on the iPad.** They change what the shack hears
  and no longer have anything to do with the iPad's own audio. They can be
  removed from the iPad if that is unwelcome.
- **The Web Console said the opposite about shack mute.** Its page and
  [WebConsole.md](WebConsole.md) claimed the downlink went silent. Both were
  corrected in the same release as this slice.
- **Pencil squeeze and double tap.** Fine tuning and a palette were chosen.
  Other candidates: toggle Listen, drop an RF notch at the tip, switch
  between the two last frequencies.
- **Lock-screen next / previous** tune one step. They could instead move
  between memories or bands once those exist on the iPad.
- **Split, VFO B and A/B swap** are left out because they move or arm the
  shack's transmit frequency. They can be added when transmit from the
  tablet is reviewed, or sooner if wanted as receive conveniences.
