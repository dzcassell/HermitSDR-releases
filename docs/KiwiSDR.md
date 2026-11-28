# KiwiSDR / Web-888 network receiver

HermitSDR can receive from a **KiwiSDR** (or a Web-888 that speaks the same
control surface): a small networked HF receiver that exposes one ~12 kHz
channel over a WebSocket. The radio does not have to be on your desk.

This is the second part of "network receivers" (#472). rtl_tcp shipped
earlier; SpyServer and using a network receiver as the SUB source are not
built yet.

It is **receive-only**. No transmitter object exists for a KiwiSDR: ARM,
PTT, TUNE and drive stay closed.

> **How far this has been tested.** Every automated test runs against a
> loopback server inside HermitSDR's own test suite. The contributor
> connected the first build to one public KiwiSDR, once, on 2026-11-27:
> the WebSocket upgraded, the server sent `MSG` (including `sample_rate`)
> as a **binary** frame whose payload starts with `MSG`, then IQ `SND`
> frames about every 43 ms, with gaps up to roughly 120 ms and an
> occasional pair of frames in one instant; sequence numbers were
> continuous, and audio and the waterfall stuttered until playout was
> paced. Everything added since then (Keychain passwords, the idle limit,
> tuning rate limit, the messages for a kick or a time limit, the handling
> of odd sample rates and frames) has been run against the loopback server
> only, never against a real receiver.

## Connect

1. Open **Connect** and type the address into **Direct IP connection**:

   | You type | Meaning |
   | --- | --- |
   | `kiwi://192.168.1.50` | port 8073, the usual default |
   | `kiwi://kiwi.example:8074` | a name and another port |
   | `kiwi://[2001:db8::10]:8073` | an IPv6 address, in square brackets |
   | `kiwi://:secret@host` | password `secret`, saved in the Keychain (see below) |
   | `kiwisdr://host` / `web888://host` | the same scheme under another name |

2. Press Return. The address is remembered.

**Passwords.** Type a password once, as `kiwi://:password@host:port`. It is
stored in the macOS Keychain for that host and port, and the field then
shows `kiwi://host:port`: the password is not kept in the remembered
address, in settings files or anywhere on screen. Later, `kiwi://host:port`
alone uses the saved password. `kiwi://:@host:port` removes it. A password
containing a space, tab or line break is refused, because it cannot be sent
to the receiver in one piece.

HermitSDR connects to the SND WebSocket, asks for **IQ** mode (not the
server's own demodulator), and resamples the ~12 kHz channel to 48 kHz for
the normal receive chain, waterfall and decoders. The S-meter comes from
the SND header. The session opens on the frequency the dial shows.

Connecting takes at most ten seconds: four for the connection and six for
the receiver to answer. A receiver that refuses the connection is reported
at once.

## A shared receiver

Most KiwiSDRs belong to someone else, have only a few channels, and are
shared with whoever else is listening. HermitSDR treats every KiwiSDR that
way:

- **Tuning is paced.** However fast you turn the dial, the receiver is
  sent at most eight retunes a second, and always the frequency you
  stopped on.
- **Nothing scans it.** The Bookmark Scanner, Search Scan and Seek, the FM
  DX scan, the ALE channel scan and the band scout sweep refuse to start,
  and say why.
- **Nothing runs unattended.** Recording Schedule entries are skipped and
  Receive Watch will not arm while a KiwiSDR is the connected radio. You
  can still record by hand.
- **An idle session ends.** If nobody clicks, types, scrolls or tunes in
  HermitSDR for a set time, the session is ended with a message, so an app
  left running does not hold a channel indefinitely. The time is in
  **Settings ▸ Hardware ▸ KiwiSDR ▸ End when idle for**: 60 minutes unless
  you change it, from 10 minutes to 8 hours. Tuning from a logging program
  over CAT, the Control API or a remote client does not count as someone
  being there.
- HermitSDR identifies itself to the receiver as `HermitSDR`. It sends no
  callsign or location, has no directory of public receivers, and does not
  reconnect by itself.

## When the session ends

HermitSDR disconnects and shows the reason; it never sits "connected" to a
stream that has stopped. The messages:

| What happened | What you read |
| --- | --- |
| Every channel is taken | The KiwiSDR is busy (all *n* channels taken). |
| Wrong or missing password | The KiwiSDR password was refused. To save a new one, type the address once as kiwi://:password@host:port. |
| The owner's time limit ran out | The KiwiSDR ended the session (time limit). |
| The owner ended it | The KiwiSDR administrator ended the session. |
| The receiver says it is down | The KiwiSDR reports it is down. |
| The receiver points elsewhere | The KiwiSDR redirected this client. (HermitSDR does not follow it.) |
| The connection dropped | The connection to the KiwiSDR was lost: *reason*. |
| Samples stopped arriving | The KiwiSDR stopped sending samples. |
| It sent compressed audio | The KiwiSDR is sending compressed audio, which HermitSDR cannot use, so the session was ended. |
| It sent audio, not IQ | The KiwiSDR is sending its own demodulated audio instead of IQ samples, which HermitSDR cannot use, so the session was ended. |
| It named an impossible sample rate | The KiwiSDR reported a sample rate HermitSDR cannot use (*value*). It accepts 8 to 48 kHz, so the session was ended. |
| Nobody used the app | The KiwiSDR session was ended after 1 hour with nobody using HermitSDR, so the channel on the shared receiver is free for another listener. Connect again to go on listening. The time is set in Settings ▸ Hardware ▸ KiwiSDR. |

## What to expect

- **One channel, about 12 kHz wide.** This is not a wide IQ tap like
  rtl_tcp; the dial moves the Kiwi's channel, and HermitSDR demodulates
  inside it.
- **Sample rate** is fixed at 48 kHz on the Mac (×4 from the Kiwi's
  ~12 kHz). The server sends that audio in ~43 ms frames, sometimes two
  at once. HermitSDR holds about 200 ms and plays it out steadily, so
  those bursts do not overrun the receiver.
- **Tuning range** in the UI is 10 kHz–30 MHz; the server decides what is
  open.
- **Settings ▸ Hardware ▸ KiwiSDR** shows the receiver's address and
  version, the two sample rates, and how much was lost: frames dropped,
  samples discarded to catch up, and gaps in the receiver's frame numbers.

## What is not there

- The server's own waterfall (`W/F`) as a display source.
- A saved-receiver list (one address is remembered; passwords are kept in
  the Keychain per host and port).
- Auto-reconnect, a public Kiwi directory, or using a Kiwi as the SUB
  receiver beside a local radio.
- Compressed (ADPCM) audio, and `wss://` (TLS) connections.
- A warning before the idle limit ends a session.
- SpyServer.

## For developers

- `HermitSDR/Protocol/Kiwi/KiwiProtocol.swift`: address parsing, `SET` /
  `MSG` text, SND frame codec, rate plan, password rules, the idle limit.
- `HermitSDR/Protocol/Kiwi/KiwiLink.swift`: the `HPSDRLink`.
- `HermitSDR/Protocol/RadioProfile.swift`: `isSharedPublicReceiver` and
  `sharedReceiverRefusal`, the one place the "no scanners, nothing
  unattended" rule lives.
- `Tests/DSPTests/KiwiLoopbackServer.swift` and `KiwiTests.swift`.

The socket is Network.framework, not URLSession. KiwiSDR speaks plain
`ws://`, and App Transport Security refuses that on URLSession.

`connect` blocks its caller, like every radio link's, for at most the ten
seconds above. What the server sends is bounded before it is used: a
`sample_rate` outside 8–48 kHz refuses the session, one SND frame holds at
most 4,096 I/Q pairs, a `MSG` is read as at most 64 short tokens, and at
most 16 frames wait between the socket and the resampler.

## Sources

Where the protocol facts in this code came from, as the contributor
(rezolytics) stated it on pull request #544:

- The client was written in a Cursor session. The prompt did not include
  kiwiclient, the KiwiSDR server or OpenWebRX, and the recorded fetches
  did not open those repositories.
- John Seamons' forum post
  [About Python KiwiClient](https://forum.kiwisdr.com/index.php?p=/discussion/2269/about-python-kiwiclient-kiwi-api-question),
  a public forum thread, gave the connect sequence:
  `ws://host:8073/<id>/SND`, `SET auth`, `SET AR OK`, `SET mod`,
  `SET keepalive`, and `MSG` replies mixed with binary `SND`.
- Two web searches led to two third-party writeups that were then used as
  protocol notes: [OnAir's `docs/kiwisdr.md`](https://github.com/adswill/OnAir/blob/main/docs/kiwisdr.md)
  and the protocol section of
  [radiolab81/ESP32_KiwiSDR](https://github.com/radiolab81/ESP32_KiwiSDR).
  OnAir's page says its message tags, `SET` commands, `SND` layout and
  error names were read from kiwiclient, and that `inactivity_timeout` and
  `kick_by_admin` are assumptions. The ESP32 page says its protocol section
  is derived from kiwiclient's `kiwi/client.py`, `kiwi/wsclient.py` and
  `kiwirecorder.py`.
- The startup `SET` list, the fatal `MSG` keys, the flag bits, the S-meter
  formula `0.1 × raw − 127` and the two `SND` paths came from those two
  writeups, not from the forum post alone.
- The 10-byte GPS block came from HermitSDR's own `kiwi` WAV stamp, in
  `docs/IQImport.md`.
- One live public receiver, after the first build, was where the binary
  `MSG` frames, the flags `0x08` and `0x0d`, the 512-pair `SND` frames and
  the sample rate near 12 kHz were checked.

The KiwiSDR server is AGPL and kiwiclient is GPL. By the contributor's own
account the two writeups are derived from kiwiclient's source, so this part
of HermitSDR was not written from public documentation alone, which is the
project's usual rule. The project owner reviewed that and accepted the code
as it stands.

The fixes made after review (passwords, session-end messages, sample-rate
checks, tuning rate limit, idle limit, bounds) used no further protocol
source: they were written from the contributor's code, his statement above
and the review, and tested against the loopback server.
