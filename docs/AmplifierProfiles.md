# Amplifier references in TX Controls (development, #330)

While SAFE, open **TX Controls → Amplifier Profile** and choose **Mercury IIIS
(3S)**, **Mercury Lite**, or **Custom / no amplifier profile**. Selection is
saved with the transmitter configuration. Older configurations open as Custom.
Selecting a model does not change drive, timing, source, ARM or PTT. Profile
changes are refused while armed or RF-hot.

Expand **Limits, scope and reference** for the manufacturer link and capability
scope. **About → Copy System Information** includes the profile and the actual
normalized native-digital timer settings, including whether the timer is off.

## Mercury IIIS (3S)

The reference is KM3KM's **full-unit operating manual v4.5 (2025)** from its
[downloads page](https://km3km.com/downloads). The UI links the exact manual.
Damon identifies his amplifier as a Mercury IIIS / 3S; the unit's hardware,
firmware and assembled-versus-kit revision still need operator confirmation.
Historical bench records describing a Lite remain historical records.

The panel summarizes documented band/mode, input-power and CW restrictions.
Those are advisory amplifier references. They do not set a radio drive
percentage or prove measured amplifier output. The manual's differing 6 m
output figures are explicitly called out for operator verification. No
manufacturer-backed IIIS TX/RX duration preset was found, so selecting IIIS
retains the existing operator timing instead of copying Lite's preset. The
amplifier's carrier trip is not used as a software TX duration limit.

RCA PTT/ALC and RF band detection are documented; no supported serial/network
control protocol is established by this reference. The profile supplies no
telemetry, antenna switching, fault reset or standby/operate driver. Use the
amplifier's own controls. ALC input voltage/interface compatibility and relay
sequencing are not established by model selection.

## Timing and protection

Only **Mercury Lite** offers **Apply timing**, an explicit action applying its
existing 60 s maximum TX / 15 s minimum RX native-digital preset. Selection alone
never enables it. For IIIS, confirm suitable limits for the specific unit and
edit **Native digital amp timing** separately when appropriate.

Configured timing is used by the FT8/FT4/beacon/JS8 controller and Native
Transmit WSPR/Feld Hell/ALE controller. Each keeps its own cooldown state;
this is not a station-wide duty interlock when changing transmit tools. Manual PTT,
voice/AM, CW, TUNE and external CAT/app transmissions are outside that timer.
Existing ARM, frequency policy, waveform watchdogs, cooldown/tail accounting,
radio protection and calibrated drive behavior remain authoritative. See
[NativeDigitalTX.md](NativeDigitalTX.md) for timing details.

Software tests cover old/unknown profile migration, persistence without ARM,
unchanged drive/timing, distinct Lite/IIIS behavior, diagnostic scope and existing
timing contracts. Presentation checks cover both skins and narrow TX columns.
Physical amplifier matching and any RF check require the operator's approved
hardware session. This work remains staged for review.
