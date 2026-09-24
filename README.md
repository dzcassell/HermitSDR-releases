<p align="center">
  <img src="assets/hermitsdr-logo.png" width="440"
       alt="HermitSDR — a hermit crab wearing headphones, its shell pouring a waterfall of spectrum. ARM UKRAINE! 🇺🇦 86 47">
</p>

# HermitSDR

A native macOS client for openHPSDR software-defined radios —
**Hermes-Lite 2 / SquareSDR** (Protocol 1) and **Apache Labs ANAN**
Orion-class radios (Protocol 2) — plus the receive-only **RFSpace
NetSDR**. Built for Apple silicon: SwiftUI +
Metal on the outside, Accelerate/vDSP DSP and a lock-free audio path on
the inside.

This is the **download home** for HermitSDR. Grab the latest signed,
notarized build from the [**Releases**](../../releases/latest) page.

For the complete release history, read the [**CHANGELOG**](CHANGELOG.md).

The planned console redesign is described in the [UI design brief](docs/UI_DESIGN.md)
and [implementation roadmap](docs/UI_IMPLEMENTATION_ROADMAP.md). These are planning
documents, not features in the current download.

> **Availability**: HermitSDR is not made available for use in the
> Russian Federation while Russia's war against Ukraine continues. The
> app checks the system region/timezone at startup and declines to run —
> an offline check by design (nothing phones home). Слава Україні. 🇺🇦

Receive *and transmit* are live-proven on **both protocols**, and the first
on-air QSOs are in the log (WU1T ↔ KA3MAJ, W8NGA, KN1B and KJ5DZV, FT8, 40 m, 2026-09-14/15): the Hermes-Lite 2 and the
ANAN-7000DLE MK2 — correct sideband both ways on each, clean key/unkey,
hardware PA interlocks, keyboard **CW keying**, and a complete
**WSJT-X FT8 cycle** validated end to end through CAT PTT.

## New in 2026.0924_001

- **RFSpace NetSDR receive support.** The connect sheet now finds an RFSpace NetSDR beside the openHPSDR radios (its own LAN discovery), shows firmware, serial and MAC with a **RECEIVE ONLY** tag, and connects over the NetSDR's TCP control + UDP I/Q protocol in 24-bit mode. Spans of 48–768 kHz are offered; the radio streams 50–800 kHz and is resampled 24/25 onto the receiver's grid. RF gain maps onto the hardware's four steps (0/−10/−20/−30 dB), the preselector stays automatic, and an A/D overload lights the OVF badge.
- **A NetSDR with no address gets one from the app.** A unit whose DHCP request went unanswered answers discovery from 0.0.0.0; its row offers **Assign IP…**, which writes a static address, mask and gateway (or DHCP mode) into the receiver — applied within seconds, no reboot.
- **Receive-only means receive-only.** On a NetSDR session the TX banner, ARM, PTT, TUNE, drive, TX antenna chip, panadapter TX footprint and the FT8 panel's transmit row are absent, and every keying source (UI, CAT, hardware key, Stream Deck, MIDI) is refused — the same way a Hermit Remote relay is treated.

Live-validated on an RFSpace NetSDR (firmware 1.13) with a 40 m dipole: discovery, static-IP assignment, a clean 400 kHz stream, correct sideband sense, and 40 m FT8 decodes. Nothing was keyed. Full suite: 1,823 tests, zero failures.

## New in 2026.0921_002

- **Any MIDI controller becomes a radio panel.** Station ▸ Control Devices ▸ MIDI Controller reads every CoreMIDI source on the Mac — DJ decks, X-Touch-style knob boxes, CTR2-MIDI, Arduino encoders, a pedal, a Bluetooth keyboard's pads — with no permission prompt, filtered by name and channel so a music keyboard cannot tune the radio. Press **Learn**, move one control, assign it: an endless encoder tunes the VFO one step per detent with speed acceleration (and honours the dial lock); a knob or pitch wheel sets AF volume without jumping (it waits to pass through the current level, then follows); a pad fires any of the Stream Deck's actions — bands, modes, NB/NR/ANF, mute, memories, antennas, spoken status, media pads — through the same executor, so the two panels can never disagree. Three encoder conventions are supported and guessed at Learn time. Unplugging the controller releases anything it was holding.
- **It cannot key the radio in this build.** PTT, TUNE, MOX and CW-paddle assignments are accepted by the editor but refused at press time with a receipt naming why; the keying wiring is staged for review.

Verified on this Mac with a virtual MIDI source (tuning, acceleration, volume pickup, band pad, PTT refusal, unplug/re-plug); no physical controller yet. Full suite: 1,798 tests, zero failures.

## New in 2026.0921_001

- **Your shack microphone no longer leaks to Discord or a live stream between overs.** With ARM and TX Monitor on, the mic check you hear in the speakers used to ride along with the receiver audio to every remote listener. Remote listeners now hear the monitor voice only while the transmitter is actually keyed — and they hear your transmission even with TX Monitor off.
- **Control API for lightweight remote clients (receive-only first milestone).** A documented, versioned WebSocket-over-TLS endpoint (`docs/ControlAPI.md` in the source tree) lets a thin client on another computer mirror the radio's state, tune, change mode/filter/gain, and receive the audio and a spectrum stream — the Mac does all the DSP. Same pairing and certificate pinning model as Hermit Remote, off by default, and it cannot transmit: transmit messages are reserved and refused.
- **The panadapter trims itself and labels peaks.** An Auto latch parks the display floor just under the band noise and follows band changes; a Peaks menu labels the strongest signals in dBm or S-units.
- **AGC you can tame.** A Max gain slider stops a quiet band roaring up between overs; slope and hang are adjustable and there is a Long speed. CW gets an audio peak filter that only the speaker hears.
- **Dial lock, a four-register band stack, and spoken status** (frequency, mode, S-meter, power/SWR) for eyes-free operating.
- **Media Deck Auto PTT.** A header latch keys the transmitter while a pad plays — behind ARM and every existing interlock, off at every launch, with a three-minute time-out.
- **Speaker Tracker learns the channel.** A channel-normalized voiceprint is the new default, with a tag-and-report tool so a real net can show whether it tells operators apart. Still unproven on real voices.
- **ANAN: sub-receiver on the RX2 input**, with its own filters — a second antenna or a second band at once.
- **Every release DMG is now checked with VirusTotal before publication**, and the website shows its SHA-256 with the verdict. This first release predates the API key, so it is marked "not scanned"; the hash and lookup link are published.

The release completed the full software suite (1,784 tests) with zero failures and clean Debug/Release builds. No radio was connected and nothing was transmitted: every feature above is verified by tests and builds only, and the on-air and by-ear checks are still to come.

## New in 2026.0920_001

- **Discord is now a practical remote front panel.** In your chosen control channel, direct mentions such as `@HermitSDR status`, `help`, `frequency`, `mode`, `signal`, `uptime`, `recording`, `decoders` and `waterfall` answer immediately without being trapped behind the conversational cooldown. Open-ended mentions still go to the isolated AI co-host. The voice connection now implements Discord's required DAVE end-to-end encryption, so live receiver audio reaches the voice channel again.
- **Two receive-side regressions fixed.** Switching Protocol 2 Diversity on or off can no longer strand the DSP and freeze the waterfall, and stale time-machine bookmark errors no longer compare buffer depths from different connection generations.

