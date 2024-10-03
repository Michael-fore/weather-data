# weather-data
Supposed to make some publicly available weather data a bit easier to use.


## Methodology
- very much subject to change as I have no idea what I am doing
Go from source file to parquet, where the file path has the location, time of prediction, resolution, then the actualy file saved as a parquet.

There will be a ledger folder to track each run and keep a running hash of all of the files.

## NOAA NBM DATA
`https://noaa-nbm-grib2-pds.s3.amazonaws.com/index.html`

NBM format: `blend.tCCz.core.fXXX.RR.grib2` where CC is the cycle, XXX is the forcast hour, RR is the region.
file format `blend.t00z.master.f001.ak.grib2` 