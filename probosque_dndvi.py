import funtions
from glob import glob
import rasterio 
import numpy as np

pathInputPlanet = '/data/input/probosque/PLANET2022/'
pathOutput = '/data/output/probosque/'

lines = glob(pathInputPlanet+'*')

print(lines)

for line in lines:
    filesMeta = glob(line+'/'+'*_metadata.xml')
    files = glob(line+'/'+'*_harmonized.tif')
    filesMeta.sort()
    files.sort()
    for fileMeta,file in zip(filesMeta,files):
        print(fileMeta)
        print(file)

        ds = rasterio.open(file)
        band6 = ds.read(6)
        band8 = ds.read(8)

        print(band6)
        print(band8)
        print(ds.width, ds.height)






