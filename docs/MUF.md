# MUF chip

The header (and the console's bottom status strip) shows a **MUF** chip
beside Kp and SFI: the maximum usable frequency over your station grid,
taken from ionosonde soundings of the past hour. It is receive-side only.
Nothing in it can key, arm or tune the radio.

## Setting it up

1. Open **Settings › Station** and enter your Maidenhead **Grid** (four or
   six characters, for example `FN31`). This is the same grid the logbook,
   PSKReporter and the maps use.
2. **Show MUF for my grid beside Kp and SFI** is on by default. Switch it
   off to remove the chip and stop the downloads. The line under the
   switch shows the current reading and the nearest ionosonde.

Without a grid the chip reads `MUF —` and no request is made.

## What the number means

`MUF 28.1` is MUF(3000)F2 in MHz: the highest frequency the F2 layer is
returning on a 3000 km hop whose midpoint is over your grid. Frequencies
below it can make that hop; frequencies above it pass through. Shorter
paths have a lower MUF, and on a multi-hop path the lowest MUF along the
route decides.

The hover text also gives:

- the highest amateur band that lies wholly below the MUF,
- **foF2**, the frequency below which a signal sent straight up comes back
  (the ceiling for NVIS),
- each ionosonde used, with its own MUF, its distance and the UTC time of
  its sounding.

The chip has no good/bad colour. It reports a measurement, not a forecast.

## Where the number comes from

Every 15 minutes HermitSDR downloads one public list,
`https://prop.kc2g.com/api/stations.json?maxage=3600`: the newest sounding
of every ionosonde that reported in the past hour (about 10 KB). The
soundings are made by the observatories of the Global Ionospheric Radio
Observatory (GIRO) and INGV's eSWua network and collected by Andrew
Rodland, KC2G, for his propagation maps.

The request is a fixed HTTPS `GET`. It carries no grid, callsign,
frequency or audio. The whole list is downloaded and the soundings
nearest your grid are chosen on your Mac.

From that list HermitSDR:

1. drops soundings older than 60 minutes, soundings whose autoscaling
   confidence is below 50, and values outside 2–60 MHz;
2. counts two instruments at one site once (the newer sounding);
3. takes up to four ionosondes within 3000 km of your grid centre;
4. averages their MUF weighted by confidence ÷ distance², so a sounder
   close to you dominates and sounders at similar range share.

## When there is no number

| Chip | Reason |
| --- | --- |
| `MUF —`, "needs your location" | No valid grid in Settings › Station. |
| `MUF —`, "waiting" | The first download has not finished. |
| `MUF —`, "could not be read" | The download failed. Soundings already held are used until they are an hour old; the next try is in 15 minutes. |
| `MUF —`, "nearest ionosonde … km away" | No ionosonde within 3000 km reported in the past hour. The hover text names the nearest one and its MUF, but the chip shows no number: the ionosphere that far away is a different sky. |

Ionosondes are sparse. Europe, eastern North America, Australia and parts
of South America and southern Africa are covered most hours; the western
United States, most of Asia, Africa and the oceans often are not. The
last row of the table is the normal state there.

## Limits

- The blend is a distance-weighted average of real soundings. It is not
  an ionospheric model and does not allow for the day/night boundary
  between you and a sounder.
- An ionosonde can report sporadic-E or a disturbed layer; the soundings
  are shown as received above the confidence limit.
- For a specific path and hour use **Log → HF Path Outlook**.
