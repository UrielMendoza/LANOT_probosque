from glob import glob
import rasterio 
import numpy as np
from xml.dom import minidom
import os

pathInput = '/data/output/probosque/planet_ndvi/'
pathOutput = '/data/output/probosque/spot_ndvi/'
pathInputSPOT = '/data/input/probosque/mosaico_ndvi_2015/ndvi_mosaico_2015_3m.tif'

lines = glob(pathInput+'*')

#print(lines)

for line in lines:
    files = glob(line+'/'+'*_ndvi.tif')
    files.sort()
    for file in files:
        print('Procesando: '+file)

        ds = rasterio.open(file)
        ndvi = ds.read(1) 
        
        print(ndvi)
        print(ds.width, ds.height)

        left, bottom, right, top = ds.bounds.left, ds.bounds.bottom, ds.bounds.right, ds.bounds.top

        print(left, bottom, right, top)

        lineDir = line.split('/')[-1]
        os.system('mkdir '+pathOutput+lineDir) 
        name = file.split('/')[-1].split('.')[0]+'_spot_ndvi.tif'

        os.system('gdal_translate -a_nodata 0 -projwin '+str(left)+' '+str(top)+' '+str(right)+' '+str(bottom)+' '+pathInputSPOT+' '+pathOutput+lineDir+'/'+name)







