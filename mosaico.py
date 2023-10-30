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
    os.system('gdal_merge.py -ot Int32 -n nan -o '+pathOutput+nombre+'_tmp.tif '+mosaicos)
    # Optimiza el geotiff
    os.system('gdal_translate -CO "TILED=YES" -CO "BLOCKXSIZE=512" -CO "BLOCKYSIZE=512" -CO "BIGTIFF=YES" '+pathOutput+nombre+'_tmp.tif '+nomMosaicTif)
    os.system('gdaladdo -r average '+nomMosaicTif+' 2 4 8 16 32')

pathInputPlanet = '/datawork/planet/acapulco/ndwi_20230819/'
pathInputSpot = '/data/output/probosque/spot_ndvi/'
pathInputDelta = '/data/output/probosque/delta_ndvi/'
pathInputDeltaClass = '/data/output/probosque/delta_class_ndvi/'

pathOutput = '/datawork/planet/acapulco/mosaicos/'

createMosaic(pathInputPlanet,'planet_ndwi_acapulco_20230819',pathOutput)
#createMosaic(pathInputSpot,'spot_ndvi_2015',pathOutput)
#createMosaic(pathInputDelta,'spot_planet_dndvi',pathOutput)
#createMosaicClass(pathInputDeltaClass,'spot_planet_dndvi_1sd','1sd',pathOutput)
#createMosaicClass(pathInputDeltaClass,'spot_planet_dndvi_2sd','2sd',pathOutput)
#createMosaicClass(pathInputDeltaClass,'spot_planet_dndvi_3sd','3sd',pathOutput)
