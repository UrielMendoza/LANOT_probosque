import funtions
from glob import glob
import rasterio 
import numpy as np
from xml.dom import minidom
import os

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
        print('Meta: '+fileMeta)

        meta = minidom.parse(fileMeta)
        radioSF_b6 = float(meta.getElementsByTagName('ps:radiometricScaleFactor')[5].firstChild.data)
        radioSF_b8 = float(meta.getElementsByTagName('ps:radiometricScaleFactor')[7].firstChild.data)
        refleSF_b6 = float(meta.getElementsByTagName('ps:reflectanceCoefficient')[5].firstChild.data)
        refleSF_b8 = float(meta.getElementsByTagName('ps:reflectanceCoefficient')[7].firstChild.data)

        ds = rasterio.open(file)
        b6 = ds.read(6) * radioSF_b6
        b8 = ds.read(8) * radioSF_b8
        ndvi = (b8 - b6) / (b8 + b6)

        print(ndvi)
        print(ds.width, ds.height)

        kwargs = ds.meta
        kwargs.update(
            dtype=rasterio.float32,
            count=1,
            compress='lzw')

        name = file.split('/')[-1].split('.')[0]+'_ndvi.tif'

        with rasterio.open(os.path.join(pathOutput, name), 'w', **kwargs) as dst:
            dst.write_band(1, ndvi.astype(rasterio.float32))






