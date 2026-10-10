# Reference Amplifier Line Protocol

This document describes the text protocol spoken by the driver that HermitSDR
lists as **Reference amplifier (line protocol)** under **Station → Control
Devices → Station Devices**, and shows how to put a real amplifier behind it
with a small bridge program. It applies to HermitSDR 2026.0907_008 and later
and was checked against the 2026.1005_001 source.

The short version: HermitSDR opens a plain TCP connection (or a serial port),
sends `ID?` once and then `ST?` about once a second, and shows whatever the
other end answers. Anything that answers those two questions in the format
below appears in HermitSDR as an amplifier panel. The other end can also raise
alarms. An alarm is either a warning, which is only shown, or a fault, and a
fault from an amplifier stops HermitSDR from transmitting until it clears.

## What has and has not been tested

Please read this before relying on anything here.

- The protocol description was written from the app's source code and its
  automated tests. Those tests run the driver against HermitSDR's built-in
  simulated amplifier, over a TCP connection on the same machine, and over a
  simulated serial port.
- The bridge in the last section, `tools/expert-amp-bridge.py`, has been run
  only against its own built-in stand-ins: a fake Expert Amp Server and a fake
  HermitSDR client (`--selftest`). The fake server's replies were written from
  the Expert Amp Server source code at version 0.4.8.
- **Nobody has yet run the bridge against a real Expert Amp Server, a real SPE
  amplifier, or the HermitSDR app itself.** No real amplifier driver ships in
  HermitSDR today; the reference driver is the only one.

Reports from real stations are what this needs next. Please send them to
<https://github.com/dzcassell/HermitSDR-releases/issues>.

## What the reference driver is for

The reference driver exists so that the station-device panel (identity,
readings, alarms, log, and the transmit interlock) can be exercised without
any hardware. Pressing **Demo amplifier** in the Station Devices window starts
a simulated amplifier inside the app that speaks this protocol.

The same driver can also talk to something outside the app. That makes it a
practical way to connect equipment HermitSDR has no native driver for: write a
small program that sits beside the equipment, translates its status into the
lines below, and listens on a TCP port. HermitSDR needs no changes.

## Setting it up in HermitSDR

1. Open **Station → Control Devices → Station Devices**.
2. Press **Add…**. A sheet titled "Add station device" appears.
3. Fill in the sheet:
   - **Name**: anything you like, for example `SPE Expert`.
   - **Driver**: `Reference amplifier (line protocol) (Amplifier)`. It is the
     only choice at present.
   - **Kind**: leave it at Amplifier. The kind decides how alarms are treated;
     see "What each value does" below.
   - **Expected model**: leave this blank the first time. If you fill it in
     and the other end reports a different model word, HermitSDR marks the
     device FAULTED, closes the connection, and does not reconnect until you
     press **Retry**.
   - **Link**: choose **TCP**, then type the **Host** (a name or address) and
     the **Port** of the program that speaks this protocol. The sheet suggests
     port 4001; any port from 1 to 65535 is accepted. **Serial** and
     **Loopback** are the other two choices; Loopback is the built-in
     simulator.
   - **Poll interval**: how often HermitSDR asks for status. One second is the
     default; the slider runs from 0.2 to 10 seconds.
   - **Hot at**: the temperature, in degrees Celsius, at which HermitSDR stops
     transmitting. The default is 80 °C.
   - **Inhibit TX while this device is offline**: off by default. Turn it on
     only if you never want to transmit without the device connected.
   - **Enabled**: on.
4. Press **Add**. The device appears in the list with a coloured lamp, and the
   panel on the right shows CONNECTING, then CONNECTED.
5. Within a second or two the Identity box shows the model, and the Telemetry
   box shows state, power, SWR, temperature and band. The Log box at the
   bottom records what happened and is the first place to look when something
   does not work.

Your settings are saved with the rest of the app's settings. The connection is
remade automatically whenever HermitSDR starts, and after any interruption.

