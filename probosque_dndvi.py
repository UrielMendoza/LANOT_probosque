import funtions
from glob import glob

pathInputPlanet = '/data/input/probosque/PLANET2022/'
pathOutput = ''

lines = glob(pathInputPlanet+'*')

for line in lines:
    files = glob(pathInputPlanet+'*_harmonized.tif')
    for file in files:
        print(file)



