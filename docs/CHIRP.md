# CHIRP channel import and export

HermitSDR's Bookmarks exchange channel lists with [CHIRP](https://chirpmyradio.com)
through CHIRP's generic CSV — the file CHIRP's **File → Export** writes and
every CHIRP radio driver can import. Use it to bring a repeater list or a
handheld's memory export into Bookmarks, or to hand a set of bookmarks to
CHIRP for programming a radio. CHIRP does the cable programming; HermitSDR
never writes to a radio's memory and nothing in this exchange keys, tunes or
offsets a transmitter.

Open the star popover (Bookmarks, or **Radio → Bookmarks…**, ⌘⇧B):

- **Import CHIRP…** opens a `.csv`, parses it off the UI, and shows a preview
  sheet before anything is stored.
- **Export… → CHIRP CSV** writes the whole library or the displayed results
  (current search and sort order).

The existing JSON library remains the backup and restore format and the CSV
spreadsheet report is unchanged. Repeater-directory search (RepeaterBook and
similar) is not part of this: it needs a licensed data source and stays a
separate item.

## The file

Header, in this order (CHIRP `chirp_common.Memory.CSV_FORMAT`):

```
Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,RxDtcsCode,CrossMode,Mode,TStep,Skip,Power,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
```

Reference: `chirp/drivers/generic_csv.py` and `chirp/chirp_common.py` in the
CHIRP repository (https://github.com/kk7ds/chirp/blob/master/chirp/drivers/generic_csv.py,
read 2026-11-02). Import maps columns by header name, so a file with the
columns in another order or with extra columns still reads; a file without
`Location`, `Name` and `Frequency` is refused. Files are limited to 1 MiB and
2,048 channels, UTF-8 with or without a byte-order mark, LF or CRLF.

## Mapping

| CHIRP column | Bookmark | Notes |
| --- | --- | --- |
| Frequency (MHz) | Receive frequency | Parsed exactly, six decimals; blank or 0 skips the row |
| Duplex / Offset | Stored transmit offset and duplex word | `+` / `-` keep the signed offset; `split` stores TX − RX; `off` marks transmit inhibited. Stored only — never used to key or tune |
| Tone = `Tone`, rToneFreq | CTCSS encode on, tone | Snapped to the standard tone set (reported when snapped) |
| Tone = `TSQL`, cToneFreq | Encode on and tone squelch on, tone | |
| Tone = `Cross`, `->Tone` | Tone squelch only | |
| Tone = `Cross`, `Tone->` | Encode only | |
| Tone = `Cross`, `Tone->Tone` | Encode and squelch on the receive tone | Reported when the two tones differ (memories hold one tone) |
| `DTCS`, `DTCS-R`, `TSQL-R`, DCS cross modes | — | Reported; the channel imports without a tone |
| Mode | Receive mode | FM, NFM, AM, USB, LSB, CW direct; DIG/PKT → DATA-U; WFM → FM, NAM → AM (6 kHz), CWR/NCW/NCWR → CW, RTTY/FSK → DATA-U, RTTYR/FSKR → DATA-L; DV/DMR/P25/DN/NXDN → NFM (carrier only); blank → FM. Every approximation is reported |
| Comment | Notes | Up to 512 characters; line breaks become spaces |
| Name | Name | Blank names become the frequency; longer than 120 characters is truncated (reported) |
| Skip, Power, TStep, URCALL/RPT1CALL/RPT2CALL/DVCODE | — | Reported (Skip, Power, D-STAR); the tuning step is dropped silently. Scan lists choose memories explicitly, so Skip has no stored equivalent |

Tones apply to FM and NFM only; a tone on an AM or SSB row is reported and
dropped. Rows with a column count different from the header are skipped and
reported, as CHIRP itself does.

## Preview sheet

Before anything changes, the sheet shows: rows read and skipped, how many
channels will be added, replace a memory or be kept, exact duplicates (same
content as an existing memory) that are skipped, and the **lossy report** —
one line per row and field that cannot be represented, with the reason.

A **conflict** is an imported channel with the same frequency (to the hertz)
and the same name (ignoring case, accents and surrounding spaces) as an
existing memory. Each conflict offers **Keep mine** (default), **Replace**
(rewrite the memory's fields in place — same identifier and position, so scan
lists that refer to it keep working) or **Add both**; the *All:* buttons set
every conflict at once. The plan is applied against the library as it is at
the moment you press Import, so a memory saved meanwhile survives. Cancel or
closing the sheet changes nothing. Imported memories are never recalled.

## Export

Channels are numbered 0, 1, 2… in the order written (library order, or the
displayed order for a displayed-results export); the Location column is not
preserved from an earlier import. Formatting follows CHIRP's own writer:
frequency and offset as MHz with six decimals (`146.520000`), tones as
`88.5`-style floats, `023` / `NN` / `023` / `Tone->Tone` defaults in the DCS
and cross columns, `TStep` 5.00 (25.00 for AM between 108 and 137 MHz), blank
Skip and Power, Comment from the notes, blank D-STAR columns, CRLF line ends,
quotes only where a cell needs them.

| Bookmark | CHIRP |
| --- | --- |
| Encode on, squelch off | `Tone`, rToneFreq = tone |
| Encode on, squelch on | `TSQL`, cToneFreq = tone |
| Encode off, squelch on | `Cross` / `->Tone`, cToneFreq = tone |
| Duplex `+` / `-` | `Duplex` and the unsigned `Offset` |
| Duplex `split` | `split` with the absolute transmit frequency in Offset |
| Duplex `off` | `off` |
| SAM, DSB | `AM` (reported) |
| DATA-U, DATA-L | `DIG` (DATA-L reported: it reimports as DATA-U) |

Filter width and shift, LNA gain, attenuation and FM deviation have no CHIRP
column and are reported once per memory that carries them; sub-hertz
frequencies round to 1 Hz. The export status line names the count and the
fields that had no column. A CHIRP export reimported into HermitSDR
reproduces the exported memories exactly (test-pinned with a 20-row fixture
of 2 m / 70 cm repeaters, simplex, split, DCS, airband AM, DMR and D-STAR rows).
