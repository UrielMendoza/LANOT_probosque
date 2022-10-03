import funtions
from glob import glob
import rasterio 
import numpy as np

pathInputPlanet = '/data/input/probosque/PLANET2022/'
pathOutput = '/data/output/probosque/'

lines = glob(pathInputPlanet+'*')

print(lines)

for line in lines:
    files = glob(line+'/'+'*_harmonized.tif')
    for file in files:
        ds = rasterio.open(file)
        band6 = ds.read(6)
        band8 = ds.read(8)

        print(band6)
        print(band8)






