import os
from pathlib import Path
from glob import glob

def createMosaic(pathInput,nombre,pathOutput):
    
    lines = glob(pathInput+'*')

    mosaicos = ''

    for line in lines:
        for path in Path(line).rglob('*.tif'):
            print(path, type(path))
            mosaicos += str(path) + ' '    

    nomMosaicTif = pathOutput+nombre+'.tif'

    # Mosaico con fecha
    os.system('gdal_merge.py -n nan -o '+pathOutput+nombre+'_tmp.tif '+mosaicos)
    # Optimiza el geotiff
    os.system('gdal_translate -CO "TILED=YES" -CO "BLOCKXSIZE=512" -CO "BLOCKYSIZE=512" -CO "BIGTIFF=YES" '+pathOutput+nombre+'_tmp.tif '+nomMosaicTif)
    os.system('gdaladdo -r average '+nomMosaicTif+' 2 4 8 16 32')

def createMosaicClass(pathInput,nombre,sd,pathOutput):
    
    lines = glob(pathInput+'*')

    mosaicos = ''

    for line in lines:
        for path in Path(line).rglob('*'+sd+'*.tif'):
            print(path, type(path))
            mosaicos += str(path) + ' '    

    nomMosaicTif = pathOutput+nombre+'.tif'

    # Mosaico con fecha
    os.system('gdal_merge.py -n nan -o '+pathOutput+nombre+'_tmp.tif '+mosaicos)
    # Optimiza el geotiff
    os.system('gdal_translate -CO "TILED=YES" -CO "BLOCKXSIZE=512" -CO "BLOCKYSIZE=512" -CO "BIGTIFF=YES" '+pathOutput+nombre+'_tmp.tif '+nomMosaicTif)
    os.system('gdaladdo -r average '+nomMosaicTif+' 2 4 8 16 32')

pathInputPlanet = '/data/output/probosque/planet_ndvi/'
pathInputSpot = '/data/output/probosque/spot_ndvi/'
#pathInputDelta = '/data/output/probosque/planet_ndvi/'
#pathInputDeltaClass = '/data/output/probosque/planet_ndvi/'

pathOutput = '/data/output/probosque/mosaicos/'

createMosaic(pathInputPlanet,'planet_ndvi_2022',pathOutput)
createMosaic(pathInputSpot,'spot_ndvi_2015',pathOutput)
