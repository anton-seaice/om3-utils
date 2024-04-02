"""
Script: cice_grid.py
Description: 
This script generates a CICE grid from the MOM super grid provided in the input NetCDF file.

Usage:
python cice_grid.py <ocean_hgrid> <ocean_hgrid>
- ocean_hgrid: Path to the MOM super grid NetCDF file.
- ocean_mask: Path to the corresponding mask NetCDF file.

"""


#!/usr/bin/env python3
# File based on https://github.com/COSIMA/access-om2/blob/29118914d5224152ce286e0590394b231fea632e/tools/make_cice_grid.py

import sys
# import os
import argparse

# my_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(my_dir, 'esmgrids'))

# print(sys.path)

from .esmgrids.esmgrids.mom_grid import MomGrid  # noqa
from .esmgrids.esmgrids.cice_grid import CiceGrid  # noqa
from .utils import Md5sum

class cice_grid_from_mom() :

    """
    Create CICE grid.nc and kmt.nc from MOM ocean_hgrid.nc and ocean_mask.nc
    """

    def run(self, ocean_hgrid, ocean_mask):

    
        mom = MomGrid.fromfile(ocean_hgrid, mask_file=ocean_mask)

        cice = CiceGrid.fromgrid(mom)

        # grid_file = os.path.join('grid.nc')
        # mask_file = os.path.join('kmt.nc')

        cice.create_gridnc('grid.nc')

        # Add versioning information    
        cice.grid_f.inputfile = f"{ocean_hgrid}"
        cice.grid_f.inputfile_md5 = Md5sum(ocean_hgrid).sum
        cice.grid_f.history_command = f"python make_CICE_grid.py {ocean_hgrid} {ocean_mask}"

        #Add the typical crs (i.e. WGS84/EPSG4326 , but in radians).
        crs = cice.grid_f.createVariable('crs', 'S1')
        crs.grid_mapping_name = "tripolar_latitude_longitude"
        crs.crs_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["radians",1,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]'

        cice.write()

        cice.create_masknc('kmt.nc')

        # Add versioning information    
        cice.mask_f.inputfile = f"{ocean_mask}"
        cice.mask_f.inputfile_md5 = Md5sum(ocean_mask).sum
        cice.mask_f.history_command = f"python make_CICE_grid.py {ocean_hgrid} {ocean_mask}"

        #Add the typical crs (i.e. WGS84/EPSG4326 , but in radians).
        crs = cice.mask_f.createVariable('crs', 'S1')
        crs.grid_mapping_name = "tripolar_latitude_longitude"
        crs.crs_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["radians",1,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]'

        cice.write_mask()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('ocean_hgrid', help='ocean_hgrid.nc file')
    parser.add_argument('ocean_mask', help='ocean_mask.nc file')
    #add argument for CRS?

    args = vars(parser.parse_args())

    grid = cice_grid_from_mom()

    sys.exit(grid.run(**args))
