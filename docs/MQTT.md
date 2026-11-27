# MQTT publishing — decodes, alerts and telemetry for dashboards and home automation

*Settings ▸ Station ▸ MQTT publishing.* Issue #416. **Off by default.** Nothing
connects until you switch it on and enter a broker address.

HermitSDR can publish what it decodes and measures to an MQTT broker you run
(Mosquitto, the broker inside Home Assistant, EMQX, …) as small JSON messages,
so Home Assistant, Node-RED, Grafana or a script of your own can react to
them: a light when a needed DX station shows up, a graph of PA temperature, a
log of every NAVTEX bulletin.

**It is publish-only.** HermitSDR never subscribes to anything and ignores
any message a broker sends it. Nothing that reaches the broker — and nobody
who can publish to it — can tune, arm or key the radio through this feature.
The `status` topic reports whether the transmitter is in use; it is a report,
not a control.

> **Not yet run against a real broker.** This client was written from the
> MQTT 3.1.1 specification and tested against a broker simulator inside
> HermitSDR's own test suite, on this Mac's loopback interface. It has **not**
> been connected to Mosquitto, to Home Assistant or to any other real broker,
> and the Home Assistant example below has not been loaded into Home
> Assistant. Please report what you see with yours.

## Setting it up

1. **Broker** — the address and port of your broker. Port 1883 is the usual
   plain port and 8883 the usual TLS port; switching **TLS** moves the port
   between the two when it was on the other default.
2. **Sign-in** — user name and password, if your broker asks for them. The
   password is stored in the macOS Keychain when you press **Save**; **Forget**
   deletes it. Leave the user name empty to connect anonymously.
3. **Topics** — the base topic (default `hermitsdr`), the client ID (generated
   once, for example `hermitsdr3fa9c21b`; change it only if you run two copies
   against one broker) and QoS 0 or 1.
4. Tick the topics you want, then switch the feature on.

The status line under the switches says what is happening:

| Status line | What it means |
|---|---|
| `connected to host:port` | The session is up. |
| `enter a broker address` | Switched on, but no broker named. Nothing is connecting. |
| `broker unreachable (Connection refused) — retry in 8 s` | No TCP connection: wrong address or port, broker not running, name not found, no route. |
| `TLS failure (…) — retry in 8 s` | The TCP connection opened but the TLS handshake failed: an untrusted or mismatched certificate, or TLS switched on for a plain-text port (1883 instead of 8883). |
| `broker rejected the user name or password (CONNACK 4) — retry in 8 s` | The broker answered and refused the sign-in. |
| `broker refused this client: not authorised (CONNACK 5) — retry in 8 s` | The sign-in is known but not allowed to connect (an ACL or a client-ID rule). |
| `broker refused the connection: … (CONNACK n)` | The other refusals the protocol defines: 1 protocol version, 2 client ID, 3 server unavailable. |
| `timed out waiting for CONNACK / PINGRESP / PUBACK` | Something answered TCP but is not behaving like a broker, or stopped answering. |

After any failure HermitSDR tries again by itself: after 2 s, then 4, 8, 16,
32 and then every 60 s, starting over at 2 s after the next successful
connection. Changing a setting tries again at once.

**TLS** uses the certificates macOS trusts. A broker with a self-signed
certificate works once you add its CA to the Keychain and mark it trusted;
there is no "skip verification" switch, and client certificates are not
supported.

## Topics

Every topic starts with the base topic. Each row has its own switch; a topic
that is switched off publishes nothing.

| Topic | Default | Retained | When it is published |
|---|---|---|---|
| `<base>/status` | on | yes | On connect and whenever a field changes, at most once a second. Also the last will. |
| `<base>/decode/<mode>` | on | no | One message per decode. |
| `<base>/spot/needed` | on | no | Each Needed DX board alert (the ones that raise a toast). |
| `<base>/qso/logged` | **off** | no | Each contact committed to the log. |
| `<base>/telemetry` | on | no | Every *N* seconds (default 10) while a radio is connected. |
| `<base>/spaceweather` | on | yes | On connect and when Kp, solar flux or the summary changes. |
| `<base>/alert` | on | no | Band-opening changes and receive-watch detections. |

`<mode>` is the mode name in lower case with spaces turned into underscores.
Modes that are published today:

| `<mode>` | Source |
|---|---|
| `ft8`, `ft4` | The FT8 / FT4 decode panel of the main receiver. |
| `js8`, `wspr`, `jt65`, `jt9`, `q65` | The Digital Modes window. |
| `selcal`, `dtmf`, `same` | Tone signalling in the Digital Modes window. |
| `dsc` | GMDSS DSC calls (including ones whose check character failed; see `extra.ecc`). |
| `navtex` | Each completed NAVTEX / SITOR-B message. |
| `aprs` | APRS packets heard on the air by the packet decoder. |
| `ale` | Each 2G-ALE address word (TIS, TWAS, TO, …). |
| `rtty` | The RTTY decoder's print, one message per line (see below). |
| `cw_skimmer` | The CW skimmer's rows (SKIM), one message per row as its text changes (see below). |
| `rds` | The broadcast-FM station's RDS name and text, when they change. |
| `acars` | Each whole ACARS message heard on VHF, from the Aircraft Messages log (multi-block messages are sent once, assembled). |
| `hfdl_acars` | Each ACARS message carried by HFDL, from the same log. |

Only off-air decodes are published: a time-machine rewind or a file replay
publishes nothing.

Three of these do not produce "a decode" the way FT8 does, so each is cut
into messages by a rule:

- **`rtty`** — RTTY prints a stream of characters. A message is one line:
  up to the next line break, or the first space after 72 characters (120 at
  most), or whatever has been printed when the decoder has been quiet for
  three seconds. `frequency_hz` is the mark tone on the air, `audio_hz` the
  mark tone in the passband; `extra` has `baud`, `shift_hz` and `reverse`.
  Retuning closes the line printed so far under the old frequency. Whatever
  the RTTY window prints is published, garble on a weak signal included; the
  rate cap bounds it.
