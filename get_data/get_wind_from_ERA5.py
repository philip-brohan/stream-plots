#!/usr/bin/env python

# Retrieve ERA5 10m winds for a single hour

import os
import cdsapi
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=False, default=2018)
parser.add_argument("--month", help="Month", type=int, required=False, default=3)
parser.add_argument("--day", help="Day", type=int, required=False, default=12)
parser.add_argument("--hour", help="Hour", type=int, required=False, default=15)
parser.add_argument(
    "--opdir",
    help="Directory for output files",
    default="%s/ERA5/hourly/reanalysis" % os.getenv("SCRATCH"),
)
args = parser.parse_args()
args.opdir += "/%04d/%02d/%02d/%02d" % (args.year, args.month, args.day, args.hour)
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir, exist_ok=True)


ctrlB = {
    "format": "netcdf",
    "product_type": "reanalysis",
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
    ],
    "year": ["%04d" % args.year],
    "month": ["%02d" % args.month],
    "day": ["%02d" % args.day],
    "time": ["%02d:00" % args.hour],
}

c = cdsapi.Client()
c.retrieve(
    "reanalysis-era5-single-levels",
    ctrlB,
    "%s/%s.nc" % (args.opdir, '10m_wind'),
)
