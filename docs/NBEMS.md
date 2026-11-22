# NBEMS Messages

**Decode ▸ NBEMS Messages** collects the emergency-net traffic that the
fldigi suite's **flmsg** (forms) and **flamp** (file transfers) put on the
air. It does not have a decoder of its own: it reads the text that the
Digital Modes, Contestia and RTTY decoders already print, picks the messages
out of it, checks them, and files them. It is receive only. Nothing in this
window can tune, arm or key a radio, and HermitSDR never opens or runs a file
it received.

## Using it

1. Tune the net frequency and start a decoder in **Decode ▸ Digital Modes**
   in the mode the net uses (MFSK32, Olivia 8/500, THOR 22 and PSK are the
   usual ones; MT63 is not available in HermitSDR).
2. Leave **Watch decoded text** ticked in the NBEMS Messages window (it is on
   by default). The window does not need to stay open.
3. When the end of a form or the last missing block of a file arrives, a row
   appears in the list.

It works the same way on a recording played back through the receiver or the
time machine; those rows are marked REPLAY. The separate **Decode a
Recording** window is not connected to it yet.

## The list

Each row shows the verdict, the file name, the kind of traffic, the UTC time,
the dial frequency and the decoder mode.

| Verdict | Meaning |
| --- | --- |
| PASS | flmsg: the checksum sent with the message matches the text received. flamp: every block passed its own check and the joined file has exactly the length the sender announced. |
| FAIL | The message arrived whole but its checksum does not match. At least one character is wrong. |
| NO CHECK | The checksum tag itself was not received. |
| INCOMPLETE | The message started but its end never arrived (fading, a mode change, or another message starting). |
| UNDECODABLE | The checks passed but the content could not be expanded (damaged base-64 or compression, or an encoding HermitSDR does not read). |

A net often repeats its traffic. A verified message that arrives again is
counted ("2 copies") rather than saved twice.

**Anything other than PASS is shown exactly as received, with a warning, and
is never laid out as a form.** A single wrong character can change a
quantity or a name without looking wrong. Ask for a repeat.

## Forms

For a verified flmsg message the detail pane shows the form's fields in the
order of the paper form, each with its label and the short tag flmsg uses
for it. **ICS-213**, **ARRL Radiogram** and **plain text** messages have
labelled layouts; the other flmsg forms (ICS-203 / 205 / 205A / 206 / 214 /
216 / 309, the HICS forms, IARU, MARS, CSV, blank) are recognised by their
file extension and shown as their tagged fields. **Data file** switches to
the text as it was sent. The stations a message passed through and the
stations that edited it are listed underneath.

## flamp file transfers

flamp sends a file as numbered blocks, each with its own check, and usually
sends the whole thing more than once. The lower left of the window lists
every transfer heard, by the four-character identifier flamp gives the file,
with a **block map**: one square per block, green once that block has been
received correctly. Blocks that fail their check are discarded; the same
block from a later pass fills the gap, and the list of missing block numbers
shrinks until the file is whole. Blocks are pooled across decoders, so a
repeat sent in another mode still counts.

When the last block arrives the file is put together, base-64 and LZMA
compression are undone if the sender used them, and it is saved. A file that
is itself an flmsg form is shown as one.

**Forget** drops a transfer and the blocks collected for it. Unfinished
transfers are kept only while the app is running.

HermitSDR does not send the "missing blocks" report or relay blocks; that
needs a transmitter and is outside this feature.

## Where things are saved

Verified messages and completed files go to **`~/Documents/HermitSDR NBEMS`**
(the Dev build uses its own folder). A form is saved as its flmsg data file,
with the name and extension the sender gave it (`.213`, `.m2s`, `.p2s` and so
on). Failed and incomplete copies go to a **`Failed`** subfolder as text,
named with the UTC time.

- **Save Copy…** writes the file somewhere else.
- **Export PDF…** makes a printable page of a verified form or text file.
- **Show in Finder** selects the saved file. Opening it is your decision.
- **Remove** and **Clear List** only change the list; the files stay.

## Safeguards

Everything here comes from an unknown station, so it is treated as untrusted:

- File names are reduced to plain letters, digits, spaces and `._-+()`. Any
  folder part is dropped, a leading dot is removed, and the name is cut to 80
  characters, so a received name cannot put a file anywhere else or hide it.
- Files are only ever created inside the NBEMS folder. An existing file is
  never overwritten (a second `msg.213` becomes `msg (2).213`), and a file is
  never written through a link. No file is given permission to execute.
- A wrap message is limited to 256 KB, a file to 4 MB after expansion, a
  transfer to 8,192 blocks, and sixteen transfers are tracked at once. The
  folder stops accepting new files at 5,000 files or 512 MB.
- Forms are drawn as plain text. Markup or scripts inside a field are shown
  as characters, not interpreted.

## Limits and what has been checked

- **Tested only with constructed messages and the examples printed in the
  fldigi suite's user manuals.** Nothing has yet been received off the air or
  exchanged with the real flmsg or flamp programs, and files exported from
  this window have not yet been opened in flmsg.
- The flamp line format, its check value and the compressed-file container
  are confirmed against the worked example in the FLAMP manual, which
  HermitSDR reassembles to the original text.
- The manuals do not say exactly which characters the **flmsg wrap checksum**
  covers, or whether lines go on the air ending in CR LF or a bare LF.
  HermitSDR accepts six plausible ranges, each read two ways, and records
  which one matched. That makes a damaged message very slightly more likely
  to pass (about 1 in 5,500 instead of 1 in 65,000) until a real message
  settles the rule.
- The PSK decoder drops bare line feeds from its text. If the sending
  program ends lines with a line feed alone, traffic sent over PSK will show
  as FAIL even when it was copied perfectly; MFSK, Olivia, THOR and DominoEX
  are not affected. Text outside plain ASCII is also unconfirmed.
- flamp has no separate whole-file checksum that HermitSDR can verify; a file
  is accepted on its per-block checks and its announced length.
- The Radiogram field labels and the ICS-213 "Incident" field are from memory
  rather than the manuals; an unrecognised field is always shown under its
  own tag, so nothing is hidden.
- flamp's base-128 and base-256 encodings are not read. Such a transfer is
  collected and reported but not saved.
- MT63, the most common NBEMS mode on VHF, is not decoded by HermitSDR.
- Contestia and RTTY cannot carry lower-case text, so real NBEMS traffic will
  not verify in those modes; they are watched for completeness.
