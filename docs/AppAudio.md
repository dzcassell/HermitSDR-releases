# App Audio in TX Controls (development candidate, issue #329)

App Audio captures playback from another application on this Mac using native
macOS audio capture. The normal route does not require BlackHole, Audio MIDI
Setup, or changes to the Mac's default audio output.

## Try it without transmitting

App-only capture requires an independent macOS audio identity. A GUI app launched
from a terminal or code host can share that host's audio group with other apps;
that ambiguous route is refused. Quit it and reopen it normally from Dock or
Finder, refresh and select it again. If macOS cannot establish isolation, use
System Audio for local preview only when you explicitly intend the broader scope.

1. Open **TX Controls** and select **App Audio — other apps** as Source.
2. Open Discord, your browser, GarageBand, or another playback app. Refresh the
   app list, choose that app, then click **Start capture**.
3. If macOS asks, allow Screen & System Audio Recording for this development
   app in System Settings → Privacy & Security. Retry capture if required.
4. Play audio in the selected app. **APP INPUT** shows its captured level.
   The chain should show **Capture: Listening**, **Program: Not admitted**,
   and **Radio: SAFE**. A listening stream can legitimately contain silence.
5. For private local preview, choose a physical listening output and enable
   **Listen**. This preview is mono at −6 dB, independent of program gain/mute.
   The source app also keeps playing through its original output; listening to
   both paths on the same speakers can sound doubled. Headphones or a separate
   listening output are useful.
6. **Add to TX program** admits freshly captured audio, but does not arm or key.
   While SAFE, the program stage says **Waiting for ARM**. App level and Mute
   control the admitted audio; the input meter measures the original capture.
7. Stop capture when finished. The main console has a capture banner and a Stop
   control even when TX Controls is closed.

Demo Mode supports capture, metering and private preview; it cannot ARM or key.
The network-isolated test instance cannot discover/connect to physical radios.
Actual radio operation requires an operator-controlled session and the existing
ARM/PTT, policy, protection and hardware checks.

## Mix with the microphone and Deck

Select **Input Mixer** as the TX source to combine microphone, Media Deck,
admitted remote guests, and admitted App Audio. Changing TX source stops app
capture and clears admission; start it again for the new route. App Audio has
its own level and mute in TX Controls. The existing mixer window owns microphone,
Deck and guest faders/EQ/effects. App Audio enters the program after those channel
processors, then passes through the same master TX gain/profile/EQ/processing
and final limiter as the other inputs. App audio is not added to the caller
return/mix-minus bus in this candidate.

**System Audio is preview-only in this candidate.** It includes other playback
and notifications, with HermitSDR instances known at capture start excluded.
Testing found that an instance launched later can enter that existing stream;
therefore System Audio cannot be admitted to the TX program, including through
the model API. Choose **Selected app** for TX-program audio. Broader TX routing
remains pending a reliable exclusion strategy. No microphone is included by
native app capture; microphone + selected-app audio uses Input Mixer.

## Session behavior and limitations

- Capture, source selection, program admission, app level/mute and private preview
  are session-only. The TX source choice uses the existing settings snapshot.
- Capture starts only on an explicit Start action. Source/scope changes, selected
  app exit, capture error, preview-output failure, disarm and application shutdown
  stop capture and clear admission. App identity includes its launch time, so a
  reused PID cannot silently substitute a relaunched process. Relaunched apps
  require selection and Start.
- Admission changes restart capture and invalidate the old capture token, so
  delayed private buffers cannot become public. Native digital ownership and
  route/disarm transitions clear queued app PCM. All queues are bounded.
- Permission denial, protected content, app-specific routing or an unsupported
  capture case can produce silence. Start playback, check permission, retry,
  and verify the input meter before admitting audio. No silent source fallback.
- This first candidate selects one application at a time, or System Audio.
  Browser tabs within the selected browser are not individually selectable.
- Virtual-device routing remains an advanced fallback: source app → BlackHole;
  HermitSDR Source **Microphone**, Mic input **BlackHole**. The native route does
  not install or configure a virtual audio device.

Native capture uses ScreenCaptureKit application filters and subscribes only to
audio buffers. No video frames or captured audio are saved by this feature.
Existing explicit TX recording/aircheck behavior remains separate.

## Validation

Automated checks cover bounded/generation-scoped capture buffering, admission,
SAFE eligibility, stereo/gain/mute, finite PCM, source settings, final processing
and limiter containment. A synthetic-buffer probe exercises the production
planar/interleaved Core Media audio extraction. The production UI-owner fixture
uses inert native devices and deterministic process inventory to cover pending
permissions, private/public epochs, app loss, capture restart failure, preview
refusal/loss and source/output changes. Preview readiness is enforced inside the
owner as well as in the view. Production-engine probes use
inert devices and never key a radio. Manual acceptance must still cover the
operator's actual Discord attachments, browser players and GarageBand projects,
source output/device changes, permissions, and an approved hardware session.