The release completed the full clean software suite with zero failures and clean Debug/Release builds. Direct mentions, slash status, waterfall posting, notification suppression and DAVE voice audio were exercised live with the ANAN; no transmission was involved.

## New in 2026.0916_003

- **Speaker Tracker works on a real band now.** Its first on-air outing on a 40 m phone net showed it could not tell one over from the next: the transmission detector listened to the AGC-levelled audio, which never goes quiet between overs, so every "transmission" ran to the 60 s limit and the analysis fell a minute behind. The tracker now watches the receiver's own signal-strength reading (the same one the squelch uses) to decide when someone is transmitting, learns the band's noise floor in the first half second, and analyses each over in about a tenth of a second on a queue that can never stall the audio. On the same net after the fix it cut 13 overs of 2 to 60 s cleanly. Whether the built-in voiceprint can tell speakers apart on SSB is still an open question that needs an operator's ears on a net with known voices.
- **Under the hood:** FM polarity and wide-FM occupancy tests, CAT `FM`/`FMN` round trip, FM settings persistence tests, the CW keyer and operator TX policy in the capability table, and documentation for audio device changes, latency and the sidetone-vs-RF timing bound.

The release completed the full software suite (1,630 tests) with zero failures. The Speaker Tracker was exercised receive-only on a SquareSDR 2; no transmission was involved.

## New in 2026.0916_002

- **Stream Deck, for real.** Station › Control Devices › Stream Deck Setup gains a **Connect** switch that opens an Elgato Stream Deck (MK.2 or the 2019 15-key model) over USB and drives it from your layout. Band, mode, tune-step, NB/NR/ANF/split/sub-RX/mute/record/skimmer toggles, palette, antenna and Media Deck pads all work from the keys, and the faces show live state: the current band lights and shows the dial, the current mode lights, toggles light when on, and PTT/TUNE keys read SAFE, ARMED, ON AIR or CARRIER. PTT on the panel is hold-to-transmit and goes through the same ARM interlocks as the on-screen button; TUNE toggles. A first run gets a ready-made starter page; the setup window mirrors the panel while it shows the page you are editing. macOS asks for Input Monitoring the first time. Quit the Elgato app first — it holds the device.
- **Fixed:** the Stream Deck editor's key previews had never rendered (a bitmap-format mistake), so they were blank in every earlier build.

The release completed the full software suite (1,618 tests) with zero failures. The panel was exercised on the bench (tiles, brightness, serial and firmware readback); no transmission was involved.

## New in 2026.0916_001

- **Ask the Crab knows the nets.** "Monitor the MAGNET HF net on 40m" now tunes 7.115 MHz USB, starts the Contestia 4/250 decoder at the published 900 Hz offset and tells you which regional net is on or next; "listen for MAGNET JS8" goes to the JS8Call watch channel. The app resolves the request from its own MAGNET HF schedule before the language model answers, so the assistant can no longer invent a frequency for it.
- **"40m" is a band, not a frequency.** A band word in a request switches band instead of being tuned as 40 MHz, and a frequency the assistant narrates that the radio's own receipts do not support is replaced by the receipt.

The release completed the full software suite (1,609 tests) with zero failures. No transmission was involved.

## New in 2026.0915_008

