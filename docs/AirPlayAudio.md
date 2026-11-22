# Receiver audio on AirPlay speakers

Station ▸ Audio & Streaming ▸ **Network Speakers** can send each receiver's
audio to an AirPlay speaker of its own (a HomePod, an Apple TV, an AirPlay 2
speaker or receiver) while the shack output carries on exactly as before.
The Mac's system sound output is not changed. Off by default. Source
issue 465.

**It is late, by several seconds.** The Mac buffers about two seconds of a
feed before it plays (measured: 2.0–2.2 s) and AirPlay 2 buffers about two
more by design, so expect something like four seconds between the shack
speakers and the AirPlay speaker. This is for listening in another room. It
is not for working a contact, and it is no use as a sidetone.

**Receive only.** A feed carries one receiver's demodulated audio and
nothing else. The CW sidetone, the transmit monitor, Media Deck pads and
everything bound for the transmitter are never sent, and each receiver is
silent on AirPlay while the radio transmits. Nothing in this feature can
key, arm or tune a radio.

**Not yet tried on a real AirPlay speaker.** See *What has been tested*.

## Using it

1. Open Station ▸ Audio & Streaming ▸ Network Speakers.
2. Under **Send receiver audio to AirPlay**, switch on **Main receiver**,
   **Sub-receiver** or both. A feed's AirPlay button, Start button, level
   and mute appear. Nothing is sent yet.
3. Click the feed's **AirPlay button** and choose the speaker. This is the
   macOS speaker list; it chooses a speaker for that feed alone.
4. Press **Start**. After a moment the status reads *Sending*.
5. Set the feed's level, or mute it. These belong to the feed: the shack
   volume and mute do not affect it, and it does not affect them.
6. Press **Stop**, or switch the feed off, when finished.

The main receiver and the sub-receiver can go to different speakers: each
feed has its own AirPlay button. The sub-receiver feed carries the
sub-receiver whether it is mixed into the shack speakers or routed to its
own device; with the sub-receiver off it carries silence.

| Control | Default | Meaning |
| --- | --- | --- |
| Main receiver / Sub-receiver switch | off | Creates that receiver's feed (its player and AirPlay button). Saved. |
| AirPlay button | none chosen | The macOS speaker picker for that feed. |
| Start / Stop | stopped | Sends, or stops sending. Never saved: every session starts stopped. |
| Level | 100 % | The feed's own level. Saved. |
| Mute | off | Silences the feed only. Saved. |

## Things to know

- **Choose the speaker before pressing Start.** macOS plays a feed that has
  no AirPlay speaker on the Mac's own output, where it arrives late as an
  echo of the shack audio. If you hear that echo, press Stop, choose the
  speaker, and press Start again. The same can happen if the speaker is
  switched off or leaves the network while a feed is sending: macOS decides
  where the feed goes then, and the app is not told.
- **The app cannot name the speaker you chose.** macOS keeps that to
  itself. The AirPlay button shows its active colour while AirPlay is in
  use; the list of speakers lower in the window is what Bonjour found on
  the network, not what is selected.
- **Sleep stops a feed.** After the Mac wakes, the status says so; choose
  the speaker again if needed and press Start. A relaunch is the same: the
  switch, level and mute come back, sending does not.
- **A speaker that keeps stalling is stopped.** A stalled feed is resumed,
  and a failed one restarted, up to five times in thirty seconds; after
  that it stops and says why. It does not retry on its own.
- **A feed is 12 kHz mono**, the receiver's communications audio. Wide AM,
  stereo sidebands, binaural CW and broadcast-FM stereo stay at the shack
  speakers; AirPlay gets the mono version of the same station.
- **Sonos** speakers are listed in the window but cannot be sent to from
  here. Use the Mac's Sound Output for those, which moves the shack audio.
- With every feed off, nothing in this feature runs: no player, no AirPlay
  button, no timer, and nothing looks for speakers. (The list of speakers
  in the same window uses Bonjour while that window is open, as before.)

## How it works

On macOS the public AirPlay speaker picker (`AVRoutePickerView`) routes an
`AVPlayer`, and only that: Apple's header for it reads "Media from an
AVPlayer, or from an AVSampleBufferAudioRenderer on iOS and tvOS, can be
routed to compatible AirPlay destinations", and its one macOS routing
property is `player`. An audio engine or sample-buffer renderer on macOS
can only be pointed at a Core Audio device, and an AirPlay speaker is not a
Core Audio device until macOS has connected to it as the system output
(checked on this Mac: five AirPlay receivers on the network, none in the
Core Audio device list).

So each feed is an `AVPlayer` of its own. What it plays is the receiver's
live audio presented as one long WAV file (12 kHz, mono, 16-bit) that grows
as the receiver produces it; the app answers the player's read requests
through `AVAssetResourceLoaderDelegate`. No private API, no AirPlay protocol
code, no aggregate device, and no second audio engine.

The receive DSP thread hands each block to the feed through a try-lock: if
the feed is busy or its two-second buffer is full the block is dropped and
counted (shown in the window as "blocks dropped"), and the receiver is
never made to wait. With the feed off the hand-over is that one try-lock.
The shack output (`AudioOutput`) is not touched by any of this: a feed
starting, stalling, restarting or stopping cannot restart it.

## What has been tested

Tested without an AirPlay speaker:

- Unit tests for the routing rule (only a receiver's own audio is
  admitted; sidetone, transmit monitor, transmit program and the final mix
  are refused), silence while keyed, the bounded hand-over, the stream
  file, and the feed's life cycle (start, stall, failure, restart limit,
  sleep, switching off).
- The player really plays the live stream on macOS 27.2: run silently
  (muted, zero level, no AirPlay route) it started, held a steady 2.0–2.2 s
  behind the receiver, carried on through a receiver that stopped
  producing audio, and stopped and restarted cleanly.

**Not tested, because no AirPlay speaker was used:**

- That the AirPlay button lists the speakers and that choosing one sends
  the feed there (this rests on Apple's documentation).
- The real delay over AirPlay.
- Two feeds on two different speakers at once.
- What macOS does when the speaker disappears, and after sleep.
- Whether level and mute act at the speaker promptly.
- Apple TV as opposed to HomePod.

## Operator check (HomePod or Apple TV)

1. With a radio or Demo Mode playing, switch on **Main receiver**, choose
   the HomePod with the AirPlay button, press Start. The HomePod plays the
   receiver; the shack speakers continue without a click or gap.
2. Clap-test the delay: tune across a strong signal and count the seconds
   between the shack speakers and the HomePod.
3. Move the feed's level and mute; the shack volume must not change.
   Move the shack volume and mute; the HomePod must not change.
4. Switch on **Sub-receiver** (with SUB on), choose a second speaker,
   press Start. Each speaker plays its own receiver.
5. Key the transmitter into a dummy load with the sidetone and the
   transmit monitor on: both AirPlay speakers go silent and neither plays
   the sidetone or your voice.
6. Unplug or power off the HomePod while sending. Note where the audio
   goes and what the status says; the shack audio must be unaffected.
7. Sleep and wake the Mac. The feed reads "Stopped when the Mac went to
   sleep" and the shack audio comes back as usual.
8. Press Start with no speaker chosen and confirm the late echo described
   above, then press Stop.
