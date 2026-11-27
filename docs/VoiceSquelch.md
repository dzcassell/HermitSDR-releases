# Voice squelch

On HF sideband a level squelch is close to useless: band noise and static
crashes sit at signal level, so a threshold that mutes the hiss also mutes
the station. The voice squelch listens for speech and ignores level. Leave it
on while monitoring a net or a calling frequency: the receiver is silent until
somebody talks.

It is **off by default** and it is receive only.

## Using it

Open the **DSP** popover and set **Squelch** to **Voice**. The choices are:

- **Off**: no squelch.
- **Level**: the squelch HermitSDR has always had. Audio opens when the signal
  beats the Level slider (S-meter scale).
- **Voice**: audio opens when speech is heard. The Level slider is not used.

Two sliders belong to Voice:

- **Voice thr** (0 to 100, default 50). How far the pitch of the audio has to
  swing before it counts as speech. Raise it if noise or interference opens
  the squelch; lower it if weak voices are missed. Below about 25 plain band
  noise starts to open it now and then.
- **Voice tail** (0.2 to 5 s, default 1 s). How long the audio stays open
  after the last sign of speech, so the pauses between words and sentences do
  not chop it.

Voice squelch works in **USB, LSB, AM and SAM**. In CW, the data modes, DSB
and FM the setting is kept but idle, and the popover says so; FM has its own
carrier and tone (CTCSS) squelch. While it is in force a small **VSQ** badge
shows beside the squelch control in the control bar and the console, with a
dot that shows what the gate is doing now: **green and filled while it is
open** (speech is being passed), **a dim ring while it is closed** (waiting
for speech). The badge's tooltip and VoiceOver say the same in words. The
dot follows the gate about ten times a second, so it stays lit through the
tail after the last word.

A Control API client can read the same two facts — the state keys
`voiceSquelchEnabled` and `voiceSquelchOpen` (true, false, or null while the
voice squelch is off or idle in the current mode) — and, from API revision 6,
the threshold and tail (`voiceSquelchThreshold`, `voiceSquelchTailSeconds`).
`setVoiceSquelch` switches it on or off and sets the two figures; see
[ControlAPI.md](ControlAPI.md). Switching it on that way is the Voice choice
of the popover: the level and noise squelch are switched off.

The spoken full status (**Speak full status**, and the Stream Deck / MIDI
key of that name) says "voice squelch closed" or "voice squelch open" while
the voice squelch is acting, so a silent speaker is explained; it says
nothing about it while the squelch is off or idle in the current mode.

A Stream Deck key or MIDI pad can carry **Voice squelch** (Toggles group):
it switches the Voice choice on and off, lights while it is on, and a Stream
Deck face reads OPEN, CLOSED or IDLE. See [StreamDeck.md](StreamDeck.md) and
[MIDIController.md](MIDIController.md).

The setting is one for the main receiver, saved with the receiver settings
and receive profiles the same way the level squelch is. The SUB receiver has
no squelch of its own yet and is not affected.

## What it does to decoders: nothing

Decoders, the passband mini-waterfall and the S-meter take
the audio ahead of the squelch. A closed voice squelch only silences the
speaker (and whatever follows the speaker audio). Receive Health reports
"Voice squelch is closed" when that is why you hear nothing.

## How it decides

It is the old syllabic squelch (W9MKV and W9YAN, 73 Magazine, August 1982,
after Motorola's constant-SINAD squelch), done in software with no outside
code. Every 10 ms it measures the dominant audio frequency, the number an
analog limiter and frequency-to-voltage converter would give. Noise holds
that number steady. A carrier or heterodyne holds it steady somewhere else.
Speech swings it by hundreds of hertz several times a second, because voiced
sounds, consonants and the gaps between them have very different spectra.
The squelch opens when the frequency goes there and back within half a
second, and each further swing restarts the tail.

Openings and closings use the receiver's normal 10 ms audio ramp, so they do
not click. The detector hears the audio a little ahead of the speaker path
(before noise reduction), which is why the first syllable is usually not
clipped. Expect roughly 150 to 250 ms from the start of a word to audio.

## What opens it and what does not

Measured on synthetic signals in the test suite at the default threshold:

| Signal | Voice squelch |
| --- | --- |
| Speech 6 dB above the noise | Opens in under 300 ms, holds through word gaps |
| Speech at 0 dB | Opens, a little later |
| Band noise | Stays closed |
| Static crashes over band noise | Stays closed |
| Steady carrier or heterodyne, also one that appears suddenly | Stays closed |
| One FT8 signal | Stays closed (its tones are only 44 Hz apart) |
| Hand-keyed CW in the voice passband | **Opens** |

Known limits, in the same family as other syllabic squelches:

- Anything whose pitch moves at speech rate opens it: CW in a sideband
  passband, music on AM, a carrier being swept through the passband.
- A steady heterodyne plus heavy static can open it: each crash drags the
  dominant frequency from the tone to the noise and back. Notch the tone, or
  raise the threshold.
- Wide or fast data signals may open it or not. A single FT8 signal does
  not, but a crowded FT8 channel opens it briefly now and then, when
  several signals start and stop together. On a three-minute off-air 40 m
  recording, 7.074 MHz was open 4 % of the time at the default threshold.
- On real band noise expect an occasional false opening. On two empty
  frequencies of that recording, three minutes each: two and seven
  openings at threshold 25, none and one at 40, none at 60. The default
  of 50 sits between the last two.
- Very weak speech, well under the noise, does not move the dominant
  frequency enough. Lower the threshold, or use Off.
- It needs the there-and-back swing, so a single short syllable ("yes") on
  an otherwise quiet frequency can be missed.

## Not included yet

Scanner "hold on voice", a squelch for the SUB receiver, and CAT control
(ZZSO / ZZSQ drive the level squelch only).
