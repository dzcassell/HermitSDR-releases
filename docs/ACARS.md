# ACARS — aircraft messages on VHF, and one log shared with HFDL

*Decode ▸ Text & Messaging ▸ Aircraft Messages* and *Decode ▸ Digital Modes ▸ ACARS (VHF)*. Issue #476. Receive only.

ACARS is the text data link airliners use for position reports, weather
requests, gate and fuel messages and link housekeeping. On VHF it is sent in
short bursts on a handful of fixed channels between 129 and 137 MHz, as AM
carrying 2400 bit/s MSK tones. On HF the same messages travel inside HFDL.

HermitSDR does three things with it:

1. **One channel**, from the receiver's audio: *Digital Modes ▸ ACARS (VHF)*.
   Tune an ACARS channel in AM with an 8 kHz filter and turn on Decode.
2. **Every channel in the sampled span at once**, from the IQ: the
   *Decode all VHF channels in span* switch in the Aircraft Messages window.
   The receiver stays where it is tuned.
3. **One log**: the Aircraft Messages window lists whole messages from both of
   the above and from ACARS carried by HFDL (*Decode ▸ Text & Messaging ▸
   HFDL (Aircraft)*), each row tagged **VHF** or **HFDL**.

> **Not verified on a real signal.** The multi-channel receiver, the message
> reassembly and the shared log have decoded synthetic test signals only,
> inside HermitSDR's test suite. No off-air recording has been run through
> the multi-channel path, and no radio was connected while it was written.
> The single-channel decoder it is built on decoded all seven checksum-valid
> blocks of a public off-air test recording in 2026.1123_001. Please report
> what you see.

## When the VHF controls appear

The ACARS (VHF) entry in Digital Modes and the VHF strip of the Aircraft
Messages window are shown only while the **connected radio tunes the whole
129–137 MHz band** — for example an SDRplay RSPdx or an Airspy, or a radio
behind a non-inverting receive converter that reaches it.
With an HF-only radio, or none, the window still opens and still logs ACARS
carried by HFDL. Digital Modes also lists ACARS (VHF) while a recording made
inside the band is being replayed in the main window. *Decode a Recording* offers both ACARS decoders whatever is
connected, because the recording decides.

## Decoding every channel in the span

Switch on **Decode all VHF channels in span**. Every channel in the list that
lies inside the span the radio is sampling is decoded at the same time. The
status line says how many channels are hosted, how many blocks have been
decoded, how many frames were thrown away, and what it costs.

- **Channel list.** Frequencies in MHz, separated by spaces or commas; press
  Return or **Apply**. At most 32, each inside 118–137 MHz. **Region** replaces
  the list with a published set:

  | Region | Channels (MHz) |
  |---|---|
  | Worldwide (default) | 131.550, 130.025, 129.125, 131.725, 131.825 |
  | North America | 131.550, 130.025, 129.125, 130.425, 130.450, 131.125, 131.475, 136.700, 136.750, 136.800, 136.850 |
  | Europe | 131.725, 131.525, 131.825, 131.850, 136.750, 136.900, 136.925 |
  | Asia-Pacific | 131.550, 131.450 |

  Channel use changes; edit the list to what is active near you. The list is
  remembered across launches. The switch itself is off at every launch.
- **Which channels are hosted.** A channel must be at least 6 kHz inside the
  span and not in its outer 3 %, where the radio's own filter rolls off. At
  most 16 channels are decoded at once; if more fit, the ones nearest the
  centre are used. With a 1536 kHz span centred on 131.6 MHz the default list
  hosts 131.550, 131.725 and 131.825; a span of 3 MHz or more centred near
  130.5 MHz hosts all five.
- **Sample rates.** Any rate from 24 kHz to 12.5 MHz, whether or not it is a
  multiple of 12 kHz.

A frame is counted as **failed checksum** when it arrived complete and its
block check sequence did not match, and as **failed parity** when its header
was good and a later character failed odd parity. Either way nothing from it
is shown. A frame is counted once, however many of the decoder's five timing
phases saw it.

## The Aircraft Messages window

Each row is one whole message: time (UTC), link, registration, flight, label
and the first line of the text. Select a row to read it in full with its
mode, block ID, message number, acknowledgement, block count and — for the
multi-channel receiver — the channel level.

