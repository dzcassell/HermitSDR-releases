# Automatic receive AGC threshold

Receiver → DSP → Auto AGC threshold follows the noise measured after native
NR, Audio Units, APF and EQ but before the AGC. It defaults off; 12 dB margin
is the initial choice (6–24 dB). More margin holds the noise farther below the
AGC target, at the cost of less amplification for very weak speech.

The narrow 12 kHz path uses a 512-point Hann periodogram, discards the channel
edges, estimates the lower power quartile and corrects its exponential-noise
bias and window noise bandwidth into integrated real-audio RMS dBFS. An isolated
carrier does not set the floor. A passband with fewer than nine raw bins before edge trimming, or with
at least half its interior much louder than the floor, is not classified.
Colored noise and speech filling the entire filter can still bias the estimate;
the control is an operating aid, not a calibrated antenna noise measurement.

Analysis uses fixed scratch buffers and runs only when enabled. The control law
runs on the existing main-actor meter tick: 0.5 s acquisition, three fresh
measurements, 0.75 dB deadband, bounded floor rise/fall and at most 3 dB/s gain
change. It does not depend on zoom, pan, display floor or S-meter RF calibration.
Actual audio gain, attenuation, filter width and processing changes are visible
to the measurement rather than guessed from a screen axis.

Manual max-gain adjustment takes over and turns Auto off. Turning Auto off
restores the remembered manual gain; automatic intermediate gains are never
written as that preference. Intent/margin and manual gain persist per radio.
SUB in Follow main inherits the main AGC law; independent SUB remains manual
and does not run another automatic estimator.

FM, wide audio and AGC Off keep manual behavior. Keying/RF-hot and replay/rewind (at least 0.5 s behind live)
pause adaptation; unkey holds for one second. Mode/filter/rate/tuning/history
changes reacquire, stale repeated measurements do not move gain, and chain
rebuilds start with empty spectral history. Controls show learning/paused status.
Fixtures cover calibration against actual demodulated RMS at 48/192/384 kHz,
carrier rejection, narrow-band refusal, mode/keyed resets, slew/deadband,
unsafe/stale/context handling and hostile parameter bounds. Operator listening
acceptance is recorded separately; these fixtures do not prove intelligibility
on every noisy voice signal.
