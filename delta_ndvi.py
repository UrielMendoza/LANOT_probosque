
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
        dndvi_mean = np.nanmean(dndvi)

        print('Delta NDVI')
        print(dndvi)
        print('Desviacion estandar')
        print(dndvi_std)
        print('Media')
        print(dndvi_mean)

        kwargs = ds_planet.meta
        kwargs.update(
            dtype=rasterio.float32,
            count=1,
            compress='lzw')      

        lineDir = lineSpot.split('/')[-1]

        os.system('mkdir '+pathOutput+lineDir) 
        name = '_'.join(fileSpot.split('/')[-1].split('.')[0].split('_')[:-2])+'_dndvi.tif'

        with rasterio.open(os.path.join(pathOutput+lineDir, name), 'w', **kwargs) as dst:
            dst.write_band(1, dndvi.astype(rasterio.float32))

        #dndvi_class = dndvi.copy()
            
        os.system('mkdir '+pathOutputClass+lineDir) 
        
        for i in range(1,4):
            inter1 = str(dndvi_mean - (dndvi_std*i))
            inter2 = str(dndvi_mean + (dndvi_std*i))

            name_class = '_'.join(fileSpot.split('/')[-1].split('.')[0].split('_')[:-2])+'_'+str(i)+'_dndvi.tif'

            os.system('gdal_calc.py --overwrite -A '+pathOutput+lineDir+'/'+name+' --outfile='+pathOutputClass+lineDir+'/'name_class+' --calc="-1*(A<'+inter1+')+0*(A*logical_and(A>='+inter1+',A<='+inter2+'))+1*(A>'+inter2+')"')



"""             for i in range(1,4):
                dndvi_class[np.where(dndvi_class < (dndvi_mean - dndvi_std*i))] = -1
                dndvi_class[np.where((dndvi_class >= (dndvi_mean - dndvi_std*i)) & (dndvi_class <= (dndvi_mean + dndvi_std*i)))] = 0
                dndvi_class[np.where(dndvi_class > (dndvi_mean + dndvi_std*i))] = 1
                
                name = fileSpot.split('/')[-1].split('.')[0]+'_class_'+str(i)+'sd_dndvi.tif'

                with rasterio.open(os.path.join(pathOutputClass+lineDir, name), 'w', **kwargs) as dst:
                    dst.write_band(1, dndvi_class.astype(rasterio.int16)) 
                                        
                with rasterio.open(os.path.join(pathOutputClass+lineDir, name), 'w', **kwargs) as dst:
                    dst.write_band(1, dndvi_class.astype(rasterio.int16))
                    
                for i in range(dndvi.shape[0]):
                    for j in range(dndvi.shape[1]):
                        if (dndvi[i,j] <= (dndvi_mean - dndvi_std*3)):
                            dndvi_class[i,j] = -3
                        elif (dndvi[i,j] <= (dndvi_mean - dndvi_std*2)) and (dndvi[i,j] >= (dndvi_mean - dndvi_std*3)):
                            dndvi_class[i,j] = -2
                        elif (dndvi[i,j] <= (dndvi_mean - dndvi_std*1)) and (dndvi[i,j] >= (dndvi_mean - dndvi_std*2)):
                            dndvi_class[i,j] = -1
                        elif (dndvi[i,j] >= (dndvi_mean - dndvi_std*1)) and (dndvi[i,j] <= (dndvi_mean + dndvi_std*1)):
                            dndvi_class[i,j] = 0
                        elif (dndvi[i,j] >= (dndvi_mean + dndvi_std*3)):
                            dndvi_class[i,j] = 3
                        elif (dndvi[i,j] >= (dndvi_mean + dndvi_std*2)) and (dndvi[i,j] <= (dndvi_mean + dndvi_std*3)):
                            dndvi_class[i,j] = 2
                        elif (dndvi[i,j] >= (dndvi_mean + dndvi_std*1)) and (dndvi[i,j] <= (dndvi_mean + dndvi_std*2)):
                            dndvi_class[i,j] = 1
                        else:
                            dndvi_class[i,j] = 0

"""










