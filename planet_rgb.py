from glob import glob
import rasterio 
import numpy as np
#from xml.dom import minidom
import os

# Funcion que crear un compuesto RGB de Planet con las bandas como dataset de rasterio
def rgb(line, file, bands, rgb_name, pathOutput):
    ds = rasterio.open(file)
    r = ds.read(bands[0])
    g = ds.read(bands[1])
    b = ds.read(bands[2])
    rgb = np.dstack((r , g , b))
    print(rgb)
    print(ds.width, ds.height)
    print(ds.bounds)
    print(type(ds.bounds))

    # Normaliza los valores de las bandas a 0-255
    rgb = (rgb/rgb.max())*255
    rgb = rgb.astype(np.uint8)

    # Copiar los metadatos del dataset original
    kwargs = ds.meta
    kwargs.update(
        dtype=rasterio.uint8,
        count=3,
        compress='lzw')
    
    # Guardar el compuesto RGB
    lineDir = line.split('/')[-1]
    os.system('mkdir '+pathOutput+rgb_name+'/'+lineDir)
    name = file.split('/')[-1].split('.')[0]+'_planet_' +rgb_name+'.tif'
    with rasterio.open(os.path.join(pathOutput+rgb_name+'/'+lineDir, name), 'w', **kwargs) as dst:
        dst.write(rgb.astype(rasterio.uint8))

# Funcion que crear los compuestos RGB de Planet
def planetRGB(lines, bands, rgb_name, pathOutput):
    for line in lines:
        #filesMeta = glob(line+'/'+'*.xml')
        files = glob(line+'/'+'*harmonized*.tif')
        #filesMeta.sort()
        files.sort()
        for file in files:
            print('Procesando: ' + file)

            # Crear compuesto RGB
            rgb(line, file, bands, rgb_name, pathOutput)

# Funncion principal
def main():
    # Parametros
    pathInputPlanet = '/data/input/probosque/PLANET2022/'
    pathOutput = '/data/output/probosque/'

    # Enlistar las lineas
    lines = glob(pathInputPlanet+'*')
    print(lines)

    # Crear compuestos RGB
    bands = {'true_color': [6,4,2], 'false_color': [8,6,4], 'nir_color': [1,8,6]}
    for rgb_name, band in bands.items():
        print('Creando compuesto RGB: ' + rgb_name)
        planetRGB(lines, band, rgb_name, pathOutput)

# Ejecutar funcion principal
if __name__ == "__main__":
    main()








