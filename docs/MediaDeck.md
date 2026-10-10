# Media Deck

Open **Station ▸ Audio & Streaming ▸ Media Deck** for a resizable, page-based soundboard. Decks are
saved automatically in Application Support and can also be exported as JSON
for backup or transfer.

In Edit mode the page grid, Rename, Delete, Export and Import tools occupy a
separate compact footer row so narrow windows keep their labels readable.
Toolbar toggles and empty-pad outlines follow the active palette immediately.

## Pad sources

| Source | What it does | Output |
| --- | --- | --- |
| Local file | Plays audio files or the audio track from a movie. Finder drops and the file picker create a security-scoped reference so the deck can reopen the file later. | Monitor, stream, or both, according to the pad route. |
| YouTube | Plays the clip in the authorized embedded YouTube player, in a panel under the pad grid (one player serves every YouTube pad; pressing another YouTube pad swaps the clip). Sign in with a Google account from the pad editor or the panel; a YouTube Premium account plays ad-free. Watch, share, Shorts, Live, embed, and privacy-enhanced URLs are normalized; pad trim values become start/end times. | The deck mix: the player's audio is tapped from WebKit's media process into the pad graph, so gain, FX, output device, "Send to stream mix" and the meter apply like a local pad and a wav pad can play at the same time. Needs the macOS System Audio Recording grant (asked on the first play); without it the clip plays to the speakers only, outside every deck bus, and the pad says so. With Auto PTT enabled and TX armed, the processed deck mix feeds the transmitter directly. The stream route remains independent. |
| Open URL | Opens a normal HTTP or HTTPS link in the default browser. | The destination application decides. |

YouTube playback uses the provider's embedded player. HermitSDR does not
download, rip or cache YouTube audio: the player decodes and renders it, and
HermitSDR only takes the PCM the player is already rendering. WebKit renders
a web view's media in its own child process (`com.apple.WebKit.GPU`); the
deck opens a Core Audio process tap on that one child (never on HermitSDR
itself, which would capture the local pads and loop them, and never on
another app) with the *muted-when-tapped* behaviour, so the clip is heard
once — through the pad graph, not from the player directly. The tap exists
only while a YouTube pad is active and is released when the player stops. It
needs the macOS **System Audio Recording** permission, requested on the first
YouTube play (never at launch). If the tap cannot be made — permission
denied, the media process not attributable, an older macOS — the clip plays
to the speakers as before, outside the RX and stream mixers, and the pad, the
player panel and the pad editor say "speakers only" with the reason. A pad
with **Send to stream mix** on routes the tapped audio into the radio's
speaker mix and so to Discord voice and the live streams, exactly like a
local pad. Since 2026.0915_008 the operator can also select **App audio** as
the TX program source: ScreenCaptureKit captures this process's own output
(other apps are excluded) and feeds it to the TX chain behind ARM and PTT,
exactly like the file player; that capture needs the macOS Screen Recording
permission. A provider error is shown on the pad and retained in the bounded
activity log so the pad can be retried.

The player panel keeps the pad grid usable: there is no modal sheet, the
other pads can be pressed while a clip plays, and the player stays visible
(at least 200 px tall) as YouTube's embed terms ask. **Stop player** in the
panel, STOP ALL, the pad itself and global pause/resume all drive the
embedded player.

### YouTube account

The sign-in sheet loads Google's own page inside the deck's web session
(`WKWebsiteDataStore(forIdentifier:)`, one per install, id in
`mediaDeckWebStoreID`). HermitSDR reads only the cookie names that prove a
session exists (`LOGIN_INFO`, `SAPISID`) to show signed in / out; Sign out
removes every record in that store. The YouTube Live OAuth token used for
streaming is a different credential and does not affect the player.

## Adding sound

Click any empty pad — in perform or edit mode — to choose audio or movie
files in Finder. Choosing several files fills the following empty pads in
order; files past the last empty pad are reported in the status log rather
than dropped silently. Files can also be dropped from Finder onto an empty pad
in either mode. Right-click an empty pad to choose files or to open the full
editor (for a YouTube or web pad). In edit mode a single new pad opens
straight into its editor.

Each local pad gets a waveform thumbnail and a duration badge, scanned in the
background after assignment and stored with the deck. The played portion of
the waveform lights while the pad is sounding.

## Editing and performing

Edit mode assigns a source, title, group, trim, gain, looping, press behavior,
route, optional keyboard shortcut, and per-pad FX. A missing local file
remains visible and can be relinked without recreating the pad. Pads can be
dragged between slots, duplicated into the first empty slot, or cleared.

Press behaviors are Restart, Pause / Resume, One-shot, and **Hold to play**.
A Hold-to-play pad sounds while the mouse button is down and stops (with its
fade-out) on release, like a momentary key on a hardware board. Keyboard
activation has no release, so it toggles start/stop instead. Momentary pads
show a hand icon.