- **YouTube on the air.** TX Controls › Source now offers **App audio**: HermitSDR captures its own audio output (the Media Deck's YouTube and web pads) and feeds it to the transmitter behind the usual ARM and PTT. Only this app is captured; macOS asks for Screen Recording permission the first time.
- **Sign in to YouTube.** The Media Deck's YouTube pads run in a persistent web session. Sign in with your Google account from the pad editor or the player sheet; a YouTube Premium account then plays without ads. Sign out wipes the session.

The release completed the full software suite (1,600 tests) with zero failures. No transmission was involved.

## New in 2026.0915_007

- **Twelve new digital decoders in one window.** Decode › Digital Modes hosts PSK31/63, Olivia, MFSK16, THOR, DominoEX, Hellschreiber, 300-baud HF packet/APRS, JS8 receive, WSPR, JT65, JT9 and Q65 — one mode at a time, receive only. Text modes print, weak-signal and packet modes list decodes with S/N and offset, Hellschreiber paints. Ask the Crab can start any of them ("decode WSPR here"). Built from the published protocols; loopback thresholds and every known limitation are listed in the docs. None has been checked on the air yet.

The release completed the full software suite (1,597 tests) with zero failures. No transmission was involved.

## New in 2026.0915_006

- **Coast Guard fax tuning, checked on the air.** "Take me to a WEFAX frequency for Boston Coast Guard and begin decoding" now lands on NMF's right outlet even when the on-device model invents a frequency or leaves the station blank, and the outlet choice considers how far you are from the transmitter: near Boston the 6340.5 kHz outlet painted the 1538Z surface analysis at S9+27 while 9110 kHz was noise. Verified live on a SquareSDR 2.
- **The crab no longer apologizes after doing the job.** If Apple's on-device model fails to write its sentence after a tool has already run, the crab answers with the tool's own result.

The release completed the full software suite (1,498 tests) with zero failures. Receive only; no transmission was involved.

## New in 2026.0915_005

- **Ask the Crab can look things up.** Ask "what is MAGNET HF?" and the crab checks HermitSDR's own features first, then — only if you turn on **Web search for unfamiliar terms** under its gear (off by default) — searches the web. On-device it uses DuckDuckGo and Wikipedia; with the Claude API it uses Anthropic's hosted web search and cites its sources. Only the search terms leave your Mac.
- **The crab knows the Coast Guard radiofax stations.** "Take me to a WEFAX frequency for Boston Coast Guard and begin decoding" tunes NMF's scheduled outlet for the current hour, 1.9 kHz below the assigned frequency in USB, and starts the decoder. New Orleans, Point Reyes, Kodiak and Honolulu are covered too. It no longer calls a ham frequency a Coast Guard one.

The release completed the full software suite (1,498 tests) with zero failures. No transmission was involved.

## New in 2026.0915_004

- **Contestia decoder.** Decode › Contestia Decoder receives Pawel Jalocha's MFSK mode natively — 4 to 64 tones, 125 to 2000 Hz, Walsh-coded FEC blocks with sync and S/N gating, LOCK / S/N / offset readouts. Written from the published protocol; no on-air reception yet.
- **Ask the Crab starts decoders.** "Monitor Contestia on 7.115" now tunes 7.115 USB and starts the decoder; the same works for FT8/FT4, CW, RTTY, SSTV, weather fax and ALE. Modes without a native decoder get an honest answer and the audio route to fldigi.
- **Speaker Tracker (2026.0915_003).** Decode › Speaker Tracker, off by default: received voice transmissions are grouped by voice as `UNKNOWN n`, and once you name a voice later transmissions are matched with a visible similarity score. Everything stays in a local file; no audio is kept.
- **Transverter profiles (2026.0915_002).** Settings › Transverters: named IF→RF paths with an explicit drive ceiling. The dial, CAT, logbook, spots and TX policy read RF; the radio stays on its IF; TX is refused for receive-only profiles.
- **CAT over the LAN now requires pairing (2026.0915_001).** With Allow LAN on, other machines may read but must send `\pair` with the code shown in Settings before they can tune, change mode or key. A legacy toggle keeps raw rigctl for Hamlib clients on another machine, behind a warning.

The release completed the full software suite (1,491 tests) with zero failures and the repository audit. No transmission was involved.

## New in 2026.0914_004

- **Replayed decodes are labeled.** FT8 and FT4 rows that came from the time machine or a file replay now carry an orange REPLAY badge in the panel, the same marker Decoder Activity already used. Those rows were never fed to the sequencer or PSKReporter; only the label was missing.

The release completed the full software suite with zero failures and the repository audit. Two more on-air QSOs (KN1B and KJ5DZV, FT8, 40 m, 2026-09-15) were worked with the previous release on the way to this one.

## New in 2026.0914_003

- **Skimmer stops reading FT8 as Morse.** A tone that never keys off during the probe is now labeled DATA rather than CW, and a candidate that follows FT8's 12.6-second-on, 2.4-second-off cadence twice stays DATA until the pattern breaks. DATA rows carry no text and are re-examined every ten seconds, so a station that opened with a tune-up gets its decoder back.
- **About window diagnostics reachable by automation.** The Copy System Information button now carries an accessibility label and identifier.

The release completed the full software suite with zero failures and the repository audit. No transmission was involved.

## New in 2026.0914_002

- **Second on-air QSO, and the sequencer learned from the first.** WU1T ↔ W8NGA (EM89), FT8, 7.074 MHz, 15:53 UTC at 20 % drive: report, R-report, one RR73, their 73, done. The morning's contact had kept repeating RR73 after the other station moved on; the cause was a retry counter that any message addressed to us could reset. RR73 now has a hard two-frame allowance, an exchange closes the moment the partner is heard working someone else, and a new caller is answered straight away once the first RR73 has gone out. Clicking a decode row no longer moves the dial while a contact is running.
- **Skimmer keeps the fast senders.** The chatter blanker introduced this morning had silenced a genuine 52 WPM station; it now judges by what a row prints (noise makes only E/T/I/S/H) rather than by speed alone. The RTTY verdict also demands two clean tones, so FT8 signals sharing a channel stop appearing as RTTY.
- **RF Vision stops calling flicker CW.** Narrow keyed-looking tracks that only poke 8 or 9 dB above the mask stay "?" instead of "CW"; real CW runs far stronger.

The release completed the full software suite with zero failures, the repository audit, and a live re-check of the rebuilt receive-analysis coordinators on the SquareSDR 2. The on-air work was owner-authorized for this session at 20 % on 40 m only; 1.7 to 1.8 W into the amplifier input at SWR 1.16, no external meter, no IMD claim.

## New in 2026.0914_001

- **First on-air QSO.** HermitSDR's native FT8 sequencer worked its first contact: **WU1T ↔ KA3MAJ, FT8, 7.074 MHz, 2026-09-14 14:06 UTC**, on a SquareSDR 2 driving a Mercury Lite amplifier into a 40 m dipole at 30 % drive. KA3MAJ answered the first CQ; the exchange ran and logged itself. Six frames keyed 12.6–12.7 s with 17.3–17.5 s receive gaps under the Mercury Lite timing preset, whose "Amp RX wait" state was seen live.
- **OmniSkimmer copies real CW.** Skimmer rows on a live band used to read 90–150 WPM strings of E and T. The per-signal decoder seeded its dit length from the very first 8 ms envelope blip and could never speed back down, so one glitch pinned a signal at maximum speed for good. It now seeds from three marks, ignores glitches, re-seeds in both directions, stays quiet between overs and blanks chatter. On 40 m it copied `CQ … DE N3CU K` and `73 DE N3CU` at 17–18 WPM within a minute, and a replayed capture reads a full ragchew verbatim.
- **Spaced JS8 confirmed.** A six-frame native JS8 message sent one frame per alternate 15-second slot — the cadence the Mercury Lite preset produces — was decoded and reassembled in order by JS8Call 3.0.3, closing the last open item on the amplifier timing controls.

The release completed 1,439 software tests with zero failures and four optional
skips, the repository audit and a receive-only decoder pass on 40 m (FT8, FT4,
time machine bookmarks, buffer export). The on-air work was owner-authorized
for this session at 30 % drive on 40 m only; app telemetry read 2.0 W into the
amplifier input at SWR 1.16, with no external meter and no IMD claim.

## New in 2026.0913_001

- **JS8 timing and handoffs.** Native JS8 keeps its normal 15-second clock and full-frame watchdog when FT4 receive mode is selected. Starting CQ or replying cleanly replaces a pending or completed JS8 program; callbacks from an old transmission cannot take over a new one.
- **Native digital amplifier timing.** TX Controls has optional maximum-TX and minimum-RX settings, including a Mercury Lite preset of 60 seconds TX / 15 seconds RX. Frames must fit with the transmit tail, and the receive interval survives STOP and mode changes. These controls apply to native FT8/FT4/JS8; manual PTT, TUNE and external CAT applications have separate operating limits.
- **Calibration panel repaired.** CAL PROFILE now displays its fields and Guided measurement fit correctly. JSON profile actions are labeled separately from CSV point imports, and imported measurement evidence is retained when saving.

The full software suite passed 1,413 tests with zero failures and three optional
skips. A SquareSDR 2 / Mercury Lite dummy-load session demonstrated amplifier
output and a per-radio calibration repeat: HermitSDR and the Bird meter agreed
at approximately 4.6 W input, with 343 W on the Mercury output display. Those
carrier checks do not validate the native digital timing controls or JS8
reassembly with inserted receive intervals; those checks remain pending.

## New in 2026.0911_002

- **Native JS8 transmit.** HermitSDR now has its own JS8 (normal submode) modulator — a clean-room port of JS8Call's transmit path (varicode frames, CRC-12, LDPC 174/87, Costas sync, FT8-parameter GFSK). It was checked against a real JS8Call 3.0.3 decoder: a six-frame @MAGNET distress message rendered by the encoder decoded frame for frame and came back reassembled as `WU1T: @MAGNET FLASH EMERGENCY TEST FROM HERMITSDR GRID FN42`.
- **MAGNET HF Emergency → SEND NATIVE JS8.** The window shows the exact frame plan (how many 15 s slots) and sends the message itself, one frame per slot, behind the same ENABLE TX, ARM, USB and transmitter-interlock checks as native FT8; STOP releases the frame on the air. The JS8Call-app hand-off, CW auto-key and voice script remain as alternatives.

The release completed 1,398 software tests with zero failures and three intentional
skips, a clean Debug build and the repository audit. No RF was transmitted: the
decoder check played the encoder's audio into a virtual sound device feeding
JS8Call, not the radio. The first keyed native JS8 frame into a dummy load is a
separately approved step, as native FT8 was.

## New in 2026.0911_001

- **MAGNET HF Emergency Broadcast.** Transmit ▸ MAGNET HF Emergency… (⌘⌥⇧E) is a distress instrument for the MAGNET HF mutual-assistance network (magnethf.com). It shows live whether a regional Contestia 4/250 net is on the air or only the round-the-clock JS8Call watch (7.115 / 14.115 MHz USB) is available, with the next net in UTC and local time and a receive-only Tune button per channel. Set your callsign, grid, state and region once; pick a precedence (FLASH / IMMEDIATE / PRIORITY / ROUTINE), type the message, and the window composes it three ways — a JS8Call directed text to @MAGNET, a spoken MAYDAY / PAN PAN script with phonetics, and a keyer-ready CW string.
- **JS8Call bridge.** HermitSDR has no JS8 modulator, so the window drives a running JS8Call over its local API (Settings ▸ Reporting ▸ API, port 2242): probe it, point it at a watch channel, stage the text, or send it. JS8Call keys the rig itself — normally through HermitSDR's rigctl server, so ARM and every interlock still apply. A CW auto-key option uses the same gated keyer path as CAT `send_morse`.

The release completed 1,384 software tests with zero failures and two intentional
skips, a clean Debug build, the repository audit, and a hands-on pass through the
window in the development app. No radio was involved, nothing was transmitted, and
no transmitter interlock behavior changed. JS8Call was not installed on the build
Mac, so the bridge's socket path awaits a live check.

## New in 2026.0909_001

- **Media Deck crash fixed.** Playing a Media Deck pad on 2026.0908_003 could abort the app the moment audio started (a Swift 6 actor-isolation trap on the audio engine's tap callback, not a DSP or radio fault). The pad-level meter and stream taps, and the crab's voice-dictation microphone tap, no longer inherit the window's main-actor isolation. Nothing about routing, levels, fades, streaming or transmit changed.

The release completed 1,376 software tests with zero failures and two intentional
skips, clean unsigned Debug/Release builds, and the CI smokes — including a new
one that drives the exact production tap code through an offline audio engine
and proves the old closure shape still traps. No radio was involved and no
transmitter interlock behavior changed.

## New in 2026.0908_005

- **Audio Unit hosting.** Station ▸ Audio & Streaming ▸ Audio Units hosts the effect Audio Units installed on your Mac as independent RX and TX insert chains. Units load out-of-process where the component allows (AUv3 and Apple's remote-hosted effects); in-process-only units are badged. Each chain starts with **master bypass on** until you audition it; a unit that errors or overruns its time budget is bypassed on that block and quarantined, and the chain keeps flowing. Latency per insert is shown. RF stays behind the same interlocks and the limiter runs after every insert; the Digital profile bypasses the block. VST3 is not hosted.
- **PureSignal memory terms (2026.0908_004).** PA Linearity gains a LUT / Memory candidate picker. The memory corrector composes the memoryless table with a bounded memory polynomial and inherits every safety clamp; it is session-only, default off, and behind the same ≥1 dB trial gate. On the ANAN dummy load it was accepted at 30 % (+21.5 dB, versus +20.3 dB for the table alone) and correctly rejected at 50 % by the no-agreement fail-safe. Bench notes record that both correctors bottom at an SFDR of about 52 dBc, pointing at the feedback measurement path as the next thing to check.

The release completed 1,376 software tests with zero failures and two intentional
skips, signed and clean unsigned Debug/Release builds, and the CI smokes. All
transmissions were bounded two-tone or file pulses into a 1500 W dummy load at
≤50 % drive with the SWR guard on; the radio finished disarmed. No transmitter
interlock behavior changed.

## New in 2026.0908_003

- **FT8 free-text beacon.** The FT8 panel gains a BEACON row: up to 13 free-text characters, an interval in seconds (default 30 — every other 15 s slot), and a repeat limit (default 5; 0 runs until stopped). It uses the same interlocked native-TX path as CQ — ARM, ENABLE TX, USB and the coordinator are re-checked on every frame — and, being unattended, stops itself with a reason on any refusal. Identification and band-plan compliance remain the operator's responsibility.

The release completed 1,346 software tests with zero failures and two intentional
skips, signed and clean unsigned Debug/Release builds, and the CI smokes. A
two-frame, 30 s beacon was verified into a dummy load at 3 % drive; the radio
finished disarmed. No transmitter interlock behavior changed.

## New in 2026.0908_002

- **PureSignal works.** A synthetic loopback fixture found why every earlier predistortion trial was a no-op (the correction table was indexed on the wrong amplitude scale) and two smaller flaws. With the fix, the first level-matched trial on the ANAN-7000DLE MK2 dummy load at 10 % drive was **accepted: IMD3 32.1 → 68.8 dBc (+36.7 dB)**, correlation 1.000, agreeing steady banks. The correction stays session-only, attenuation-only (peak power unchanged) and behind Capture → Trial LUT → the ≥1 dB gate → hard bypass by default.
- **Trustworthy trial verdicts.** Analysis windows that span an unkey or contain ramp/silence are labeled SETTLING / TAIL and never set the reference or judge a trial; trials skip 0.75 s of settling, need two agreeing steady banks, and fail safe. The PA Linearity window shows window levels, wire mapping and the reference/trial levels side by side.

The release completed 1,325 software tests with zero failures and two intentional
skips, signed and clean unsigned Debug/Release builds, and the CI smokes. All
transmissions were 5.5 s two-tone pulses into a 1500 W dummy load at 3–10 %
drive with the SWR guard on; the radio finished disarmed. No transmitter
interlock behavior changed.

## New in 2026.0907_008
## New in 2026.0907_008

Seven releases since 001, all landed on the same day:

- **Media Deck FX rack** — pitch, speed, echo, reverb, drive and tone sliders live on every playing pad, eighteen one-click profiles (Stadium, Underwater, Chipmunk, Demon, Gum Mouth and more), per-pad FX pins, hold-to-play pads, waveform thumbnails, and click-an-empty-pad-to-add-files.
- **FT8/FT4 station clock drift** — the panel's CLOCK row learns your slot-clock offset from the stations heard and applies a bounded correction to decode capture and native TX slots; live-converged on 40 m.
- **CW send_morse fix** — CAT Morse messages no longer release the key at the first word gap, and every refused key request (UI, CAT, paddle, hardware key) now shows in the TX Controls banner.
- **Ten-band parametric TX EQ** with per-block bypass in the TX Chain Map and gain-matched A/B; the eight-band graphic EQ remains the default.
- **Wave Editor** (Station ▸ Audio & Streaming) — record RX, microphone or the processed TX monitor to 48 kHz WAV, edit non-destructively with undo/redo, export atomically, and hand the result to the TX file player or a Media Deck pad. Editing never keys.
- **Adaptive noise reduction** — a clean-room NR2/EMNR-class reducer beside the spectral gate and RNNoise, with strength and artifact controls and a level-matched A/B latch.
- **Station devices** (Station ▸ Control Devices) — a framework for amplifiers, tuners and band directors over TCP or serial, with a demo amplifier; device faults can only add a TX inhibit, never key the radio.

The release completed 1,305 software tests with zero failures and two intentional
skips, signed and clean unsigned Debug/Release builds, and the CI smokes. Bench
work on the ANAN dummy load at 3 % drive confirmed the two-tone and limiter
scopes, the CW fix and the parametric EQ keying cleanly; audible A/B checks
remain the operator's. No transmitter interlock behavior was weakened.

## Recent feature additions

- **Features catalog:** Station → Features… (⌘⇧F) searches 53 tools and lets
  you show or hide entry points. Requirements and dependencies are explained;
  settings, saved data and ongoing activity are preserved. Reset restores
  visibility without enabling services, AI, decoders or transmit.
- **Logbook workspace:** Log → QSO Log adds ADIF import/edit/export, bulk
  changes, saved filters and automatic backups, tested with 100,000 contacts.
  Its **Awards…** and **World & radar…** buttons open DXCC/WAS/grid analysis,
  an interactive globe, UTC gray line, paths and local DX radar.
- **Waterfall visibility:** palette icon → Dynamic Underlays offers Aquarium,
  Night Garden and Deep Space. Deep Space and Night Garden now have separate
  **Signals over scenery** and **Underlay brightness** sliders, signal colors
  and a **High contrast** shortcut. Scene and marquee settings also open from
  View and the Features catalog. SKIM continues to start off each launch.

## Download & install

1. Open the [latest release](../../releases/latest) and download
   **`HermitSDR-<version>.dmg`** (or the `.zip`).
2. Open the `.dmg` and drag **HermitSDR** to your Applications folder.
3. Launch it. The build is signed with an Apple Developer ID and
   notarized by Apple — the disk image itself is signed and stapled too —
   so it opens without any "unidentified developer" warning.
4. On first launch, grant the **Local Network** permission when macOS
   asks — discovery and streaming need it.

**Staying current is automatic.** HermitSDR checks for its own updates
(**HermitSDR ▸ Check for Updates…**, plus a quiet daily background check
you can turn off) and, when a newer signed build exists, shows you the
release notes and offers a one-click **Install & Relaunch** — it verifies
the download's Apple notarization and developer signature before
replacing itself. You can always come back here and grab a build by hand.

Every release ships with a `SHA256SUMS` file; verify a download with
`shasum -a 256 -c SHA256SUMS`.

## Requirements

- Apple silicon Mac (M1 or newer)
- macOS 15 (Sequoia) or newer
- An openHPSDR radio on your LAN (Ethernet recommended at 384 kHz and
  above): **Hermes-Lite 2 / SquareSDR**, or an **Apache Labs ANAN /
  Orion-class** radio on Protocol 2 firmware (an ANAN-7000DLE MK2 on
  fw 2.2.10 is the reference — fw ≤2.1.18 receives but is not recommended
  for transmit)

## Capabilities

<!-- Mirrors the app's built-in capability table (DSP/Capabilities.swift). -->
| Capability | Support |
| --- | --- |
| Radios | Hermes-Lite 2 / SquareSDR (openHPSDR Protocol 1) · Apache Labs ANAN Orion-class, e.g. 7000DLE MK2 (Protocol 2) |
| RX / TX | Receive + transmit live-validated on both protocols (dummy load; on-air QSOs user-gated) |
| Sample rates | 48–384 kHz (P1) · up to 1536 kHz (P2) |
| Demod modes | USB, LSB, CW, AM, SAM, FM, NFM, DSB · separate wide/narrow FM deviation · CTCSS encode/decode |
| FT8 / FT4 | Receive: waterfall spots, decode panel, stations-heard ADIF (FT4 exported as MFSK/FT4), PSKReporter uploads, 15 s / 7.5 s UTC slots, time-machine replay. Transmit: native slot-clocked modulator + auto-sequencer behind ARM/TXCoordinator (native FT8 dummy-load validated; on-air validation pending), or WSJT-X via CAT PTT + audio routing |
| SSTV | Martin M1, Martin M2, Scottie S1, Scottie S2, Scottie DX, Robot 36, Robot 72, PD50, PD90, PD120, PD160, PD180, PD240, PD290 — auto VIS + manual mode/start, slant/phase correction, PNG export |
| WEFAX | IOC 576 · 120 LPM, IOC 576 · 90 LPM, IOC 576 · 60 LPM, IOC 288 · 120 LPM — polarity, slant/phase, crop/rotate, PNG with metadata |
| RTTY | 45.45/50/75/100 Bd · 170/200/425/850 Hz shifts · normal/reverse polarity · bounded AFC |
| CW | Adaptive 8–60 WPM decoder at the 700 Hz pitch · **OmniSkimmer**: GPU polyphase channelizer skims every CW signal across the whole span at once (~375 Hz bins, per-signal decoders, waterfall labels + panel) |
| Spotting | DX cluster telnet client (multiple nodes at once, RBN-ready, waterfall labels + Times Square ticker) · LoTW user badges + TQSL sign-and-upload · PSKReporter uploads · live planetary K-index |
| Logbook | ADIF import/export with preserved fields · editing, bulk changes, saved filters and backups · precise LoTW contact matching · DXCC/WAS/grid coverage · interactive worked-world globe, gray line and local DX radar · 100,000-contact performance fixture |
| Feature catalog | Searchable inventory of 51 tools and surfaces · dependency-aware menu/control visibility · direct settings links · safe visibility reset |
| Extras | Sub-RX (VFO B) · diversity RX (P2) · RF time machine (180 s IQ) with decoder-event replay + excerpt export · IQ record/replay (.hiq) · 3D waterfall + ×2–×8 history compression (~9 min of band activity) · analog multimeter + GPU TX meters · lightning-static watch · hamlib NET rigctl CAT · tuning-device knobs (Ulanzi D100H template, user-remappable with per-control tune steps, off by default) · optional Discord integration (status bot + Opus voice streaming + /waterfall snapshots, off by default) |
| Platform | macOS 15+, Apple silicon only |

## The story so far

**Transmit era.** The full TX audio rack, the complete ANAN feature set
— antenna matrix, ADC dither/random, 768/1536 kHz rates, a 0–61.44 MHz
wideband bandscope, **dual-ADC diversity receive** — a 16-sound
roger-beep portfolio (sorry), a 19-effect voice-FX shelf from plate
reverb to a true Bode frequency shifter (also sorry), the TX diagnostics
window, and the broadcast-processing generation: true-peak lookahead
limiter, phase rotator, gate/de-esser, CESSB, multiband compression, an
Optimod-style AM profile with +125% positive peaks, a two-tone IMD
source, and a live audio-chain map with snap-in rack units.

**Decoder era.** A shared decoder-session layer with an activity window,
fourteen SSTV modes with slant/phase correction, configurable RTTY with
bounded AFC, WEFAX profiles with image recovery, 2G-ALE monitoring,
decoder-event replay through the RF time machine with IQ excerpt export,
the optional Discord integration, and uninstall-proof settings.

**AM broadcast arc.** A TX program file player, the NRSC air chain
(pre-emphasis, RX de-emphasis, platform AGC, 5-band compression,
adjustable positive peaks), **C-QUAM AM stereo** — receive with a
pilot-driven STEREO lamp, and a transmit encoder whose matched
difference chain holds real channel separation through the full
broadcast processing stack (hardware-validated at 35/32 dB L/R) — a
7-band RX graphic EQ, tuning-knob support, and repeated full-codebase
performance sweeps.

**The GPU generation.** An 8192-bin fluid waterfall with a Metal post
chain — phosphor persistence, dual-scale bloom, EDR output brighter than
SDR white on XDR panels, seventeen palettes including two that evolve
with wall time, a 3D heightfield mode with a live-aurora sky driven by
the real planetary K-index, CRT glass, a liquid boundary ribbon, and an
arcade sprite layer (fireworks, achievements, a koi that swims through
the data, and friends). Plus **OmniSkimmer**: a Metal polyphase
channelizer that decodes every CW signal across the whole sampled span
at once.

**Instruments & integrations.** A finely-detailed analog taut-band
multimeter, the GPU TX meters with a phosphor modulation scope, a
lightning-static watch that reads storms off the noise blanker's impulse
detector, DX cluster spotting (multiple nodes at once, waterfall labels,
a Times Square ticker), LoTW user badges + TQSL sign-and-upload, two
visual **skins** (the warm analog "Hermit" look and a flat SmartSDR-style
"Flux Radio"), and a notarized self-updating distribution.

**The operator era** *(current)*. Everything a transmitter control app
owes its operator: a single authoritative **TX coordinator** every key
source passes through (UI, CAT, keyboard, hardware — typed policy,
ownership, latched protection trips), per-radio **calibration catalogs**
with guided power/PA-current fitting against external DC ground truth,
board/firmware **radio profiles** that keep unknown hardware
receive-only, **keyboard CW** and Hamlib CAT Morse through a
sample-clock keyer (live-validated), FM/NFM/DSB with CTCSS, ANAN
**PureSignal** feedback capture and PA characterization with a gated
predistortion trial, a validated end-to-end **WSJT-X FT8** contract,
the **Media Deck** soundboard, **Stream Deck** setup, a software **TX
latency map**, a **Digital Mode Check** doctor, the **Hi-Fi SSB profile
laboratory**, the **Band DVR**, and the **Super Skimmer**.

## Highlights

- **Two radio families, one app**: dual-protocol discovery lists P1
  (HL2/SquareSDR) and P2 (ANAN/Orion-class) radios side by side. The P2
  stack does discovery, streaming at up to **1536 kHz**, NCO phase-word
  tuning, Alex band-pass/low-pass control, an RX antenna matrix
  (ANT1/2/3, EXT1, XVTR, bypass — per-band memory), ADC dither/random,
  the hardware step attenuator, persistent **radio network
  configuration** (static IP or DHCP, written to the radio from the
  connect sheet), and **transmit** — validated live: TX to a
  **selectable ANT1/2/3** jack (the RX routing can never steer the PA),
  drive mapped to the measured PA compression knee, calibrated power/SWR
  metering, and hardware protections (SWR trip, rear-panel TX INHIBIT)
  riding the ANAN's 1 ms TX telemetry.
- **TX safety as architecture**: every key request — click, CAT, CW
  paddle, hardware — flows through one pure, exhaustively-tested
  coordinator with typed refusals, per-source ownership, and protection
  trips that latch until you disarm. Radio profiles resolve board +
  firmware before any PA command is allowed; unknown hardware is
  receive-only. Nothing keys without an explicit ARM, ever.
- **Wideband bandscope** (P2): the entire 0–61.44 MHz raw-ADC spectrum
  in its own window — click to tune, band shading, doubles as a live
  view of the Alex preselector relays.
- **Demodulation**: USB / LSB / CW / AM / SAM (synchronous AM with a
  carrier-tracking PLL) / **FM and narrow FM** (with CTCSS encode and
  decode) / **DSB**, 48–384 kHz spans on P1 and up to 1536 kHz on P2.
- **Sub-receiver**: a second hardware NCO slice (RX2) on VFO B with its
  own panadapter window — split/pileup listening, audio summed with its
  own level. VFO A/B swap, SPLIT, RIT/XIT.
- **Diversity receive** (P2): both of the Orion's phase-synchronous ADCs
  on one frequency, combined as A + w·B with a Thetis-style polar
  steering pad (drag radius = gain, angle = phase) — null local noise
  with a second antenna.
- **Super Skimmer** (P2): the Orion's four spare DDC receivers parked on
  the FT8 sub-bands of **four different bands at once**, each with its
  own decode chain — an all-band spot firehose from your own antenna,
  feeding PSKReporter and the heard map with each monitor's true
  frequency. Receive-only by construction, suspended automatically while
  diversity or PureSignal needs the hardware.
- **Band DVR**: continuous, disk-backed recording of the *entire sampled
  span* with a hard byte budget (2/8/32 GiB by resource preset, oldest
  segments pruned first). A wall-clock timeline in Radio ▸ Band DVR shows
  everything on the shelf — click any moment and it replays through the
  production chain exactly as live: re-tune, re-mode, re-decode the past.
- **RF time machine**: the last 3 minutes of the whole span buffered in
  RAM. Rewind by slider or **⌥-click a waterfall row**, re-tune/re-filter
  the past, replay decoder events from their bookmarks, and export any
  window as a replayable IQ excerpt.
- **Decoders**: in-process **FT8 and FT4** (callsign spots on the
  waterfall + decode panel + ADIF stations-heard export + PSKReporter
  uploads), **SSTV** (14 modes across Martin/Scottie/Robot/PD with
  slant-phase correction), **weather fax** (four IOC/LPM profiles with
  image recovery), **CW**, **configurable RTTY**, and a **2G-ALE
  monitor**. All report through a shared session layer (Decoder Activity
  window) and bookmark themselves into the time machine.
- **CW transmit**: keyboard paddles or Hamlib CAT `send_morse` drive a
  deterministic sample-clock keyer through the TX coordinator — shared
  RF/sidetone envelope, watchdog-guarded, live-validated on the air side
  of a dummy load.
- **Channel filter**: 513-tap complex bandpass run as 1024-point FFT
  overlap-save convolution — −120 dB stopbands, ~100 Hz skirts,
  continuously variable width, independent IF-shift, all click-free while
  you drag.
- **Noise tools**: impulse blanker, spectral-gate NR, **RNNoise ML noise
  reduction** (recurrent network, <1% CPU; press **N** to A/B by ear),
  manual + LMS auto-notch, calibrated squelch, overload auto-mute,
  two-band RX EQ.
- **Panadapter**: Metal waterfall + spectrum, GPU zoom ×1–×8,
  pan-over-span without retuning, averaging modes, adjustable speed, peak
  hold, and an audio-passband mini-waterfall (23 Hz/bin) for precise
  CW/digital placement.
- **Transmit**: 48 kHz mic → profile bandpass → 3-band EQ → compressor →
  voice FX → Hilbert-pair SSB modulator (≥40 dB image suppression) or
  full-carrier AM → per-protocol IQ. Pixel-art TX console with ARM/PTT
  interlocks, TUNE tone, drive, mic meter, live telemetry (PA current,
  watts, FWD/REV, SWR), and a **roger beep** picker — classic plus 14
  deliberately weird ones. CAT PTT keys it from WSJT-X, still behind ARM.
  It never keys without an explicit ARM.
- **Digital modes, properly plumbed**: a processor-enforced **Digital
  TX profile** (voice processing hard-bypassed, channel filters and the
  safety limiter always in charge), a **Digital Mode Check** doctor that
  names exactly what's misconfigured before you key, a validated
  **WSJT-X** CAT + PTT + audio contract, and a read-only **TX Latency
  Map** that itemizes every software delay from microphone to
  packetizer with provenance labels.
- **Per-radio calibration**: a versioned catalog keyed to the physical
  radio + firmware. **PWR CAL** promotes your wattmeter's reading to
  operator-measured truth; **CAL PROFILE** fits the full power and
  PA-current models from guided measurement points (the reference ANAN's
  current detector is fitted against external DC clamp measurements) and
  exports the evidence as CSV/JSON.
- **PureSignal** (ANAN): synchronous PA-feedback capture, delay/gain/
  AM–AM/AM–PM characterization with credible two-tone IMD readings, and
  a strictly-gated memoryless predistortion trial that hard-bypasses
  itself unless the feedback actually improves.
- **TX program source**: Microphone, **Audio file**, or the **Media
  Deck** — a soundboard of local clips and web audio with groups,
  fades, keyboard shortcuts, VoiceOver support, and interlocked routing;
  the file player streams any WAV/AIFF/MP3/AAC/FLAC into the TX chain at
  real-time pace.
- **TX audio rack**: any input device (hot-swaps while armed, with a
  channel picker for multichannel interfaces); fourteen voicing profiles
  from DX SSB and Contest to ESSB Wide, Hi-Fi AM, and the Optimod/NRSC AM
  air chains; an eight-band ±12 dB transmit EQ; **custom profiles** that
  snapshot voicing + EQ + FX under your own name; and the **Hi-Fi SSB
  Profile Laboratory** — record one voice passage, hear two candidate
  profiles loudness-matched A/B through the real chain, with objective
  spectrum/dynamics measurements.
- **Voice effects**: nineteen with an intensity slider — the classic
  shelf (doubler, slap, echo, chorus, room/hall/plate reverb) plus the
  weird ones (Jet Flanger, Phaser, Space Echo, Dalek, Chipmunk, a true
  Bode frequency-shifter Alien, 8-Bit). All causal, zero added latency,
  with an automatic post-FX bandpass so nothing leaves the channel.
- **TX Meters**: a floating diagnostics window — a scrolling
  **modulation scope** with a target zone and a mic-technique coach
  (two-tone tests trace the actual wire IQ); MIC CLIP / FLAT TOP /
  OVERDRIVE / UNDERRUN lamps; the full gain-staging meter rack plus
  PWR / SWR bars and PA temperature/current.
- **Broadcast-grade TX processing**: true-peak lookahead limiter + phase
  rotator + post-limiter band cleanup (always on); optional noise gate,
  de-esser, multiband compression, and **CESSB** controlled-envelope SSB;
  an **Optimod AM Broadcast** profile with +125% positive peaks; a
  **2 TONE** IMD test source; and a live **TX Audio Chain** stage map
  hosting snap-in rack units (Tilt / Warmth / Exciter / Leveler /
  Density).
- **The GPU display**: an 8192-bin FFT waterfall with buttery sub-row
  scrolling and a full Metal post chain — phosphor persistence,
  dual-scale bloom, chromatic aberration, vignette, film-grain **CRT
  Glass** — plus true EDR (hot carriers render *brighter than SDR white*
  on XDR panels), seventeen palettes (two computed live in the shader), a
  **3D heightfield mode** with a draggable camera and a starfield-aurora
  sky that follows the **real planetary K-index**, and an optional
  **Arcade FX** layer (S-meter floaters, prefix fireworks, achievements
  with a trophy case, a koi that swims *through* the data, a rotating
  cast of critters — press **A** to toggle it). Two **skins** restyle the
  chrome and metering: the warm analog **Hermit** look, or a flat,
  SmartSDR-inspired **Flux Radio**.
- **OmniSkimmer**: a Metal compute polyphase filter bank splits the whole
  sampled span into ~375 Hz channels (4096 at 1536 kHz) and a per-signal
  decoder fleet tracks and reads every CW — and probe-qualified RTTY —
  signal at once: per-signal WPM and confidence, green labels with SNR
  health bars, click to tune.
- **RF Vision**: a resource-budgeted signal classifier watches the
  waterfall for CW / FSK / FT8-shaped activity — click a detection to
  tune it, route it to the right decoder, rewind to its first
  appearance, or pin and export it.
- **Ask The Crab**: an optional assistant with on-device and explicitly configured
  provider options, plus radio tools: tune, set
  modes and filters, identify signals, look up schedules and DXCC
  standings, watch for band openings, run an active multi-band **Band
  Scout** sweep and offer ranked tune-tos, and — in OAuth YouTube Live
  sessions — answer viewer questions from chat behind a strict
  reporting-only boundary (viewers can ask what's on the waterfall; they
  can never tune, change settings, or reach TX).
- **Streaming**: optional built-in **YouTube Live** integration — RTMP
  session management, live captions from the decoder fleet, and the
  co-host above — plus Discord voice streaming of the speaker mix.
- **Instruments**: the header S-meter is a Metal shader (LED segments,
  analog ballistics, EDR comet head, boost flames past S9);
  Transmit ▸ Measurements & Checks ▸ **Analog Multimeter** is a finely-drawn taut-band meter with a
  spring-physics needle, peak-drag pointer, and six functions on a rotary
  knob; a **Performance Budget** window shows the app's live memory/GPU
  plan and lets you pick Conservative / Balanced / Maximum.
- **Spotting**: a telnet **DX cluster** client that monitors multiple
  nodes at once (human clusters and RBN skimmer feeds), merges and
  dedupes spots, labels them on the waterfall, and optionally crawls them
  across the bottom as a **Times Square ticker**. **LoTW** integration
  badges spotted calls that upload to Logbook of The World and
  sign-and-uploads any ADIF log through TrustedQSL. A live **Kp chip**
  calls the propagation weather.
- **Advisories**: a lightning-static watch counts broadband impulse
  crashes off the noise blanker's always-on detector — sustained storm
  rates raise a dismissable warning (and an airplane towing a banner,
  because this app is what it is).
- **Integration**: hamlib NET rigctl CAT server on TCP 4532
  (WSJT-X-ready), selectable audio output (BlackHole-friendly),
  PSKReporter uploads, **Stream Deck** offline setup with a rendered
  MK.2 tile preview, tuning-knob devices, and a seven-segment UTC clock.
- **Performance**: the whole RX chain costs ≈0.7% of one core at 384 kHz;
  audio crosses to CoreAudio through a lock-free ring; the GPU owns
  everything per-pixel; and the app holds a formal real-time contract —
  per-boundary cadences, deadlines, and overload behavior, verified by a
  30-scenario benchmark on Apple M4 Pro.

## Technology

For the technically curious — what's actually under the shell:

- **Native everything.** Swift 6 (strict concurrency), SwiftUI chrome,
  Metal for every per-pixel and per-channel job (waterfall, post chain,
  3D mode, polyphase channelizers, S-meter), Accelerate/vDSP for the
  per-sample DSP. No Electron, no Python, no runtime downloads.
- **Two wire protocols, implemented from the spec.** openHPSDR
  Protocol 1 (EP2/EP6 framing, register rotation, sample-count-paced
  pacing) and Protocol 2 (per-DDC UDP streams, NCO phase words,
  high-priority C&C at 10 Hz, DUC IQ at 800 packets/s) — both written
  against the published specs and cross-checked against reference
  implementations, with the firmware quirks documented and pinned by
  tests.
- **A real DSP chain.** Complex mixing, FIR decimation cascades, a
  513-tap FFT overlap-save channel filter with −120 dB stopbands,
  WCPAGC-style AGC, spectral-gate and RNNoise neural noise reduction
  (vendored, BSD-3), carrier-PLL synchronous AM, C-QUAM stereo
  matrix decode/encode, CTCSS, and Hilbert-pair SSB with CESSB envelope
  control on transmit.
- **FT8 the honest way.** The vendored ft8_lib (MIT) provides LDPC(174,91)
  + CRC-14 decode; slot scheduling is wall-clock disciplined; spots ride
  IPFIX to PSKReporter.
- **Deterministic transmit.** One pure TX coordinator state machine
  (11 events × 6 states, exhaustively tested), a sample-clock CW keyer,
  fixed-capacity lock-free queues on every real-time boundary, and a
  release benchmark that fails the build if percentile timings or
  allocator growth regress.
- **Memory that behaves.** The 180 s IQ history lives in one page-backed
  mmap that degrades gracefully under memory pressure; the Band DVR
  prunes itself to a byte budget; Metal textures resize on allocation
  failure. The Performance Budget window shows you the plan.
- **Tested like it matters.** 1,090 package tests (two intentional fixture skips)
  run on every push — DSP math, protocol framing against a deterministic virtual radio
  (drop/duplicate/reorder/truncate/stall faults), decoder fixtures for
  every supported mode, concurrency stress under sanitizers, and a
  docs-consistency gate that fails the build if this capability table
  drifts from the code.
- **Distribution you can verify.** Developer ID signed, Apple-notarized,
  stapled (app inside the ZIP, and disk image), SHA-256 manifests on every
  release, and a self-updater that re-verifies signature + notarization
  before replacing anything.
- **Privacy-respecting by design.** On-device AI and explicitly configured
  providers, opt-in integrations, secrets in the Keychain, and an anonymous daily ping you can turn off (see Privacy below).

## Using it

| Action | How |
|---|---|
| Tune | Click the waterfall (SSB lands the passband on the click), scroll, arrows, drag the red VFO marker (10 Hz), spin the flywheel under the dial, or scrub the readout digits |
| Tune step | Step menu in the tuning row (10–500 Hz or Auto); ⇧ = ÷5 fine, ⌥ = ×10 coarse |
| Decoders | FT8 / SSTV / FAX / CW / RTTY toggles under the mode picker — each opens its window |
| VFO B / split / sub-RX | VFO cluster: A⇄B, SPL, SUB (own panadapter window), RIT popover |
| Enter frequency | Double-click the VFO readout, type MHz |
| Notch a tone | Right-click it on the waterfall or the audio mini-waterfall |
| Rewind time | Clock button (slider) or ⌥-click a waterfall history row |
| Record | Header buttons: raw IQ (`.hiq`) and demod audio (WAV); replay from the connect sheet |
| Band DVR | **Radio ▸ Band DVR**: record toggle, wall-clock timeline (click = replay that moment), budget + shelf accounting |
| Super Skimmer | **Decode ▸ Super Skimmer** (ANAN): pick up to four bands, watch the per-band decode rates and spot feed |
| Band jump / step | Band menu (per-band memory), ◀/▶ 1–100 kHz grid steps |
| Noise / squelch / AGC / EQ | DSP popover; press **N** over the panadapter to cycle NR off/gate/ML |
| FM / CTCSS | DSP popover in FM/NFM: deviation, tone squelch, CTCSS encode |
| Display & skins | Palette icon: color schemes, Dynamic Underlays and their settings, marquee, 3D Waterfall, CRT Glass, Arcade FX (**A**), and skins |
| Transmit console | Pixel-art ACTIVATE TX CONTROLS banner (top center) |
| CW keying | TX Controls ▸ CW setup (keyboard paddles, WPM, sidetone); CAT `send_morse` works too |
| TX meters / mod scope | Gauge button in the TX Controls header |
| Media Deck | **Station ▸ Audio & Streaming ▸ Media Deck**: pads, groups, shortcuts; route behind the interlocks |
| Diversity RX | Gear popover (P2 only): enable + polar steering pad |
| CAT / audio / station | **HermitSDR ▸ Settings… (⌘,)** or gear button; output device stays in the control bar |
| CW skimmer | **SKIM** toggle in the decoder row; panel button beside it |
| RF Vision | **VISION** toggle: classified detections with click-to-tune/decode/rewind/pin |
| DX cluster / LoTW | **Log** menu (clusters, ticker toggle, LoTW badges + TQSL upload) |
| YouTube / Discord | **Station ▸ Audio & Streaming** menu (stream setup, captions, co-host; Discord bot + voice) |
| Instruments | **Radio**, **Transmit**, **Decode**, **Log** and **Station** menus; Multimeter retains ⌘⇧M |
| Feature visibility | **Station ▸ Features… (⌘⇧F)** or Settings → Features… |
| Logbook / awards / globe | **Log ▸ QSO Log**, then Awards… or World & radar… |
| Antennas (ANAN) | RX/TX chips in the header — glance for the live jacks, click to switch |
| Ask The Crab | Crab button in the header — or just ask it to find you something to listen to |
| Check for updates | **HermitSDR** menu ▸ Check for Updates… |

## Keyboard shortcuts

Bindings are remappable under the ⌨ mapping table in Settings. Defaults
include **Space** (push-to-talk hold), **N** (cycle noise reduction),
**A** (toggle the Arcade FX animations), **V** (swap VFO A/B),
**= / −** (zoom), **B** (bookmark the current frequency), and **Esc**
(mute). CW paddles ride the keyboard from the CW setup panel.

## Troubleshooting

- **No radios found** — check the **Local Network** permission, or an
  access point blocking broadcast: use the manual IP field in the connect
  sheet.
- **Choppy audio at 384 kHz** — watch `seq err` in the status bar; busy
  Wi-Fi drops UDP packets. Use Ethernet or a lower sample rate.
- **FT8 decodes but no PSKReporter spots** — set your callsign + grid in
  the gear popover; uploads go out every ~5 minutes.
- **S-meter reads high or low** — it's antenna-referenced via LNA/ATT;
  trim it against a known source with
  `defaults write com.hermitsdr.app sMeterCalOffsetDb <dB>`.
- **ANAN watts look wrong** — run PWR CAL against a real wattmeter, or a
  full CAL PROFILE fitting session; calibration is stored per physical
  radio + firmware.
- **No TX mic level on a multichannel interface** — check the **Ch**
  picker next to the mic device (XLR 1 = Ch 1). macOS offers no safe
  automatic downmix for layout-less multichannel devices, so HermitSDR
  captures exactly one channel by design.
- **Hermes-Lite 2 shows as receive-only** — update to gateware 68 or
  newer; older gateware (and unrecognized boards generally) are kept
  receive-only on purpose.

## Build lifecycle

Development builds expire: 30 days after its release date a build stops
**transmitting** and runs receive-only, asking you to download the
current one; at 90 days it stops entirely. This is a transmitter control
app under active development, and stale builds can carry known TX
defects onto the air — but a stale build should never take your
*receiver* away mid-net, so it doesn't. Your settings, logs, and
recordings are never touched by an update.

## Privacy

HermitSDR sends one anonymous usage ping per day (turn it off in
**Settings ▸ Privacy**): a random install ID, the app version, the macOS
version, and the CPU type — nothing else, ever. The receiving server
additionally records the connection's IP address, as every web server
does, and derives a coarse country from it locally; no third-party
analytics are involved. No callsigns, frequencies, audio, or radio data
ever leave your Mac unless you enable an integration that exists to send
them (PSKReporter spotting, DX cluster posting, LoTW upload, Discord,
YouTube Live) — each is off by default and scoped to exactly its job.
Ask The Crab can use on-device or explicitly configured providers; selected
cloud providers receive submitted prompts/audio. The "Check for Updates" feature
contacts GitHub to read the public releases list — the same data this
page shows.

## What's next

On-air work is operator-gated, not code-gated: the first on-air QSO,
with the **native FT8 transmit engine** implemented, live multi-band validation
of the Super Skimmer, a two-antenna diversity null test, and ear/eye acceptance for the newest decoders. On
the feature side: PureSignal predistortion beyond the gated trial,
physical Stream Deck hardware, the experimental lab modes on the CASCADE
modem, and whatever GPU eye-candy strikes the mood.

---

Built by **WU1T**. Questions and bug reports are welcome on the
[issue tracker](../../issues).

> **A note on the "Source code" links under each release:** GitHub adds
> those automatically and provides no way to remove them. Here they are
> **intentionally empty** — every release tag points at an empty commit.
> HermitSDR's source code is not published; the real downloads are the
> notarized `.dmg` / `.zip` app assets above them.
