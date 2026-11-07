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

1. In **TX Controls**, choose **App Audio — other apps** as Source and pick
   the running app.
2. Click **Send app to TX**. This starts capture and routes the selected app
   into the TX program. It does not arm or key the radio. If macOS asks,
   allow Screen & System Audio Recording and retry if needed.
3. Play the app. **APP INPUT · BEFORE GAIN** shows its captured level.
   **Waiting for ARM** means the app is routed and the transmitter is SAFE.
   **Ready for PTT** means the app is routed and signal is present.
4. For private listening, use **Capture for preview**, choose a physical
   listening output and enable **Listen**. Preview is mono at −6 dB and
   independent of App level and Mute. The source app keeps its normal playback.
5. **Stop sending app audio** stops capture and clears the route. The main
   console also has a capture banner and a Stop control.


Demo Mode supports capture, metering and private preview; it cannot ARM or key.
The network-isolated test instance cannot discover/connect to physical radios.
Actual radio operation requires an operator-controlled session and the existing
ARM/PTT, policy, protection and hardware checks.

## Mix with the microphone and Deck

Open **Input Mixer**, choose **Use Input Mixer** if needed, then use
**Add app** once for each running app you want in the mix. Each app starts
capture and gets its own input meter, fader and mute. You can mix up to eight
app channels alongside the microphone, Media Deck and remote guests.

**Stop** pauses one app and keeps its fader setting. **Remove** frees its
slot. **Stop all apps** ends all app captures in the mixer. Disarming or
changing TX source stops capture. Use **Start** to resume a strip. If the app
was relaunched, remove the old strip and add the new process.

The app channels share the existing master TX processing and final limiter.
They do not feed the remote guest return bus. macOS must be able to isolate
each app's audio. The app picker includes regular and menu bar apps that
macOS reports as running. Tabs and helper processes inside one app share
its channel.

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
- Capture starts only on an explicit Send or Capture action. Source/scope changes, selected
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
- The standalone App Audio route selects one app at a time. Input Mixer supports multiple app channels.
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
