# iPhone location link

This receives the phone's location independently of the radio. The new
[RDF Session recorder](RDFSession.md) can save these fixes alongside channel
measurements when you explicitly start a recording. Signal fingerprinting,
source localization and route guidance remain future work. The Mac location receiver is included from 2026.1120_001. The companion requires
separate developer installation; no App Store/TestFlight build is distributed.

## On the Mac

Open **Radio → iPhone Location…**. A radio connection is not required.

1. Click **Start session**. Allow Local Network access if macOS asks.
2. Click **Copy pairing invitation**.
3. On the iPhone, open **Hermit Location**, paste the invitation and tap
   **Share location**. Allow Location (While Using), Precise Location and
   Local Network access.
4. Check the Mac's connection status, coordinates, reported accuracy and fix
   age. Green CURRENT requires a fix no older than 10 seconds and reported
   horizontal accuracy no worse than 50 m. This is an admission threshold,
   not an independent accuracy measurement or a guarantee of RDF precision.
5. Tap **Stop sharing** on the phone when finished to stop its location
   updates. **End session** on the Mac disconnects the phone and invalidates
   the invitation. The phone keeps acquiring location while retrying after a
   lost connection, so end it on the phone as well. A new Mac session requires
   a new copy/paste.

Universal Clipboard may make the paste convenient when both devices use the
same Apple Account and meet Apple's Continuity requirements. The location
connection itself does not use iCloud or require matching accounts. Keep Wi-Fi
on. Bonjour discovery and Apple peer-to-peer Wi-Fi are enabled; the devices can
also use the same local Wi-Fi network. Internet service is not needed. Actual
hotspot and peer-to-peer background behavior still needs field acceptance.

The phone requests standard Core Location updates during an active session,
including background updates with the system indicator. It sends at most about
one new fix per second; it never changes a cached fix's original timestamp.
Without a fresh fix it reports unavailable. Stopping the phone stops Core
Location, browsing, the connection and its retry task. A killed phone or a lost
link causes the Mac to lose its usable fix or mark it stale.

The Mac displays speed and true course of travel when supplied by iOS. Course
is **not** phone orientation, vehicle heading while stationary or antenna
heading. The phone may be some distance from the antenna; future measurement
fusion must account for that offset and position uncertainty.

## Build and install the companion

The companion is a separate native SwiftUI iOS/iPadOS 17+ target, with no
third-party dependencies. On an iPad the same app also opens a receive
console ([iPadCompanion.md](iPadCompanion.md)); on an iPhone it is the
location sender described here:

```sh
open Companion/HermitLocation.xcodeproj
```

Select the **Hermit Location** scheme, select the intended connected iPhone,
and configure an Apple Development signing identity/provisioning profile for
`com.hermitsdr.location` in the appropriate team. Build and Run from Xcode.
The new companion target uses automatic development signing; the Mac app's
manual Developer ID settings are unchanged. Device installation, registration
and any App Store/TestFlight distribution are separate operator steps.

Compile checks without installation:

```sh
xcodebuild -project Companion/HermitLocation.xcodeproj \
  -scheme 'Hermit Location' -configuration Debug -sdk iphonesimulator \
  -derivedDataPath /private/tmp/hermit-location-ios-build \
  CODE_SIGNING_ALLOWED=NO build
python3 tools/swiftpm.py test --filter PhoneLocationTests
```

## Protocol and ownership

- `Integration/Location/LocationWire.swift` is compiled from the same source by
  both apps and the regression package. Version 1 uses newline-delimited JSON
  with a monotonically increasing sequence and either `fix` or `unavailable`.
  A fix includes WGS84 coordinates, Unix capture time, horizontal accuracy and
  optional altitude, speed and true course. No device name or account is sent.
- `LocationTransport` generates a random 128-bit key and UUID for each explicit
  Mac session. Bonjour advertises `_hermitgps._tcp` under a UUID service name;
  it never advertises the key or coordinates. The copy/pasted invitation carries
  the key. Treat the invitation as a secret while the session is active.
- Network.framework TLS 1.2 uses the single PSK AES-128-GCM-SHA256 suite (RFC
  5487, 0x00A8). Both peers must know the invitation before application bytes
  pass. There is no plaintext fallback or disabled certificate verification.
  PSK without ephemeral DH does not provide forward secrecy if the session key
  is later compromised. The key is session-only and never written to settings,
  Keychain, a log or a file; copying explicitly puts it on the system clipboard.
- The Mac admits one authenticated sender, at most four pending handshakes,
  a 12-second handshake timeout, lines under 4 KiB and at most ten messages per
  second. The phone retains at most one newest pending send, times out stuck
  sends and retries interrupted connections at three-second intervals.
- Owners and callbacks are main-actor isolated, with generation checks rejecting
  callbacks from stopped/replaced sessions. No radio, audio, DSP, telemetry or
  transmit object is referenced. Nothing starts at application launch or just
  because the window opens. Closing the Mac window leaves the explicit session
  running; End session or quitting ends it.
- The tracker rejects invalid/nonfinite coordinates, negative accuracy, replayed
  sequences, duplicate/backwards capture times, fixes over ten seconds old and
  capture times more than five seconds in the future. It uses both original
  capture age and monotonic receipt age for staleness. Grossly mis-set device
  clocks must be corrected before use. Disconnect/unavailable clears the fix.
- This link's locations and invitations are memory-only. It performs no
  recording, analytics, cloud lookup, cloud transport or background upload.
  The separate RDF Session recorder can save fixes only after the operator
  explicitly creates a recording there. Pairing keys are never included. The Mac's own
  location permission is unnecessary because it receives the phone's fixes.

## Acceptance still required

The automated tests use generated coordinates and loopback only. They cannot
prove GPS accuracy or iOS background reliability. Before treating this as a
field-ready location source, test on a physical iPhone and Mac:

- First-run location, precise-location and local-network prompts; deny/revoke
  each and recover through the UI.
- Copy/paste pairing, incorrect invitation, two nearby Macs, occupied session,
  new-session invitation invalidation and stop/restart on both devices.
- Same Wi-Fi, peer-to-peer without internet, and personal hotspot setups.
- Lock the phone and drive with a passenger operating the laptop; observe at
  least 15 minutes of fresh updates, reconnect after Wi-Fi interruption, then
  stop and verify the location indicator goes away.
- Loss of satellite reception, reduced accuracy, delayed/cached updates and
  changed device clocks must never leave an old location labeled current.

No RF transmission or radio connection is needed for these tests.

## Software verification on 2026-11-19

- Mac Developer ID Debug and Release builds passed.
- iOS simulator Debug and iPhone SDK unsigned Release builds passed. These
  compile checks do not install an app or prove background operation.
- Nine GPS wire/freshness/encrypted-loopback tests passed. A final 121-test
  focused run also covered Automation, DocsConsistency and FeatureCatalog.
- The full package run executed 4,868 tests with 26 skipped and one failure
  from an old two-key Info.plist expectation. That expectation was updated to
  check the exact permitted keys (including Bonjour) and passed in the focused
  rerun. The full suite was not rerun after that correction and the small
  callback-lifetime cleanup.
- The actual stopped Mac window rendered in Dark/Light at 440/520 pt widths
  and all four images were inspected. The listener remains off on window open.
  The live pairing/readout surfaces and iPhone UI await device inspection.