- **Search** looks in the registration, flight, label, the label's plain name
  and the text. It is plain text, not a pattern.
- **Filters**: link (all, VHF, HFDL), registration, flight (both "contains"),
  and label (the exact two characters).
- **Aircraft** tab: one row per aircraft with first heard, last heard,
  message count and the links it was heard on. Click a row to see its
  messages. An aircraft is known by its registration, or by its flight
  identifier when a message carried no registration.
- **Channels** tab: messages in the log per channel, and, while the
  multi-channel receiver is on, blocks / failed checksum / failed parity and
  level for each hosted channel.
- **Export ▸ CSV… / JSON…** saves the rows shown, filters applied, to a file
  you choose. Text came off the air, so a CSV cell that starts with `=`, `+`,
  `-` or `@` is prefixed with an apostrophe so a spreadsheet does not run it.

Everything is bounded: the newest 2,000 messages, 500 aircraft (the one
heard longest ago goes first) and 64 channels. **Clear** empties the log.
The log is kept in memory only; it is not written to disk unless you export.

### What the fields are

| Field | Meaning |
|---|---|
| Mode | One character. `2` is category A: the message is for any ground station (shown as **A**). Other characters address one ground station (category B, shown as **B** with the character). |
| Registration | The aircraft's registration, seven characters on the air with leading dots removed. |
| Acknowledges | The block ID of the block this one acknowledges, or NAK when it acknowledges nothing. |
| Label | Two characters saying what kind of message it is. |
| Block ID | One character. Digits `0`–`9` are downlinks (aircraft to ground); letters are uplinks. |
| Message number | Downlinks only: four characters at the start of the text, for example `M01A`. The last one counts the blocks of one message: A, B, C … |
| Flight | Downlinks only: the six characters after the message number, for example `UA0123`. |

The message number and flight are cut from the text only when the block is a
downlink and its first ten characters have that shape. Otherwise the text is
left whole.

### Multi-block messages

A block that ends with ETB says more blocks follow; ETX ends the message. A
message sent in several blocks is shown **once**, when its last block
arrives, with the texts joined.

- Blocks of one downlink share the first three characters of the message
  number and step the fourth; blocks of an uplink follow one another for the
  same aircraft and label.
- A block that is sent again (no acknowledgement reached the sender) is
  dropped and counted as a repeat. So is a whole single-block message heard
  again within 60 seconds.
- A message is marked **partial** when a block is missing: its first blocks
  were never heard, a block in the middle was lost, or the rest did not arrive
  within 5 minutes.
- Bounds: 64 unfinished messages at a time (the oldest is released as partial
  when one more starts), 16 blocks and 4,096 characters per message.

ACARS carried by HFDL arrives from the HFDL decoder one block per data unit
and is logged as it arrives; HFDL blocks are not joined to each other.

### Label names

The label column shows the two characters; the detail pane and the search
also know a plain name for about a hundred labels, for example `Q0` Link
test, `SQ` Ground station squitter, `H1` Message to or from an onboard
terminal, `5Z` Airline designated, `A9` ATIS report, `B9` Request for ATIS
report, `QA`–`QT` the OUT / OFF / ON / IN movement reports. A label that is
not in the table shows as its two characters. Airline-defined labels
(`80`–`89`, `5Z`, `H1` text) mean whatever that airline's software put in
them; HermitSDR does not interpret message text.

## Decode a Recording

*Decode ▸ Decode a Recording…* has two ACARS entries:

- **ACARS (VHF)** — one channel, from an AM IQ recording at the dial you give
  or from demodulated audio. Blocks are listed one by one.
- **ACARS, all channels** — an IQ recording only. Every channel of the list in
  the toolbar that lies inside the recorded span is decoded, messages are
  reassembled, and each is stamped with the recording's own UTC. A message
  still unfinished when the recording ends is listed as partial. A recording
  made behind an inverting converter is refused.

The replay command line knows it as mode `ACARS SKIM`.

## MQTT

With *Settings ▸ Station ▸ MQTT publishing* on and the Decodes topic ticked,
each message that enters the log is published once, whole:

| Topic | Source |
|---|---|
| `<base>/decode/acars` | ACARS heard on VHF. |
| `<base>/decode/hfdl_acars` | ACARS carried by HFDL. |

