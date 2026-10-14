# CW receive listening pitch

In CW mode, Receiver → DSP → CW RX pitch selects 300–1000 Hz in 10 Hz steps;
700 Hz remains the default. The mixer parks the received carrier at this pitch.
Main and SUB CW filters/APF, the main Morse decoder, binaural center and audio/
RF notch markers follow the same choice. The RF dial, RIT, transverter mapping
and transmit carrier are unchanged. Keyer sidetone is an independent preference;
changing receive pitch never changes it or requests keying.

The existing Single pole and Double pole APF choices remain. At equal center
boost and −3 dB width, the double-pole resonator has faster skirts and dips
below unity beside the tone; the single-pole response stays above unity.
Production response and sample-processing fixtures pin that distinction.
Additional upstream-style shapes are not added just to multiply controls.

Pitch changes reset partial Morse timing and APF/binaural state under their
existing synchronized owners; the receive-chain duck covers the transition.
The optional receiver-profile field decodes older version-1 snapshots as 700 Hz.
Fixtures verify real production-chain audio at 300/450/700/1000 Hz, APF alignment,
Morse decoding at alternate pitches, default/catalog compatibility and unchanged
RF/tuning geometry. Live listening evidence is a separate operator check.
