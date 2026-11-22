# Command palette and text size

Two interface aids added together. Neither changes radio, decoder, network or
transmit behaviour.

## Command palette (⌘K)

**View › Command Palette…** or **⌘K** from any HermitSDR window opens a small
floating panel in the upper middle of the screen that holds the pointer. Type
a few letters, choose with **↑ ↓**, press **Return**. **Escape**, a choice, or
a click in any other window closes it.

What it finds:

| You type | You get |
| --- | --- |
| part of a tool's name or description (`dx`, `rdf`, `morse`, `ytb`) | every tool window in the Features catalog that is not hidden, opened exactly as its menu item opens it |
| a frequency, optionally with a mode (`27.385 lsb`, `14074`, `7200 khz usb`) | **Tune to …** as the first row |
| `mode` or a mode name | **Mode: USB**, **Mode: LSB**, … for the modes the current radio offers |
| `text` or `size` | **Text Size: Standard / Large / Extra Large** |
| `main`, `settings`, `recordings` | Show Main Window, Settings…, Show Recordings Folder |

With nothing typed, the last eight things you chose come first, then
everything else alphabetically.

### How a frequency is read

- With a unit (`hz`, `khz`, `mhz`, attached or after a space) the unit decides.
- Without one: a number below 1000 is MHz (`14`, `27.385`, `0.518`); a whole
  number below 1 000 000 is kHz (`14074`, `7200`), as is a larger number with
  a decimal point (`7200.5`); a whole number from 1 000 000 up is Hz.
- A comma is accepted as the decimal separator (`14,074` is 14.074 MHz).
- The mode word must be one the radio offers now. `27.385 wfm` on a radio
  without WFM is not offered as a tune; it falls through to an ordinary search.
- Offered range is 10 kHz to 6 GHz. The radio still decides: if it refuses
  (nothing connected, out of the radio's range), the palette stays open and
  says so.

Tuning behaves like **Radio › Set Frequency…**: it is a deliberate
destination, so the dial lock lets it through, the band's remembered settings
are restored, the display recentres, and a mode you typed is then applied to
the new band.

### What it will not do

Nothing in the palette arms, keys, tunes up or changes a transmitter setting.
Transmit tools appear because they are tool windows; choosing one opens the
window and nothing else, the same as its menu item.

Search and ranking are in `HermitSDR/App/CommandPalette.swift` and tested in
`Tests/DSPTests/CommandPaletteTests.swift` (including "every catalog feature
can be found by its title"). The window is
`HermitSDR/Views/CommandPaletteView.swift`.

## Text size

**Settings › Text size**, **View › Appearance › Text size**, or the palette.
Applies to every window immediately and is remembered.

| Setting | Type | Smallest type drawn |
| --- | --- | --- |
| Standard | as designed | as designed (7 pt exists) |
| Large | × 1.12 | 10 pt |
| Extra Large | × 1.25 | 11 pt |

Standard is exactly the layout the app has always had. At the larger sizes,
fixed label and value columns widen by the same factor so labels are not cut
off, the console's receiver and transmitter banks widen, and the Settings
pane widens. Row heights, window sizes, the frequency readout, meters, the
waterfall and its scales, and native menus do not change.

### Limits

- Windows do not grow on their own. A small tool window at Extra Large can
  wrap or truncate a line until you widen it.
- Checked by eye at all three sizes: main console, Settings, TX Controls, RDF
  Session, DX Cluster, Digital Modes, Features, the palette. The other tool
  windows compile against the same mechanism but were not each looked at.
- Text drawn by AppKit or a web view (menus, file panels, the manual's web
  content) follows the system, not this setting.

### How it works (for whoever edits the views next)

`HermitSDR/Views/ScaledFonts.swift` declares `Font.system(size:weight:design:)`
and the text styles (`.caption`, `.headline`, …) with the same signatures as
SwiftUI's. Inside the app the compiler prefers the app's declarations, so
existing and future `.font(.system(size: 10))` call sites scale without being
rewritten. At Standard each returns SwiftUI's own value
(`Font.SwiftUICore::system(…)` is how the file reaches the original).

The same file adds `frame(width:)` and `frame(minWidth:)` overloads that take
a number written in the source (`.frame(width: 62)`); a computed width still
resolves to SwiftUI's `frame` and is not scaled. Widths of 600 points or more
are left alone. For a named width that should follow the text, use
`.textScaled` (`.frame(width: labelWidth.textScaled)`).

Rules that follow from this:

- A font kept in a `static let` is built once and will not follow the
  setting. Use a computed `static var`.
- A smoke fixture that compiles `Views/Instrument.swift` must also compile
  `Views/ScaledFonts.swift` and `App/TextSize.swift`.
- The setting is `interface.textSize.v1` in the app's defaults
  (`standard`, `large`, `extraLarge`).

## Debug hooks

For a pointer-free interface check of a Debug build:

- `HERMITSDR_OPEN_WINDOWS="command-palette,settings,dxcluster"` opens the
  named scenes four seconds after the main window mounts.
- `HERMITSDR_PALETTE_QUERY="dx"` pre-fills the palette;
  `HERMITSDR_PALETTE_RUN=1` runs its first result two seconds later.
