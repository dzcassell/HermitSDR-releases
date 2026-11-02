# JS8 Conversations

Decode › JS8 Conversations. The native JS8 decoder in the Digital Modes window
hears individual 15 s frames; this window turns them into the conversations a
JS8Call operator would see — directed and multi-frame messages assembled per
the JS8Call grammar, threads with timestamps, an inbox of traffic addressed to
your call or your groups with an unread badge, a heard roster and search. The
history survives relaunches. **Receive only and read-only:** there is no
compose field, nothing here keys the radio or queues a transmission, and the
MAGNET HF JS8 transmit path is untouched.

## Getting traffic into the window

1. Settings › Station: set your **Callsign** (the base call matches, so `WU1T/P`
   receives traffic for `WU1T`) and, optionally, **JS8 groups** — space or
   comma separated, `@MAGNET @MR08`. `@ALLCALL` is implicit; `@HB` carries
   heartbeats only.
2. Open Digital Modes, choose **JS8** and turn **Decode** on (the window's
   **Start JS8 decoding** button does both), tuned to a JS8 channel in USB or
   DATA-U — 7.078 MHz is the usual 40 m frequency, MAGNET HF watches 7.115 and
   14.115 MHz.
3. Every verified frame reaches the conversation layer as it is decoded,
   including frames replayed from the time machine or a recording (badged
   REPLAY; replayed traffic never inflates the roster).

## What the window shows

- **Inbox** — messages addressed to you: your call as the recipient, as the
  final hop of a relay (`A>B>WU1T …`), as a `MSG TO:` destination, or one of
  your groups; `@ALLCALL` traffic with text counts, heartbeats and CQs never
  do. Unread messages carry a dot and the segmented control shows the count.
  Opening a thread marks its messages read; **Mark all read** clears the badge.
- **Threads** — every conversation heard, newest activity first: you ↔ a
  station, two stations you overheard (`N0CALL ↔ K1ABC`), and one thread per
  group (`@MAGNET`, `@ALLCALL`, `@HB`). The right-hand pane shows the selected
  thread as bubbles: sender → recipient, a command badge (SNR?, GRID, ACK,
  RELAY, MSG TO:, …), the text with JS8Call's `♢` end glyph, the relay path
  and HEARING list when present, UTC time, frame count and span, S/N, dial and
  audio offset, grid. Messages addressed to you are outlined until read.
- **Roster** — every station heard with grid (from heartbeats, compound frames
  or a GRID reply), last heard, last S/N, heartbeat and message counts and
  where it was heard. Click a station to open its conversation.
- **Search** filters all three lists by callsign, text, grid or relay path.
- **Clear history** forgets everything (with confirmation); the header shows
  transmissions still in progress.

## Message status

| Badge | Meaning |
| --- | --- |
| *(none)* | First and last frame heard, no gap, checksum valid when the command carries one |
| CRC OK | A buffered command (`>`, MSG, MSG TO:, QUERY…, CMD) whose CRC-16/KERMIT checksum verified; the three checksum characters are stripped from the text |
| MISSING *n* | The last frame arrived but *n* slots inside the transmission produced no frame — part of the text is gone |
| MISSED START | The opening frame was not decoded; shown as a fragment |
| BAD CHECKSUM | A checksummed command whose text did not verify (a corrupt or missing fragment) |
| STALE | The station went quiet for a minute without an end-of-message frame; what arrived is shown as-is |
| REPLAY | Heard from the time machine or an offline recording decode |

## Protocol notes (sources)

The grammar follows JS8Call's own sources (GPL-3.0 — the tables are protocol
facts, the implementation here is HermitSDR's own):

- `varicode.cpp`: the `directed_cmds` table (`SNR?`=0, `>`=5, `MSG`=9,
  `MSG TO:`=10, `QUERY MSGS`=12, `ACK`=14, `GRID`=15, `INFO?`=16, `SNR`=25,
  `HEARTBEAT SNR`=29, plain text=31, …), `cqs`, `snr_cmds` {25, 29},
  `buffered_cmds` {5, 9, 10, 11, 12, 13, 15, 24} and `checksum_cmds` (16-bit
  on every buffered command except GRID). `JS8Modulator.Varicode` carries the
  same tables for the transmit side.
- `mainwindow.cpp`: frames are buffered per audio offset and a buffered command
  completes when a frame carries the last-frame bit; JS8Call force-completes a
  buffer 60 s after its last frame and drops it at 90 s. A checksummed
  command's text ends in a space plus three base-41 characters checked with
  `checksum16Valid`. A relay (`>`) builds its path by joining the sender and
  the leading `CALL>` hops; `MSG TO:` is stored (`STORE`) and acknowledged
  with `PATH ACK`. Replies are `FROM SNR -05`, `FROM GRID FN42`,
  `FROM HEARING A B C`, `FROM YES MSG ID n` / `FROM NO`.
- The `♢` end-of-transmission glyph is JS8Call's display default
  (`m_config.eot()`); nothing is transmitted for it — the last-frame bit is
  the end marker. Only normal-speed frames are decoded today; fast / turbo /
  slow submodes and JSC-compressed data frames are reported as such by the
  decoder and never guessed.

## Storage

`~/Library/Application Support/HermitSDR/js8/conversations.json` (the Debug
build and station instances use their own folders): the newest 2,000 messages,
512 roster entries and the lifetime total, written atomically two seconds after
a change and at quit. A torn or foreign file is ignored and a fresh store
starts; clearing writes an empty document.

## Not in this slice

Multi-speed (fast / turbo / slow) decoding, composing, replying, queued or
relayed transmit, automatic heartbeats and auto-replies are deliberately
absent. Any future transmit side stays behind ARM, the TX coordinator and the
owner's review (#324).
