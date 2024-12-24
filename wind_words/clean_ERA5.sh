#!/bin/bash

# Make the ERA5 .nc files iris-compatible
#  That is, delete the 'expver' variable

ncks -C -x -v expver Wind_2024120706.nc Wind_2024120706_no_expver.nc

