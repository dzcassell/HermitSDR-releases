# Ask The Crab: application controls

The app-control bridge is included in 2026.1020_001. Software checks do not
establish hardware or on-air acceptance.

## Choosing a backend

The gear in the Ask The Crab window chooses which model answers. Every
backend drives the app through the same tools, the same permission rules and
the same action receipts; none can do something the others cannot, and none
can arm or key the radio.

| Backend | What it needs | What leaves the Mac |
| --- | --- | --- |
| On this Mac (private) | Apple Intelligence on a supported Mac | Nothing you ask. |
| Claude | An Anthropic API key | Your question, the one-line "Radio now" status and tool results go to Anthropic (api.anthropic.com) over HTTPS. |
| OpenAI | An OpenAI API key | The same text goes to OpenAI (api.openai.com) over HTTPS, or to the compatible server you enter. |
| Ollama | Ollama running on this Mac or on your network, with a tool-capable model | On this Mac: nothing. On another machine: the same text goes to that machine unencrypted over the local network. |

API keys are stored in the macOS Keychain. They are not written to the
settings file, are not placed in a URL and are not shown again after you save
them; the pane only says that a key is saved. **Test connection** sends one
small request to the selected backend and shows either success or the
server's own error. With **On this Mac** selected the app sends nothing to
any of the others.

**Claude.** Paste the key, press Save, and pick a model: Claude Opus 5.5 (the
default), Claude Fable 5.2, Claude Sonnet 5.5 or Claude Haiku 5.5. The Model
ID field accepts any other model ID your account offers.

**OpenAI.** Paste the key, press Save. The Model field is free text because
model names change. Leave Server at `https://api.openai.com`, or enter another
server that speaks the same Chat Completions API. A custom server must use
`https://` unless it is on this Mac or your local network. The saved key is
sent to whichever server is entered.

**Ollama.** No key. Server defaults to `http://127.0.0.1:11434`, which is
Ollama on this Mac. To use another machine, enter its address, such as
`http://192.168.1.20:11434` or `http://studio.local:11434`; on that machine
Ollama has to listen on the network (`OLLAMA_HOST=0.0.0.0`). Only this Mac,
private network ranges (10.x, 172.16–31.x, 192.168.x, 169.254.x) and `.local`
names that resolve to them are accepted; a public internet address is refused
with a message, and a redirect to another host is never followed. The Model
menu lists what that server has installed; the arrow button asks again. If
the server cannot be reached the pane says "Cannot reach Ollama at …" with
the reason.

The crab works through tools, and many local models cannot call tools. When
the chosen model has no tool support the crab says so in plain words and
names what to do, rather than answering from imagination. Install a model
that supports tools, for example `ollama pull qwen3`, then pick it. Small
local models also choose tools less reliably than the cloud models; the
action receipts in the chat remain the record of what the radio actually did.

When co-host mode answers viewer questions, those questions go to the selected
backend too. Viewer chat keeps its reporting-only tools on every backend and
never gets web search.

## Application controls

The operator's Crab session can discover controls rather than relying on a
fixed list of receiver tools. Every backend exposes:

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

## Reviewing SSB audio

“Review my SSB transmit configuration and suggest tweaks for muddy audio”
runs an English-language, read-only review of the configured input, voice
profile, passband and EQ. The report gives a small adjustment to audition
and identifies the settings behind it. Use a matched playback level in
the [SSB Profile Laboratory](SSBProfileLaboratory.md) to compare recordings.

The review reads settings directly. It has no measurement of the signal
at the receiving station. Use an actual recording or a monitored comparison
to evaluate the effect. The app's on-device model can summarize supplied
facts and work with narrow tools. Apple recommends a larger model when a
task requires more reasoning or context. The local MCP interface makes
selected, expiring evidence available to a compatible desktop client.
[Apple Foundation Models](https://developer.apple.com/documentation/foundationmodels) ·
[Local MCP](LocalMCP.md)

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
