# Waterfall Display (#455)

A second screen that shows the main waterfall and nothing else: no buttons,
no meters, no spectrum trace, no tuning. It is meant for a small field monitor
next to the radio (the request was a Feelworld FW279 / FW279S on HDMI) or a
television across the room (an Apple TV used as an AirPlay display). All
operating stays in the main HermitSDR console.

Receive display only. The surface takes no clicks, scrolling, gestures or
keys, so it cannot tune, change mode, arm or key. Opening, moving or closing
it changes nothing in the receiver, the audio, a recording or which window has
the keyboard.

## Where

**Radio ▸ Waterfall Display…** (Feature catalog `waterfall-display`, Radio
category) opens the setup window. The surface itself has no controls, so this
window is where it is opened, closed and configured.

## Setting it up

1. Connect the display. In macOS **System Settings ▸ Displays** it must be an
   extended (separate) display, not a mirror of the main one. For an Apple
   TV, choose it under the Displays **+** menu or Control Centre ▸ Screen
   Mirroring and pick **Use As Separate Display**.
2. Open **Radio ▸ Waterfall Display…**. Every connected screen is listed under
   the name macOS gives it, with its resolution and refresh rate.
3. Press **Show Here** on the screen you want. The waterfall fills that screen
   and HermitSDR remembers the display.
4. Optionally switch on **Open automatically when this display is connected**.
   It is off until you switch it on.

**Close Waterfall Display** at the top of the window closes the surface.
**Forget This Display** closes it and clears the remembered display.

## iPad Sidecar check

Demo Mode filled the iPad in landscape. With the iPad upright, the test
device showed the waterfall in the upper portion and a horizontal Pencil
offset. macOS still reported a 2148 × 1578 Sidecar surface. Landscape is
the verified orientation for that setup.

## What it shows

- The main receiver's waterfall, filling the screen edge to edge, above that
  screen's menu bar and Dock.
- The same part of the band the main panadapter shows: zoom, pan, the dB
  range and the palette follow the console. With a living-scene underlay
  (Aquarium, Night Garden and the others) selected in the console, the
  external surface uses the Classic palette; the scenes are not drawn there.
- An optional frequency scale along the top edge, in MHz (**Show the frequency
  scale**). There is no time scale.
- Its history starts when the surface opens and is as deep as the screen is
  tall. It is not a copy of the console's long history and cannot be
  scrolled.

When nothing is being received (no radio connected, Demo Mode off, no replay
running) the screen goes black with **No receiver running**, or **Waiting for
the receiver** when a radio is connected and no data has arrived for two
seconds. The old picture is dropped, not held, and drawing stops until data
returns.

## Which display, and when

HermitSDR never puts the surface on a display you did not choose.

- A display is remembered by what it reports to macOS: its display UUID, its
  vendor, model and serial numbers, and its name. Open **What this display
  reports** under any screen to see them.
- When displays change, the remembered one is looked for in this order, and
  the search stops at the first that fits:
  1. the same UUID (exact);
  2. the same vendor, model and non-zero serial number (exact for a display
     that has a serial; covers another port or adapter);
  3. the same vendor, model and name, when no serial is reported, and only if
     exactly one connected display fits;
  4. the same name alone, only with **Accept a display with the same name
     when nothing else matches** switched on, and only if exactly one fits.
- If two connected displays fit equally well, neither is used and the window
  says so.
- The built-in display and the main display (the one that carries the menu
  bar) are never used. If the remembered display becomes the main display
  because the other one was unplugged, the surface closes.
- The surface does not open on a screen that holds any HermitSDR window. It
  sits above everything on its screen and ignores the pointer, so a window
  under it could not be reached. The setup window names the windows to move;
  move them and press **Show Here**. (If a window ends up under the surface
  anyway, close the surface from **Radio ▸ Waterfall Display…** or disconnect
  the display.)

| Event | What happens |
| --- | --- |
| Launch, remembered display connected, auto-open on | Opens there. |
| Launch, auto-open off | Stays closed until you press Show Here. |
| Remembered display connected while running, auto-open on | Opens there. |
| Display unplugged or AirPlay ended | Closes. It does not move to another screen or onto the console. |
| Display returns, auto-open on | Opens there again. |
| Display returns, auto-open off | Stays closed. |
| Resolution, scaling or arrangement changed | The surface is resized and moved to fill the screen again. |
| Mac or displays sleep and wake, display still connected | Nothing; drawing pauses while the screen is off. |
| Sleep drops the display and it returns within 30 s of waking | Reopens, even with auto-open off. |
| You close it by hand, display still connected | Stays closed until the display is disconnected and reconnected, auto-open is switched on again, or the app is relaunched. |
| A second external display is connected or removed | Nothing. Only the remembered display is ever used. |

## The Feelworld FW279 / FW279S and an Apple TV

Nobody has yet measured what either reports to macOS, so HermitSDR contains
no Feelworld or Apple TV identifiers and recognises neither by model.

- A screen whose **name** contains "Feelworld" or "FW279" is labelled *name
  suggests Feelworld* in the list. That is a label only: it does not open
  anything, and an HDMI adapter may replace the name.
- macOS has no public interface that says "this screen is AirPlay". An Apple
  TV is treated like any other external display.
- Both are used the same way as every other display: choose it once with
  **Show Here**, and it is remembered by the identity it reports.

**Copy Display Report** copies the identity of every connected screen and the
modes it offers. If you have either device, the report from your Mac (with
the adapter you use) is what would allow exact recognition to be added, and
would show whether the FW279 and FW279S can be told apart.

The FW279 / FW279S panel is 1920 × 1200; the modes it offers over HDMI are
whatever the report lists. The surface fills whatever mode macOS is using and
does not change the display mode. Video reaches these monitors over HDMI
(directly or through a USB-C / Thunderbolt adapter). HermitSDR does not drive
SDI and does not send video over the monitor's USB port.

Over AirPlay expect a delay of a fraction of a second and visible video
compression. That is the AirPlay link, not the renderer.

## Cost

- No second radio connection, FFT, DSP chain or audio route. The main
  renderer hands each waterfall row it receives (about 30 a second) to a
  second renderer; the row is shared, not copied.
- The second renderer has its own Metal pipelines and its own history
  texture: 16 MB for a screen up to 1,024 pixels tall, 32 MB up to 2,048
  (the Feelworld's 1,200), 64 MB above that. It exists only while the
  surface is open.
- It draws at up to 30 frames a second, and only while its window is visible
  on a screen and there is live data. The main panadapter keeps its own frame
  rate.

GPU and CPU load with the surface open, and audio continuity, have not been
measured on hardware.

## Debug hook

Debug builds only: `HERMITSDR_WATERFALL_DISPLAY="size=960x600"` opens the same
surface three seconds after launch as an ordinary-level borderless window of
that size at the top left of the main screen, for a screenshot without a
second display. It remembers nothing and changes no setting. Combine it with
`HERMITSDR_DEMO=1` for a live picture; without a receiver it shows the idle
state.

## Tested and not tested

Display selection, identity matching and every lifecycle case above are
covered by package tests on simulated display lists
(`WaterfallDisplayPlanTests`). The window, the Metal surface and the real
display notifications are compiled in the app and have not been run against a
Feelworld monitor, an Apple TV or any second display.
