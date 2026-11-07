# Antenna rotator (hamlib rotctld) — Station Devices driver

HermitSDR can read and, on your explicit command, turn an antenna rotator
through **hamlib's `rotctld`** daemon, under **Station → Control Devices →
Station Devices**. The driver is listed there as **Rotator (hamlib rotctld)**.
It shows the rotator's model and range, its current azimuth (and elevation
when it has one), the target of the last move and whether it is still
turning; it offers **Point to**, **Park** and a **STOP** button; and it puts
a **Point rotator** action beside the heading line on the Worked World / DX
radar map and in the QSO editor.

## Read this first: what moves, and when

- **Nothing moves unless you click.** HermitSDR never tracks a spot, a
  selected map point, a satellite or anything else. Selecting a point on the
  map, opening the map, opening a contact, connecting or reconnecting to
  `rotctld`, restarting the app — none of these sends a motion command.
  The only commands that move the antenna are the **Point to** button on the
  Station Devices panel, the **Point rotator** menu on the map and in the QSO
  editor, and **Park**; every one is a click, and every one is written to
  the device log with where it came from.
- **Large swings ask first.** The *Confirm swings over* threshold is 90°
  by default. The dialog uses travel inside the controller's limits, which
  can be longer than the distance between two compass bearings. A stale
  position or missing limits block pointing. Park requires confirmation
  and explicit Park support from the controller.
- **STOP is always available** while the link is up (also ⌘. on the panel).
  It sends `\stop` immediately and ahead of anything queued: a point or park
  waiting behind an in-flight write is discarded, never sent afterwards.
- **Off by default.** A freshly added rotator device starts disabled; turn
  it on once `rotctld` is running. A disabled device opens no connection and
  sends nothing.
- **It can never touch transmit.** A rotator is not an interlock: a rotator
  fault or a lost link shows as a warning on the interlock strip, never as a
  TX inhibit, and nothing in the rotator path can key, arm or tune the radio.
- **Hardware motion review.** This feature is staged for the owner's review
  of the motion paths before it ships; it has been exercised only against a
  simulated `rotctld` (see *What has been tested*). Treat the first session
  with a real rotator as an acceptance test: stand where you can see the
  antenna, keep a hand on the controller's own stop, and start with a small
  move.

## Setting it up

1. Start `rotctld` for your rotator, for example
   `rotctld -m 1` (the hamlib dummy rotator, for a dry run) or
   `rotctld -m <model> -r /dev/cu.usbserial-XXXX -s 9600`. It listens on TCP
   **4533** by default (`rotctld -t <port>` changes it). `rotctl -l` lists the
   model numbers.
2. In HermitSDR open **Station → Control Devices → Station Devices**, press
   **Add…**, pick **Rotator (hamlib rotctld) (Rotator)**. The link switches to
   TCP `127.0.0.1:4533`; change the host if `rotctld` runs on another machine.
3. **Poll interval**: 1 s is the default (1 Hz position readback); 0.5 s
   gives 2 Hz. The readback is marked **STALE** after 3 × the interval
   without a reply, and the link reconnects after max(10 s, 4 × interval)
   of silence.
4. **Confirm swings over**: the degrees beyond which a Point-to asks first.
5. Leave **Enabled** off until `rotctld` is running, then switch it on. The
   Identity box shows the model, manufacturer (in the Serial row) and backend
   version from `\dump_caps`; Telemetry shows the range and the position.

## What is sent and when

| HermitSDR sends | When | rotctld answers |
| --- | --- | --- |
| `+\dump_caps` `+_` | Once per connection | capabilities block, `Info:` line, each ending `RPRT 0` |
| `+\get_pos` | Every poll interval | `Azimuth:` / `Elevation:` lines, `RPRT 0` |
| `+\set_pos az el` | **Point to** / **Point rotator**, after any confirmation | `set_pos: az el`, `RPRT 0` (or an error code) |
| `+\stop` | **STOP** | `stop:`, `RPRT 0` |
| `+\park` | **Park** | `park:`, `RPRT 0` |

Every command carries hamlib's `+` extended-response prefix, so each reply is
a self-contained block that ends in `RPRT n`. `RPRT 0` is success; a negative
code is a hamlib error, logged with its name (for example `RPRT -9 RIG_ERJCTED
— command rejected by the rotator`) — a rejected move clears the target and
leaves the link up. Map and QSO bearings are degrees true. Align the rotator controller with
true north before using these targets. A target is sent only if it lies
inside the range the rotator reported (an overlap rotator such as −180…450°
receives the representation nearest its current position), otherwise the
command is refused in the log. The controller range is checked again after
rounding to the two decimal places used on the wire.

Elevation: an **Az-El** rotator gets the elevation you type on the panel (the
map and QSO editor send azimuth only and keep the current elevation); an
azimuth-only rotator is sent `0` for elevation, which Hamlib backends ignore.
Explicit elevation requests are refused for azimuth-only controllers.

Sources: the hamlib manual pages
[rotctld(1)](https://hamlib.sourceforge.net/html/rotctld.1.html) and
[rotctl(1)](https://hamlib.sourceforge.net/html/rotctl.1.html); the `RPRT`
codes are `enum rig_errcode_e` in hamlib's `include/hamlib/rig.h`.

## Bearings on the map and in the QSO editor

- **Worked World / DX radar**: select a located grid cell or a radar spot.
  Beside the distance/heading line a **Point rotator** menu offers the
  **short path** and the **long path** (short + 180°). Map markers are
  reported *grid centers*, not exact positions, and the confirmation says so.
- **QSO editor**: a *Bearing* line appears under the fields when a rotator
  device exists. The target is the contact's **grid** (GRIDSQUARE, at the
  precision logged) or, when there is none, the **DXCC entity centroid** for
  the callsign from the country file — the line names which one was used.
  The station end is MY_GRIDSQUARE, else the grid in Settings. No bearing is
  invented when neither resolves.
- Headings are **true**, not magnetic: `rotctld` and every rotator controller
  work in true azimuth once calibrated to the mast's north.

## What has been tested

The driver was written from the hamlib manual pages above and exercised
only against a **simulated rotctld** in HermitSDR's automated tests
(`Tests/DSPTests/RotctldRotatorTests.swift`): the exact command strings and
response grammar, `dump_caps` parsing and range handling, polling, a move
that converges over successive readbacks, **stop mid-move** (including stop
preempting a queued move), rejected moves (`RPRT -9`), out-of-range targets
refused before the wire, silence → stale → reconnect with **no move re-sent
on reconnect**, a disabled device opening no connection, the confirmation
threshold, and the real TCP transport against a loopback fixture server.
**Nobody has yet pointed a real rotator with it.** If you do, please report
what happened at <https://github.com/dzcassell/HermitSDR-releases/issues>.

Not included: satellite or any continuous tracking (deliberately — it would
be a separately armed consumer of this interface, not a side effect),
magnetic bearings, rotator calibration, serial rotator protocols without
`rotctld`.