If the other end is on another computer, macOS must allow HermitSDR to use the
local network (System Settings → Privacy & Security → Local Network). HermitSDR
already needs that permission to reach the radio.

## The wire protocol

### Connection and framing

- The TCP link is an ordinary, unencrypted TCP connection. HermitSDR is the
  client; your program listens. The serial link is 8 data bits, no parity, one
  stop bit, at the baud rate you choose (300 to 230400), with no flow control.
- Everything is plain text, one message per line.
- HermitSDR ends every line it sends with carriage return and line feed
  (`CR LF`).
- In the other direction HermitSDR accepts a carriage return, a line feed, or
  both as the end of a line, and ignores empty lines.
- Words on a line are separated by one or more spaces. Tabs are not
  separators.
- The first word of a line, the names inside a status line, and alarm codes
  are not case-sensitive.
- A line may be at most 1024 bytes. If more than that arrives without an end
  of line, HermitSDR throws the unfinished text away and writes "frame buffer
  overflow" in the log.
- When a connection is made, anything left over from the previous connection
  is thrown away, so a new connection always starts at the beginning of a
  line.
- HermitSDR does not match replies to questions. Every line that arrives is
  read on its own, in order, whenever it arrives. Your program may therefore
  send a status line or an alarm at any time, not only when asked.

### What HermitSDR sends

| Line | When it is sent | Expected answer |
| --- | --- | --- |
| `ID?` | Once, first, each time a connection is made. | `ID …` |
| `ST?` | Straight after `ID?`, and then once every poll interval. | `ST …` |
| `OPER` | Only when the operator presses **Operate** in the panel. | `OK`, or `ERR` and a reason |
| `STBY` | Only when the operator presses **Standby**. | `OK`, or `ERR` and a reason |
| `TUNE` | Only when the operator presses **Tune request**. | `OK`, or `ERR` and a reason |
| `BAND <metres>` | Only when the operator presses **Set band** (a whole number from 1 to 160). | `OK`, or `ERR` and a reason |
| `LOGIN <secret>` | Never, in the app as shipped. See "Authentication". | `OK` or `ERR AUTH` |

HermitSDR sends `ID?` and `ST?` one after the other without waiting for the
first answer. It never sends `OPER`, `STBY`, `TUNE` or `BAND` by itself: not
when it connects, not when it reconnects, not when settings are restored, and
not when you change band on the radio. Those four lines are only ever the
result of a button press in the Station Devices window.

The four buttons are always shown for this driver, whatever is at the other
end. A device that cannot or will not act on one should answer `ERR` with a
short reason; the reason appears in the Log box.

### What HermitSDR understands

| Line | Meaning |
| --- | --- |
| `ID <model> FW <firmware> SN <serial>` | Identity. `<model>` is required and must be a single word. `FW` and `SN` are optional. |
| `ST [OPER\|STBY\|TUNING] PWR <watts> SWR <ratio> TEMP <celsius> BAND <metres> FLT <code\|NONE>` | A complete set of readings. See the rules below. |
| `ALM <code> <text>` | Raise an alarm, or update its text. `<code>` is one word. |
| `CLR <code>` | Clear that alarm. |
| `OK` | A command was accepted. Nothing is shown. |
| `ERR <text>` | A command was refused. The log shows "device rejected: " and the text. |
| anything else | Ignored, apart from a log entry "unrecognized line". |

Rules for the `ID` line:

- If the model word is missing, the line is logged as malformed and the
  Identity box stays empty.
- If you entered an **Expected model**, it is compared with the model word
  without regard to case. A difference is a fault: the connection is closed,
  nothing more is sent, and HermitSDR waits for you to correct the field and
  press **Retry**.

Rules for the `ST` line:

- The word after `ST` gives the state. `OPER` means operate, `STBY` means
  standby, and `TUNING` means operate with a tune cycle in progress. If the
  state is not known, **leave the word out**. Do not put any other word there:
  it would be taken for the first reading name, and every reading after it
  would be lost.
