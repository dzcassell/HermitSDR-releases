# APRS-IS Internet feed (read-only)

HermitSDR can watch the Internet side of APRS beside what its packet decoder
hears off the air. Settings › Station › **APRS-IS Internet feed (read-only)**
opens one TCP connection to an APRS-IS server, logs in as your callsign with
passcode −1 (a receive-only, unverified session) and asks the server for the
stations around your grid. Whatever it streams back runs through the same
APRS parser as RF packets (`APRSProtocol.swift`, see
[DigitalModes-Window.md](DigitalModes-Window.md) › "1200 Bd packet and APRS
on the heard map") and lands on the Stations Heard map, labelled apart from
RF. Off by default. Source issue 325.

## What is and is not sent

The client writes exactly one line, once per connection:

```
user WU1T pass -1 vers HermitSDR 2026.1101_001 filter r/42.3625/-71.0417/100 b/WU1T*
```

That is the whole upload. Nothing you hear on RF is forwarded to the
Internet, no position report is sent, no message is sent, and no code path
exists that could: the client has a single `send`, it carries the login line,
and a test (`APRSISTests`) both greps the source for that and runs the client
against an in-process server that records every byte it receives while
packets flow — the recording equals the login line. Passcode −1 means every
APRS-IS server treats the session as unverified and drops anything a client
sends anyway. The receive-only RF→Internet iGate (contributing what you hear)
is a later, separate opt-in with its own review; it is not in this build.

The Settings row repeats the live login line under **Privacy** so you can see
what goes out.

## Settings

| Field | Default | Meaning |
| --- | --- | --- |
| Switch | off | Opens the socket; needs a callsign and either a valid grid or buddy calls (otherwise the row says what is missing). |
| Server | `rotate.aprs2.net` | Any APRS-IS server; the rotate name picks a Tier 2 server for you. |
| Port | `14580` | The user-defined-filter port every server offers. |
| Radius | `100` km | Range filter around the centre of your grid, `r/lat/lon/km`, clamped to 1–1000 km. |
| Buddies | empty | Calls received wherever they are, `b/CALL1/CALL2…`; commas or spaces between, `*` wildcards (`WU1T*`), up to 32 entries. |

Callsign and grid come from Settings › Station and are not stored twice.
Changing any field while the feed is on reconnects with the new login line.
The status row shows the connection state (`Connected to T2SWEDEN as WU1T
(unverified, receive only)`), packets per minute over the last 60 s and the
session total; the line under it shows the exact filter in use.

Reconnects back off 2 → 4 → 8 … 60 s and reset only when a server answers
the login. A server that refuses the login (`# Login by user not allowed`)
stops the client instead of retrying; turn the switch off and on after
fixing the callsign. Lines are read through a bounded inbox (512 lines) and
a 64 KiB receive buffer; a server that overflows either loses the oldest
lines, counted but not shown.

## On the map

Stations Heard › **APRS** layer:

- **Green pin** — heard off the air by the packet decoder (as before).
- **Violet pin** — known only from APRS-IS.
- **Green pin with a violet ring** — heard both ways.
- Hover shows `heard on RF 3× · via APRS-IS 5×` (per-feed counts) after the
  age/report line. The dial and S/N on a pin always come from RF; an
  Internet relay never overwrites them.
- The **APRS-IS** checkbox (shown while the feed is on, or while Internet
  pins exist) hides Internet-only pins; **Clear APRS** empties the layer as
  before.

APRS-IS relays what iGates hear, so a station you also decode off the air
usually arrives twice. The same information field from the same sender on
the other feed within 60 s is folded into the existing pin as that feed's
tag — the report count does not grow and the pin does not move. A different
report from either feed updates the pin as usual. The grid-pin and path
layers count APRS-IS reports under the APRS tag like RF ones.

## Protocol sources

- Connection and login line: <http://www.aprs-is.net/Connecting.aspx>
  (`user CALL pass PASSCODE vers NAME VERSION filter …`; `# logresp CALL
  verified|unverified, server NAME`; `#` lines are comments and keepalives).
- Server-side filters: <http://www.aprs-is.net/javAPRSFilter.aspx> (`r/`
  range, `b/` budlist, space-separated clauses).
- Packet lines are TNC2 monitor format `SRC>DEST,PATH,qAC,SERVER:info`,
  parsed by the existing `APRSPacket.parse(monitorLine:)` from the APRS
  Protocol Reference 1.0.1.

Constants live beside these notes in
`HermitSDR/Integration/APRSIS/APRSISProtocol.swift`.

## Boundaries

- Receive only. No upload, no iGate, no Internet→RF path, no keying, no
  transmitter involvement of any kind.
- No credentials: passcode −1 is a constant, nothing is stored in the
  Keychain for this feature.
- The socket opens only while the switch is on and closes with the app.
