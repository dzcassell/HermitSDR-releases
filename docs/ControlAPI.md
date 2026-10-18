# HermitSDR Control API — protocol version 1

Status: **milestone 1 (receive-only)** of issue #122. Transmit messages are
reserved in this document and refused by every server that implements it.

The Control API is the *thin-client profile* of HermitSDR. The shack Mac owns
the radio and does all DSP; it sends **demodulated receiver audio**, a
**decimated spectrum row stream** and **state**, and accepts **control
commands**. A client needs a TLS WebSocket, an audio device and a way to draw
a line graph. It needs no Swift, no Metal and no SDR code.

This document is the contract. It is language-neutral and complete: the
reference client `tools/control-api-client.py` (Python 3 standard library
only) was written from it, and the byte-level examples in it are pinned by
`Tests/DSPTests/ControlAPITests.swift`, so they cannot drift from the server.

How it differs from its neighbours:

| Surface | Port | Carries | Client must be |
| --- | --- | --- | --- |
| Hermit Remote (`docs/RemoteOperation.md`) | 4995 | relayed IQ, tune/rate/gain | a full HermitSDR |
| Hamlib NET rigctl | 4532 | frequency/mode/PTT text | a logger / WSJT-X |
| **Control API** (this document) | **4996** | audio + spectrum + state + control | anything with a WebSocket |

Conventions used below: **MUST / SHOULD / MAY** as in RFC 2119. "Server" is
HermitSDR; "client" is your program. All JSON is UTF-8. All binary integers
and floats are **little-endian** (note: Hermit Remote's TLV protocol is
big-endian — this one is not).

---

## 1. Transport

* **WebSocket (RFC 6455) over TLS 1.2 or later**, TCP port **4996** by default
  (operator-configurable). URL: `wss://<host>:4996/control/v1`.
* The client MUST offer the WebSocket subprotocol **`hermitsdr-control.v1`**
  (`Sec-WebSocket-Protocol`). The server selects it. The request path SHOULD
  be `/control/v1`; version 1 servers do not inspect the path.
