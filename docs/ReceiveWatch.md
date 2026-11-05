# Receive Watch

Open **Radio → Receive Watch → Recipe** to edit a draft or import a version
1 watch recipe. Use **Export Recipe** to share its exact settings. A watch
matches a peak that meets both the absolute dBFS floor and the requested
prominence over the median bin in its watch range. Frequencies are RF
frequencies. When using a transverter, the recipe still uses the displayed RF
span. Sample rate and FFT bin width determine the smallest practical range.

Use **Replay Preview…** with a local IQ recording before watching live. The
preview shows matching intervals and peak frequencies. Choose **Compare
Decoders…** to carry the selected recording and interval into an isolated
decoder trial. The same comparison is available in **Decode → Decode a
Recording**. Threshold hits alone cannot identify the mode or
station.

The live watch uses the current live receive span. It requires two
consecutive matching samples to open a detection and two quiet samples to
close it. It ends on a timeline or geometry change, disconnect, replay, TX
arm or transmit. It also ends after eight hours. The radio retains its
existing frequency and receive settings.

**Start and Save IQ Clips…** saves short excerpts in the chosen folder when
IQ history is available. A session keeps up to eight excerpts and a
versioned JSON checkpoint. Use **Export → Open Saved Session…** to review
the checkpoint or an exported report later. A completed session summary
can be shared explicitly with Local MCP. The summary excludes recording data
and paths.
