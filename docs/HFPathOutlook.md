# HF Path Outlook

**Log → HF Path Outlook** shows a locally computed or otherwise supplied
model result by frequency and UTC hour. It keeps the model name and version,
transmitting and receiving endpoints, model month, power, antenna, noise
and solar assumptions visible. Missing cells show a dash. An old modeled
month remains available for review with a past-month label.

An outlook is a prediction for the model's time period and assumptions.
It cannot establish that a station is transmitting or audible now. Open **Related Cluster Reports** to show recent reports of an exact callsign
on the modeled amateur bands. These reports describe observations from their
reported spotters. The calendar keeps announced windows separately.

The ITU's [P.533 recommendation](https://www.itu.int/rec/R-REC-P.533/en)
defines the prediction method. The [ITU study group's reference implementation](https://github.com/ITU-R-Study-Group-3/ITU-R-HF)
can generate point-to-point reports. HermitSDR imports results and includes
no model executable, code or ionospheric coefficient data. The reference
repository contains a permission notice in its source and lacks a separate
SPDX license in its repository metadata. Review its terms and dependencies
before redistributing a build or model data.

1. Choose **Export P.533 Input…** in HermitSDR. The station profile grid
   and a second grid provide the two endpoints. Choose the direction,
   model month, smoothed sunspot number R12 and assumed transmit power.
   The template uses isotropic antennas, rural noise, 2.4 kHz analog
   bandwidth, short-path geometry, and nine frequencies for all 24 UTC
   hours. Its inputs use the grid centers.
2. Set `DataFilePath` in the exported input to the coefficient data
   directory of your separately installed solver. Review the assumptions,
   including that R12 belongs to the modeled month. Run the solver with
   the -c flag for CSV output.

       ITURHFProp -c hermitsdr-path.in report.csv

3. Convert the actual input and result together.

       python3 tools/ituhfprop-to-outlook.py path.in report.csv --model-version 14.2 > outlook.json

   Use the version printed by your run. Add --generated-at with the actual
   ISO 8601 run time if known. Use --solar-index-month YYYY-MM when the R12
   data month is known. The app flags a month that differs from the forecast
   month and labels missing R12 date provenance. The converter keeps the report's 01–24 UTC
   hour labels. It checks the month, endpoint geometry and metric ranges.
   CSV frequencies are rounded. The converter recovers each exact configured
   frequency from the original input and rejects ambiguous or missing cells.
4. Choose **Import Outlook** in HermitSDR. The app keeps one cache in the
   station profile. **Clear** removes that cached result.

Agents can validate a generated result before import with the app's
--hermit-check-outlook command. The import format requires provenance, both
endpoints and the assumptions shown above, plus up to 16 frequencies and one
value per UTC hour and frequency. The command emits validated results as JSON.
