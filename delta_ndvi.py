import funtions
from glob import glob
import rasterio 
import numpy as np
from xml.dom import minidom
import os

pathInputSpot = '/data/output/probosque/spot_ndvi/'
pathInputPlanet = '/data/output/probosque/planet_ndvi/'
pathOutput = '/data/output/probosque/delta_ndvi/'
pathOutputClass = '/data/output/probosque/delta_class_ndvi/'

linesSpot = glob(pathInputSpot+'*')
linesPlanet = glob(pathInputPlanet+'*')

#print(lines)

for lineSpot, linePlanet in zip(linesSpot, linesPlanet):
    filesSpot = glob(lineSpot+'/'+'*_ndvi.tif')
    filesPlanet = glob(linePlanet+'/'+'*_ndvi.tif')

    filesSpot.sort()
    filesPlanet.sort()

    for fileSpot, filePlanet in zip(filesSpot, filesPlanet):
        print('Procesando: '+fileSpot)
        print('Procesando: '+filePlanet)

        ds_spot = rasterio.open(fileSpot)
        ds_planet = rasterio.open(filePlanet)

        ndvi_spot = ds_spot.read(1) 
        ndvi_planet = ds_planet.read(1)
        
        print(ndvi_spot)
        print(ndvi_planet)

        dndvi = ndvi_spot - ndvi_planet 
        dndvi_std = np.nanstd(dndvi)

        print('Delta NDVI')
        print(dndvi)
        print('Desviacion estandar')
        print(dndvi_std)

        dndvi_class = np.where(dndvi < dndvi_std, 1, dndvi)
        dndvi_class = np.where(dndvi_class < dndvi_std, 2, dndvi_class) 
        dndvi_class = np.where(dndvi_class < dndvi_std, 3, dndvi_class) 

        kwargs = ds_planet.meta
        kwargs.update(
            dtype=rasterio.float32,
            count=1,
            compress='lzw')      

        lineDir = lineSpot.split('/')[-1]

        os.system('mkdir '+pathOutput+lineDir) 
        name = fileSpot.split('/')[-1].split('.')[0]+'_dndvi.tif'

        with rasterio.open(os.path.join(pathOutput+lineDir, name), 'w', **kwargs) as dst:
            dst.write_band(1, dndvi.astype(rasterio.float32))

        os.system('mkdir '+pathOutputClass+lineDir) 
        name = fileSpot.split('/')[-1].split('.')[0]+'_class_dndvi.tif'

        with rasterio.open(os.path.join(pathOutputClass+lineDir, name), 'w', **kwargs) as dst:
            dst.write_band(1, dndvi_class.astype(rasterio.float32))







