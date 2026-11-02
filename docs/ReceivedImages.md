# Received Images

**Decode ▸ Received Images** is the library of every picture the SSTV,
Weather Fax and MFSK decoders have saved. The decoders still write their
PNGs exactly where they always have — `~/Documents/HermitSDR Recordings`
with names such as `SSTV-MartinM1-20261102-143501.png`,
`WEFAX-20261102-150000.png` or `MFSK-MFSK32-20261102-151212.png` — and the
library keeps a small metadata index beside them so they can be browsed,
filtered, exported and copied automatically. Nothing in this window touches
a decoder, the receiver or the transmitter.

## What is recorded

Each completed picture (and each "Save corrected" / "Save processed"
re-render) becomes one row with:

| Field | Source |
| --- | --- |
| Mode | SSTV, Weather Fax or MFSK picture |
| Detail | SSTV mode (Martin M1 …), WEFAX profile (IOC 576 · 120 LPM …) or MFSK variant |
| Received | Wall-clock time of the save, shown local and UTC |
| Dial | Effective receive frequency (VFO + RIT) at the save |
| RX mode | Receiver demodulation mode (USB, LSB, …) |
| Radio | Connected radio profile model, when a radio was connected |
| Callsign | Empty until you type it in the detail pane (the decoders do not recover a sender's call) |
| Size | Pixel dimensions and file size |
| Corrected / replay | Slant-corrected re-render; decoded from the time machine or a recording |

The index lives at `~/Library/Application Support/HermitSDR/ReceivedImages/
index.json` (the Dev build uses its own folder), with cached thumbnails in a
`Thumbnails` folder beside it. It is written atomically a couple of seconds
after a change and again at quit. Deleting the index loses only the
metadata: the pictures stay, and the next launch indexes them again from
their filenames.

**First launch** after this feature arrives scans the recordings folder once
and indexes every `SSTV-*`, `WEFAX-*` and `MFSK-*` PNG it finds. Those rows
carry the mode and timestamp from the filename; frequency, receiver mode and
radio are unknown for them and show as "—". Rows whose file has since gone
are dropped at each launch.

## Browsing

- The **grid** shows thumbnails newest first. Click selects a picture;
  ⌘-click or ⇧-click extends the selection. Right-click a thumbnail for
  Reveal in Finder, Open and Move to Trash.
- **Search** matches every word you type against the mode, detail, callsign,
  radio, receiver mode, filename and frequency (MHz or Hz).
- **Filter** (one-level in-window menu): mode, date range (today, last 7 or
  30 days), sort (newest, oldest, by mode) and whether corrected re-renders
  are included. **Reset** clears all of it.
- The **detail pane** shows the full picture, the metadata table and a
  **Call** field: type the sending station's callsign and press Return (or
  Set). The call is saved into the index and fills the `{call}` export
  token.
- **Reveal in Finder** selects the PNG. **Delete** (also the Delete key)
  moves the selected files to the Trash after a confirmation and forgets
  their rows; the Trash can bring the file back, the metadata is gone.
- **Export…** copies the selected pictures into a folder you choose, named
  by the filename template below. Nothing is ever overwritten: a taken name
  gets `-2`, `-3`, … appended.

## Auto-export and the filename template

The bar at the bottom of the window sets an optional **export folder** and a
**filename template**. With *Auto-export new pictures* on, every newly
received picture is copied there as soon as the decoder saves it; the
original in the recordings folder is untouched, and the row shows where the
copy went. A failed copy (folder gone, disk full) is reported in the status
line and never disturbs the decoder.

The template is the filename without `.png`. Tokens expand in **UTC**:

| Token | Expands to |
| --- | --- |
| `{date}` | `yyyyMMdd` |
| `{time}` | `HHmmss` |
| `{mode}` | `SSTV`, `WEFAX` or `MFSK` |
| `{submode}` | Mode detail without spaces: `MartinM1`, `IOC576-120LPM`, `MFSK32` |
| `{freq}` | Dial in kHz with one decimal: `14230.0` |
| `{mhz}` | Dial in MHz with four decimals: `14.2300` |
| `{call}` | Sending callsign, or `NOCALL` |
| `{rxmode}` | Receiver mode: `USB`, `LSB`, … |
| `{radio}` | Radio model, or `RADIO` |
| `{name}` | The original auto-saved filename stem |

The default is `{date}-{time}-{mode}-{freq}`. Unknown tokens are left as
typed; path separators and control characters become `_`, and an empty
result falls back to the original name. The **Tokens** menu appends a token
to the field, and the preview beside it shows the expanded name for the
selected picture.

The folder and template are remembered with the receive profile of each
physical radio (`docs/RadioOperatingProfiles.md`), so a station with two
radios can export each one's pictures to its own folder; a radio connected
for the first time keeps the current choice.

## Not in this slice

FTP/FTPS upload of received pictures to a web gallery (the rest of #268) is
not implemented yet; the export folder is the hand-off point for any sync
tool in the meantime. Transmitted images are not part of the library.
