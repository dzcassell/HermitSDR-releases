# Ask The Crab: application controls

The app-control bridge is included in 2026.1020_001. Software checks do not
establish hardware or on-air acceptance.

The operator's Crab session can discover controls rather than relying on a
fixed list of receiver tools. Both the on-device and Claude backends expose:

- `app_capabilities(query)`: search registered settings, commands and the entire
  feature catalog. Empty query gives domains. Results contain exact IDs,
  accepted values and current state. Ordinary words such as “automatic notch,”
  “receive volume” and “compressor attack” find their native control IDs.
  Follow the returned `page=N` query to
  browse additional matches without overflowing the on-device context.
- `app_control(action,target,value)`: get/set typed settings, open/show/hide a
  feature, or run a registered command. Values use documented units and finite
  ranges. The bridge reads back the real owner after a setting change.
- `media_deck(action,target,route)`: play a YouTube URL or saved pad, stop,
  pause/resume, list saved pads and inspect actual playback/capture/TX status.

Examples: “turn on the automatic notch,” “set RX squelch to −105 dBm,” “open
Weather Fax,” “use the Broadcast Hi-Fi receive EQ,” “recall my receive preset,”
“switch OBS to [known scene],” “join Discord voice,” “stop the live stream,”
“play this YouTube video [URL],” and “media deck status.” Controls expose RX,
noise processing, AGC, decoder switches/RTTY parameters, display/palette,
resource presets, bounded TX audio processing, RX/TX graphic EQ arrays, Media Deck gain/FX and shared keyboard actions.
Receive preset/EQ libraries and TX profile/effect/source commands reuse their
native owners. Capability discovery reports exact names and arguments.

Every feature has a navigation destination. Opening controls does not start
that feature. This bridge does **not** claim every button or every workflow is
scriptable: experimental labs, credential editing, radio discovery/connection,
calibration, arbitrary file import, account setup and final social publishing
continue in their native interfaces. Unknown IDs return a refusal. No shell,
arbitrary defaults writes, KVC, secret reads or synthetic UI clicks are exposed.

## YouTube and transmission

“Play this YouTube video audio over the air [URL]” is handled before either
model is invoked. Its exact URL is passed to the existing authorized embedded
player. The receipt describes a **request**, then reports actual state; preparing
or buffering never means playback succeeded or RF was observed. Provider and
capture failures remain visible in Media Deck and `media deck status`.
Receiver tuning, mode, volume and filter changes cannot substitute for media.
Directions and negated requests do not authorize a media transmission. Quoted
titles and URLs do not provide route permission. Explicit on-stream requests
select the stream route; unqualified playback remains local. Shared keyboard
commands use an explicit reviewed allowlist rather than inheriting future actions.

The route is explicit: `local`, `stream`, or `air`. Local/stream requests refuse
while Auto PTT is enabled, while TX is already keyed, or while App audio is the armed TX input. Saved pads do not silently retain an external stream
route when requested locally. The tool does not invent URLs, download video or
bypass System Audio Recording permission. Only YouTube URLs embed media; ordinary
web-link pads are not represented as captured audio.

Air playback requires the operator to request it explicitly, ARM locally and
pass the existing coordinator/policy/ownership/protection gates. It never arms
the radio or changes drive, frequency, antenna or safety policy. Existing deck
playback must be stopped first so other pads cannot inadvertently join the new
transmission. A temporary Crab Auto PTT enable expires on stop, pause, failure,
completion or external unkey. It cannot automatically re-key a refused over.
An Auto PTT latch the operator had already enabled remains the operator's choice.

Native Feld Hell, ALE calling and a single WSPR attempt are available as
registered commands only after local ARM and the existing per-mode Native
Transmit enable. Hell text and ALE destinations must appear in an explicit
operator send/call request. WSPR requires explicit advertised dBm, uses the
configured station call/grid, current dial and one attempt at a 1500 Hz audio
offset. The advertised value does not change drive. Longer finite WSPR schedules
remain in Native Transmit. Native status/stop reuse the existing owner and leases.

## External services and privacy

Discord connection/voice and OBS connection/scene/stream actions require an
operator request naming the service and operation. YouTube startup operates the
configured internet broadcast destinations; it is distinct from playing a clip
through radio TX. Setup, permissions and credentials remain with the native
owners. Service receipts distinguish requested operations from confirmed state.
Social announcements can be prepared for the existing preview; publication is
still a separate action in that window. Public viewer/co-host chat cannot invoke
any of these new controls or discover the private control registry.

## Verification

The focused tests pin the screenshot request, route admission, URL fidelity,
provider parity, public-chat exclusion and tool budget. The Debug-only
`HERMITSDR_CRAB_CONTROL_PROBE=/absolute/output.json` hook runs in Demo and checks
the real settings owners, every feature destination, invalid input refusals,
ARM/protection exclusion and the screenshot's SAFE refusal without invoking an
AI backend. The hook mutes its owned app before requesting Demo. Run it only with network, Keychain and operator
preferences denied. It does not open a video, arm or key a radio.

Physical RF, browser playback, live account permissions and third-party service
responses require separate operator-assisted acceptance. A source build or fake
provider test does not prove those interactions.

Run the owned-app check with `tools/crab-control-smoke.sh <signed Debug app>`.
`tools/crab-native-control-smoke.sh` exercises the production native-TX request
admission against inert ports; no radio or sample player is constructed.

Historical stage verification (2026-10-18): 2,774 tests, seven intentional skips,
zero failures; 121 focused checks; signed Debug/Release and strict signatures;
owned native startup, actual-owner and inert admission/media smokes plus repository
audit. The owner probe covers 117 settings and 76 navigation destinations using
an inert navigation sink, not visual acceptance of every window. The screenshot
request invokes no model. Live provider/account/capture permissions and RF remain
unverified. Current combined-release evidence is recorded in the October handoff.