* The server is **off by default** and listens **only while the operator has
  enabled it and a radio session is live** — or, since 2026-10-11 (#154), a
  file replay or Demo Mode is running (`radio.link` is then `"replay"` and
  `txCapable` is false: the chain demodulates and tuning works within the
  recorded span). When the session ends the listener closes and every
  client receives `bye` (`server_stopping`).
* Bonjour: the server advertises `_hermitsdr-ctl._tcp` with the radio's name.
* **Text frames** carry one JSON object each (control and state).
  **Binary frames** carry audio and spectrum (§ 6). Fragmented messages are
  allowed by WebSocket; the server sends every message unfragmented.
* WebSocket ping/pong: the server answers pings. Clients SHOULD also use the
  JSON `ping` (§ 5.4) to measure round-trip time.
* Limits: a text frame larger than **16 384 bytes** is ignored with an
  `oversize` error (not fatal). A WebSocket message larger than **65 536
  bytes** is a transport violation and the connection is closed (1009).
* At most **4** authenticated clients at a time; a fifth is denied `busy`.
* **Browser sessions** (`hello.platform` = `"browser"`, what the web console
  page sends — `docs/WebConsole.md`) are additionally bounded while the
  operator has the web console on: at most its session cap (1–4, default 3)
  are paired at once, a further one is denied `busy` ("the web console
  allows N browser sessions at a time"), and an optional time limit closes
  the session with `bye` (`kicked`, "web console session limit … reached —
  reconnect to continue"). This is resource policy keyed on a self-declared
  field, not authentication; every other rule in this document still applies.

### 1.1 Trust: certificate pinning

The server presents a **self-signed ECDSA P-256 certificate** — the same
identity Hermit Remote uses, so one shack has one fingerprint. It is not
issued by any CA and its names are meaningless; a client MUST NOT validate it
against a trust store. Instead:

1. The operator reads the **certificate fingerprint** in HermitSDR
   (Settings ▸ Control API): the SHA-256 of the certificate's DER encoding,
   shown as 32 upper-case hex bytes separated by colons.
2. On first contact the client computes the same hash of the leaf certificate
   the server presented and either compares it with a fingerprint the user
   typed in, or shows it and asks (trust on first use). It then stores it.
3. On every later connection the client MUST compare and MUST refuse to
   continue on a mismatch.

Pinning authenticates the *server*. The pairing code (next section)
authenticates the *client*, inside the tunnel.

### 1.2 The pairing code

The operator reads a **pairing code** in the same Settings section: a 160-bit
random token rendered as 32 RFC 4648 **base32** characters (alphabet
`A–Z2–7`, no padding) in hyphenated groups of four, for example
`AMFB-CGA7-EYWT-IO2C-JFIF-OXTF-NRZX-VAMI`. To recover the 20 token bytes:
upper-case the string, delete `-` and spaces, base32-decode.

The token never crosses the wire. The server keeps it in the macOS Keychain.
It is separate from Hermit Remote's pairing code, so rotating one does not
unpair the other. **Rotate code** in Settings invalidates it for everybody.

---

## 2. Message envelope

Every text frame is one JSON object with a string field **`t`** (the message
type). Client messages MAY carry an integer **`id`** (0 … 2^53); the server
echoes it in the matching `ack`, `error`, `pong`, `subscribed` or `state`
reply. Numbers may be sent as integers or as integral floats (`7074000` and
`7074000.0` are the same frequency). Unknown *fields* are ignored. Unknown
*message types* get an `unknown_message` error and are otherwise ignored —
they never end a session, so an old client survives a newer server and the
reverse.

Units are fixed: frequencies in **Hz**, levels in **dB** / **dBm**, volume
**0.0 … 1.0**, times in seconds unless a field name says otherwise.

---

## 3. Handshake

```
client                                   server
  | ---- hello ---------------------------> |
  | <--- challenge ------------------------ |   (or denied + close)
  | ---- auth ----------------------------> |
  | <--- welcome -------------------------- |   (or denied + close)
  | <--- state (full) --------------------- |
  | <--- meter … (10 Hz) ------------------ |
```

The handshake MUST finish within **10 seconds** or the server sends `denied`
(`handshake_timeout`) and closes. Before `welcome`, **any** protocol error is
terminal: the reply is `denied` and the socket closes.

### 3.1 `hello` (client → server)

| Field | Type | Meaning |
| --- | --- | --- |
| `t` | `"hello"` | |
| `apiVersion` | integer | The version the client speaks. MUST be within the server's `minApiVersion … apiVersion` (both currently `1`). |
| `clientId` | string, 1–64 chars of `A–Z a–z 0–9 . _ -` | A stable identifier the client generates once and keeps (a UUID is fine). The operator's per-client permissions and Revoke are keyed by it. |
| `name` | string, 1–64 | Human-readable name shown to the operator. |
| `platform` | string, ≤ 64, optional | e.g. `"windows"`, `"linux"`, `"browser"`. |
| `features` | array of strings, optional | What the client would like: any of `"control"`, `"audio"`, `"spectrum"`. Omitted or empty = everything the operator allows. Unknown names are ignored. |

### 3.2 `challenge` (server → client)

| Field | Type | Meaning |
| --- | --- | --- |
| `nonce` | string | base64 (standard alphabet, padded) of **32** random bytes. |
| `apiVersion`, `minApiVersion` | integer | The range this server speaks. |

### 3.3 `auth` (client → server)

`answer` = base64 of the 32-byte value

```
transcript = UTF8(hello text frame) ‖ 0x0A ‖ UTF8(challenge text frame)
answer     = HMAC-SHA256(key = token, message = nonce ‖ SHA256(transcript))
```

where both text frames are the **exact bytes that crossed the wire** (the
client must keep the hello string it sent and the challenge string it
received — do not re-serialize them). This is Hermit Remote's
challenge–response unchanged: the nonce defeats replay, and the transcript
hash binds the answer to this session's hello.

### 3.4 `welcome` (server → client)

| Field | Type | Meaning |
| --- | --- | --- |
| `apiVersion` | integer | Version in force for this session. |
| `apiRevision` | integer | Additions this server understands within the version (§ 8). Absent = 0. |
| `sessionId` | string | Opaque; for logs. |
| `server` | object | `app` (`"HermitSDR"`), `version` (e.g. `"2026.0921_001"`). |
| `radio` | object | Static profile, below. |
| `granted` | array of strings | The feature set **this** client holds: always `"state"` and `"meters"`, plus any of `"control"`, `"audio"`, `"spectrum"`. TX uses the separate session decision in §5.6. |
| `transmit` | object | `available: false` and a `reason`. |
| `limits` | object | `maxTextBytes`, `commandsPerSec`, `maxSpectrumBins`, `maxSpectrumRowsPerSec`, `meterHz`. |
| `audio` | object | `codecs` (`["pcm_s16le"]` — the negotiation field reserved for Opus later), `sampleRateHz` (12000), `channels` (1), `frameSamples` (240). |

`radio`:

| Field | Type | Meaning |
| --- | --- | --- |
| `name`, `model` | string | e.g. `"SquareSDR 2"`, `"Hermes-Lite 2"`. |
| `link` | string | `"P1"`, `"P2"`, `"remote"`, `"replay"` or `"none"`. |
| `sampleRateHz` | integer | The radio's IQ rate (informational). |
| `tuneMinHz`, `tuneMaxHz` | integer | RF range `tune` accepts. |
| `rfGainMinDb`, `rfGainMaxDb` | number | Range `setRFGain` accepts (−12…+48 on a Hermes-Lite 2, −31…0 on an ANAN, where it is attenuation). |
| `bands` | array of `{name, minHz, maxHz}` | Names `setBand` accepts. |
| `modes` | array of strings | Names `setMode` accepts, e.g. `USB LSB CW AM SAM FM NFM DSB DATA-U DATA-L` (the last two since revision 2). |
| `agcModes` | array of strings | `fast med slow off`. |
| `txCapable` | boolean | The *hardware* can transmit. Says nothing about this API. |
| `filters` | object, mode → `{presetsHz, minHz, maxHz, stepHz}` | Revision 1. Per mode: the widths the shack's own preset buttons offer (in their order — `setFilterPreset` indexes this array), and the range and quantum `setFilter` clamps to. |

### 3.5 `denied` (server → client, then close)

`{"t":"denied","code":"…","message":"…"}`. Codes: `unsupported_version`,
`auth_failed`, `cooldown`, `busy`, `revoked`, `auth_required`,
`handshake_timeout`, `bad_json`, `bad_message`, `bad_state`, `oversize`.

**Strikes:** three `auth_failed` from one IP address start a **60-second
cool-down** during which that address is denied `cooldown` before any
challenge is issued. Every failure is written to the operator's audit log.

**Closing.** Whenever the server ends a connection (`denied`, or `bye` in
§ 5.5) it sends the text frame, then a WebSocket close frame, and then
**waits for the client's close frame or end of stream** — up to five
seconds — before it closes the socket. A client therefore always receives
the reason; it should read it, answer the close (most WebSocket libraries
do so by themselves) and disconnect. Servers before revision 1 closed the
socket straight after their close frame; a client's answering close frame
could then meet a closed socket, the connection was reset, and the client's
own stack discarded the reason before the application read it. A client
that sees a reset or "socket is not connected" in place of a `denied` from
such a server should treat it as a refusal and not retry at once.

---

## 4. State

### 4.1 `state` (server → client)

```json
{"t":"state","seq":1,"full":true,"s":{ …every key… }}
{"t":"state","seq":2,"full":false,"s":{"rfHz":7076000,"mode":"CW"}}
```

The first `state` after `welcome` has `full: true` and every key. After that
the server sends `full: false` objects holding **only the keys whose values
changed** (a JSON `null` value means "now absent"). A client keeps one
dictionary and merges each `s` into it. `seq` increases by one per `state`
message on this connection. Deltas are latest-wins: if the client was slow,
several changes to one key arrive as one value. `getState` (§ 5.3) requests a
fresh full snapshot at any time.

State keys:

| Key | Type | Unit / range | Meaning |
| --- | --- | --- | --- |
| `connected` | bool | | A live radio session exists. |
| `radioName`, `radioModel`, `link` | string | | As in `welcome.radio`. |
| `sampleRateHz` | int | Hz | Radio IQ rate. |
| `rfHz` | int | Hz | **The dial**: operator-facing RF of VFO A, transverter-aware. |
| `ifHz` | int | Hz | What the radio hardware is tuned to (= `rfHz` without a transverter). |
| `transverter` | string \| null | | Active transverter profile name. |
| `mode` | string | | Demodulator mode, one of `radio.modes`. Revision 2 adds `DATA-U` / `DATA-L` (the data modes); a client that shows only the names it knows should fall back to the string. |
| `filterWidthHz` | int | Hz | Channel filter bandwidth. |
| `filterShiftHz` | int | Hz | Passband shift. |
| `filterPreset` | int \| null | index | Revision 1. Which entry of `radio.filters[mode].presetsHz` the width sits on; null between presets. |
| `band` | string \| null | | Band containing `rfHz`, or null. |
| `stepHz` | int | Hz | Tuning step `tuneStep` uses. |
| `agc` | string | `fast` `med` `slow` `off` | |
| `nr`, `nb`, `anf` | bool | | Noise reduction, noise blanker, automatic notch. |
| `rfGainDb` | number | dB, 0.1 | LNA gain / attenuation. |
| `rfGainMinDb`, `rfGainMaxDb` | number | dB | Current hardware range. |
| `attDb` | int | 0 10 20 30 | Digital step attenuator (positive = attenuation). |
| `volume` | number | 0…1, 0.01 | **Shack** speaker volume. It also scales the audio downlink, which is the final receiver mix. |
| `muted` | bool | | Shack mute (silences the downlink too). |
| `squelchEnabled` | bool | | |
| `squelchDbm` | number | dBm | |
| `ritEnabled` / `ritHz` | bool / int | Hz, ±9999 | Receive incremental tuning. |
| `xitEnabled` / `xitHz` | bool / int | Hz | Read-only in version 1. |
| `split` | bool | | Split armed. |
| `vfoBHz` | int | Hz | VFO B (RF). |
| `txArmed` | bool | | Read-only: the shack's ARM interlock. |
| `txKeyed` | bool | | Read-only: the shack is transmitting (its own operator). |
| `txInhibitReason` | string \| null | | Read-only: why the shack would refuse to key now. |

Clients MUST ignore keys they do not know; later servers add keys.

### 4.2 `meter` (server → client, 10 Hz)

```json
{"t":"meter","sMeterDbm":-87.3,"sUnits":"S7","overload":false,"txKeyed":false}
```

`sMeterDbm` is antenna-referenced dBm (0.1 dB). `sUnits` uses S9 = −73 dBm,
6 dB per unit, `S9+10` … above. `overload` = ADC overload. While the shack is
keyed the message adds `fwdW` (forward watts) and `swr` (either may be
`null`). Meters are **latest-wins**: at most one is in flight per client; a
slow client simply sees fewer. `subscribe` with `"meters": false` stops them.

---

## 5. Client messages after `welcome`

Every command is answered by **`ack`** `{"t":"ack","id":N}` once it has been
applied, or by **`error`**. Replies carry `id` only when the request did.
Commands need the `control` grant; without it they fail `forbidden`.

### 5.1 Commands

| `t` | Fields | Range | Effect |
| --- | --- | --- | --- |
| `tune` | `hz` number | `radio.tuneMinHz … tuneMaxHz` | Absolute RF dial frequency (VFO A). |
| `tuneStep` | `steps` integer | −1000…1000, ≠ 0 | Move by `steps × stepHz`. |
| `setBand` | `band` string | a `radio.bands[].name` | Jump to the band, restoring its memory. |
| `setMode` | `mode` string | a `radio.modes[]` (case-insensitive) | |
| `setFilter` | `widthHz` and/or `shiftHz` | 50…20000 / −5000…5000, clamped to the mode | |
| `setRFGain` | `db` number | `rfGainMinDb … rfGainMaxDb` | |
| `setAttenuation` | `db` integer | 0, 10, 20, 30 | |
| `setAGC` | `mode` string | `fast` `med` `slow` `off` | |
| `setDSP` | any of `nr`, `nb`, `anf` bool | | Toggles named; others untouched. |
| `setVolume` | `volume` number | 0…1 | |
| `setMute` | `muted` bool | | |
| `setSquelch` | `enabled` bool and/or `dbm` number | −160…0 | |
| `setRIT` | `enabled` bool and/or `hz` number | ±9999 | |
| `swapVFO` | — | | Exchange VFO A and B. |
| `setSplit` | `enabled` bool | | Arms split for the shack's transmitter. It keys nothing. |
| `setVFOB` | `hz` number | `radio.tuneMinHz … tuneMaxHz` | Revision 1. VFO B as RF, rounded to 10 Hz. Refused (`refused`) while the shack is transmitting or its dial is locked: with split armed, VFO B is the transmit frequency. |
| `setFilterPreset` | `index` integer | 0 … the mode's preset count − 1 | Revision 1. Sets the width to `radio.filters[mode].presetsHz[index]` for the current mode. The shift is untouched. |

**Coalescing.** Commands from one client are applied in order. The server
gathers commands for about 8 ms (and for as long as the previous batch is
still being applied) before touching the radio; within that window a run of
adjacent `tune` (or `tuneStep`, `setRFGain`, `setAttenuation`, `setVolume`,
`setFilter`, `setSquelch`, `setRIT`, `setVFOB`) commands collapses to the
newest (steps add up). A different command in between is a barrier, so "tune, change mode,
tune" keeps its meaning. A superseded
command is acknowledged immediately with `{"t":"ack","id":N,"coalesced":true}`
— it was not applied on its own, its successor was. A dial can therefore
send every detent without queueing.

**Rate limit.** 50 commands per second sustained, bursts of 100. Beyond that
each command fails `rate_limited` (not fatal). More than 400 frames of any
kind in one second closes the connection with `bye` (`flood`).

Tuning commands (`tune`, `tuneStep`, `setBand`, `setMode`, `swapVFO`,
`setVFOB`) answer `refused` while the shack is keyed, tuning, sending two
tones, still RF-hot after unkey, or between the frames of a native FT8/JS8
program — the next frame would otherwise key on the new frequency. An
ARMED but idle shack still accepts them (that is how a client drives an
FT8 session). The dial-lock and out-of-range refusals are unchanged.

### 5.2 `subscribe`

```json
{"t":"subscribe","id":3,"audio":true,"meters":true,
 "spectrum":{"enabled":true,"bins":512,"rowsPerSec":5}}
```

All fields optional; absent = unchanged. After `welcome`: meters **on**,
audio **off**, spectrum **off**. `bins` 16…1024 (default 512), `rowsPerSec`
1…10 (default 5). Needs the `audio` / `spectrum` grant, else `forbidden`.
Reply: `{"t":"subscribed","id":3,"audio":true,"meters":true,"spectrum":{"enabled":true,"bins":512,"rowsPerSec":5}}`.

### 5.3 `getState`

`{"t":"getState","id":4}` → a `state` message with `full: true` and the `id`.

### 5.4 `ping`

`{"t":"ping","ts":1234.5}` → `{"t":"pong","ts":1234.5}`. `ts` is echoed
verbatim (number or string ≤ 64 chars).

### 5.5 `bye`

Either side may send `{"t":"bye"}` before closing. The server's carries a
`message` and, when it is the server's decision, a `code`: `kicked`,
`revoked`, `server_stopping`, `slow_consumer`, `flood`.

### 5.6 Session-approved transmit — revision 3

TX remains off by default. Authenticate normally. The local operator must ARM
in TX Controls and choose **Allow TX this session** beside this live connection
in Settings → Control API. Approval is tied to the server's random session ID,
never the self-declared client ID or stored registry. Reconnection needs fresh
local approval. Editing permissions, Kick/Revoke, rotation, server stop and
disarm remove the grant or stop TX. A shared pairing code does not identify a
person; rotate it to lock out a code holder.

`welcome.transmit.available` remains false because no newly authenticated
session is approved. After an operator decision the server sends
`{"t":"txPermission","allowed":true,"leaseMs":450}` (or `allowed:false`).
Until approved, all TX names and microphone frames return `tx_disabled` and
produce no TX owner request. `arm` is always refused. Existing RX grants and
clients remain compatible; `apiVersion` stays 1, `apiRevision` is 3.

| Request | Fields and bounds |
| --- | --- |
| `micConfig` | `sampleRate:48000`, `channels:1`, `sampleCount:480`, `codec:"pcm16"`; send before using PTT in this session |
| `ptt` | `down:true` starts a momentary microphone over; `down:false` releases only this session's over |
| `txLease` | Renew this session's active over before its deadline; send at least every 200 ms |
| `txTune` | `seconds:0.1…10`; bounded TUNE, also requires lease renewal |
| `setDrive` | `percent:0…100`, limited to the current locally selected drive (remote clients can lower it) |
| `setTXProfile` | `name`: exact built-in or saved custom profile name, at most 80 UTF-8 bytes |
| `setMicGain` | `gain:0…4`, linear gain |

Normal `id`/`ack`/typed `error` behavior applies. Settings edits require an idle
transmitter. ARM, policy, calibration, profile, station, protection and ownership
checks remain authoritative. CW microphone keying is refused. A single over
is capped at 60 seconds. Requests older than 150 ms are refused rather than
turning a delayed command into a fresh lease. Deadlines use the receive
monotonic timestamp plus 450 ms, not the time the main actor processes them.
The radio protocol queue checks the lease every 20 ms and can drop MOX even
while the UI is stalled; it can never grant a key. Remote ARM is unavailable.

Microphone uplink: a **976-byte** binary frame with the RX audio header layout,
except byte 0 is `0x10`, codec byte 1 is 0, flags are 0, sample rate is 48000,
channels 1 and sample count 480. Payload: 480 signed int16 little-endian samples
(10 ms). Sequence increments modulo 2^32 for every frame. Start with at least
three frames (30 ms jitter buffer). A maximum of ten frames (100 ms) is queued;
up to three missing sequence numbers insert silence, and empty ticks produce
silence. Replay, overflow, malformed audio or starvation approaching 200 ms
fails closed. The server bounds incoming batches to sixteen items per peer
and one main-actor batch in flight; it never creates one Task per PCM frame.
Microphone audio does not renew the lease. Session loss/revocation/lease expiry
force-unkeys; ordinary PTT-up retains exclusive program ownership through the
actual coordinator tail. Generation tokens reject stale audio after teardown.

The implementation ships in 2026.1018_001; hardware TX acceptance remains pending.
See [NativeTransmit.md](NativeTransmit.md) for the review and dummy-load checks.

---

## 6. Binary frames (server → client)

Byte 0 is the frame type. All fields little-endian. Clients MUST ignore
frame types and header `format`/`codec` values they do not know.

### 6.1 RX audio — type `0x01`

The **final receiver mix** the shack operator hears (after AGC, squelch,
volume and mute), 12 kHz mono, in 20 ms frames (50 per second, 496 bytes).

| Offset | Size | Type | Field |
| ---: | ---: | --- | --- |
| 0 | 1 | u8 | type = `0x01` |
| 1 | 1 | u8 | codec = `0` (PCM signed 16-bit LE). Other values reserved. |
| 2 | 2 | u16 | flags. bit 0 = **discontinuity**: frames were dropped before this one. |
| 4 | 4 | u32 | `seq` — increments by one per frame, wraps at 2^32. A jump = lost audio. |
| 8 | 4 | u32 | sample rate in Hz (`12000`) |
| 12 | 2 | u16 | channels (`1`) |
| 14 | 2 | u16 | sample count N (`240`) |
| 16 | 2·N | i16[N] | samples |

Play them through a small jitter buffer (60–100 ms). On a `seq` gap insert
silence or simply continue. While the shack transmits, receiver audio is
muted by the radio and the frames carry silence (or the operator's TX
monitor, if they enabled it).

### 6.2 Spectrum row — type `0x02`

One row of the panadapter for the **span the shack operator is looking at**
(their zoom and pan), peak-decimated to the bin count the client asked for.

| Offset | Size | Type | Field |
| ---: | ---: | --- | --- |
| 0 | 1 | u8 | type = `0x02` |
| 1 | 1 | u8 | format = `0` (u8, dB-scaled). Other values reserved. |
| 2 | 2 | u16 | flags. bit 0 = discontinuity. |
| 4 | 4 | u32 | `seq` |
| 8 | 8 | f64 | `centerHz` — RF frequency of the centre of the row |
| 16 | 8 | f64 | `spanHz` — width of the row |
| 24 | 2 | u16 | bins N (may be **less** than requested when the visible span has fewer analyzer bins) |
| 26 | 2 | u16 | reserved, `0` |
| 28 | 4 | f32 | `minDb` |
| 32 | 4 | f32 | `stepDb` |
| 36 | 4 | f32 | `dbmOffset` |
| 40 | N | u8[N] | values |

Decoding: `dBFS = minDb + value × stepDb` (version 1 servers send −160 and
0.5, i.e. −160 … −32.5 dBFS, but read the header). Approximate antenna dBm =
`dBFS + dbmOffset`. **Bin 0 is the lowest frequency**; bin *k* is centred on
`centerHz − spanHz/2 + (k + 0.5) × spanHz / N`. Draw the row as a line for a
panadapter and push it into your own scrolling image for a waterfall. The
receiver's passband is `rfHz + filterShiftHz ± filterWidthHz/2` relative to
the mode's carrier convention; the dial marker is `rfHz`.

### 6.3 Backpressure

The server never lets a slow client delay the radio. Per client, at most 25
audio frames (0.5 s), 2 spectrum rows and 1 meter message are in flight; when
a lane is full new frames are **dropped** (the next one carries the
discontinuity flag). Control replies and state are never dropped — a client
that lets 256 of them (or 1 MiB) pile up is closed with `bye`
(`slow_consumer`).

---

## 7. Errors

`{"t":"error","id":N,"code":"…","message":"…"}`. After `welcome` errors are
**never fatal**. `message` is for humans and may change; switch on `code`.

| Code | Meaning |
| --- | --- |
| `bad_json` | Frame was not valid JSON (or nested deeper than 8 levels). |
| `bad_message` | A required field is missing or has the wrong type. |
| `unknown_message` | Unknown `t`. Ignore and carry on. |
| `oversize` | Text frame over 16 384 bytes. |
| `bad_state` | Message not valid now (e.g. `hello` twice). |
| `out_of_range` | A value is outside the documented or hardware range. |
| `forbidden` | The operator has not granted this client that feature. |
| `rate_limited` | Over 50 commands per second. |
| `unavailable` | No radio session, or this radio cannot do that. |
| `refused` | The shack refused; `message` says why (e.g. a transverter limit). |
| `busy` | Too many clients, or the command queue (64) is full. |
| `tx_disabled` | Reserved transmit message (§ 5.6). |
| `unsupported_binary` | The client sent a binary frame; unapproved sessions accept none; revision 3 permits approved type 0x10 microphone frames. |
| `unsupported_version`, `auth_required`, `auth_failed`, `cooldown`, `revoked`, `handshake_timeout` | Handshake (`denied`). |
| `kicked`, `server_stopping`, `slow_consumer`, `flood` | In `bye`. |

WebSocket close codes: **1000** after `bye` from either side, **1001** when
the server stops, **1008** after `denied` / `kicked` / `revoked` / `flood` /
`slow_consumer`, **1009** message too big.

---

## 8. Versioning and capability negotiation

* `apiVersion` is a single integer. A server announces the range it speaks in
  `challenge`; a client announces the one it speaks in `hello`. Out of range
  → `denied` `unsupported_version`.
* **Within a version the protocol only grows**: new state keys, new optional
  fields, new message types, new binary frame types, new `codec`/`format`
  values (sent only to clients that asked for them). Both sides ignore what
  they do not know. Nothing documented here changes meaning or is removed
  without a new `apiVersion`.
* **Each batch of additions raises `apiRevision`** — the minor number. It is
  announced in `welcome` and is information only: a server never refuses a
  client for it and a client never has to send one. A client that wants a
  newer message checks `welcome.apiRevision` first; sent to an older server
  the message is answered `unknown_message` and the session carries on.

  | `apiRevision` | First release | Added |
  | --- | --- | --- |
  | 0 | 2026.0921_001 | Everything not marked with a revision. `welcome` has no `apiRevision` field. |
  | 1 | 2026.0929_001 | `setVFOB`, `setFilterPreset`, `welcome.radio.filters`, state key `filterPreset`, `welcome.apiRevision`. The server waits for the client's close before it closes the socket (§ 3.5). |
  | 2 | unreleased | New `radio.modes` / `radio.filters` entries `DATA-U` and `DATA-L` (the data modes, #130), which `setMode` accepts and the `mode` state key reports. No new messages. |
* **Capabilities are per client.** `hello.features` asks; `welcome.granted`
  answers, after intersecting with what the operator allows that `clientId`.
  The operator can change a client's permissions while it is connected; the
  client then gets `forbidden` for what it lost (its streams stop) — it
  should re-read `granted` on its next connection.
* Future capability groups (decoders, logbook, cluster, Opus audio,
  transmit) will be new feature names; a version 1 client never sees them.

---

## 9. Operator controls (what the person at the shack can do)

Settings ▸ Control API: enable, port, pairing code (Copy / Rotate),
certificate fingerprint, the list of connected and known clients with
per-client **Control / Audio / Spectrum** permissions, **Kick** (close now),
**Revoke** (deny that `clientId` from now on) and **Forget**.

Revoke is keyed by the `clientId` the client chose; every client proves the
same pairing code. To lock out someone who *has the code*, rotate it.

Audit trail: unified log, subsystem `com.hermitsdr.app`, category
`controlapi-audit` — listener start/stop, every pairing success and failure
with the peer address, cool-downs, kicks, revocations, refused transmit
requests and slow-consumer/flood closes.

---

## 10. Worked example

Fixture (pinned by `ControlAPITests.testWorkedExampleHandshakeMatchesTheDocument`):

```
token bytes  03 0a 11 18 1f 26 2d 34 3b 42 49 50 57 5e 65 6c 73 7a 81 88
pairing code AMFB-CGA7-EYWT-IO2C-JFIF-OXTF-NRZX-VAMI
nonce bytes  a0 a1 a2 … bf      (byte i = 0xA0 XOR i, 32 bytes)
```

**1. Client → server, text** (133 bytes, sent exactly like this):

```
{"t":"hello","apiVersion":1,"clientId":"bench-01","name":"Bench laptop","platform":"linux","features":["control","audio","spectrum"]}
```

**2. Server → client, text:**

```
{"apiVersion":1,"minApiVersion":1,"nonce":"oKGio6SlpqeoqaqrrK2ur7CxsrO0tba3uLm6u7y9vr8=","t":"challenge"}
```

**3. Client computes**

```
transcript     = <line 1> ‖ 0x0A ‖ <line 2>
SHA256         = 5efa11129690fa7b6600eae45a135c594c749b2576e333039037c590e921c89e
HMAC-SHA256(token, nonce ‖ SHA256)
               → base64  rw+mfaEeZl7Gj6QfEVlFHGuhNZfMzDmYFoucQz6Rnqo=
```

and sends `{"t":"auth","answer":"rw+mfaEeZl7Gj6QfEVlFHGuhNZfMzDmYFoucQz6Rnqo="}`.

In Python:

```python
h = hashlib.sha256(hello.encode() + b"\n" + challenge.encode()).digest()
answer = base64.b64encode(hmac.new(token, nonce + h, hashlib.sha256).digest())
```

**4. Server → client:** `welcome` (abridged), then the full state:

```
{"apiVersion":1,"audio":{"channels":1,"codecs":["pcm_s16le"],"frameSamples":240,"sampleRateHz":12000},"granted":["state","meters","control","audio","spectrum"],"limits":{…},"radio":{"agcModes":["fast","med","slow","off"],"bands":[{"maxHz":7300000,"minHz":7000000,"name":"40m"},…],"link":"P1","model":"Hermes-Lite 2","name":"SquareSDR 2",…},"server":{"app":"HermitSDR","version":"2026.0921_001"},"sessionId":"…","t":"welcome","transmit":{"available":false,"reason":"…"}}
{"full":true,"s":{"agc":"med","anf":false,"attDb":0,"band":"40m","connected":true,"filterShiftHz":0,"filterWidthHz":2700,"ifHz":7074000,"mode":"USB","rfHz":7074000,…},"seq":1,"t":"state"}
```

**5. The client tunes, asks for audio, and the dial moves:**

```
→ {"t":"tune","hz":7076000,"id":1}
→ {"t":"subscribe","audio":true,"id":2}
← {"t":"ack","id":1}
← {"full":false,"s":{"ifHz":7076000,"rfHz":7076000},"seq":2,"t":"state"}
← {"audio":true,"id":2,"meters":true,"spectrum":{"bins":0,"enabled":false,"rowsPerSec":0},"t":"subscribed"}
← {"overload":false,"sMeterDbm":-87.3,"sUnits":"S7","t":"meter","txKeyed":false}
← binary, 496 bytes:
   01 00 00 00  00 00 00 00  e0 2e 00 00  01 00 f0 00  <240 × int16 LE>
   │  │  └flags └seq = 0     └12000       └1ch  └240 samples
   │  └codec 0 (PCM s16le)
   └type 0x01 (RX audio)
```

A five-sample audio frame with `seq` 0x01020304 and the discontinuity flag,
byte for byte (samples 0, 1, −1, 32767, −32768):

```
01 00 01 00 04 03 02 01 e0 2e 00 00 01 00 05 00 00 00 01 00 ff ff ff 7f 00 80
```

A spectrum frame header for 256 bins centred on 7 100 000 Hz, 384 000 Hz
wide, `seq` 9:

```
02 00 00 00  09 00 00 00  00 00 00 00 98 15 5b 41  00 00 00 00 00 70 17 41
00 01 00 00  00 00 20 c3  00 00 00 3f  00 00 c0 c0   <256 × u8>
└bins=256    └minDb −160  └stepDb 0.5  └dbmOffset −6
```

**6. A transmit attempt is refused and changes nothing:**

```
→ {"t":"ptt","down":true,"id":9}
← {"code":"tx_disabled","id":9,"message":"ptt: transmit control is reserved for milestone 2 and is not enabled on this server","t":"error"}
```

**7. Goodbye:** `→ {"t":"bye"}`, close 1000.

---

## 11. Reference client and conformance

* `tools/control-api-client.py` — Python 3, standard library only (its own
  minimal RFC 6455 client over `ssl`). Pairs, pins the fingerprint, prints
  state and meters, tunes, and writes N seconds of receiver audio to a WAV.
* `HermitSDR/Resources/WebConsole/console.html` — the in-app browser client
  (`docs/WebConsole.md`): a complete client of this protocol in plain
  JavaScript, including the pairing HMAC, served by the overlay HTTP server.
* `tools/control-api-smoke.sh` — builds the production server owner against a
  fake `ControlAPIPort` on loopback and drives it through the subprotocol
  gate, pairing, replay, malformed input, refused transmit, coalescing,
  audio/spectrum delivery, a stalled reader, a live permission edit, Kick,
  Revoke, forty refusals in a row that must each be read before the close
  (`CONTROL_API_SMOKE_REFUSALS` sets the count), Stop and the strike
  cool-down. It then runs the Python reference
  client against that server twice: over the plaintext loopback test mode,
  and over **real TLS** with a throwaway identity imported to memory
  (fingerprint pinned; a wrong fingerprint must be refused).
  `CONTROL_API_SANITIZER=thread|address` instruments the run.
* `Tests/DSPTests/ControlAPITests.swift` — the pure contract.

## 12. Known limits of milestone 1

* Receive only. No IQ (that is Hermit Remote), no decoder output, no logbook.
* VFO B can be set, swapped with A and armed for split, but the API tunes
  and hears VFO A only: there is no sub-receiver audio or control yet.
* PCM audio only (192 kbit/s). Opus is reserved in `audio.codecs`.
* The audio downlink is the shack's final speaker mix, so shack volume and
  mute affect it; a separate remote audio bus is future work.
* No cloud relay or accounts: LAN, the operator's VPN, or their own
  port-forward — the same trust model as Hermit Remote.
