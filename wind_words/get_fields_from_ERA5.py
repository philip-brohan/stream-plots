#!/usr/bin/env python

# Retrieve surface weather variables from ERA5
#  for one hour.

import cdsapi

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": ["10m_u_component_of_wind", "10m_v_component_of_wind"],
    "year": ["2024"],
    "month": ["12"],
    "day": ["7"],
    "time": ["06:00"],
    "data_format": "netcdf",
    "download_format": "unarchived",
}
client = cdsapi.Client()
client.retrieve(dataset, request, "Wind_2024120706.nc")
