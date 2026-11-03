// The 48 kHz AudioContext owns pacing. Emit 480-sample/10 ms frames including
// silence; timestamps let the consumer reject queued pre-stall audio.
class HermitPCM extends AudioWorkletProcessor {
  static get parameterDescriptors() {
    return [{ name: 'gain', defaultValue: 1, minValue: 0, maxValue: 3, automationRate: 'k-rate' }];
  }
  constructor() { super(); this.reset(); }
  reset() { this.buffer = new ArrayBuffer(960); this.view = new DataView(this.buffer); this.pos = 0; this.peak = 0; }
  process(inputs, outputs, parameters) {
    const channels = inputs[0] || [];
    const n = outputs[0][0].length;
    for (let i = 0; i < n; i++) {
      let sample = 0;
      for (const channel of channels) sample += channel[i] || 0;
      sample = Math.max(-1, Math.min(1, (channels.length ? sample / channels.length : 0) * parameters.gain[0]));
      if (!Number.isFinite(sample)) sample = 0;
      this.peak = Math.max(this.peak, Math.abs(sample));
      this.view.setInt16(this.pos++ * 2, Math.round(sample * 32767), true);
      if (this.pos === 480) {
        this.port.postMessage({ pcm: this.buffer, peak: this.peak, time: currentTime }, [this.buffer]);
        this.reset();
      }
    }
    return true; // Outputs stay zero; the monitor uses a separate source path.
  }
}
registerProcessor('hermit-pcm', HermitPCM);
