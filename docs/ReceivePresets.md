# Named receive DSP presets

Radio → Receive Presets… (also Receiver → DSP → Receive Presets…) saves and
recalls named DSP setups. This complements automatic per-radio profiles; it
does not replace them or frequency bookmarks.

Enter a unique name (1–80 characters), then Save current DSP as new preset.
Choose a saved preset to see every stored value before Recall…. The confirmation
uses the same preview. Rename uses the entered name; Remove retains the last
removed preset, including across restart, until Undo last removal or another
removal. Up to 64 presets are retained in `rxDSPPresets.v1`; corrupt, oversized
or unknown-schema data is preserved and the library becomes read-only.

Saved: filter width/shift, receive CW pitch, AGC speed/max gain/slope/hang and
Auto threshold intent/margin, NB method/level, SNB switch/level, exclusive NR
choice and controls, automatic notch, seven-band EQ curve/switch, CW APF
shape/width/gain and binaural switch/spread.

Mode and frequency are deliberately excluded. Recall adapts width and shift
to the current mode and reports the applied values. RF gain/attenuation, sample
rate, antennas, sub-receiver/diversity routing, output device, volume/mute,
manual transient notches, calibration, recordings, services and transmitter
settings are also excluded. Recall refuses while armed, keyed, tuning,
two-toning or RF-hot. It cannot initiate any transmission.

Version-1 payloads have validated types, bounded size/count and optional Auto
AGC fields. Fixture coverage proves current-mode adaptation, excluded-domain
preservation, names/duplicates, restart, remove/undo and corrupt-data retention.
Optional import/export is deferred; the first milestone is a local library.
