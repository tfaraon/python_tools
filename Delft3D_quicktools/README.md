In this folder are stored some scripts made to create some create and read Delft3D files.

#CREATING/

create_lake.py  --> is made to create all the file (bathy, grid, enclosure) to launch a D3D simulation. Here is a simple example on a circular lake with max depth in the center. 

#READING/

Basically it extracts Netcdf data and allows it to be stored in python vars.

To use it, just work in D3D_output_main.py and use the modules FLOW and WAVE readers.