- **`cw_skimmer`** — the skimmer re-reads every signal several times a
  second. A row is published when its text has changed and it was last
  published ten or more seconds ago, and once more when the signal goes if
  its last text was never sent; `text` is the row as the panel shows it, so
  consecutive messages for one row overlap. `extra` has `wpm`, `confidence`
  and `row` (the row's number, the same for every message about one signal).
  Rows the skimmer classed as RTTY, or has not classed yet, are not
  published.
- **`rds`** — published when a station's name (PS) or RadioText first
  arrives and when either changes, at most every five seconds for one
  station; a different station is published at once. `text` is the
  RadioText, or the name when no RadioText has arrived; `call` is the
  callsign derived from a North American PI code; `extra` has `pi` (four hex
  digits), `ps`, `pty`, `pty_name` and `tp`.

**Not published yet:** Super Skimmer monitor decodes from other bands, the
ALE whole-passband skimmer, and APRS packets that arrive from APRS-IS rather
than from the air. The radio's supply voltage is also not in `telemetry` yet.

### What each topic contains — and whose data it is

| Topic | Contains | Your own station data? |
|---|---|---|
| `status` | Whether a radio is connected and its name, the dial frequency (to the kilohertz), mode, band, and whether the transmitter is idle, armed or transmitting. HermitSDR's version. No callsign, no grid, no address. | **Yes** — it says what your station is doing right now. |
| `decode/<mode>` | What was heard on the air: the decoded text, the sender's callsign and grid when the mode carries them, frequency, signal-to-noise ratio. | No — other stations' transmissions, already public on the air. It does reveal which band you are listening to. |
| `spot/needed` | A station the Needed DX board flagged, with the reason it is needed. | Partly — the reason ("new DXCC entity", "new band") is derived from your log. |
| `qso/logged` | The contact's full ADIF record: the other station's call, time, band, mode, reports, and every other field you logged — names, comments, your own callsign and grid. | **Yes** — your logbook. Off by default for that reason. |
| `telemetry` | S-meter, noise floor, PA temperature, PA current, forward power, SWR. | **Yes** — your equipment's readings. |
| `spaceweather` | Planetary Kp, solar flux and the Space Weather window's summary lines. | No — public NOAA data. |
| `alert` | A band-opening headline, or a receive-watch detection with its frequency and level. | Partly — what your receiver noticed. |

All of it goes to one place: the broker you entered. HermitSDR does not send
it anywhere else, and no HermitSDR server is involved. What the broker does
with it — who may subscribe, whether it bridges to another broker or to the
internet — is your broker's configuration. Without TLS, everything, the user
name and password included, crosses your network unencrypted.

The password is kept in the macOS Keychain only. It is never written to
HermitSDR's settings or the `Settings.plist` mirror, never logged, and is not
part of the support information or the diagnostics report. While MQTT
publishing is on, **Copy System Information** (About window) includes one
MQTT line: the connection status with the broker's address and port, TLS or
plain TCP, whether a user name is set (not the name), the QoS and the
published / dropped / rate-limited counts.

## Payloads

Every payload is one JSON object in UTF-8. Every object has **`"v": 1`**, the
schema version. A new field may appear without the version changing; the
version goes up only when a field is removed or changes meaning. A field with
no trustworthy value is **left out** — never `null`, never a made-up zero —
so read fields defensively. Times are UTC, ISO 8601, whole seconds
(`2026-11-16T12:34:30Z`). Frequencies are in hertz at the antenna (a
transverter offset is already applied).

### `status` (retained)

```json
{"app":"HermitSDR","band":"20m","dial_hz":14074000,"mode":"USB",
 "radio":{"connected":true,"name":"Hermes-Lite 2"},
 "state":"online","time":"2026-11-16T12:34:30Z","tx":"receive",
 "v":1,"version":"2026.1115_001"}
```

| Field | Type | Meaning |
|---|---|---|
| `v` | integer | Schema version, 1. |
| `state` | string | `online`, or `offline` (below). |
| `app`, `version` | string | `HermitSDR` and its version. |
| `time` | string | When this status was built. |
| `radio.connected` | boolean | A radio is connected and streaming. |
| `radio.name` | string | The connected radio's name. Absent when none. |
| `dial_hz` | number | Dial frequency, rounded to 1 kHz. |
| `mode` | string | `USB`, `LSB`, `CW`, `AM`, … |
| `band` | string | `20m`, … Absent outside the amateur bands. |
| `tx` | string | `receive`, `armed` (the ARM interlock is on, not transmitting) or `transmitting` (keyed, TUNE or two-tone). Read-only. |

When HermitSDR quits, is switched off, or drops off the network, the retained
status becomes:

```json
{"app":"HermitSDR","state":"offline","v":1}
```

On a clean switch-off HermitSDR publishes this itself and then disconnects.
If it crashes, quits or loses the network, the broker publishes the same
message as the session's **last will** as soon as it notices the connection
is gone — at once when the connection is closed, otherwise when the 60 s
keep-alive runs out (brokers allow one and a half times that).

### `decode/<mode>`

```json
{"audio_hz":1500,"call":"K1ABC","dt_s":0.5,"frequency_hz":14075500,
 "grid":"FN42","mode":"FT8","snr_db":-12,"text":"CQ K1ABC FN42",
 "time":"2026-11-16T12:34:30Z","v":1}
```

| Field | Type | Meaning |
|---|---|---|
| `mode` | string | The mode as HermitSDR names it (`FT8`, `NAVTEX`, `ALE`). |
| `time` | string | When the signal was received (the slot start for FT8 / FT4 / WSPR). |
| `text` | string | The decoded text, at most 4,000 characters. |
| `call` | string | Sender's callsign, MMSI (DSC) or address (ALE, SELCAL code), when the mode has one. |
| `grid` | string | Maidenhead locator, when the message carried one. |
| `frequency_hz` | number | The signal's radio frequency. |
| `audio_hz` | number | Offset inside the audio passband (FT8-family and tone modes). |
| `snr_db` | number | Signal-to-noise ratio, when the decoder estimates one. |
| `dt_s` | number | Time offset against the slot (FT8 / FT4 / WSPR). |
| `extra` | object of strings | Mode-specific details, below. |

`extra` by mode — every value is a string:

| Mode | Keys |
|---|---|
| `wspr` | `power_dbm`, `drift_hz` |
| `dsc` | `ecc` (`ok` / `bad`), `to` (addressed MMSI), `channel_khz` |
| `aprs` | `destination`, `path`, `summary`, and `latitude` / `longitude` when the packet has a position. `text` is the raw packet. |
| `ale` | `type` (`TIS`, `TWAS`, `TO`, …), `sounding` (`true` / `false`), `golay_errors` |
| `navtex` | `header`, `subject`, `transmitter`, `serial`, `complete` (`true` / `false`), `errors` |
| `ais` | `mmsi` (nine digits), `type` (AIS message number), `channel` (`A` / `B`), and when the message or the station's row has them: `name`, `latitude`, `longitude`, `sog_kn`, `cog_deg`, `heading_deg`, `destination`. `call` is the ship's radio call sign once heard; `frequency_hz` is the AIS channel. See `docs/AIS.md`. |
| `acars`, `hfdl_acars` | `link` (`VHF` / `HFDL`), `label`, `label_name`, `flight`, `mode`, `block_id`, `message_number`, `ack`, `direction` (`uplink` / `downlink`), `blocks`, `complete` (`true` / `false`). `call` is the aircraft registration. See [ACARS.md](ACARS.md). |

### `spot/needed`

```json
{"band":"20m","call":"3Y0J","entity":"Bouvet","frequency_hz":14023000,
 "mode":"CW","reason":"New DXCC entity","score":87,"source":"Cluster",
 "spotter":"W1AW","time":"2026-11-16T12:34:30Z","v":1}
```

`source` is `Heard here`, `Cluster`, `Skimmer` or `PSKReporter`. `reason`,
`entity`, `snr_db` and `spotter` are present when known.

### `qso/logged`

```json
{"adif":{"BAND":"20m","CALL":"W1AW","FREQ":"14.074000","GRIDSQUARE":"FN31",
         "MODE":"FT8","QSO_DATE":"20261116","RST_RCVD":"+03","RST_SENT":"-05",
         "STATION_CALLSIGN":"WU1T","TIME_ON":"123430"},
 "time":"2026-11-16T12:34:30Z","v":1}
```

`adif` holds the contact exactly as the logbook would export it to an ADIF
file: field name → value, all strings. Which fields appear depends on what
was logged. Published once, when the contact is committed; later edits,
deletions, ADIF imports and backup restores are not published.

### `telemetry`

```json
{"forward_w":5,"noise_floor_dbfs":-104.2,"pa_current_a":1.8,
 "pa_temperature_c":41.3,"s_meter_dbm":-73,"swr":1.1,
 "time":"2026-11-16T12:34:30Z","v":1}
```

| Field | Present when |
|---|---|
| `s_meter_dbm` | A radio is connected. The same calibrated number as the S-meter. |
| `noise_floor_dbfs` | The receiver's noise estimator is running (Auto AGC threshold). In dB relative to full scale, not dBm. |
| `pa_temperature_c` | The radio has a PA temperature sensor (Hermes-Lite 2, Flex). |
| `pa_current_a` | The reading is above the level HermitSDR trusts (about 1 A on a Hermes-Lite 2), the same rule as the header cell. |
| `forward_w`, `swr` | While transmitting, with forward power above the meter floor. |

Nothing is published while no radio is connected.

### `spaceweather` (retained)

```json
{"kp":2.33,"sfi":148,"summary":["Latest 3-hourly planetary Kp is 2.33 (12:00 UTC)."],
 "time":"2026-11-16T12:34:30Z","v":1}
```

### `alert`

```json
{"band":"10m","kind":"band_opening","text":"10 m: open — 14 stations heard in 10 minutes",
 "time":"2026-11-16T12:34:30Z","v":1}
```

`kind` is `band_opening` (with `band`) or `receive_watch` (with
`frequency_hz` and `level_dbfs`).

## Rate cap and the send queue

- **Rate cap** — decodes, spots and alerts share a cap (default 20 a second,
  1–200). It is an average over ten seconds, so a full FT8 period of 50
  decodes still goes out at once; a flood beyond that is dropped and counted
  ("over the rate cap" in the status line). **Logged QSOs have an allowance
  of their own**, the same size, so a flood of decodes cannot cost a
  `qso/logged` message. `status`, `telemetry` and `spaceweather` are paced by
  their own timers instead.
- **Send queue** — up to 512 messages wait when the broker is slow or away.
  When the queue is full the **oldest** message is dropped and counted
  ("dropped"). A dashboard wants the newest reading; a stale one is not worth
  keeping the fresh one out.
- **The receiver never waits for the broker.** Publishing a message means
  adding it to that queue and returning; the network work happens on a queue
  of its own. Measured by the test suite on a Mac mini M4 Pro, 100,000
  messages per case, in five runs: with the broker refusing connections,
  queuing a message took 1.1–1.3 µs on average; with a broker that had
  accepted the session and then stopped reading, 1.1–1.3 µs. Building the
  JSON for a decode and queuing it took 11–12 µs. The slowest single call in
  any run was 7 ms, in runs where other builds were loading the machine (36 µs
  in the quietest run). A busy FT8 period of 50 decodes therefore costs under
  a millisecond, once, on the main thread after the decoder has finished —
  the decoder and the receive path are not touched. What has not been
  measured is decode latency inside the running app with a real broker
  switched off.
- **QoS 1** — the broker acknowledges each message; at most 16 wait for an
  acknowledgement at a time. A message that was sent but not acknowledged
  when the connection dropped is sent again after reconnecting, so a
  subscriber can see it twice.

## Home Assistant

Two ways; use one.

**Automatic (discovery).** Tick *Home Assistant discovery for the telemetry
sensors* (it needs the Telemetry topic). HermitSDR then publishes retained
sensor definitions under `homeassistant/sensor/<client ID>/…/config`, and
Home Assistant's MQTT integration adds a **HermitSDR** device with six
sensors: S-meter, noise floor, PA temperature, PA current, forward power and
SWR. They show as unavailable while the `status` topic says `offline`. To
remove them later, switch discovery off and delete the device in Home
Assistant (or clear the retained `…/config` topics on the broker).

**By hand.** In `configuration.yaml`:

```yaml
mqtt:
  sensor:
    - name: "HermitSDR PA temperature"
      unique_id: hermitsdr_pa_temperature
      state_topic: "hermitsdr/telemetry"
      value_template: >-
        {% if value_json.pa_temperature_c is defined %}{{ value_json.pa_temperature_c }}
        {% else %}{{ this.state }}{% endif %}
      unit_of_measurement: "°C"
      device_class: temperature
      availability_topic: "hermitsdr/status"
      availability_template: "{{ 'online' if value_json.state == 'online' else 'offline' }}"
    - name: "HermitSDR S-meter"
      unique_id: hermitsdr_s_meter
      state_topic: "hermitsdr/telemetry"
      value_template: "{{ value_json.s_meter_dbm }}"
      unit_of_measurement: "dBm"
      device_class: signal_strength
      availability_topic: "hermitsdr/status"
      availability_template: "{{ 'online' if value_json.state == 'online' else 'offline' }}"
  binary_sensor:
    - name: "HermitSDR transmitting"
      unique_id: hermitsdr_transmitting
      state_topic: "hermitsdr/status"
      value_template: "{{ 'ON' if value_json.tx == 'transmitting' else 'OFF' }}"
```

An automation that announces a needed DX station:

```yaml
automation:
  - alias: "Needed DX heard"
    trigger:
      - platform: mqtt
        topic: "hermitsdr/spot/needed"
    action:
      - service: notify.notify
        data:
          message: >-
            Needed: {{ trigger.payload_json.call }} on {{ trigger.payload_json.band }}
            {{ trigger.payload_json.mode }} — {{ trigger.payload_json.reason | default('') }}
```

To watch everything from a terminal on the broker's machine:
`mosquitto_sub -h localhost -t 'hermitsdr/#' -v`.

## What this does not do

- No subscribing, no commands, no remote tuning or keying. If that is ever
  added it will be a separate, separately switched feature.
- MQTT 3.1.1 only — not MQTT 5, no QoS 2, no MQTT over WebSockets.
- No client certificates and no way to skip certificate checks.
- One broker at a time.
- Not yet run against a real broker (see the note at the top).

## For developers

- `Integration/MQTT/MQTTProtocol.swift` — pure MQTT 3.1.1: packet encoders,
  the incremental parser, `MQTTSessionMachine` (CONNECT → CONNACK → PUBLISH /
  PUBACK / keep-alive, time injected), the drop-oldest queue, back-off and
  the rate limiter. No socket, no logging, no SUBSCRIBE encoder.
- `Integration/MQTT/MQTTPayloads.swift` — topics, JSON builders, Home
  Assistant discovery.
- `Integration/MQTT/MQTTClient.swift` — one `NWConnection` on the
  `hermitsdr.mqtt` serial queue; state in a typed lock; every delayed
  callback carries the epoch it was created under and is dropped when a
  start, stop or failure has moved it on.
- `Integration/MQTT/MQTTPublishCenter.swift` — settings (UserDefaults keys
  `mqtt…`), the Keychain account `mqtt.broker.password`, and the main-actor
  owner that turns events into messages.
- `App/RadioState+MQTT.swift` — the reads and the event hand-offs.
- `Tests/DSPTests/MQTTTests.swift` — byte-exact packets, the state machine,
  payload schemas, and the client and center against a loopback broker
  simulator (wrong password, TLS on a plain port, refused connection,
  stalled broker, inbound PUBLISH ignored, password never in settings or
  status text).