- After the state come pairs of a name and a value, in any order. Names that
  HermitSDR does not know are skipped together with their value.
- `PWR` is forward power in watts, `SWR` is a ratio such as `1.25`, and `TEMP`
  is in degrees Celsius. All three may have a decimal point. `BAND` is a whole
  number of metres, for example `20`.
- A reading that is missing, or whose value is not a number, is shown as a
  dash (—). **This is how to say "not available": send `-` or leave the pair
  out. Never send a made-up number.** Do not send `nan` or `inf`; they count
  as numbers.
- Every `ST` line replaces all the readings. A reading that was present in the
  last line and is absent from this one becomes a dash.
- `FLT` is read and then ignored. It is kept in the line for people reading a
  capture. **A fault only reaches HermitSDR through an `ALM` line.**

Rules for alarms:

- An alarm whose code begins with the letter `W` is a **warning**. Every other
  alarm is a **fault**. Choose your codes accordingly: `WATCHDOG` would be a
  warning.
- There is one alarm per code. Sending `ALM` again for a code that is already
  raised only replaces its text.
- An alarm stays raised until HermitSDR receives `CLR` with the same code.
  **HermitSDR keeps alarms across a lost connection.** A device should
  therefore say, soon after every new connection, which of its alarms are not
  active (by sending `CLR` for them) as well as which are.
- If an alarm is stuck, see "Known limits" below.

### An example exchange

This is a typical exchange between HermitSDR and its built-in simulated
amplifier. Lines from HermitSDR are marked `>`, lines from the amplifier `<`.

```
> ID?
> ST?
< ID HERMIT-AMP-1K FW 1.4.2 SN DEMO-0001
< ST STBY PWR 0 SWR 1.10 TEMP 38 BAND 20 FLT NONE
> ST?
< ST STBY PWR 0 SWR 1.10 TEMP 38 BAND 20 FLT NONE
> OPER                                   (operator pressed Operate)
< OK
> ST?
< ST OPER PWR 0 SWR 1.10 TEMP 37 BAND 20 FLT NONE
< ALM OVERDRIVE protection trip          (the amplifier tripped, unasked)
> ST?
< ST STBY PWR 0 SWR 1.10 TEMP 38 BAND 20 FLT OVERDRIVE
> OPER
< ERR FAULT
< CLR OVERDRIVE                          (the trip was reset)
```

Between the `ALM` and the `CLR` line HermitSDR refuses to transmit.

You can talk to any program that speaks this protocol by hand. For example,
with the bridge from the last section running on the same machine:

```
nc 127.0.0.1 4001
ID?
ST?
```

## Timing

| Event | What HermitSDR does |
| --- | --- |
| Connecting | Gives up after 10 seconds. A refused or unreachable address fails at once. |
| Connected | Sends `ID?`, then `ST?`. |
| Every poll interval | Sends `ST?`. The default is 1 second. Stored values are kept between 0.2 and 60 seconds. |
| No `ST` line for more than 3 poll intervals | Marks the readings **STALE**: they stay on screen, greyed, with their age, and a warning is added. |
| Nothing at all received for 10 seconds, or 4 poll intervals if that is longer | Closes the connection with "no response" in the log and reconnects. |
| Connection lost or failed | Waits 1 second and tries again. Each further failure doubles the wait (2, 4, 8, 16, 32 seconds) up to 60 seconds. The wait returns to 1 second once a line has been received on a new connection. |
| TCP keep-alive | Probes an idle connection after 30 seconds, every 10 seconds, three times. |

There is no time limit on an individual answer. A command that is never
answered is not repeated and is not reported; only complete silence closes the
connection. HermitSDR writes one line at a time. If the operator presses
Operate and then Standby while a line is still being written, only the later
one is sent.

The panel and the transmit interlock are refreshed at most ten times a second.

## Authentication

**The app as shipped does not authenticate and does not encrypt.** The
password box does not appear for this driver and `LOGIN` is never sent. Anyone
who can reach the port can read what the device says, and the device has no
way to know who is asking. Keep the port on the same machine or on a trusted
station network.