The payload is the usual decode object ([MQTT.md](MQTT.md)): `call` is the
registration, `text` the message text, `frequency_hz` the channel, and
`extra` has `link`, `label`, `label_name`, `flight`, `mode`, `block_id`,
`message_number`, `ack`, `direction` (`uplink` / `downlink`), `blocks` and
`complete`. A time-machine rewind or a file replay publishes nothing.

HermitSDR does not send aircraft messages to any aggregator or sharing
network. The MQTT feed goes only to the broker you entered.

## How the multi-channel receiver works, and what it costs

For each hosted channel the span is mixed to that channel and reduced to
12 kHz in two stages:

1. An integer decimation to between 48 and 96 kHz. Its filter has **eight
   taps for every sample it drops** — 32 taps at 192 kHz, 256 at 1536 kHz,
   1,024 at 6144 kHz — so the stopband is 80 dB down at every rate. The
   mixer is folded into the taps and the filter is computed once per output
   sample with vDSP.
2. A polyphase windowed-sinc resampler from that rate to 12 kHz, flat to
   ±4 kHz and 70 dB down by ±6.5 kHz.

The 12 kHz envelope, divided by its own 10 ms mean, goes to the same
2400 Bd detector the single-channel decoder uses: five timing phases, odd
parity on every character and the 16-bit block check.

Measured by the test suite on synthetic signals: channel gain within 0.5 dB
of the carrier from the centre to ±3.6 kHz, and more than 60 dB of rejection
12.5 kHz and 25 kHz away and at the first alias frequency, at 48, 192, 1536,
2000 and 6144 kHz. Three channels at once, each 10 dB above the noise in an
8 kHz channel (total carrier power over noise power) and 80 dB below full
scale, all decode at 192, 1536, 2000 and 6144 kHz.

**Processor time** on the worker thread, Mac mini (M4 Pro), one run of
`ACARSSkimmerTests.testReportsProcessingTimePerChannel` on one second of
noise, taken while other builds were loading the machine. The figures are a
share of one core:

| Span | Channels hosted | Optimized build, per channel | Optimized build, all channels | Debug build, per channel |
|---|---|---|---|---|
| 192 kHz | 3 | 0.12 % | 0.37 % | 1.6 % |
| 1536 kHz | 3 | 0.29 % | 0.86 % | 1.7 % |
| 6144 kHz | 5 | 1.16 % | 5.78 % | 2.3 – 5.1 % |

The released app is an optimized build. These are test-harness figures; the
load has not been measured inside the running app with a radio connected.

The cost grows with the span because every input sample is filtered once per
channel. None of it runs on the receive thread: the radio thread appends IQ
to a bounded queue (half a second) and returns. If the worker falls that far
behind, the backlog is dropped and counted, every channel receiver starts
again, and the status line shows the drops.

## Limits

- Conventional ("plain old") ACARS only. VDL Mode 2 and satellite ACARS are
  different links and are not decoded.
- No decoding of message content: no position parsing, no map pins from VHF
  ACARS, no CPDLC or ADS-C decoding.
- No signal-to-noise figure per message; the multi-channel receiver reports
  the channel level in dBFS.
- HFDL blocks are not reassembled across data units.
- Not verified on a real signal (see the note at the top).

## References

Written from public descriptions only. No source code of another ACARS
decoder was read.

- Frame layout, parity, mode characters, block identifiers, the general
  response label and channel lists:
  [WAVECOM decoder online help, "ACARS"](https://www.wavecom.ch/content/ext/DecoderOnlineHelp/worddocuments/acars.htm).
- Message fields and an example transmission:
  [Wikipedia, "ACARS"](https://en.wikipedia.org/wiki/ACARS).
- Label names and regional channel usage:
  the table published at [allsdr.blogspot.com](https://allsdr.blogspot.com),
  checked against the WAVECOM help (`SQ`, `:;`, the general response) and the
  published section titles of ARINC Specification 620 (`A0`, `A6`–`A9`).
  Entries marked unassigned or reserved there are left out.
- The standards themselves are ARINC Specifications 618 (air/ground
  protocol) and 620 (ground system and labels). They are sold by SAE ITC and
  were not available; where a public description was missing, the feature
  was left out rather than guessed.
