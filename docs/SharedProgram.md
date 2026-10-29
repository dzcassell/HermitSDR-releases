# Shared Program & Instances

This first version connects HermitSDR instances on **one Mac**. One master shares its Input Mixer program with up to eight followers. Each instance connects to a different radio and keeps its own frequency, mode, drive, TX profile, protections, ARM and PTT.

The mix is stereo 48 kHz PCM after the microphone/Media Deck channel faders, EQ and effects, before each radio's final TX processing. It is neither RF I/Q nor receiver/speaker audio. Different voice modes and bandwidths can carry the same performance. Native digital generators and CW keying are separate local paths.

## Get started

1. Open **Station → Control Devices → Shared Program & Instances…**. The existing copy is **Main station** and retains its settings.
2. Enter a distinct station name, such as **HL2 10 m**, and choose **Create & open**. Connect that copy to its intended radio. Repeat for additional radios. A profile can be open only once.
3. In the master copy, open **Input Mixer**. Select its microphone, adjust the two channels, and prepare clips in **Media Deck**. Give the program a recognizable name and choose **Start sharing**. This starts microphone capture, including while that radio is SAFE or disconnected. It does not ARM or PTT any radio.
4. In a follower, choose the master under **Master on this Mac**, keep the recommended **40 ms** cushion, and choose **Connect audio**. This selects **Shared program** as its TX input and disables its MIDI input. Wait for **Audio ready**.
5. Use each radio's local ARM/PTT controls when ready. Play clips and operate the MIDI mixer in the master. The follower receives that program while applying its own final TX settings. Monitor from one instance to avoid hearing duplicate delayed audio.

Roles start off after launch. Select and start the links again for a new session; a remembered TX-source choice cannot automatically start a microphone, join an old session, ARM or key a radio.

## Controls and recovery

- **Audio cushion:** 20 ms reduces delay; 40 ms is the recommended starting point; 80 ms adds timing cushion. Stop the link and disarm before changing it. The buffer status is the currently queued duration, not an RF phase/synchronization measurement.
- **Program level:** measures the shared audio before the local radio's final processing. A silent microphone or clip can legitimately show a low level while the transport is ready.
- **Sharing banner:** remains in the main window while linked. It opens the setup controls and provides **Stop & disarm** even when the setup window is closed.
- **Stop link & disarm this radio:** stops this instance's link and disarms its radio. Stopping a follower leaves the master and other followers alone. Stopping the master removes their audio source; it does not remotely change their ARM controls.
- **Audio not ready:** confirm the master is sharing, its microphone is selected, the right program is selected and the cushion has filled. If the master restarted, stop and reconnect the follower to its new session.
- **Interrupted stream or stalled consumer:** fresh arrivals alone cannot renew a shared-input voice key. Actual consumed PCM renews an existing short host TX lease. Missing/stale PCM stops renewal; the radio protocol's independent lease guard drops that key. Recovery never automatically re-keys—use a fresh local PTT action.
- **MIDI in followers:** disabled so the same physical controller cannot operate the mix in several copies. After stopping the link, enable MIDI manually if that copy needs independent controls.

## Finding and owning radios

Discovery probes can interrupt an active ANAN stream or steal its firmware's source-port ownership. While any local HermitSDR instance owns a radio, the other instances pause broadcast/fallback discovery and show **Known radio** entries from an earlier scan. Use the radio's IP address if it is missing, or disconnect all copies briefly to rescan. These cached entries do not prove a radio is still reachable.

Two instances cannot claim the same radio, including known MAC aliases. A local instance also cannot release or change the network settings of a radio owned by another instance. Disconnect it in that instance first. These protections coordinate this version's copies; close older versions before setting up multiple instances.

## Separate profiles

Named stations use separate defaults, support/recording paths and Keychain services. They do not inherit Main station's credentials, integrations, automatic reporting consent or MIDI input. CAT and control services start off and have separate default ports; the station list shows each CAT port. Opt into reporting separately if desired.

The application bundle is shared. Close the other instances and install updates from Main station; named stations direct you there. Opening an already-open profile explains the conflict rather than creating another copy with the same settings.

## Scope and acceptance

This stage shares local audio only. LAN followers, linked group PTT and automatic master takeover are later work. Buffered program audio does not provide phase-coherent RF or sample-aligned radio clocks. Each radio's own interlocks and local controls remain authoritative.

Software tests and separate-process loopback fixtures exercise isolation, transport, freshness, source ownership and cleanup. Physical multi-radio audio/RF acceptance remains operator-assisted and pending; a software pass does not establish radio behavior.