For completeness, the protocol defines `LOGIN <secret>`, sent after `ID?` and
before the first `ST?`, and answered with `OK` or `ERR AUTH`. The app has the
code for it: a password would be kept in the macOS Keychain, never in the
settings file and never in the log, which shows `login ••••` instead. It is
used only by the app's own tests at present. A device should not require
`LOGIN` today, because HermitSDR will not send it.

## Error handling

- **Wrong model.** Explained above: the device is FAULTED until you press
  **Retry**.
- **Refused command.** `ERR <text>` is written to the log and nothing else
  happens.
- **Unknown line.** Written to the log (the first 80 characters) and ignored.
- **Over-long line.** Thrown away, with a log entry.
- **Write failure or closed connection.** The connection is closed and remade
  after the wait described under Timing. Commands waiting to be sent are
  dropped, not replayed.
- **Buttons while disconnected or faulted.** The four device buttons are
  greyed. A command that arrives anyway is refused and counted, never saved
  for later.
- **Late data.** Anything that arrives from a connection HermitSDR has already
  given up on is discarded and counted as "stale" in the Frames row.

The log keeps the last 200 lines.

## Known limits

These describe how the app behaves today. They are not promises of a change.

- **Alarms are not cleared when the connection is remade.** HermitSDR
  remembers every alarm a device has raised until it receives `CLR` for that
  code. Losing the connection and reconnecting does not clear anything. If a
  device raises a fault and then goes away, or comes back without sending
  `CLR`, the fault stays on screen and goes on inhibiting transmit. To clear it
  by hand, switch the device off and on again with its toggle in the device
  list; that starts it afresh with no alarms. Quitting and reopening HermitSDR
  does the same. A well-behaved device avoids the problem by sending `CLR` for
  each alarm that is not active soon after every new connection, as the bridge
  in the last section does.
- **The four device buttons are always shown** for this driver, even when the
  other end cannot act on them.
- **There is no authentication and no encryption**; see "Authentication".
- **`FLT` in the status line has no effect**; only `ALM` lines do.

## What each value does inside HermitSDR

For a device whose kind is Amplifier:

| What arrives | Effect |
| --- | --- |
| State (`OPER`, `STBY`, `TUNING`) | Display only. |
| `PWR` | Display only. |
| `SWR` | Display only; highlighted above 2.0. It does not stop a transmission. HermitSDR's own SWR protection reads the radio, not this value. |
| `TEMP` | Display. At or above the **Hot at** setting it **inhibits transmit**. |
| `BAND` | Display only. HermitSDR does not tell the device which band the radio is on. |
| `FLT` | Nothing. |
| `ALM` with a fault code | **Inhibits transmit** until `CLR`. |
| `ALM` with a `W…` code | Warning only. |
| Wrong model | Fault: **inhibits transmit** until corrected. |
| Readings stale | Warning only. |
| Device not connected | Warning only, unless **Inhibit TX while this device is offline** is on, in which case it **inhibits transmit**. |
| Device switched off in the list | Nothing at all. |

If you change the kind to Band Director or Device, faults become warnings and
the temperature rule does not apply.

**What an inhibit does.** The strip at the top of the Station Devices window
turns red and reads INHIBIT with the reason. HermitSDR refuses every request
to transmit, whether it comes from the PTT button, TUNE, a key or paddle, a
control surface or a CAT program, and the TX Controls window shows a notice
with the reason.
ARM is not changed. If the inhibit appears while HermitSDR is transmitting,
HermitSDR stops transmitting in the normal way and says so in the same notice.
When the last reason goes away the inhibit lifts by itself; HermitSDR does not
start transmitting again.

A warning is shown in the same strip in amber, and in the TX Controls notice
when no other warning is showing. It never stops a transmission.

Please treat the inhibit as a courtesy, not as protection. It reacts within
about one poll interval of the device reporting a problem, which is far slower
than an amplifier's own protection circuits.

