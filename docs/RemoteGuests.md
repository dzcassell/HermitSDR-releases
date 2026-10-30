# Remote Guests & Call Setup — local prototype

Connect an existing calling app to Input Mixer. Zoom can host app guests and,
when the account supports it, meeting telephone dial-in guests. A SIP phone app
can answer a number supplied by a compatible telephone provider. HermitSDR does
not create a phone number, place calls, join a meeting, or replace that app's
answer/hold/hang-up controls. All remote voices share one mono Guest strip.

## Route audio once

Use Loopback to create **Caller In** and **To Call**, or use two distinct
BlackHole devices (for example 2ch and 16ch). These are two independent routes;
one virtual device used in both directions creates a feedback loop.

| Source | Destination |
| --- | --- |
| Calling app speaker | Caller In virtual device |
| Caller In, channel 1 | HermitSDR Remote Guests input |
| HermitSDR caller return | To Call virtual output |
| To Call | Calling app microphone |
| HermitSDR private guest preview | Physical headphones |
| Host microphone | Input Mixer microphone, selected in TX Controls |

The host microphone is the fourth device in this loop. Setup refuses a caller
input or return device that is the host microphone selected in TX Controls (or
the system default input when none is selected). While the bridge runs, the host
microphone is pinned to that exact device: if it disappears, the Input Mixer
reports the failure and disarms rather than silently capturing whatever macOS
makes the default input, which could be the caller route itself.

Keep system output/notification sounds on another device. If using Loopback app
capture instead of selecting a virtual speaker in the calling app, capture only
that calling app; do not include HermitSDR's full output or your host microphone.
A default/global system mix can carry notification sounds and unrelated audio.
Do not include either virtual route in a monitor/aggregate feeding the other.

1. Open **Transmit → Input Mixer → Remote Guests & Call Setup…**.
2. While SAFE, select the three distinct devices and the caller input channel.
   No device is selected automatically. Check the host microphone in TX Controls.
3. Choose **Start audio bridge**. This starts host/caller capture and two local
   outputs. It neither answers a call nor arms/keys a radio. Microphone permission
   applies to virtual audio capture too. Route selections/routing are session-only.
4. Speak to the guest using **Private talkback**, listen through **Hear guests in
   headphones**, and check the Guest/Return meters. Talkback keeps your microphone
   off the entire transmit program, including shared followers; Deck and already
   admitted guests can continue. Microphone channel mute/fader still applies.
5. Select return sends: **My microphone** defaults on; **Media Deck** and **Radio
   receive audio** default off. Caller audio never enters this return. Zoom handles
   its guests hearing one another without returning their combined audio.
6. End private talkback and choose **Admit guests to transmit mix** when ready.
   Use the normal independent radio controls for any separately authorized RF test.
   This toggle admits all audio from the selected calling-app route, including
   newly joined callers and any sounds the app plays. Screen/mute in that app.

The console banner stays visible when the setup window is closed. It identifies
private preview, admitted guests, or private talkback and provides **Guests
private**, **Call setup…**, and **Stop bridge**. Closing the window keeps audio and
its current privacy state running. Stop leaves the external call open.

## Levels, quality and controller

Input Mixer has microphone, Deck and Remote Guests strips. Each has a smoothed
fader, mute, seven-band EQ, optional voice compressor and effects. The compressor
uses a −18 dBFS threshold, 3:1 ratio, 5 ms attack and 120 ms release with no makeup
gain. Digital bypasses strip processing. Final TX processing/limiting still owns
the RF output. The separate mono return/preview are bounded to ±1; reduce send
levels if return peaks reach 0 dBFS. They are not the final TX limiter monitor.

**MIDI Controller → Set up nanoKONTROL2 → Call-in Mixer** assigns sliders 1/2/3 to
Mic/Deck/Guest, knobs 1/2/3 to their FX amounts and M1/M2/M3 to momentary channel
mute toggles. Existing Mix + FX and Full EQ layouts keep their original mapping.
MIDI Learn also exposes Guest EQ/effect controls. No binding admits a caller or
operates ARM/PTT. Physical controller checks remain pending.

For several radios on one Mac, start **Shared Program** as master before starting
the bridge in that instance. Followers receive the post-channel admitted mix;
no follower opens a separate caller/return route. Stop the call bridge before
changing shared roles. Each radio retains its local mode, final processing and
ARM/PTT. This prototype does not provide LAN calling or linked group PTT.

## Recovery and validation

Device departure stops the bridge and clears admission/talkback. Caller capture
requires the exact selected UID/channel and never intentionally falls back to a
system microphone. Outputs remain bound to their chosen UID; a stopped graph may
settle on that same device with bounded retries, never another output. Return
and guest FIFOs are bounded and stop/reconnect invalidates old capture tokens.
Microphone capture is replaced at talkback boundaries to discard private PCM and
FX tails; admission changes similarly replace guest capture. Allow a brief gap.

Start again and check privately before readmitting guests. Refresh devices while
stopped if a device is missing. A silent source can legitimately show no level;
check the calling app's mute/speaker selection and channel. The receive return is
tapped after keyed receive mute, before Deck, CW sidetone and TX monitor, so none
of those can feed a caller back into itself. Use headphones to prevent acoustic
feedback; software routing cannot prevent a loudspeaker feeding your microphone.

Software fixtures validate routing, privacy epochs, persistence migration,
controller maps and lifecycle without any actual calls or RF. The first real
Zoom/SIP call, physical route changes, audio quality/latency and radio hardware
checks remain operator-assisted acceptance; no live validation is implied.
