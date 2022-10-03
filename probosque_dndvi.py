import tools
from glob import glob

pathInputPlanet = '/data/input/probosque/PLANET2022/'
pathOutput = ''

files = glob(pathInputPlanet+'*_harmonized.tif')

for file in files:
    print(file)

    