## Safety contract

- **A device can stop a transmission. A device can never start one.** Nothing
  in this protocol keys the radio, arms the transmitter, changes the drive
  level or changes frequency. There is no line a device can send that makes
  HermitSDR transmit.
- A device can only add a reason not to transmit, or a warning. It cannot
  remove a refusal that comes from anywhere else: ARM, HermitSDR's SWR
  protection, the radio's TX INHIBIT input and the operator's frequency limits
  all continue to apply.
- `OPER`, `STBY`, `TUNE` and `BAND` are requests to the external device,
  made only by a button press. "Tune request" asks the device to run its own
  tuning cycle; it does not make HermitSDR send a carrier.
- Connecting, reconnecting and restoring settings never send a command that
  changes the device. They send `ID?` and `ST?` only.

## Connection ownership

A serial port can have only one program in charge of it. The USB port on an
amplifier is a serial port, so only one program can control the amplifier
through it at a time.

That is the reason to prefer a network bridge. A server that sits beside the
amplifier owns the serial port and can then serve several programs at once
over the network: its own web page, a logger, and HermitSDR. HermitSDR opens
exactly one TCP connection per device in your list and never touches a serial
port unless you choose the Serial link and name the port yourself.

If you do use the Serial link, HermitSDR asks macOS for sole use of the port.
If another program already holds the port for its sole use, the attempt fails
and the log says why. If the other program did not ask for sole use, both
programs would be reading the same port and neither would work properly, so
do not point two programs at one port.

Do not point the Serial link at the USB port of an SPE amplifier. The
reference driver speaks the text protocol in this document, not SPE's own
protocol, and the two cannot understand each other.

## Bridging an SPE Expert amplifier through Expert Amp Server

[Expert Amp Server](https://github.com/w9fyi/expert-amp-server) is a program
for a Raspberry Pi (or similar) connected to the USB port of an SPE Expert
amplifier. It shows the amplifier's front panel in a web browser and offers
the amplifier's status to other programs. The repository linked here is a copy
of the original at <https://github.com/FtlC-ian/expert-amp-server>.

The bridge connects the two. It asks Expert Amp Server for the amplifier's
status and answers HermitSDR in the protocol above. It needs Python 3.7 or
newer and nothing else.

The bridge is the file `tools/expert-amp-bridge.py` in the public repository
<https://github.com/dzcassell/HermitSDR-releases>, beside this document
(`docs/ReferenceAmplifierProtocol.md`). To fetch just that one file:

```
curl -O https://raw.githubusercontent.com/dzcassell/HermitSDR-releases/main/tools/expert-amp-bridge.py
```

```
  SPE Expert ──USB── Expert Amp Server ──HTTP── expert-amp-bridge.py ──TCP── HermitSDR
                       (port 8088)                  (port 4001)
```

### What the bridge will and will not do

- **It only watches by default.** Without `--allow-control`, it makes
  only `GET /api/v1/status` requests and never presses a front-panel key or
  changes operate or standby.
- Started without `--allow-control`, it answers `OPER`, `STBY`, `TUNE` and
  `BAND` with `ERR READONLY`. The four buttons are still shown in HermitSDR;
  pressing one writes the refusal to the log and does nothing else.
- **`--allow-control` honours Operate and Standby** (bridge 1.1). Expert Amp
  Server offers the amplifier's OPERATE key, which flips between operate and
  standby, and has no separate "standby" action, while `OPER` and `STBY` in
  this protocol mean "be in operate" and "be in standby". The bridge therefore
  treats each as a verified toggle: it reads the amplifier's state fresh from
  the server (never from its poll cache); if the state already matches it
  answers `OK` without pressing anything; otherwise it presses OPERATE once,
  waits `--control-settle` seconds (1 s by default), reads again and answers
  `OK` only when the amplifier reports the requested state. If the state did
  not move at all it presses once more; it never presses more than twice for
  one command. Any other outcome is `ERR STATE …` naming what the amplifier
  reports, and nothing further is pressed — check the front panel. `OPER` is
  refused with `ERR ALARM` while the amplifier reports an alarm (`STBY` is
  always allowed). `TUNE` and `BAND` stay refused: the server offers no
  absolute action for them. The residual risk is a hand on the front panel in
  the second between the read and the press; the verification reports it
  rather than hiding it. Operate/standby through the bridge was checked
  against the built-in fake server only (`--selftest`, 65 checks), not a real
  amplifier.
- **Losing sight of the amplifier is a warning, not a stop.** If the bridge
  cannot get the amplifier's status (the amplifier is switched off, or Expert
  Amp Server cannot be reached), it shows dashes and raises a warning.
  HermitSDR goes on transmitting normally, so you can operate without the
  amplifier. You can ask for the stricter behaviour with `--link-loss fault`;
  see "About losing the amplifier's status" below.
