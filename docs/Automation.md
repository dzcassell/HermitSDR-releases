# macOS automation: Shortcuts, Siri, Spotlight and AppleScript

HermitSDR can be driven from the Shortcuts app, from Siri and Spotlight, and
from AppleScript (Script Editor, `osascript`, Keyboard Maestro, Automator
folder actions). It can also run a script of yours each time a contact is
logged.

**Receive and read-only.** Automation can tune, change mode and filter, recall
bookmarks and presets, record, switch decoders, save a waterfall picture and
read values. It cannot transmit: there is no PTT, TUNE, send-CW or call-CQ
action, not even a disabled one. Transmit intents are a separate milestone
(#415) that will need the same local approval the Control API's transmit
needs.

**Status.** The mapping, checks and wording are covered by unit tests against
a stand-in radio. No Shortcut and no `osascript` command has been run against
the app yet, and Siri phrases have not been spoken to it. Treat the first use
of each as a test and report what you see.

## What happens to a request

Every action goes through the same command layer the
[Control API](ControlAPI.md) uses for a network client:

- Tune, mode, filter and mute are sent as that API's own receive commands
  (`tune`, `setMode`, `setFilter`, `setMute`). The dial lock, a transverter's
  range, a recording's span in replay and "the transmitter is busy" therefore
  behave exactly as they do for a browser or a control head.
- Bookmarks, receive presets, recordings, decoders and the waterfall picture
  have no Control API message. They run on the same radio object, behind the
  same check that a radio session (or a replay, or Demo Mode) is live.
- A refusal is a sentence, for example `HermitSDR refused: the dial is
  locked.` or `HermitSDR has no radio connected and no recording playing.`
  In Shortcuts it stops the shortcut with that text; in AppleScript it is the
  error message.

Nothing is switched on by installing the app: the actions exist, and do
nothing until a shortcut or script calls them. The script hook is off until
you turn it on.

## Shortcuts actions

Open Shortcuts, add an action and search for HermitSDR.

| Action | Parameters | Result |
|---|---|---|
| Tune to Frequency | Frequency in MHz | What happened, as text |
| Set Mode | Mode (the radio's own list; `DIGU`, `PKTUSB` mean DATA-U) | Text |
| Set Filter | Width and / or shift in Hz | Text |
| Mute or Unmute | Mute / Unmute | Text |
| Recall Bookmark | Bookmark name | Text |
| Recall Receive Preset | Preset name (Radio › Receive Presets) | Text |
| Start or Stop Audio Recording | Start / Stop | Text |
| Start or Stop IQ Recording | Start / Stop | Text |
| Start or Stop a Decoder | Start / Stop; FT8, FT4, CW, RTTY, Skimmer, NAVTEX, SSTV, Weather fax, ALE | Text |
| Save Waterfall Snapshot | none | The PNG file |
| Get Frequency | none | Hertz, as a number |
| Get Mode | none | Text, for example `USB` |
| Get S-Meter | none | dBm, as a number (spoken with S units) |
| Get Last Decodes | Decoder (FT8 and FT4, CW, RTTY, NAVTEX); count 1–50 | A list of lines, oldest first |
| Get Last Logged QSO | none | Text: call, band, mode, frequency, UTC time |
| Get Next Satellite Pass | none | Text, from the Satellite Pass Planner's saved plan |
| Get Space Weather | Summary, Planetary Kp or Solar Flux | Text |

Notes:

- A bookmark or preset name may be shortened if only one name starts with (or
  contains) what you typed. Two matches are refused and listed; nothing is
  guessed.
- Starting a recording that is already running, or stopping one that is not,
  succeeds and says so.
- IQ recording is refused while a recording is being replayed.
- Save Waterfall Snapshot needs the main window to be drawing. If it is
  closed, minimised or fully covered the action fails after about three
  seconds and says why.
- A decoder that needs a particular mode (CW decode needs CW; FT8 needs USB
  or DATA-U) is switched on as asked and starts decoding when the mode fits,
  as it does from the menu.
- Get Next Satellite Pass reads the plan the planner last saved. With none it
  says so.
- The actions run without bringing HermitSDR to the front. If the app is not
  running, macOS starts it; with no radio connected the action then fails
  with the "no radio connected" sentence.

Example — "at 00:00 UTC tune 5 MHz AM and record ten minutes": a personal
automation at that time with *Tune to Frequency* 5, *Set Mode* AM, *Start
Audio Recording*, *Wait* 600 seconds, *Stop Audio Recording*.

### Spotlight and Siri phrases

These appear without building a shortcut ("HermitSDR Dev" in a development
build):

- "Tune HermitSDR"
- "What frequency is HermitSDR on"
- "What is the HermitSDR signal strength"
- "Mute HermitSDR" / "Unmute HermitSDR"
- "Start HermitSDR audio recording" / "Stop HermitSDR audio recording"
- "Start the FT8 decoder in HermitSDR" (any decoder name)
- "Save a HermitSDR waterfall snapshot"
- "Get space weather from HermitSDR"
- "When is the next satellite pass in HermitSDR"
- "What was my last contact in HermitSDR"

## AppleScript

Open the dictionary with Script Editor › File › Open Dictionary › HermitSDR.

Objects:

- `receiver 1` — `frequency` (Hz), `mode`, `filter width`, `filter shift`,
  `muted` (all settable); `signal strength` (dBm) and `S units` (read-only).
- `current radio` — `name`, `model`, `link`, `connected`.
- `bookmarks` — each with `name`, `frequency`, `mode`.
- `last QSO` — `callsign`, `frequency`, `mode`, `band`, `start time`; or
  `missing value` with an empty log.
- `next satellite pass`, `space weather` (text), `planetary K index`,
  `solar flux` (numbers, or `missing value`).

Commands: `tune to`, `recall bookmark`, `recall receive preset`, `start audio
recording`, `stop audio recording`, `start IQ recording`, `stop IQ recording`,
`start decoder`, `stop decoder`, `save waterfall snapshot`, `mute`, `unmute`,
`recent decodes`. Each returns a sentence saying what happened (`save
waterfall snapshot` returns the file's path, `recent decodes` a list).

```applescript
tell application "HermitSDR"
	get frequency of receiver 1
	tune to 14074000
	set mode of receiver 1 to "DATA-U"
	start decoder "FT8"
	delay 60
	recent decodes "FT8" count 5
end tell
```

```sh
osascript -e 'tell application "HermitSDR" to get frequency of receiver 1'
```

The first time another app scripts HermitSDR, macOS asks whether to allow it
(System Settings › Privacy & Security › Automation).

## Run a script when a contact is logged

Settings › Station › Automation › **Run my qso_logged script when a contact
is logged**. Off by default.

Put one file named `qso_logged` in HermitSDR's scripts folder (**Open Scripts
Folder** shows it; it is `~/Library/Application Scripts/` followed by the
app's bundle identifier). Each contact added to the log — by the Log button, a
contest entry, an FT8 sequence — runs it once. Imports do not.

- An AppleScript (`qso_logged.scpt`, `.scptd` or `.applescript`) must define
  this handler:

  ```applescript
  on qso_logged(theCall, hertz, theMode, theBand, utcTime)
  	display notification theCall & " on " & theBand & " " & theMode with title "Logged"
  end qso_logged
  ```

- Any other executable file named `qso_logged` (a shell or Python script with
  its execute bit set) is run with the same five values as arguments.

All five values are text: the call, the frequency in whole hertz, the mode as
logged, the band (`20m`, or empty outside the amateur bands) and the start
time in UTC (`2026-11-16T12:34:30Z`). If both kinds of file are present the
AppleScript runs.

The script is your own program. It runs outside HermitSDR with your user
account's rights, one at a time; HermitSDR passes it text and reads nothing
back except whether it failed, which the Settings row shows. If scripts pile
up (more than 16 waiting) further contacts are not passed on until they
finish.

## Limits

- One receiver (`receiver 1`, the main receiver). The sub receiver and the
  independent receivers are not scriptable yet.
- No band, AGC, noise-reduction, squelch, volume or RIT actions yet; the
  Control API has them.
- No Shortcuts trigger ("when a contact is logged, run this shortcut") — the
  script hook is the way to react to an event.
- Queries return text or a number, not structured records.
- Transmit actions are not part of this and will arrive, if at all, as a
  separately reviewed change.
