# Receive-path health

When a decoder prints nothing, HermitSDR now says why. A one-line verdict
sits under the **Digital Modes** window header, a short cue appears beside
the FT8/FT4 toggles in the decoder row when something actually stops
decoding, and **About › Copy System Information** exports the complete
findings list with the evidence behind it. The same diagnosis feeds all
three surfaces; nothing is changed automatically — every finding ends with
an action for you to take, and the app never retunes, re-arms, keys or
touches the system clock on its own.

## What it looks at

Once per second the app takes a snapshot of the receive path from state it
already tracks: the radio connection (and whether macOS has denied the
Local Network permission), IQ packets per second against the rate the
protocol should deliver, dropped-packet (sequence error) rate, the S-meter
level, ADC overload, the chosen output device, mute and volume, squelch,
the receive mode, the dial frequency, which decoder is switched on and
whether its gate lets it run, recent decodes, and the FT8 clock-drift
estimate (ourClock − UTC).

## The states

Findings are ordered by how completely they stop decoding, then by where
they sit in the signal path. The first one is the verdict you see.

| State | Severity | Meaning | Typical action |
| --- | --- | --- | --- |
| disconnected | blocking | No radio or recording is feeding the chain. With Local Network denied the text names the permission. | Connect a radio (or allow Local Network and reconnect); open a recording to replay. |
| noIQ | blocking | Connected, but no IQ packets arrive. | Check the LAN path and that no other client owns the radio; reconnect. |
| clockUnlocked | warning | IQ arrives, but at under half the expected rate or with ≥ 5 dropped packets/s, so decoder timing cannot lock. | Wired Ethernet, a lower sample rate, less competing traffic. |
| overloaded | warning | ADC overload — every decoder sees clipped samples. | Reduce LNA gain or add attenuation until OVF clears. |
| decoderPaused | warning | A decoder is on but its gate holds it (FT8/FT4 need USB or DATA-U; the CW decoder needs CW mode). | Switch mode; decoding resumes on the next slot. |
| wrongModeOrBand | warning / notice | Warning: a digital decoder with the receiver in AM/FM/DSB. Notice: FT8/FT4/WSPR/JS8 decoding more than 3 kHz from a conventional dial frequency. | Switch to USB/DATA-U; or tune to the named dial frequency. |
| clockOffset | warning / notice | The Mac's clock is ≥ 1.5 s (warning) or ≥ 0.75 s (notice) from the FT8 slot clock, with a confident estimate. | Turn on automatic time setting in System Settings › General › Date & Time; leave drift compensation on. |
| muted | notice | Mute, zero volume or a missing output device: *you* hear nothing. Decoders tap the audio before the speaker path and keep working. | Unmute, raise volume, or pick an available device. |
| squelched | notice | Squelch is closed. Same as muted: the decoder feed is upstream of the gate. | Lower the threshold or turn squelch off. |
| quietButHealthy | info | Everything upstream checks out and the decoder is running; there is simply nothing to decode (it says how long ago the last decode was). | Wait a few cycles, try another band, check the antenna if the noise floor looks flat. |
| healthy | info | Decoding normally (with the recent-decode count), or receiving normally with no decoder switched on. | — |

Blocking states suppress the downstream warnings (an overload or a paused
decoder is meaningless without a source); the operator-side notices (muted,
squelched) are still listed. When nothing blocks or impairs decoding, one
summary finding — `healthy` or `quietButHealthy` — closes the list.

## Where it appears

- **Digital Modes window**: the verdict line under the header, coloured by
  severity (red blocking, orange warning, yellow notice, green info); hover
  for the full sentences.
- **Decoder row** (FT8/FT4/SKIM/VISION toggles): a short cue such as
  `no IQ from radio` or `ADC overload` appears only when a decoder is on and
  the finding is at least a warning. The existing `paused · needs USB /
  DATA-U` cue keeps saying the mode case.
- **About › Copy System Information**: a `Receive path health:` block with
  every finding numbered as `[state/severity] explanation action`, followed
  by an `Evidence:` line (link state, Local Network, packets/s, sequence
  errors, signal level, overload, mode, dial, decoder state, recent decodes,
  clock estimate, mute/volume/output device, squelch). Paste it into a
  feedback report: the verdict in the UI and the one in the report come
  from the same snapshot.

## What is deliberately not here

- No automatic fixes. The actions are suggestions for you.
- No guided first-run setup flow (callsign/grid, radio, audio devices, log
  import). That is a separate, later slice of the same request.
- Decoder-internal reasons (sync failure, insufficient samples) stay where
  they are, in the **Decoder Activity** window's session status.

## For developers

`HermitSDR/App/ReceivePathDiagnosis.swift` is pure and package-tested
(`ReceivePathDiagnosisTests`: one fixture per state plus precedence and
export tests). `ReceiveHealthMonitor` publishes the findings and diffs the
cumulative sequence-error counter. `RadioState+ReceiveHealth.swift` builds
the snapshot from observable state in the 1 Hz stats tick and mirrors the
top finding into `DecoderCenter.receiveHealth` for the decoder windows,
which observe the center rather than the facade. `SupportInfo.receiveHealthSummary`
carries the export block. Nothing in the slice touches the transmit path.