- **An alarm from the amplifier itself is always a fault**, and HermitSDR will
  not transmit until it clears, whichever setting you choose.

### Running it

The simplest place to run the bridge is on the Raspberry Pi, beside Expert Amp
Server.

1. Copy `expert-amp-bridge.py` to the Pi.
2. Check it: `python3 expert-amp-bridge.py --selftest`. This talks to no real
   device. It should end with "0 failed".
3. Start it:

   ```
   python3 expert-amp-bridge.py --listen 0.0.0.0 --amp-url http://127.0.0.1:8088

  # the same, with Operate / Standby from HermitSDR honoured (verified toggle)
  python3 expert-amp-bridge.py --listen 0.0.0.0 --amp-url http://127.0.0.1:8088 --allow-control
   ```

   `--listen 0.0.0.0` lets other computers on your network connect. Without
   it the bridge accepts connections from the same machine only.
4. In HermitSDR, add a device as described under "Setting it up", with link
   **TCP**, host = the Pi's name or address, port = `4001`, and **Expected
   model** blank.

What to expect: within a few seconds the panel shows CONNECTED, the model
(for example `EXPERT-2K-FA`), and the state, power, SWR, temperature and band.
The strip at the top of the window reads CLEAR. If the amplifier is switched
off, or the bridge cannot reach Expert Amp Server, the readings turn into
dashes, the alarm `WLINK` appears with the reason, and the strip reads WARN;
HermitSDR still transmits. If the amplifier reports an alarm of its own, the
alarm `AMPALARM` appears, the strip reads INHIBIT, and HermitSDR will not
transmit until the amplifier's alarm clears.

You can instead run the bridge on the Mac that runs HermitSDR. In that case
leave `--listen` out, give `--amp-url http://<the Pi>:8088`, and use host
`127.0.0.1` in HermitSDR. Python 3 on a Mac comes with Apple's command line
developer tools.

To keep the bridge running on the Pi, a systemd unit along these lines works
(adjust the path and the user):

```
[Unit]
Description=HermitSDR bridge for Expert Amp Server
After=network-online.target expert-amp-server.service

[Service]
ExecStart=/usr/bin/python3 /home/pi/expert-amp-bridge.py --listen 0.0.0.0
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target
```

`python3 expert-amp-bridge.py --help` lists every option. The ones you are
most likely to want:

| Option | Default | Meaning |
| --- | --- | --- |
| `--amp-url` | `http://127.0.0.1:8088` | Where Expert Amp Server is. |
| `--listen` | `127.0.0.1` | Address the bridge listens on. |
| `--port` | `4001` | Port the bridge listens on. |
| `--poll` | `1.0` | Seconds between status requests to Expert Amp Server. |
| `--stale-after` | `3.0` | Readings older than this many seconds are reported as unavailable. |
| `--link-loss` | `warning` | What to tell HermitSDR when the amplifier's status is lost: `warning` only warns, `fault` also stops transmitting. See below. |
| `--allow-control` | off | Explicitly enable verified Operate/Standby requests; Tune and Set band remain read-only. |
| `--control-settle` | `1.0` | Seconds to wait after an OPERATE key press before verifying the requested state. |
| `--model` | (from the server) | Model word to report, if you want it fixed. |
| `--verbose` | off | Log every line received from HermitSDR. |