Perform mode makes a press execute the pad. Group policies may interrupt,
queue, or mix clips. The activity control lists current and queued pads;
global pause/resume affects active media, and **STOP ALL** (Command-period)
immediately stops active and queued pads. Command-left-bracket and
Command-right-bracket change pages. Arrow keys move through available pads.

## FX rack

The header **FX** latch opens the live effects rack under the grid:

| Control | Range | Notes |
| --- | --- | --- |
| Pitch | ±24 semitones | Speed is unchanged. |
| Speed | ¼× – 4× | Pitch is unchanged. |
| Echo / Echo time / Feedback | 0–100 % · 0.02–2 s · 0–95 % | Feedback is capped short of runaway. |
| Reverb | 0–100 % + space | Small room … cathedral, plate, chambers. |
| Drive | 0–100 % + flavor | Crunch, broken speaker, radio tower, alien, cosmic, robot, lo-fi, bit crush, cell phone, waves. |
| Low-pass / High-pass | 200 Hz–20 kHz · 20 Hz–4 kHz | Log-scaled; the range end is off. |

Slider moves apply to every playing pad immediately. The rack is saved with
the deck; the **ON** latch bypasses it without losing the setting. **Surprise
me** rolls a random, always-audible setting within the slider ranges; **Reset**
returns to dry. The footer shows an FX lamp whenever the rack holds a
non-neutral setting.

Profiles are one-click rack settings: Stadium, Underwater, Chipmunk, Demon,
Gum Mouth, Helium, Robot, Telephone, Alien, Haunted, Megaphone, Slow-Mo, Fast
Forward, Cathedral, Walkie-Talkie, Canyon, Lo-Fi, and Cosmic. The chip whose
values exactly match the rack is highlighted.

The pad editor's **FX** menu lets a pad follow the rack (default), copy the
current rack, or pin a profile. A pinned pad ignores the rack and its ON/OFF
switch and shows an **FX** chip on its face.

Effects are Apple's built-in AVAudioUnit time-pitch, distortion, EQ, delay
and reverb units in series between each pad's player and its mixer. The
stream-mix tap sits after the rack, so Discord and YouTube hear the same
sound. A neutral rack bypasses every unit and is audibly identical to a deck
without effects. A YouTube pad in the deck mix passes through the same rack
and tap; an Open-URL pad plays in the browser and is not affected.

The header output meter shows the loudest pad after master volume, the
tapped YouTube player included.
Preparing, buffering, playing, paused, queued, completed, stopped, missing,
and failed are distinct visible and accessibility states. The pin keeps the
deck above normal windows and is saved with the deck. Standard macOS window
controls provide resizing and full screen.

## Transmit safety

With **Auto PTT** enabled and **ARM** on in TX Controls, playing pads feed the
transmitter directly: YouTube and local pads share a bounded 48 kHz stereo mix
from their post-FX mixers, including pad gain/fades and master volume. The
operator does not need to select App audio or change the pad's stream route.
RX speaker muting and a muted monitor route do not interrupt this program feed.
The deck temporarily takes the TX input for its own over, then restores the
prior input. An input changed by the operator during the over is respected.

The YouTube pad must be playing, in **DECK MIX**, and delivering non-zero captured
frames before it can start Auto PTT. A speakers-only clip cannot provide TX
program; its capture failure remains visible. The macOS System Audio Recording
grant for the existing player tap is still required. This direct program route
does not require the separate Screen Recording/App audio capture permission.
**TX · DECK MIX** marks the player while the deck holds the key.

Manual PTT and TX Controls' File/App audio sources retain their existing behavior.
All key requests still pass through `TXCoordinator`, ARM, policy, mode and
hardware protections. The deck never arms a radio.

By default the operator keys with PTT. The header's **Auto PTT** latch lets
the deck ask for the key instead:

- It keys when the first pad becomes audible and unkeys 0.4 s after the deck
  goes quiet (a queued follow-on pad keeps the over up; pause unkeys).
- The request goes through the same `setPTT` path as the PTT button. With
  ARM off, an unsupported mode, a policy inhibit or a tripped protection the
  key is refused and the reason appears in the deck's activity log.
- The deck never adopts a key it did not raise, and it never re-keys by
  itself: after a manual unkey, a disarm, a protection trip or a refusal the
  same playback stays off the air until a pad is started again.
- There is no fixed playback-duration cutoff. Long videos, live streams and
  looping pads stay keyed until playback ends, pauses or is stopped, Auto PTT
  is switched off, or the normal transmitter controls/protections unkey.
- The latch is never saved. Like ARM, every launch starts with it off, and
  editing or importing a deck document cannot turn it on.

## Deck compatibility

Older deck documents continue to load as local-file decks. Newer documents
also persist source type, URL, selected page, always-on-top preference, the
FX rack and its switch, per-pad FX, waveform thumbnails and durations. Every
FX field is optional and clamped on load; an unknown press policy plays as
Restart. HermitSDR refuses documents with a future schema version instead of
guessing at fields it does not understand.
