# Bookmark activity scanner

Open **Radio → Bookmark Scanner**, or **Bookmarks → Bookmark Scanner…**.
The scanner listens to one existing memory at a time and holds on **receive
power**. A carrier, noise or interference can hold it; this is not voice or
decoded-message classification.

## Make and run a list

1. Save the stations in Bookmarks, including their receive mode, width/shift
   and gain/attenuation where needed. Missing fields use
   existing bookmark recall defaults, including per-mode filter memory.
2. Choose New, name the list, select 1–128 memories and Save list. Up to 32
   lists are stored. Lists refer to bookmark IDs; they do not create another
   station-memory format. Edits/deletions in the bookmark library interrupt a
   running scan so it cannot silently use an obsolete memory.
3. Set timing and threshold, save changes, then Start with a live connected,
   disarmed receiver. No scan starts at application launch or reconnect.

| Control | Bounds / meaning |
| --- | --- |
| Settle | 0.2–10 s, default 0.5; a complete fresh meter window must begin after this delay |
| Dwell | 0.2–60 s, default 2; quiet-channel measurement time, starting with the first valid post-settle report |
| Threshold | −160–0 dBm, default −100; choose above the measured channel noise floor |
| Hysteresis | 1–30 dB, default 6; an active hold continues above threshold minus this amount |
| Hang | 0.1–30 s, default 1; time below the lower threshold before leaving an active channel |

All values must be finite and inside their bounds. Start uses the saved list.
The list's ID order is used for scanning. Save takes the selected memories in
their current library order. Stored frequencies retain the bookmark library's
IF units; the window and activity log display the current mapped RF in MHz.

Pause keeps the list position. Resume explicitly retunes/reacquires that memory;
it never trusts the last hold measurement. Skip advances once. Lock out this
memory excludes it for the current session; locking out every memory pauses.
Stop and end the session, then Start to clear lockouts.

## Stop, ownership and restore

Stop cancels the active hop token immediately. Choose **Keep current / End
session** or **Restore original receive settings**. Restore is allowed only
when the same connection and unchanged scanner-owned receiver state remain.
A manual tune (including a deliberate recall of the current frequency),
mode/filter/gain change, RF pan, session or FM-control change discards the old
restore offer. It cannot undo an intervening operator edit, even if the dial
later happens to return to the same value.

Dial lock, file replay/time shift, SUB/linked VFO, manual recording, ALE scan,
Band Scout, or armed/keyed/tuning/two-tone/RF-hot/program-owned transmission
refuse or pause scanning. Resume is always explicit. A replacement connection
requires ending the old session and starting a new one. These checks do not
arm, key or release a transmitter.

Scanner recalls use the existing bookmark/tuning owner and prefer in-span
mixer moves. When a center retune is unavoidable, IQ history is cleared and
DVR starts a new frequency segment; the window counts these retunes. Restore
can restore the original dial/center/display/filter/gain/notches, but cannot
reconstruct discarded history. Automated hops leave saved per-mode filter
memories and band stacks unchanged; the final explicit Keep/Restore choice can
remember the resulting receiver normally.

FM receive deviation and tone squelch follow the memory. Its transmit encode
flag and transmit tone/deviation are not recalled by the scanner. Pause/Stop
return transient FM receive overrides to the existing FM controls. Power hold
can still detect a carrier whose tone squelch keeps its audio closed.

## Timing and bounded work

The main RX chain stamps completed pre-AGC meter windows with a fresh hop token
after submitted mixer settings have been applied. Arming a hop resets the
meter integration window. Delayed old-token, pre-settle, nonfinite, duplicate,
future or stale reports cannot start/refresh a hold. Without fresh reports,
scanning pauses rather than pretending the radio has settled.

The DSP callback copies one immutable snapshot into a single nonblocking slot;
contention drops optional measurements. No UI, disk, timer or protocol wait is
added to the audio callback. A main-actor 10 Hz controller drives the pure
monotonic-clock state machine through existing receive commands. The activity
list keeps the newest 256 UTC reports in memory and is not uploaded or saved.
List persistence is bounded to 256 KiB; malformed saved data is retained until
the operator explicitly saves a replacement. Neither active state nor lockouts
are persisted.

Software geometry tags prove which DSP configuration produced a report. They
are not a hardware acknowledgement of NCO/relay settling. Network buffers and
radio firmware can add settling time; live RF timing and listening are separate
acceptance, not established by synthetic fixtures.

## Receive-only operator acceptance

Use a disarmed HL2 or ANAN receive session and leave transmit controls alone:

1. Save one quiet and one clearly active frequency within the sampled span,
   plus a suitable receive frequency outside it. Check each manually first.
2. Start with settle 0.5 s, dwell 2 s, hysteresis 6 dB and hang 1 s; choose a
   threshold above the observed quiet-channel floor. Confirm the quiet station
   advances and the active station holds, with matching name/RF/mode/UTC/level.
3. Try Skip, temporary lockout, Pause and explicit Resume. Check audio and relay
   settling; increase settle if your radio needs it. Verify no old-channel hold
   immediately after a hop.
4. Tune manually during a scan. Confirm immediate pause and that Restore cannot
   undo your change. End/restart, Stop normally and explicitly Restore; verify
   the original receive settings return.
5. Try the outside-span memory. Expect the indicated center retune and IQ-history
   reset. Disconnect/reconnect and replay must not automatically restart a scan.

No hardware transmission is part of this checklist. Record the radio/firmware,
receive rate, memories, timing and observed result before claiming live success.