### How the readings are translated

Expert Amp Server answers `GET /api/v1/status` with
`{"success": true, "data": { … }}`. The bridge uses these parts of `data`:

| HermitSDR shows | Taken from | Notes |
| --- | --- | --- |
| Model | `modelName` | "EXPERT 2K-FA" is sent as `EXPERT-2K-FA`. `UNKNOWN` until the server has named it. |
| Firmware | — | Shows the bridge's own version, `bridge-1.1`. The amplifier's firmware is not in the status. |
| Serial | — | Always a dash. |
| State | `operatingState` | `operate` → OPERATE, `standby` → STANDBY, anything else → dash. |
| Power | `powerWatts` | Watts. A dash when the server does not report it. |
| SWR | `swr` | The SWR on the amplifier side of its tuner. The amplifier reports 0.00 when it is not measuring; anything below 1.0 is shown as a dash. |
| Temp | `temperatureC`, `temperatureLowerC`, `temperatureCombinerC` | The hottest of the sensors reported, in °C. |
| Band | `bandText`, else `band` | "20m" → 20. |

The bridge raises these alarms:

| Code | Kind | When |
| --- | --- | --- |
| `AMPALARM` | fault — **inhibits transmit** | The amplifier reports an alarm (`alarmCode`, `alarmsText`). The text is the server's wording, for example "S swr exceeding limits". |
| `WAMP` | warning | The amplifier reports a warning (`warningCode`, `warningsText`), for example "K atu bypassed". |
| `WLINK` | warning | The amplifier's status is not available: Expert Amp Server cannot be reached or gave an unusable answer for longer than `--stale-after`; or it says it has had no recent contact with the amplifier (`recentContact` is not true, as when the amplifier is switched off); or it is running on built-in sample data because no serial port is configured. This is the default. |
| `LINK` | fault — **inhibits transmit** | The same situations, but only when the bridge was started with `--link-loss fault`. |
| `WNOSTATUS` | warning | The server has only what it can read off the amplifier's display (`provenance` is not `status-poll`). Power and the amplifier's alarm codes are not available in that case. |

While `WLINK` or `LINK` is raised, **every reading is a dash and the state is
blank**. The bridge never repeats old numbers as if they were current.

Alarm lines are sent together with the answer to `ST?`. On the first `ST?` of
every connection the bridge also sends `CLR` for each of its codes that is not
active, so that nothing is left over from an earlier connection.

**About losing the amplifier's status.** By default this is a warning only.
Switching the amplifier off, unplugging its USB cable or stopping Expert Amp
Server raises `WLINK`; the readings turn into dashes, the strip in HermitSDR
reads WARN, and HermitSDR goes on transmitting. This matches what HermitSDR
does itself when it cannot reach a device: it warns, and stops transmitting
only if you have turned on **Inhibit TX while this device is offline** for
that device. It also means you can operate with the amplifier switched off.

Bear in mind what the warning means: while it is showing, the bridge cannot
see the amplifier, so it cannot pass on an amplifier alarm either. If you
would rather HermitSDR refused to transmit whenever the amplifier's state is
unknown, start the bridge with `--link-loss fault`. The same situations then
raise `LINK`, a fault, and HermitSDR will not transmit until status returns.
With that setting, switch the device off with its toggle in HermitSDR's list
when you want to operate without the amplifier.

An alarm reported by the amplifier is a fault with either setting.

### Limits you should know about

- **Not yet tried on real equipment**, as stated at the top.
- **How fresh is "fresh"?** Expert Amp Server counts contact as recent for 5
  seconds, the bridge allows `--stale-after` (3 seconds) on top, and HermitSDR
  asks once a second. In the worst case a reading can be roughly 9 seconds old
  before it turns into a dash.
