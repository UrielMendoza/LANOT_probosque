from glob import glob
import rasterio 
import numpy as np
#from xml.dom import minidom
import os

# Funcion que pasa a tif un ds de rasterio y un numpy array
def toTif(name, array, ds, pathOutput):
    kwargs = ds.meta
    kwargs.update(
        dtype=rasterio.uint8,
        count=1,
        compress='lzw')
    
    name = os.path.join(pathOutput, name + '.tif')
    with rasterio.open(name, 'w', **kwargs) as dst:
        dst.write_band(1, array.astype(rasterio.uint8))

    return name

# Funcion que crea el RGB con GDAL
def gdalRGB(line, file, bands, rgb_name, pathOutput):
    ds = rasterio.open(file)
    r = ds.read(bands[0])
    g = ds.read(bands[1])
    b = ds.read(bands[2])    
    
    # Verificar y ajustar las dimensiones de las bandas si es necesario
    if r.shape != g.shape or r.shape != b.shape:
        raise ValueError("Las dimensiones de las bandas no son consistentes")
    
    # Convierte a tif cada banda
    r_file = toTif('r', r, ds, './')
    g_file = toTif('g', g, ds, './')
    b_file = toTif('b', b, ds, './')
    
    # Guardar el compuesto RGB
    lineDir = line.split('/')[-1]
    os.makedirs(os.path.join(pathOutput, rgb_name, lineDir), exist_ok=True)
    name = file.split('/')[-1].split('.')[0] + '_planet_' + rgb_name + '.tif'
    
    # Ejecutar el comando de gdal_merge
    os.system('gdal_merge.py -separate -co PHOTOMETRIC=RGB -o '+name+' '+r_file+' '+g_file+' '+b_file)

    # Borrar los archivos temporales
    os.system('rm '+r_file+' '+g_file+' '+b_file)



# Funcion que crea los compuestos RGB con las bandas de Planet
def rgb(line, file, bands, rgb_name, pathOutput):
    ds = rasterio.open(file)
    r = ds.read(bands[0]) * 0.01
    g = ds.read(bands[1]) * 0.01
    b = ds.read(bands[2]) * 0.01
    
    # Verificar y ajustar las dimensiones de las bandas si es necesario
    if r.shape != g.shape or r.shape != b.shape:
        raise ValueError("Las dimensiones de las bandas no son consistentes")
    
    rgb = np.dstack((r , g , b))
    rgb = (rgb / rgb.max()) * 255
    rgb = rgb.astype(np.uint8)
    # Aplica una correccion gamma
    rgb = np.power(rgb, 1/2.2)

    kwargs = ds.meta
    kwargs.update(
        dtype=rasterio.uint8,
        count=3,
        compress='lzw')
    
    # Guardar el compuesto RGB
    lineDir = line.split('/')[-1]
    os.makedirs(os.path.join(pathOutput, rgb_name, lineDir), exist_ok=True)
    name = file.split('/')[-1].split('.')[0] + '_planet_' + rgb_name + '.tif'    
    with rasterio.open(os.path.join(pathOutput, rgb_name, lineDir, name), 'w', **kwargs) as dst:
        dst.write(rgb.transpose(2, 0, 1).astype(rasterio.uint8))

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
            #gdalRGB(line, file, bands, rgb_name, pathOutput)

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








