# FT8 DXpedition mode: reading a Fox

Large DXpeditions run FT8 in *DXpedition mode*. The expedition is the **Fox**;
everyone calling it is a **Hound**. A Fox answers several callers at once: it
can send up to five FT8 signals side by side, 60 Hz apart, low in the passband
(300–900 Hz), in the even slots (:00 and :30 of each minute), and it packs two
callers into one frame:

    K1ABC RR73; W9XYZ <KH1/KH7Z> -12

That frame tells K1ABC that its contact is in the Fox's log and, in the same
breath, gives W9XYZ a signal report. The Fox's own callsign is sent only as a
short hash, shown in angle brackets.

HermitSDR's FT8 decoder reads these frames and the FT8 panel presents them.
**This is receive only.** HermitSDR does not work a Fox as a Hound: it does not
call above 1000 Hz, move to the Fox's frequency for the report, or run the
Hound sequence. It also does not decode **SuperFox** (see below).

## What you see

Turn on **FT8** in the control bar, tune to the expedition's announced FT8
frequency in USB or DATA-U, and open the FT8 panel.

- **One frame, two rows.** A two-caller frame is listed as the two messages it
  stands for, both marked **FOX**:

      K1ABC <KH1/KH7Z> RR73
      W9XYZ <KH1/KH7Z> -12

  Both rows carry the frame's time, S/N, DT and tone. Hovering either row
  shows the frame as it was sent. Clicking either tunes to the signal, as for
  any row.
- **Your callsign.** If one half names your callsign (Settings › Station),
  that row takes the red *My call* colour and its badge says which half it is:
  **FOX RR73 YOU** means the Fox confirms your contact; **FOX RPT YOU** means
  the Fox is sending you a report and expects `R` plus your report in reply.
  HermitSDR does not send that reply for you.
- **The Fox's other transmissions.** A CQ or a single report from a station
  HermitSDR has identified as a Fox is also marked **FOX**. A station is
  identified as a Fox when it sends two or more different messages in the same
  slot on tones at least 40 Hz apart, or when a two-caller frame's hash
  resolves to it (then only in the slots of the parity those frames arrived
  in).
- **Fox filter.** In the filter bar (funnel button), **Fox** shows only Fox
  rows. It combines with the other filters; **To me** plus **Fox** leaves only
  the Fox's messages to you. Filters hide rows; they change nothing else.
- **Row colours** are the usual ones. Both rows of a frame are the Fox's
  transmissions, so a Fox in an entity you have not logged shows as *New DXCC*.

## The Fox's callsign

The two-caller frame carries a 10-bit hash of the Fox's callsign, not the
callsign. HermitSDR shows `<...>` until it has decoded the Fox's full callsign
in another message in the same session (its CQ, for example), and
`<KH1/KH7Z>` afterwards.

A 10-bit hash has 1,024 values, so the callsign in brackets is a lookup among
stations heard in this session and can name the wrong one. For that reason:

- the callsign stays in angle brackets in the list;
- a two-caller frame is **not** uploaded to PSKReporter and is not entered in
  the *stations heard* ADIF export. The Fox's CQs and single reports carry its
  callsign in full and are reported and exported like any other decode.

Programs that receive HermitSDR's WSJT-X-style decode broadcast get the frame
as one line, exactly as sent.

## Limits

- **Receive only.** No Hound operation. The **Reply** button is offered on CQ
  rows as before and runs an ordinary FT8 exchange, which is not how a Fox
  expects to be called. Do not use it to work a Fox.
- **SuperFox is not decoded.** Since WSJT-X 2.7 many expeditions use SuperFox:
  one 1512 Hz wide constant-envelope signal carrying up to nine callers plus a
  signature. The published SuperFox User Guide describes how to operate it; it
  does not specify the waveform, the error-correcting code or the message
  layout, and signature checking is done by a server operated for the
  expeditions. HermitSDR's decoders are written from published specifications,
  not from other programs' source code, so SuperFox is not implemented. A
  SuperFox station is invisible to the FT8 list; you will see only the Hounds
  calling it.
- **FT8 only.** FT4 decoding is unchanged and ignores this frame type.
- **No Hound view.** There is no waterfall marking of the calling region and
  no warning when the dial is off the expedition's announced frequency.
- **Not yet confirmed off the air.** The frame layout was implemented from the
  published FT8 protocol description (Franke, Somerville and Taylor, *The FT4
  and FT8 Communication Protocols*, QEX July/August 2020) and the *FT8
  DXpedition Mode User Guide*, and tested on signals HermitSDR generated
  itself, including five simultaneous streams. No recording of a real
  DXpedition has been decoded yet and the output has not been compared with
  WSJT-X on the same audio.

## For developers

`ftx_message_decode_dxpedition` in `HermitSDR/DSP/FT8/message.c` unpacks the
frame (two 28-bit callsigns, the 10-bit hash, a 5-bit report counting even
decibels up from −30). `HermitSDR/Integration/FT8FoxDecode.swift` holds the
pure presentation policy; `FT8FoxDecodeTests` pins both. The sequencer's
parser returns nothing for a Fox frame, and a test pins that too.
