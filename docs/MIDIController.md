# MIDI controller support

HermitSDR reads any CoreMIDI source as a radio panel (issue #127): DJ
decks with jog wheels, Behringer X-Touch and similar knob boxes,
CTR2-MIDI, Arduino or Teensy encoders, a sustain pedal as a paddle, a
Bluetooth MIDI keyboard's pads. The work follows the Stream Deck split: a
pure mapping layer (package-tested), a CoreMIDI transport, a device
controller that runs the mapping engine, an offline document owner, and a
radio-side executor. Only the last of those can touch the radio.

## Using it (2026.0921_002)

1. Connect the controller — USB, Bluetooth MIDI (pair it in Audio MIDI
   Setup ▸ Window ▸ Show MIDI Studio ▸ Bluetooth), or a network session.
   No permission prompt is involved; CoreMIDI input is not gated by Input
   Monitoring the way HID knobs and the Stream Deck are.
2. Open **Station ▸ Control Devices ▸ MIDI Controller** and flip
   **Enabled** on. The switch is persisted (`midiOn`) and defaults to off.
   Every MIDI source on the Mac is listed under *Sources*; the status line
   reads `connected: <names>` for the ones the filter accepts.
3. Choose **Choose input devices** in *Sources* and check each controller
   you want to use together. The optional name and channel filters still
   apply. Turn off **Choose input devices** to return to the automatic list.
4. Press **Learn new control**, then move ONE control. The row shows the
   device and the channel and number (for example, `ch 1 CC 16`). Two
   devices can use the same channel and number for different actions.
   The mode is guessed from the message:
   a note is a **Button**; a CC whose first value is 1/127 or 63/65 is an
   **Endless encoder** (with the encoding guessed to match); any other CC
   or a pitch wheel is a **Knob / fader**.
5. Assign the row's action from its menu, and correct the mode or the
   encoder convention if the guess was wrong (an encoder that only turns
   one way, or jumps, has the wrong encoding).
6. Watch *Live input*: it prints every message the controller sends,
   whether it was mapped, and the receipt of what the radio did.

**Learn shared control** creates the original kind of mapping, usable from
all eligible devices. Existing mappings and imported presets are shared.
Device-specific mappings use the Mac’s CoreMIDI endpoint ID. Relearn them
if you move the profile to a Mac that assigns different IDs. A device-specific
row normally takes precedence for its own device. PTT,
TUNE, MOX, CW paddles, and Media Deck playback stay on the shared mapping
path. A shared keying or playback mapping takes precedence on its control
number, including when a device-specific row also uses that number. Use the
source selection to limit which devices can send shared controls.

## What a control does

| Mode | Action | Behaviour |
| --- | --- | --- |
| Endless encoder | **Tune VFO (wheel)** | One tune step per detent (the row's fixed step, or the control bar's), signed by the encoder's convention. Speed acceleration: ≥ 8 detents/s multiplies the step ×4, ≥ 20/s ×10 (both editable under *Wheel acceleration*, or off). Goes through `tuneBy(source: .tuningDevice)`, so the dial lock (#138) holds it. |
| Endless encoder | **AF volume** | ±2 % per detent, clamped 0–100 %. |
| Endless encoder | any deck action | Each detent, either direction, is one press (down then up). |
| Knob / fader / pitch wheel | **AF volume** | **Pickup:** the knob does nothing until it passes within 4 % of the current volume, then follows the knob exactly. Pickup restarts when the document is edited, the controller is unplugged or the feature is switched off. |
| Knob / fader | any deck action | A switch: crossing 50 % upward presses, crossing back releases. |
| Button (note, or CC ≥ 64 / < 64) | any deck action | Down on note-on / CC ≥ 64, up on note-off / CC < 64. The same `DeckAction` model and the same executor as a Stream Deck key: bands, modes, tune steps, NB/NR/ANF/split/sub/mute/record/skimmer/FT8/arcade/dial lock, band memories, palette, spoken status, RX/TX antennas, Media Deck pads, URLs. |
| Button | **PTT (hold)**, **TUNE**, **MOX** | Exactly a Stream Deck key: momentary `setPTT(_, source: .hardware)` / `toggleTune(source: .hardware)` through `performDeckAction`; a vanished controller unkeys (TUNE and MOX get an explicit off). Behind ARM and every interlock. |
| Button | **Paddle — dot / dash** | `handleHardwarePaddle` → `CWKeyInputMapper` → `setCWPaddles`, the keyboard paddles' path. **CW mode only** — in any other mode the receipt reads `Paddle — dot — CW paddles are available only in CW mode.` and nothing reaches the engine. |

Rows are keyed by control: learning a control that already has a row
replaces it; a control maps to exactly one action.

## Input Mixer controls (2026.1028_001)

USB MIDI control surfaces work through the existing CoreMIDI input and Learn
window. Audio stays in HermitSDR; the controller sends settings, not microphone
or clip audio. No controller is enabled automatically and no mapping chooses a
TX source, arms or keys. Input Mixer and its controller profiles are available from 2026.1028_001.
Physical-controller and RF verification remain operator-assisted.

Select Input Mixer in TX Controls. **MIDI controls…** opens the existing setup
window. Enable input, restrict the source filter/channel to your controller,
Learn a fader or knob and assign a target under **Input Mixer · Microphone** or
**Input Mixer · Media Deck**. Correct Learn's guessed mode to **Knob / fader**
for an absolute control, especially if the first value was 1 or 127. For a mute
button choose **Button** mode and configure it to send momentary press/release
messages.

| Target | Physical control | Range / behavior |
| --- | --- | --- |
| Level | Fader or encoder | −60…+6 dB; bottom = silence; encoder 0.5 dB/detent |
| EQ 100 / 200 / 400 / 800 / 1600 / 3200 / 5000 Hz | Knob, fader or encoder | ±12 dB; encoder 0.5 dB/detent |
| Effect selection | Knob or encoder | Existing Off/effect order; encoder one effect/detent |
| FX amount | Knob, fader or encoder | 0…200%; encoder five percentage points/detent |
| Mute (toggle) | Momentary button | One toggle per press; releases/device loss never toggle again |

Absolute controls wait until their position approaches or crosses the current
software value. Pickup resets after a software/other-control edit, a mapping
change, source/filter change, disable or device loss. Effect selection uses the quantized preset value
for pickup. Audio encoders do not use tuning-wheel acceleration. Pitch-bend
faders use their existing 14-bit input resolution. Per-strip fader smoothing and
the existing master processing/limiter still apply.

A [Korg nanoKONTROL2](https://www.korg.com/us/products/computergear/nanokontrol2/page_1.php)
offers eight faders and eight knobs; its generic CC mode is a compact layout
for the main levels and chosen EQ/FX controls. A
[Novation Launch Control XL 3](https://novationmusic.com/products/launch-control-xl)
has eight faders and 24 encoders, enough for separate control of both strips'
EQ and FX. Use a Custom Mode that sends ordinary MIDI CC messages. An X-Touch
Mini offers eight encoders and one fader, so it favors knobs.

One XL-style layout is faders 1/2 for mic/Deck, knobs 1–14 for their EQ bands,
knobs 15/16 for FX amount, knobs 17/18 for effect selection and two momentary
buttons for mute. These are physical control positions, not assumed CC numbers:
use Learn for the actual channel/CC and encoder convention. No physical controller has been validated for these new
mixer targets. Motorized-fader position output and encoder rings are not
implemented; the existing supported deck-action lamps remain, and the Input
Mixer's mute/ducking state can light a control surface's strip buttons (see
**Mixer LEDs** below).

New mapping documents use format version 2; adding a mixer target upgrades an
older document to v2 so older apps refuse it clearly, and an imported or
hand-edited file that already carries mixer rows is stamped v2 when it is read.
Existing v0/v1 mappings remain readable. The pre-import backup is a copy of the
mapping file on disk, so a file this build could not read is still preserved.
Existing MIDI keying refusals remain in force.

## Korg nanoKONTROL2 presets (2026.1028_001)

The built-in **Set up nanoKONTROL2…** button under MIDI Controller → Sources
loads either layout below without learning the controls individually. Disable
MIDI input first. Inspect the preview, then Apply; this replaces the entire
mapping document, restricts it to source names containing `nanoKONTROL2` and
MIDI channel 1, and writes a JSON backup. **Undo import** restores the previous
complete document in the current session while input remains disabled. The JSON
backup remains on disk after quitting. Applying never enables input,
selects Input Mixer, starts Deck playback or arms/keys the radio. Existing other
controller mappings are replaced, not merged, so old transport bindings cannot
remain active accidentally.

Use CC mode. Korg's [owner's manual](https://cdn.korg.com/jp/support/download/files/06ad1c7822e7ab86908f875bd3c860b2.pdf)
documents holding **SET MARKER + CYCLE** while connecting USB. Check that the
unit sends the assignments shown in the preview on channel 1 (wire channel 0).
The profiles expect sliders 1–8 = CC 0–7, knobs 1–8 = CC 16–23, and M1/M2 =
CC 48/49. Continuous controls send 0–127; M1/M2 are momentary, sending 127 on
press and 0 on release. These are the profile's required assignments, not a
claim that the app has read or reset the hardware scene. Korg's
[parameter guide](https://cdn.korg.com/us/support/download/files/c8d0cd6808e12d3672845cadcdbbfe9b.pdf)
explains changing CC numbers, channels, ranges and button behavior in KORG
KONTROL Editor. Customized units can instead use Learn to match their actual
messages. No SysEx or device programming is sent by the preset loader.

| Position | Mix + FX | Full EQ |
| --- | --- | --- |
| Slider 1 / 2 (CC 0 / 1) | Mic / Deck level | Same |
| Slider 3 / 4 (CC 2 / 3) | Mic / Deck FX amount | Mic EQ 100 / 200 Hz |
| Slider 5 / 6 (CC 4 / 5) | Unassigned | Mic EQ 400 / 800 Hz |
| Slider 7 / 8 (CC 6 / 7) | Unassigned | Mic EQ 1600 / 3200 Hz |
| Knob 1 (CC 16) | Mic EQ 200 Hz | Mic EQ 5000 Hz |
| Knob 2 / 3 (CC 17 / 18) | Mic EQ 800 / 3200 Hz | Deck EQ 100 / 200 Hz |
| Knob 4 (CC 19) | Mic effect selection | Deck EQ 400 Hz |
| Knob 5 / 6 / 7 (CC 20 / 21 / 22) | Deck EQ 200 / 800 / 3200 Hz | Deck EQ 800 / 1600 / 3200 Hz |
| Knob 8 (CC 23) | Deck effect selection | Deck EQ 5000 Hz |
| M button 1 / 2 (CC 48 / 49) | Mic / Deck mute toggle | Same |

Mix + FX loads 14 bindings; Full EQ loads 18. Both layouts leave S, R,
transport/function and other M buttons unassigned. Existing pickup protects
every continuous control after connection, profile changes and software edits.
Move a control through the current on-screen value before expecting it to
follow. FX choices are discrete; FX amount is continuous. Switch layouts with
input disabled, then enable it manually. On-screen mute indicators are the
source of truth; the unit's M and S LEDs can mirror them (the sheet's **Light
M (mute) and S (ducking) LEDs** switch, off by default — see **Mixer LEDs**
below). Motor feedback and ring feedback are not implemented. This
device-specific CC profile is software-tested; validate the actual unit's
ports, CCs, pickup, mute releases, LED mode and reconnect behavior when it
arrives. No physical nanoKONTROL2 certification is claimed.

## Lamps (LED feedback)

A button row whose action has a radio state to show offers a **Lamp**
switch and a velocity. With it on, the controller's matching output
receives the row's control as a **note-on at that velocity when the state
is active and a note-off (status 0x80) when it is not** — a CC button gets
the CC at the velocity / at 0. Which rows: bands, modes, every toggle
(NB, NR, ANF, split, sub RX, arcade, FT8, skimmer, record, mute, dial
lock), tuning step, bookmarks, RX/TX antenna selections, Stop media, and
Media Deck pads (a pad lights while its clip or URL is playing). The
active rule is the Stream Deck's key-face rule, so a MIDI pad and a deck
key for the same band always agree. Velocity is what LED controllers read
as colour or brightness (X-Touch Mini: 1 on, 2 blink; Launchpad / APC:
colour index); 127 is a safe default.

- **Never for keying.** PTT, TUNE and MOX rows offer no Lamp and echo
  nothing whatever the transmitter does — a lit pad is not an ON AIR
  indicator; the app's interlocked displays own that. Pinned by
  `MIDIFeedbackTests.testTransmitActionsEchoNothingEvenWhenKeyed`.
- **Quiet by default.** Nothing is sent while MIDI is disabled, with no
  Lamp row, or when nothing is active: an idle launch sends no message at
  all. Only CHANGES go out (a diff against what was last sent), coalesced
  80 ms after a state change, so a meter tick costs no MIDI traffic.
- **Where it goes.** Each connected input gets at most one output. The
  transport prefers a unique output on the same CoreMIDI entity, then a
  unique exact name match. With one input, the name filter can also select
  a single output. Ambiguous routes are left unpaired. The status line reads
  `connected: … · lamps → <names>`;
  the Controls panel warns when Lamp rows exist but no output is paired.
- **Loss and disable.** Switching Enabled off, quitting, or losing the
  source clears affected lamps (one note-off each, sent while the paired
  output is still present), and a source that reappears is relit from
  scratch — the hardware powered up dark. A send that fails is logged and
  the destination dropped until the next hot-plug rescan; there is no
  retry and no queue.
- The pure engine is `MIDIFeedbackEngine` (`Integration/MIDI/
  MIDIFeedback.swift`, package-tested); the document gains an optional
  `lamp` per row (`{"velocity": 127}`), absent in older files.

The document lives at `~/Library/Application Support/HermitSDR/MIDI/
mappings.json` (pretty JSON, atomic writes, versioned — a file from a
newer build is refused rather than silently truncated; the window shows
the error).

## Mixer LEDs (Input Mixer strip-button feedback)

A control surface's **S / M / R** buttons are a fixed table per controller,
not learned rows, so the Input Mixer lights them from its own state through
a layout chosen under **Controls → Mixer LEDs** (or the nanoKONTROL2
sheet's **Light M (mute) and S (ducking) LEDs** switch). It is **off by
default**; the on-screen mixer stays the source of truth and the LEDs only
mirror it.

| Lamp | Lit while | nanoKONTROL2 (factory CC-mode scene) |
| --- | --- | --- |
| **M** on a strip | that strip's **mute** is on | CC 48 / 49 / 50 (Mic / Deck / Guests), 127 on, 0 off |
| **S** on the Deck strip | **voice-over ducking** is dipping the Deck by ≥ 1 dB | CC 33, 127 on, 0 off |
| **R** | never written — the mixer has no record arm | CC 64–71 left dark |

Strip order follows the presets: strip 1 = Microphone, 2 = Media Deck,
3 = Remote Guests, so the M lamp sits over the M button that toggles that
strip's mute.

- **Set the unit's LED Mode to External.** Korg's
  [parameter guide](https://cdn.korg.com/us/support/download/files/c8d0cd6808e12d3672845cadcdbbfe9b.pdf)
  ("LED mode", p. 9): with **LED Mode = External** a button's LED "will
  light-up or go dark when a message with the control change number …
  assigned to that button is received from the computer — light-up when an
  On Value … is received, and go dark when an Off Value … is received." The
  factory setting is Internal (the LED follows the button locally); change
  it in KORG KONTROL Editor. The factory CC-mode scene puts S / M / R on
  CC 32–39 / 48–55 / 64–71, channel 1, On 127 / Off 0 (the guide documents
  the fields; the numbers are the factory scene as read back by the editor
  and used by every published nanoKONTROL2 host map, e.g. the
  SuperCollider class's `sbutton 32 / mbutton 48 / rbutton 64`). A unit
  whose buttons were reassigned needs the same CCs restored, or Learn the
  rows and leave the LEDs off. HermitSDR sends **no SysEx** and never
  programs the device.
- **Only changes go out.** The pure `MixerLampFeedback` diffs the mixer's
  mute/duck snapshot against what was last sent, coalesced with the row
  lamps 80 ms after a state change; an idle mixer costs no MIDI traffic.
- **Resync on connect.** The mixer lamp layout uses one paired controller.
  If several are paired, exactly one must identify as a nanoKONTROL2 for
  strip lamps to be sent. When the target connects, every driven lamp is
  written once explicitly — on or off — so an LED left lit by an earlier
  session cannot survive; after that only changes are sent.
- **Quiet when off.** Nothing is sent while MIDI is disabled, with the
  layout Off, or with no paired output (same pairing rule as the row lamps).
  Switching the layout Off darkens what it lit, once; Enabled off, quit and
  source loss clear every lit lamp with the row lamps.
- **Output only.** The table maps state → lamp, never lamp → state: a lamp
  message cannot move a fader, toggle a mute, select a source, arm, key or
  change drive/policy. The M lamps share the M buttons' CCs, so mixer rows
  offer no per-row Lamp (no double write).
- Data-driven: `MixerLampLayout` (`Integration/MIDI/MixerLampFeedback.swift`,
  package-tested by `MixerLampFeedbackTests`) holds the channel, control
  numbers per button row and strip, on/off values, strip order and which
  condition each button row shows; another controller is a second static
  table listed in `MixerLampLayout.all`. The document stores the layout id
  as `mixerLamps` (absent = off, format version unchanged).

## Keying

The operator route this exists for (first real request 2026-10-11, LB2EG:
HL2+, a CTR2-MIDI paddle interface, CW left/right mapped to Paddle — dot /
dash): a paddle contact on a MIDI pad or pedal is a CW keyer input, no more.

- **Paddles.** `performMIDIDispatch(.paddle)` calls
  `RadioState.handleHardwarePaddle`, which is `setCWKeyInput` — the keyboard
  paddles' own entry. Its first stop is `CWKeyInputMapper.gate(…, cwMode:
  mode == .cw)` (package-pinned): outside CW mode a press is **refused**
  with "CW paddles are available only in CW mode." (also shown in the
  connect sheet's `lastError`) and a release is ignored; the logical paddle
  state never moves, so nothing reaches the engine. In CW mode the shared
  logical paddles (keyboard and MIDI OR into one `CWKeyInputMapper`, so a
  release from either source releases — the safe direction) go to
  `RadioEngine.setCWPaddles(dot:dash:policy: currentTXPolicy)`, which
  refuses again unless the engine's own mode is CW, then runs the
  `CWKeyingSession` → `TXCoordinator` handshake: ARM, TX profile, operator
  policy, frequency range, calibration, protection and station interlocks
  decide whether RF rises, and the session's stuck-key watchdog
  (`stuckKeyWatchdogMilliseconds`) force-drops a contact that never
  releases and refuses re-key until a physical release arrives. The engine
  attributes MIDI paddles to the `.keyboard` keying source (they share the
  keyboard's session slot; CAT `send_morse` is refused `.busy` while a
  paddle is held, and vice versa). Receipt on the setup window:
  `Paddle — dot ↓ → CW keyer (keyed)`, or the refusal.
- **PTT (hold), TUNE, MOX.** `performDeckAction`, exactly as a Stream Deck
  key: `setPTT(phase == .down, source: .hardware)` for momentary PTT (both
  edges), `toggleTune(source: .hardware)` and `setPTT(!txKeyed, source:
  .hardware)` on the down edge for TUNE and MOX. The receipt is the deck's
  `txReceipt` (`PTT down → keyed`, or `PTT down — <refusal>`).
- **Releases.** The device controller releases held pads through
  `MIDIMapper.safeRelease`, which emits the `.up` edge for momentary PTT and
  `pressed: false` for paddles, and an explicit `.ptt(false)` / `.tune(false)`
  press for latched PTT, MOX and TUNE — toggles whose `.up` phase does
  nothing, so a plain "up" would have left the carrier on. It fires on
  **source loss**, **Enabled off**, **quit** (`shutdown()` → `stop()`), a
  **mapping document change** that touches the rows (a row deleted,
  unassigned or re-moded under a held finger; the mapper also honours the
  stale release edge itself if it arrives first), and **app deactivation**
  (`NSApplication.willResignActiveNotification` — keying pads only, as the
  keyboard's `KeyMap` does; a held band pad keeps its edge state). Note
  that a TUNE pad is a toggle: after a tap and release nothing is held, and
  TUNE runs until the next tap, the on-screen button or CAT — the same as
  the Stream Deck and the UI; only a pad still down when the controller
  vanishes is released.
- **What a MIDI controller cannot do.** The transport, device controller,
  document owner and setup window hold no radio handle (`DocsConsistency`
  forbids `setPTT(`, `toggleTune(`, `setCWPaddles(`, `TXCoordinator`,
  `RadioEngine` in all four); the executor file reaches keying only through
  `performDeckAction` and `handleHardwarePaddle`; `RadioState` has exactly
  one `engine.setCWPaddles(` call site. Lamps never echo keying. Thetis
  import excludes MOX/TUNE rows unless the reviewer includes them, and an
  included row is a live keying control once input is enabled.
- **Tests.** `MIDIKeyingTests` (paddle note-on/off → `CWKeyInput` in CW
  mode, refused outside it; the gated state through `CWVirtualRadioHarness`
  with the real `TXCoordinator` — disarmed refused, armed keyed, watchdog
  force-drop and re-key only after a physical release; `releaseAll` for
  every keying action including latched ones; `releaseKeying` scope; stale
  release edges after a row edit), `MIDIMappingTests` (held PTT released on
  device loss), `DocsConsistencyTests` (entry points, release hooks and the
  operator text above), `tools/cw-session-smoke.sh` (production
  `setCWPaddles` refuses outside CW mode with the coordinator untouched).

**Not yet keyed on hardware.** The first keyed test is a dummy-load session
with Damon's approval; the review packet is on #127.

## Safety boundary

- `MIDIMappingController` and `MIDISetupView` own no MIDI client, radio
  facade, engine, coordinator or executor: editing a mapping can never send
  a message or operate the radio.
- `MIDIInputTransport` and `MIDIDeviceController` hold no radio handle;
  RadioState installs an `execute` closure and a volume reader at launch.
- A held pad is released (its safe release delivered — see *Keying*) when
  its source disappears, when Enabled is switched off, when the mapping
  document's rows change, at application quit, and (keying pads only) when
  the app deactivates.
- Both CoreMIDI callback blocks are `@Sendable`. A closure literal inside a
  `@MainActor` class is otherwise inferred main-isolated, and Swift 6 emits
  an executor check at entry that traps on the CoreMIDI thread — the same
  #113 crash class as the Media Deck tap. The transport's receive block
  decodes the packet's words into values and makes one hop to the main
  actor per callback. The test suite pins both blocks.

## Record

2026-09-21, macOS 26 on the Mac mini, virtual CoreMIDI source created by a
20-line script (`MIDISourceCreateWithProtocol`, `MIDIReceivedEventList`):
the Dev build connected the moment the source appeared; five slow
2's-complement detents moved the dial +500 Hz at a 100 Hz step; a 12-detent
spin at 40 ms spacing moved it −5.7 kHz (3 detents ×1, 6 ×4, 3 ×10); a CC 7
knob at 100 %, 70 % and 30 % left a 38 % volume alone, engaged at 37.8 %
and then tracked 15.7 % → 78.7 %; a note pad switched to 40 m
(`setBand("40M")` → 7.100 MHz); a PTT pad returned the refusal receipt with
CAT `t` still 0; disposing the source logged `MIDI source lost` and
recreating it reconnected and tuned within a second. The first run of the
transport crashed at the receive block's executor check (see above); the
fix is in this release. No physical controller has been tried yet.

2026-10-07, lamp feedback, same virtual-source recipe plus a virtual
destination of the same name that logs what the app sends (isolated Dev
build, no hardware): at connect the Demo-Mode 20 m pad lit at velocity 100
and the NR and mute pads lit from their persisted state while the 40 m,
PTT and Speak rows sent nothing; pad presses produced exactly one message
per change (mute off → note-off, on → note-on 5; NR off → CC 20 = 0); a
40 m pad press in Demo Mode (band jump clamped) sent nothing, truthfully;
PTT and Speak pads sent nothing. Enabled off → one note-off for the lit
lamp, a pad while disabled → nothing, Enabled on → relit. Quit → note-off.
A relaunch that opened a 7074 kHz recording sent `note-off 36, note-on 37`
in one sync — the band change darkening 20 m and lighting 40 m. Disposing
the source → note-off (the paired output was still there) and no relight
(the first build relit through the lingering output, fixed before
landing); recreating it → relit. Window seen by capture: Lamp + velocity
on the band / NR / mute rows, none on PTT and Speak, `lamps → <name>` in
the status line. No physical LED controller has been tried.

## Remaining

- Physical controller (X-Touch Mini, a DJ deck, a pedal) — confirm the
  encoding guess and acceleration feel; adjust the default rates if a real
  jog wheel wants them.
- Encoder rings (a relative value shown as a ring of LEDs) are not
  driven; lamps cover on/off state only.
- Lamp feedback has been seen with a virtual destination only (below); a
  physical LED controller's velocity-to-colour table is unconfirmed.
- More continuous targets (RF gain, filter width, squelch, drive) are a
  small addition to `MIDIAction` once the wheel and knob paths have been
  felt on hardware.

## MIDI 2.0

The input port is created with `MIDIInputPortCreateWithProtocol(…, ._1_0,
…)`, so CoreMIDI converts a MIDI 2.0 controller's channel-voice messages
to MIDI 1.0 UMP words (type 2) before the receive block sees them — the
per-note 16-bit velocities and 32-bit controller values are downscaled by
the system. Should a type-4 (2.0 channel voice, two-word) message arrive
anyway, `MIDIMessageDecoder.decode(word1:word2:)` turns it into the same
`MIDIMessage` events, scaled to 7 / 14 bits (velocity `>> 25`, pitch bend
`>> 18`), and the mapper treats them identically;
`MIDIMappingTests.testMIDI2ChannelVoiceWordsDecodeToTheSameEvents` pins
it. Per-note controllers, JR timestamps and other 2.0-only messages are
skipped by word count. Lamp output is MIDI 1.0 words only.

## Import Thetis Midi2Cat XML (#172)

Disable MIDI input, choose **Import Thetis XML…**, and inspect the preview.
Select one exported controller, the matching macOS source name, the actual
MIDI channel (1–16) and the encoder convention. Thetis exports do not establish
the latter two. The importer uses the DataSet controller name and skips schema,
settings and Not Saved working-copy sections. It does not copy upstream code.

Supported commands: VFO A wheel (101), AF volume (209), split (4), MOX (13),
mute (15), blanker (16), auto-notch (18), TUNE (76), and the supported band
buttons (78, 79, 81–88). Other commands, malformed records, duplicates and
custom MinValue/MaxValue scaling are reported as skipped. PL-1/Micro device
control-number remaps need Learn instead. Buttons may use note or CC input;
continuous controls require CC. With MIDI keying enabled (see *Keying*), an
imported MOX or TUNE row is a live keying control — which is why keying rows
are excluded unless explicitly reviewed.

Merge replaces matching physical controls; Replace starts with no old rows.
The selected source filter applies to the entire document and the global
channel filter is cleared (each row carries its own channel). Keying rows
are excluded unless explicitly reviewed. Nothing is dispatched during import.
The previous JSON document is saved as mappings-before-import-<UUID>.json
before the new file is atomically written and published. **Undo import**
restores that backup while input is disabled; backups remain available on disk.
A failed write leaves the active mapping document unchanged.

### Call-in Mixer prototype

The **Call-in Mixer** nanoKONTROL2 layout adds three faders (Mic, Deck, Guests),
three FX-amount knobs and M1/M2/M3 channel mute toggles: nine mappings. Guest EQ,
effect selection and FX amount are also available through MIDI Learn. Admission
to the transmit mix and private talkback stay in Remote Guests & Call Setup;
there are no caller-admission or RF bindings. Existing Mix + FX / Full EQ layouts
retain their original 14 / 18 mappings. See [Remote Guests](RemoteGuests.md) for
the two virtual routes, headphone preview, return sends and call-app setup.
