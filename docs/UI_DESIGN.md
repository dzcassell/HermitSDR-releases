# HermitSDR console UI design

Status: agreed direction plus explicitly proposed implementation details; no runtime change.
Recorded 2026-09-16 from the owner's “MacOS app examples” discussion and follow-up.
See [implementation roadmap](UI_IMPLEMENTATION_ROADMAP.md) for repository evidence and delivery gates.

## Decisions to preserve

- **Waterfall dominates.** Use a hybrid console: a permanent spectrum/waterfall center with independently collapsible left, right, and bottom controls. Collapsing panels returns their space to the visualization.
- **Dense, compact controls.** Flat framing, restrained corners, tight typography, aligned label/value/slider rows, small unit labels. Avoid oversized cards, switches, margins, and decorative chrome. Anti-VOX and Keyer controls should fit side by side where their labels remain legible.
- **Six palettes, Cold Cyan by default:** Arena Teal, Cold Cyan, Instrument Amber, Phosphor Green, Ion Blue, Ultraviolet.
- **LED Amber VFO:** digital-clock-style amber readout; the final three numeric digits are red. Separators do not count as digits. For `7.074.000`, `000` is red. This readout identity remains stable across palettes.
- **RX S-meter:** graduate toward red as signal strength rises, retaining calibrated values and existing measurement/ballistics behavior.
- **Ask the Crab:** a prominent, dedicated button with the text “Ask the Crab” and a modern AI Crab icon. It must remain accessible when all panels are collapsed.
- **Fixed TX safety colors:** active TX red; armed amber/yellow; fault/interlock fixed red or red-orange. Palette changes must not redefine those meanings. Use explicit state text as well as color; the red VFO digits and strong RX signals do not indicate transmission.

## Proposed layout and interaction contract

```text
Persistent header: connection | LED VFO / mode | RX meter | TX state | Ask the Crab | palette
Left RX panel   | spectrum (smaller) + waterfall (dominant) | Right TX panel
                |               central canvas            |
Bottom deck: Activity / Decoders / Log / Media workspace tabs
Persistent footer: connection/audio/performance status + panel restore controls
```

Panel allocation is a proposal, not a requirement to relocate every existing tool.
Preserve specialized windows and their native menu entries where embedding them would
crowd the waterfall. Reuse existing actions, feature visibility rules, shortcuts,
and underlying models.

- Left: frequently adjusted RX gain, AGC, noise reduction/blanker, squelch and filters.
- Right: TX source, drive, mic processing, Anti-VOX and Keyer, with existing arm/PTT controls and refusals.
- Bottom: tabbed activity/decoder/log/media workspace; show one selected workspace rather than several fixed-width analysis panes competing for the canvas.
- Header retains connection, frequency/mode, RX meter, TX state and Crab access. A safe stop/unkey action remains reachable when the TX panel is hidden, through the existing coordinator.
- Each panel has a visible collapse handle, menu action, keyboard access and persistent restore affordance. Remember visibility, selected tab and last expanded size; provide Reset Layout. Hidden panels must not implicitly stop decoders, change radio settings, arm or unkey the radio.
- Preserve the spectrum renderer's identity and data ownership while resizing. Collapsing UI must not clear waterfall/IQ history or recreate radio sessions.

Starting measurements for visual review, not frozen specifications: 24–28 pt rows,
4–6 pt internal gaps, 11–12 pt labels, monospaced numeric values, approximately
200–240 pt side panels and a 140–200 pt bottom deck. At a proposed 1440×900 pt
review size, target at least 60% of usable height for the spectrum/waterfall
region, with waterfall taking at least two thirds of that region. Validate a
smaller 1280×800 pt layout too; these are review sizes, not new minimum requirements.
If existing tools cannot fit, use tabs/overflow or retain their separate window.
Do not squeeze their minimum widths until they overlap the waterfall.

Compact controls still need clear focus, tooltips, accessible labels/values,
keyboard adjustment, disabled/refusal explanations, and direct numeric entry where
supported. Preserve current fine/coarse tuning modifiers and digit-scrub behavior.
Editing frequency or a numeric control must not accidentally trigger PTT/keyer shortcuts.

## Color and asset implementation

Extend the existing semantic skin system after checking the current source;
do not create a competing global theme owner. Separate interface palette from
waterfall color-map selection and optional visualization effects. A palette switch
must not unexpectedly change the user's waterfall mapping or DSP settings.

Initial colors from the earlier study are provisional and need contrast review:

| Palette | Canvas | Panel | Raised | Accent | Bright |
|---|---|---|---|---|---|
| Arena Teal | #101315 | #1A1E20 | #242A2D | #55C7B0 | #8BE4D2 |
| Cold Cyan (default) | #0D1115 | #151B20 | #202830 | #3BC6E4 | #79E7FF |
| Instrument Amber | #11110F | #1C1B17 | #29271F | #D9AA44 | #F3CC6B |
| Phosphor Green | #0D1210 | #151C19 | #202A25 | #4EC99B | #7AF0BD |
| Ion Blue | #0E1117 | #171B23 | #222936 | #5D91E8 | #8EB7FF |
| Ultraviolet | #100F15 | #1B1922 | #292532 | #A77BE8 | #C49CFF |

Define semantic backgrounds, borders, text, focus, hover/pressed/disabled, accent,
VFO amber/red, RX meter stops, and fixed safety tokens. Feed the same resolved
colors to SwiftUI and Metal. Provide a compact header selector and native
View → Appearance → Palette menu; switch immediately and persist selection.
Use Cold Cyan for fresh settings; preserve or explicitly migrate existing skin
preferences instead of silently overwriting them.

Choose the S-meter color stops only after inspecting the existing calibrated
scale; review noise-floor, S9 and strong above-S9 fixtures. Never change dB-to-S
conversion to achieve a visual gradient. Keep numeric/scale labels readable.

For the AI Crab, commission a small, clean crab silhouette with recognizable claws
and a subtle circuit/node motif; review at 16, 20 and 24 pt in normal, hover,
focused and disabled states. Keep the text label and VoiceOver name. The existing
repository logo is branding, not an approved replacement icon. The final icon,
LED glyph implementation/font and its license remain implementation deliverables.

## Visual acceptance

Review screenshots at both proposed window sizes, all six palettes, all eight
left/right/bottom visibility combinations, and key disconnected/RX/armed/TX/fault
states using fixtures. Confirm no clipping, hidden restore handles, unlabeled
safety states or layout movement when VFO digits change. Test keyboard-only and
VoiceOver operation. Approve a disconnected interactive prototype before moving
all production controls; approve an integrated build before changing the default UI.
