# iPad companion (first slice)

A native iPad screen for a HermitSDR running on a Mac on the same network:
it finds the Mac, pairs with it, shows the dial, mode, band, S-meter, a
panadapter and a waterfall, and offers receive controls. It is the existing
**Hermit Location** companion made universal: on an iPhone the app is the
location sender exactly as before ([iPhoneLocation.md](iPhoneLocation.md));
on an iPad it opens on a **Radio** tab and keeps the location sender in a
**Location** tab.

This is the first slice of issue #469. It is an own-device build installed
from Xcode. There is no App Store or TestFlight build.

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
- **Draws** a panadapter line and a scrolling waterfall from the Control
  API's spectrum rows (512 points, ten rows a second). It follows whatever
  span the operator has on the Mac's own panadapter. When that window moves
  or zooms, older waterfall rows are redrawn on their true frequencies.
- **Controls the receiver:** drag the spectrum sideways to tune (the signal
  follows your finger), tap a signal to land on it, step buttons for one and
  ten tuning steps (hold to repeat), band, mode, the mode's filter presets,
  and the shack's volume and mute.
- **Reconnects by itself** when the Mac sleeps, its radio session ends, the
  network drops or the app returns from the background. It does not retry a
  refused pairing code (three failures start the Mac's one-minute
  cool-down), and it does not reconnect after the operator's **Kick** until
  you tap **Try again**.
- Keeps the screen awake while it is connected.

## On the Mac

1. Open **Settings ▸ AI & APIs ▸ Control API** and switch it on. It is off
   by default. The listener, and so the Bonjour advertisement, exists only
   while it is on **and** a radio is connected (or Demo Mode or a replay is
   running).
2. Leave that pane open: it shows the **certificate fingerprint** and the
   **pairing code** you need on the iPad.
3. After the iPad pairs it appears in the client list there. **Control** and
   **Spectrum** are its permissions; the app does not ask for **Audio** in
   this slice. **Kick**, **Revoke** and **Rotate code** work as for any
   other Control API client ([ControlAPI.md](ControlAPI.md) § 9).

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

**Shack volume** and mute are the Mac's own speaker controls: the Control
API has no separate volume for a client. They change what is heard in the
shack.

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
  Network, CryptoKit, Security), no UIKit. It was written from
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
  - `HermitLinkSpectrum.swift`: waterfall history, panadapter trace and the
    touch-to-frequency maths.
- `Companion/HermitLocation/Console*.swift` are the SwiftUI views and a thin
  model around the client. The location sender's files are unchanged.
- The connection is TLS 1.2 or later to the Mac's self-signed certificate,
  accepted only when its SHA-256 matches a fingerprint the user has paired
  with. There is no plaintext mode in the app (a test-only loopback mode
  exists in the kit and a test checks that the app never names it), and no
  App Transport Security exception.
- Nothing is sent anywhere except to the paired Mac. No analytics, no
  cloud, no account.

## Verified, and not

Verified by tests on macOS (`HermitLinkWireTests`, `HermitLinkLoopbackTests`,
28 tests):

- Every codec against the server's own and against the byte examples in
  ControlAPI.md.
- The client against the **production** Control API server on loopback:
  pairing, state, meters, tune, step, band, mode, filter preset, volume,
  mute, a refused tune while the shack is keyed, spectrum rows, a session
  without the Control permission, the server stopping and returning, a
  background pause and resume, Kick, a wrong code, and a missing code.
- Real TLS on loopback with a throwaway certificate: an unknown certificate
  is reported and nothing is sent; after pairing the link works; a device
  pinned to another certificate refuses.
- A scripted fake server: silence treated as a lost link, a full server
  retried, a later protocol version not retried.
- A Bonjour advertisement with the Mac's TXT record, confined to the
  loopback interface, found by the app's browser and connected to by name.
- The app compiles for the iOS Simulator SDK (universal, iPhone and iPad).

**Not verified. Nothing has run on an iPad or in a simulator:**

- The screen itself: layout at 11 inches in both orientations, touch
  targets, Dynamic Type, VoiceOver, colours, the waterfall's look and frame
  rate, the feel of drag tuning.
- Discovery across a real network between two devices, the iPadOS Local
  Network prompt, and the Mac's real Keychain TLS identity (the tests use a
  throwaway certificate and the loopback interface).
- TLS and a Bonjour-name connection together (each is tested separately).
- The iPad Keychain (tests use an in-memory stand-in).
- Behaviour when the app is backgrounded, the iPad locks, the Mac sleeps or
  Wi-Fi roams, on real hardware.
- That the iPhone location sender is unchanged in use. Its source files are
  untouched and the app still opens on it on an iPhone, but it was not run.

Checklist for the first run on the iPad:

1. The Mac appears under **On this network** within a few seconds of the
   Control API being switched on with a radio connected.
2. The fingerprint on the sheet matches the Mac's; a wrong code is refused
   with a clear message; the right code connects.
3. Frequency, mode, band and S-meter follow the Mac.
4. Drag tuning feels right and lands where expected; tap lands on a signal.
5. Band, mode, filter and step buttons act; volume and mute act on the shack.
6. Switch the Control API off and on at the Mac: the iPad says why it is
   reconnecting and comes back by itself.
7. Press the Home button, wait a minute, return: it reconnects.
8. **Kick** on the Mac: the iPad stays disconnected until **Try again**.
9. Key the shack transmitter on a dummy load (with the operator's usual
   approval): the iPad shows "Shack is transmitting", refuses to tune and
   says why.
10. On the iPhone, the app is still the location sender and still shares.

## Known limits of this slice

- **No audio.** The app does not ask for the audio stream.
- The waterfall is a simple image redrawn ten times a second from 512-point
  rows, not the Mac's renderer. It shows the span the Mac's operator has
  chosen; the iPad cannot pan or zoom on its own, because the Control API
  sends only that window.
- No passband overlay, no pinch, no Apple Pencil tools, no tuning ring.
- No spots, decoder text, memories or second-screen panes.
- One Mac at a time. Volume and mute are the shack's.
- The tuning step is the Mac's current step; the Control API has no command
  to change it.

## Next slices

1. **Audio.** Subscribe to the Control API's 12 kHz PCM stream, play it
   through a jitter buffer, and keep it running with the screen locked or
   another app in front (needs the `audio` background mode and an audio
   session; no paid entitlement). The Control API's downlink is the shack's
   final speaker mix, so shack mute silences the iPad too. A separate remote
   audio bus on the Mac would fix that and is a Mac-side change.
2. **Metal waterfall.** Share the Mac's waterfall renderer and palette where
   they are platform-neutral, at the display's refresh rate, with pinch zoom
   and a passband overlay. Independent pan and zoom need a Control API
   addition (a client-chosen span), which is also Mac-side work.
3. **Apple Pencil.** Hover for a frequency cursor without tuning, tap for
   exact tuning, drag the filter edges, squeeze and double-tap actions. The
   Web Console's pencil tools ([WebConsole.md](WebConsole.md)) are the model.
4. A tuning ring, memories and spots, lock-screen controls, a widget,
   Shortcuts and an external keyboard.
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
- **Audio.** Accept the shack's speaker mix for the next slice, or add a
  separate remote audio bus on the Mac first.
- **Shack volume and mute on the iPad.** They change what the shack hears.
  They can be removed from the iPad if that is unwelcome.
- **Split, VFO B and A/B swap** are left out because they move or arm the
  shack's transmit frequency. They can be added when transmit from the
  tablet is reviewed, or sooner if wanted as receive conveniences.
