# Native transmit tools — #122, #223, #72 and #174

Available since 2026.1018_001, published with explicit owner authorization.
Software validation does not establish hardware acceptance.
All four issues remain open for the operator checks below.

Open **Transmit → Native Transmit…**. Opening the window never enables TX.
ARM remains in TX Controls. Each mode requires an explicit, session-only enable;
STOP clears all three enables and cancels synthesis, audio, retries and slots.
Closing the window stops its program. USB or DATA-U is required. Changing radio,
dial, mode, sample rate or filter invalidates the program. Split TX uses the
shown transmit frequency. Another RF owner taking the channel cancels pending
native calls and beacon slots before they can resume after that over. All key requests pass through TXCoordinator, the
existing operating policy, profile capability, calibration, transverter,
protection and station interlocks. Unknown radio profiles cannot transmit.

## Feld Hell

Enter 1–80 characters, inspect the raster, then Send text. Supported characters
are A–Z, 0–9, space and `. , ? / + - =`; lowercase converts to uppercase.
Unsupported input is refused before any key request. The original hand-drawn
5×7 font has blank side columns and vertically doubled dots: seven columns,
14 half-dots per column, 245 half-dots/s, 2.5 characters/s. Every whole ink dot
lasts at least 1/122.5 s. Sample boundaries use rational rounding at 48 kHz;
1 ms envelope ramps soften transitions without inserting gaps within ink.

The chosen audio center is 500–2500 Hz. Digital profile bypasses speech
processing for the program. The operator's current profile (including custom
settings) is reapplied after actual RF release. Audio ownership remains through
the coordinator tail. Late worker blocks carry a UUID and are rejected by the
TX chain after that generation ends.

Software fixtures recover the native raster through the production decoder
with deterministic noise, verify at least 98% of unfiltered audio power lies
within ±500 Hz of the selected center, and reject worker stalls instead of
catching up. This spectral bound is a software fixture, not an RF measurement.
The text field starts from the configured station identity; identification
remains visible in the preview and is not silently appended when sending.

Timing reference: [Feld Hell technical specifications](https://www.qsl.net/zl1bpu/DOCS/Hellspec.pdf).
No external implementation or font was copied.

## ALE calling

Enter valid local and remote ALE addresses and Call on the current dial.
The existing ALE caller/controller builds the call, waits for its coordinator
key grant and actual release, receives complete decoder bursts, and sends the
acknowledgment for a matching response. Terminate sends the normal termination
exchange; STOP cancels immediately. Retry/timeout behavior comes from the
existing tested ALECallingSession configuration. A local session log retains
the last 100 protocol/lifecycle events. Scanning cannot retune while
calling, waiting for a response or linked. Its previous enabled state and
channel index remain available when ownership ends. No autonomous answering,
frequency hopping or unattended sounding is introduced.

## WSPR

Choose the dial locally, then callsign, four-character grid, advertised dBm,
audio center, interval and number of attempts. The advertised power must be
one of the standard type-1 WSPR values and does not change actual drive.
The waveform uses the existing encoder, continuous-phase 4-FSK, 162 symbols,
32768 samples/symbol at 48 kHz: exactly 110.592 seconds.

Start schedules the next future even UTC minute plus one second. Intervals
are 2–30 slots (at most 50% nominal duty), 1–30 attempts, with a one-hour
session expiry. Missed slots more than 100 ms late are skipped, never queued
for catch-up. A wall/monotonic disagreement above 500 ms cancels the session,
including an active final frame. No automatic clock synchronization is done.
Existing native digital amplifier limits can refuse the entire frame when its
duration plus the maximum tail exceeds the selected amplifier limit; they
also retain the required receive interval through STOP and later programs.

Timing reference: [WSPR overview](https://wsjt.sourceforge.io/WSPR_QST_Nov_2010.pdf).
The nominal software start does not establish antenna-port timing. Protocol
preload, DSP group delay, relays and RF envelope must be measured on each radio.

## Control API TX

See [ControlAPI.md](ControlAPI.md#56-session-approved-transmit--revision-3).
The browser console itself remains receive-only. A paired API client must be
locally granted TX for that exact connected session; it cannot ARM. Approval is
never stored or restored from a client-selected ID. Stop/disconnect/revoke/
permission changes/rotation/disarm remove authorization or stop the owner.
Disarm clears approvals synchronously; a quick re-arm cannot restore them.
The main header identifies the active program/client and offers STOP TX.
Each queued key request and packet stream is bound to its lease generation.
Clearing or replacing that lease invalidates queued keys before they can encode
MOX; an expired or stale key cannot become an unrestricted local request.
A 450 ms deadline is enforced independently on the protocol queue, with a
20 ms check period; clients should renew every 200 ms. The shorter deadline
leaves margin inside the 500 ms host dead-man budget. Hardware MOX response and
network-loss behavior still require measurement.

## Operator acceptance still required

Before any RF test, confirm the radio, TX jack, dummy load, band, drive, ARM and
interlocks in that session. No such test has been authorized or performed here.
On both HL2 Protocol 1 and ANAN Protocol 2, measure waveform timing, spectrum,
actual RF tail/release, STOP/disarm/protection, radio disconnect, UI stall and
remote lease loss. Receive Hell/WSPR on an independent decoder; exchange ALE
call/response/ACK/termination with an independent station or test set on the
load. Check amp cooldown and calibrate WSPR antenna-port slot timing. The
second-machine TLS/Keychain/LAN/mobile acceptance from #122 is also outstanding.
Keep all four issues open until their relevant hardware acceptance is recorded.