- **Freshness is per answer, not per reading.** Expert Amp Server combines two
  sources: answers to the amplifier's status request, and the amplifier's
  display. If the status answers were to stop while the display carried on,
  the server would go on reporting the last power, SWR, temperature and alarm
  figures and still say contact is recent. The bridge cannot detect that from
  `/api/v1/status`.
- **SPE-LAN-UNIT.** One operator measured an SPE-LAN-UNIT with firmware 1.0.3
  answering none of 100 status requests while display data arrived normally.
  Expert Amp Server talks to the amplifier's USB port, so a normal
  installation is not affected. If the server were reached through such a LAN
  unit and never received a status answer, it would serve display readings
  only; the bridge would then show state, band, SWR and temperature from the
  display, a dash for power, and the `WNOSTATUS` warning — and it could not
  see amplifier alarms at all. This case has not been tested.
- **Temperature unit.** The amplifier sends temperature as a bare number.
  Expert Amp Server converts it to Celsius according to its own
  `amplifierTemperatureUnit` setting. If that setting does not match the
  amplifier's menu, the temperature — and so the **Hot at** rule — will be
  wrong.
- **No transmit indication.** The status says whether the amplifier is
  transmitting; the protocol has nowhere to show it.
- **Fixture-tested from Expert Amp Server 0.4.8 source.** A real server
  and amplifier have not been tested. A later version may rename things. A field the bridge does not find becomes
  a dash, not a guess.
- **No password.** Neither Expert Amp Server nor the bridge asks who is
  connecting. Keep both on a trusted network. Default monitor mode exposes
  status;
  with `--allow-control`, any connected client can also request Operate or
  Standby. Neither mode authorizes or keys the radio.

### If it does not work

| What you see in HermitSDR | Likely cause |
| --- | --- |
| RECONNECTING, log says "unreachable" or "failed" | Wrong host or port; the bridge is not running; the bridge was started without `--listen 0.0.0.0`; a firewall; or macOS Local Network permission. |
| CONNECTED, all readings are dashes, alarm `WLINK` (or `LINK`) | The bridge cannot get the amplifier's status. The alarm text says why: the amplifier may simply be switched off. Otherwise open Expert Amp Server's web page to check that it sees the amplifier. |
| HermitSDR will not transmit and the strip reads INHIBIT | Read the reason in the strip. `AMPALARM` is the amplifier's own alarm; `LINK` appears only if the bridge was started with `--link-loss fault`; "hot" is the **Hot at** setting. An alarm left over from an earlier session is covered under "Known limits". |
| FAULTED, "Model mismatch" | Clear the **Expected model** field (or correct it) and press **Retry**. |
| Alarm `WNOSTATUS` | Expert Amp Server is not getting answers to its status requests; check its settings page. |
| Log says "device rejected: READONLY …" | Operate/Standby require explicit `--allow-control`; Tune request and Set band are always refused. |
| Log says "device rejected: BUSY too many clients" | More than four programs are connected to the bridge (`--max-clients`). |

The bridge prints what it is doing to its terminal: each connection, and each
change in its contact with Expert Amp Server.

### Writing your own bridge

The bridge is also meant as an example. The parts that matter are small: a
listening socket; for each line received, answer `ID?` with one `ID` line and
`ST?` with one `ST` line; send `-` for anything you do not know; raise `ALM`
with a code that does not start with `W` when transmitting should stop, and
`CLR` when it may resume; and after every new connection, send `CLR` for the
alarms that are not active. Running `--selftest` shows the exchanges the app
makes and checks every answer by the same rules the app uses.

## Feedback

Please report what you find — especially from real amplifiers — at
<https://github.com/dzcassell/HermitSDR-releases/issues>. The most useful
reports include the amplifier model and firmware, the Expert Amp Server
version, where the bridge runs, a copy of the Log box from HermitSDR, and the
bridge's terminal output. Nothing in this document asks you to transmit; the
panel, the readings and the alarms can all be checked while receiving.
