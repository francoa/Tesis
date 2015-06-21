# Importar los modulos ovito
from ovito.io import *
from ovito.modifiers import *

# Importar numpy
import numpy

# Importar trayectoria lammps
node = import_file("../Dataset/dataset_muestraPorosa/MuestraPorosa_0.lammpstrj")

# Setear los modificadores
## 1 modificador surface mesh
mod_surfaceMesh = ConstructSurfaceModifier(radius = 2.5)
node.modifiers.append(mod_surfaceMesh)
## 2 modificador atomic strain
mod_atomicStrain = AtomicStrainModifier(
	cutoff = 5.0,
	eliminate_cell_deformation = True
)
mod_atomicStrain.reference.load("../Dataset/dataset_muestraPorosa/MuestraPorosa_0.lammpstrj")
node.modifiers.append(mod_atomicStrain)

# Obtener numero de particulas
numofParticles = node.source.data['Position'].size

# Funcion de calculo de numero de atomos superando umbral
def atomic_strain(shearStrain,umbral):
	conteo = 0
	for i in shearStrain:
		if i>umbral:
			conteo=conteo+1
	return conteo

# Archivo de salida
outFile = open('Ovito_scriptDePrueba.out', 'w')

# Loop de computo
for frame in range(0, ovito.dataset.anim.last_frame + 1):

	ovito.dataset.anim.current_frame = frame

	node.compute()

	svf = mod_surfaceMesh.solid_volume/mod_surfaceMesh.total_volume
	conteo = atomic_strain(node.output["Shear Strain"].array,0.2)

	outFile.write('%.3f\t%.3f\t%i\n' % (frame*0.005, svf, conteo))

# Cierre del archivo
outFile.close()
