# Heard by: where is my signal being received?

The Stations Heard map shows what your antenna hears. The **Heard by** layer
shows the other direction: stations that reported receiving *your* callsign,
drawn on the same map with a great-circle path from your grid to each of them.

It is information only. Nothing here transmits, keys the radio or changes
anything about how you transmit; it looks at reports other stations published
after you transmitted — from this app or from any other radio using your
callsign.

## Turning it on

1. Set your callsign and grid in **Settings › Station**.
2. Open the Stations Heard map (the globe button in the FT8 panel).
3. Tick **Heard by** in the layer bar. This alone collects spots of your
   callsign from DX-cluster / RBN nodes you have already connected.
4. Click the small chart button next to it to open the panel, and tick
   **Ask PSK Reporter** if you also want PSK Reporter's reports.

Both switches are off until you turn them on, and they are remembered.

## What you see

- **On the map:** a diamond at each reporter, coloured by band, with a dashed
  path from your grid (the Paths checkbox hides the paths). Hover a diamond
  for the band, mode, signal report, distance, bearing and age. A hollow
  diamond means the position is only the reporter's country.
- **Show the last:** 15 minutes to 6 hours. Older reports fade, then drop off.
- **In the panel:**
  - reporters per band over the last hour, the farthest report and the best
    signal report on each band;
  - a polar plot — every reporter by direction (north up) and distance. A
    gap in one direction over several sessions says something about your
    antenna or your horizon;
  - the list of reports, newest first;
  - **Export CSV…** saves every stored report (up to six hours): time (UTC),
    source, reporter, locator, band, frequency, mode, signal report, distance,
    bearing, and whether the position is a locator or only a country.

The status line says how old the PSK Reporter data is and when the next query
is due. After an error it shows the error, keeps the reports it already has,
and waits longer before trying again.

## Where the reports come from

| Source | What is contacted | Position of the reporter |
| --- | --- | --- |
| PSK Reporter | One HTTPS request to `retrieve.pskreporter.info`, at most every 5 minutes | The reporter's own locator |
| RBN (skimmers) | Nothing extra: spots of your callsign from cluster nodes already connected in the DX Cluster window | Its country only, unless PSK Reporter also knows its locator |
| DX cluster (human spots) | Nothing extra, as above | As above |

To see RBN reports, connect an RBN node in the DX Cluster window (for example
the "RBN — CW/RTTY skimmers" preset) and call CQ on CW or RTTY.

WSPRnet is not queried. WSPR reports that monitors also send to PSK Reporter
do appear, tagged WSPR.

## Privacy

- Off by default.
- The PSK Reporter request contains your public callsign and nothing else
  about you or the station: no grid, no frequency, no account, no cookie. The
  request names the app ("HermitSDR") as its user agent. Like any web server,
  PSK Reporter sees your IP address.
- No request is made while **Heard by** or **Ask PSK Reporter** is off, or
  while no callsign is set.
- Reports are kept in memory for up to six hours and are written to disk only
  when you export them.

## How often PSK Reporter is asked

PSK Reporter asks applications to retrieve data no more often than once every
five minutes (https://pskreporter.info/pskdev.html). HermitSDR never asks more
often than that, whatever you click: the **Refresh** button, switching the
layer off and on, changing the callsign and restarting the app all share the
same five-minute spacing. After a failed query the wait doubles each time (10,
20, 40 minutes … up to two hours) and returns to five minutes after the next
success.

Reports reach PSK Reporter a few minutes after monitors decode you, so expect
the first ones about five minutes after you transmit.

## Limits

- At most 500 reports per query, covering the last hour; 300 pins on the map.
- A reporter that sent no locator is listed in the panel without a pin.
- Cluster spotters are placed at their country's reference point, which is
  rough for large countries.
