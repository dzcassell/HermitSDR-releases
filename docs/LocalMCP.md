# Local MCP for HermitSDR

HermitSDR exposes a local Model Context Protocol server through the installed
app executable. The client launches the helper over standard input and output.
The helper has no network listener and reads only the data explicitly shared
from the app.

Open **HermitSDR → Settings → Local MCP** and choose **Copy Claude Desktop
Config**. In Claude Desktop, open **Settings → Developer → Edit Config**.
Add the copied HermitSDR entry to the existing `mcpServers` object and restart
the client. For other stdio-capable clients, use the executable and arguments
in the copied config. A client that requires an HTTP server needs a separate
transport configuration.

| Tool | Share from HermitSDR | Expiry |
| --- | --- | --- |
| `get_receive_profile` | **Settings → Local MCP → Share RX Snapshot** | 1 hour |
| `get_transmit_profile` | **Settings → Local MCP → Share TX Snapshot** | 1 hour |
| `run_ssb_experiment` | **SSB Profile Lab → Share Take with Local MCP** | 20 minutes |
| `get_waterfall_case` | **Station → Performance → Mark Glitch**, then **Share Mark with Local MCP** | 1 hour |
| `get_receive_watch_summary` | **Radio → Receive Watch → Share Summary with Local MCP** after stopping | 1 hour |

The transmit snapshot contains profile, source type, passband, EQ, dynamics,
effects and bypasses. Share a fresh snapshot after changing settings. Custom
names, callsign, logbook, credentials, device IDs and paths are excluded.

The receive snapshot contains mode, sample rate, filter, AGC, noise blankers
and reducers, EQ and CW DSP settings. It excludes the tuned frequency, station
identity, hardware identity and audio or IQ. Share it to ask a client to
explain an RX signal chain or propose a reversible listening comparison.

A shared take is an explicit copy of up to eight seconds of voice in the local
account's application support directory. The tool accepts two to four draft
trials and returns metrics. It offers no file paths or audio playback to the
client. Use the Lab window to listen. Stopping the share removes the local
copy, and the app cleans up expired audio. Trials support a built-in SSB
profile, optional graphic or parametric EQ, and an optional single-band
compressor override. Use the Lab's **Audition Recipe** to play those settings
on your local take.

A waterfall case returns intervals around a marked glitch, with drawable
acquisition, busy Metal staging skips, spectrum rows, link sequence and
audio counter changes. The
receive watch summary carries detection counts and up to 20 peaks. It
excludes IQ, recording names and file paths. Sharing a summary does not start
or extend a watch.

Each source window can revoke its own share. **Settings → Local MCP**
shows active shares with their expiry times and offers **Stop All Sharing**. Revocation
and expiry prevent further reads by the helper. A client may retain or send
data it previously received according to its own settings.

The server also offers prompt templates for SSB review, waterfall diagnosis,
replay scan interpretation and receive watch summaries. Ask for one proposed
adjustment and one way to compare it, with the evidence labeled. Tools can
analyze a copy or render an offline trial. HermitSDR has no MCP tool to apply
a setting, tune, arm or transmit.
