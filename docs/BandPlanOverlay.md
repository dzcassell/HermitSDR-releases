# Band plan strip

A thin coloured strip above the panadapter's frequency scale shows what each
part of the band is used for. It is a display aid only. It never changes what
the transmitter may do: your licence and **Settings › TX operating policy**
decide that.

## What you see

| Colour | Meaning |
| --- | --- |
| Light blue | CW |
| Green | Data and narrow modes (RTTY, FT8, PSK …); in the US plan, the CW/data segments |
| Orange | Phone and "all modes" segments |
| Red-orange | Beacons (International Beacon Project and beacon segments) |
| Pink | Satellite |
| Yellow | Broadcast bands (long, medium and short wave) |
| Grey | Guard band |
| White (thin line above the strip) | Your own segments from the local file |

- **Band edges** are dashed vertical lines with the band name. While an edge
  is on screen, the part of the spectrum outside the amateur band has a faint
  grey wash.
- **Pointer readout.** Move the pointer over the panadapter: a line above the
  strip names the segment under it, its limits, the maximum bandwidth the plan
  gives, the US licence classes (US plan), the plan's note, and any local
  segment there. If TX policy enforcement is Warn or Inhibit, the line ends
  with the policy's verdict for that frequency.
- **Spot frequencies.** Small ticks mark FT8, FT4, WSPR, JS8, SSTV and QRP
  frequencies. Click a label to tune there in its usual mode (USB for the
  digital modes, LSB or USB for SSTV and QRP SSB, CW for QRP CW). When labels
  would overlap, only the first is shown; zoom in to see the rest.
- **VoiceOver** reads the segment under the VFO as "Band plan at the VFO".
  **Speak full status** adds "in the CW segment" (or data, phone, beacon,
  satellite, a broadcast band) after the frequency.

## Settings

Open the **Display** button (waveform with magnifying glass) in the control
bar. The strip is **on** by default.

- **Band plan strip** — the whole overlay on or off. The same switch is in
  the menu bar as **View › Band Plan Strip**, and a Control API client can
  read it (state key `bandPlanStrip`) and set it (`setBandPlanStrip`, see
  [ControlAPI.md](ControlAPI.md)); the other options below are in the
  popover only.
- **Plan** — `Auto`, `US`, `R1`, `R2`, `R3`. Auto follows the region in
  Settings › TX operating policy: an IARU region selects that region's plan;
  Unspecified or Custom selects the US licence-class table.
- **My class** (US plan) — `T`, `G`, `A` or `E` dims the segments that class
  may not use. Technician CW-only privileges on 80, 40 and 15 m stay lit; the
  pointer readout carries the "CW only" note.
- **Spot frequencies** and **Shortwave broadcast bands** — each on or off.

The Features window lists it as **Band Plan Strip**.

## Your own segments

Click **Edit…** in the Display popover. HermitSDR creates an example
`BandPlan.json` in its Application Support folder and shows it in Finder. Edit
it with any text editor:

```json
{
  "segments": [
    { "name": "Club net", "lowerKHz": 7185, "upperKHz": 7195,
      "kind": "phone", "note": "Sundays 14:00 UTC", "maxBandwidthHz": 2700 },
    { "name": "60 m channel 3", "lowerKHz": 5357.0, "upperKHz": 5359.8 }
  ],
  "spots": [
    { "label": "NET", "kHz": 3760, "mode": "LSB", "note": "County net" }
  ]
}
```

- A segment needs `name`, `lowerKHz` and `upperKHz`. `kind` is optional: `cw`,
  `data`, `phone`, `beacon`, `satellite`, `broadcast` or `local` (the default).
  `note` and `maxBandwidthHz` are optional.
- A spot needs `label` (up to 8 characters) and `kHz`. `mode` is optional:
  `USB` (default), `LSB`, `CW`, `AM`, `SAM`, `FM` or `NFM`.
- A saved change appears within two seconds. No restart is needed.
- If the file has a mistake, nothing from it is drawn and the Display popover
  shows the problem with its line number, for example
  `line 5: invalid range: "upperKHz" (7100) must be greater than "lowerKHz" (7200)`.
  Fix the line and save again.
- The file is plain JSON: no comments and no trailing commas. Frequencies are
  the RF you see on the dial.

## Where the bundled plans come from

| Plan | Source | Bands |
| --- | --- | --- |
| US | FCC Part 97 licence-class segments (the same table Ask The Crab uses) | 160 m – 70 cm |
| R1 | IARU Region 1 HF Band Plan, effective 16 October 2020 (plus 2 m and 70 cm) | 160 m – 10 m, 2 m, 70 cm, including 60 m |
| R2 | IARU Region 2 Band Plan, September 2020 (plus 2 m and 70 cm) | 160 m – 10 m, 2 m, 70 cm, including 60 m |
| R3 | IARU Region 3 Band Plan, R3-004 rev. 2, November 2024 (plus 2 m and 70 cm) | 160 m – 10 m, 2 m, 70 cm, including 60 m |
| Broadcast | ITU broadcasting allocations for the plan's region | Long wave (Region 1), medium wave, 120 m – 11 m |

The IARU plans are voluntary and national rules differ; check your own licence
conditions. Not bundled: the 2200 m and 630 m bands, 6 m for the IARU plans,
bands above 70 cm, and national plans other than the US.

Three places where the published Region 3 tables contradict themselves are
drawn as follows:

- 30 m: the table starts at 10110 kHz, but the allocation starts at 10100 kHz.
  The strip draws CW from 10100 kHz.
- 20 m: the rows 14070–14110 and 14100–14112 kHz overlap. The strip draws
  narrowband modes to 14099.5 kHz, the beacon guard 14099.5–14100.5 kHz, then
  the mixed segment to 14112 kHz.
- 10 m: the rows 29510–29590 and 29520–29620 kHz overlap. The strip draws one
  FM segment 29510–29700 kHz.

Two overlapping rows in the Region 1 and Region 2 80 m tables (the automatic
data station sub-segment at 3600 kHz) are drawn as their own sub-segment with
both notes.

Spot frequencies are the WSJT-X defaults (FT8, FT4, WSPR), the JS8Call
defaults (JS8) and the image and QRP centres of activity each plan lists (ARRL
conventions for the US plan).

## Notes

- A boundary between two segments belongs to the upper one. A band's top edge
  belongs to the band, the same rule the TX operating policy uses for its
  ranges, so the strip, Ask The Crab's band-plan answer and the policy agree
  on every frequency.
- With a transverter, the strip follows the RF on the dial. With an inverting
  transverter the strip is not drawn.
- The strip is laid out again only when you tune, zoom, resize or change a
  setting; it adds nothing to the per-frame drawing.
- The US plan shows no maximum bandwidth. Its table is the licence-class
  table Ask The Crab uses, which lists segments, modes and classes but no
  bandwidth, so the readout has nothing to quote; the IARU plans carry the
  figure from their published tables.
- Nothing is downloaded and no service is contacted.
