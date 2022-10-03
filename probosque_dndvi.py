import funtions
from glob import glob
import rasterio 
import numpy as np
from xml.dom import minidom

pathInputPlanet = '/data/input/probosque/PLANET2022/'
pathOutput = '/data/output/probosque/'

lines = glob(pathInputPlanet+'*')

#print(lines)

for line in lines:
    filesMeta = glob(line+'/'+'*_metadata.xml')
    files = glob(line+'/'+'*_harmonized.tif')
    filesMeta.sort()
    files.sort()
    for fileMeta,file in zip(filesMeta,files):
        print('Porcesando: '+file)

        meta = minidom.parse(fileMeta)
        radioSF_b6 = meta.getElementsByTagName('ps:radiometricScaleFactor')[5].firstChild.data
        radioSF_b8 = meta.getElementsByTagName('ps:radiometricScaleFactor')[7].firstChild.data
        refleSF_b6 = meta.getElementsByTagName('ps:reflectanceCoefficient')[5].firstChild.data
        refleSF_b8 = meta.getElementsByTagName('ps:reflectanceCoefficient')[7].firstChild.data
        print(radioSF_b6)
        print(radioSF_b6)
        print(refleSF_b8)
        print(refleSF_b8)

        ds = rasterio.open(file)
        band6 = ds.read(6)
        band8 = ds.read(8)


        print(band6)
        print(band8)
        print(ds.width, ds.height)






