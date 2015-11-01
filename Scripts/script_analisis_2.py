# ------------------------------------------------------
# IMPORTAR

## 1 : Importar modulos ovito
from ovito.io import *
from ovito.modifiers import *
## 2 : Importar NumPy
import numpy
## 3 : Importar un snapshot de la muestra (se cargan todos los demas)
node = import_file("Compression_porous_5_0.lammpstrj")

# ------------------------------------------------------
# AGREGAR LOS MODIFICADORES AL NODO

## 1 : Voronoi Analysis (esta configuracion del modificador
	# es para una muestra porosa. Para muestras sin porosidad se puede
	# setear use_cutoff = True para que el calculo sea mas rapido.
node.modifiers.append(VoronoiAnalysisModifier(
    compute_indices = True,
    use_radii = False,			
    edge_count = 6,
    edge_threshold = 0,
    use_cutoff = False,
    cutoff = 6.0
))
## 2 : Atomic Strain
mod_atomicStrain = AtomicStrainModifier(
	cutoff = 5.0,
	eliminate_cell_deformation = True
)
mod_atomicStrain.reference.load("Compression_porous_5_0.lammpstrj")
node.modifiers.append(mod_atomicStrain)

# ------------------------------------------------------
# OBTENER (Y DEFINIR) OTROS DATOS RELEVANTES

## 1 : Obtener numero de particulas para calculo posterior
numofParticles = node.source.data['Position'].size
## 2 : Tipos de Voronoi segun Arman
arr = numpy.array([[0,0,0,0,12,0] , [0,0,0,2,8,2] , [0,0,0,2,8,1] , [0,0,0,3,6,3] , [0,0,0,3,6,4] , [0,0,0,1,10,2] , [0,0,0,2,8,3] , [0,0,0,4,4,3] , [0,0,1,0,9,3] , [0,0,0,12,2,0]])
arrs = numpy.ascontiguousarray(arr).view([('', numpy.int64)] * 6)

# ------------------------------------------------------
# DEFINICION DE FUNCIONES

## 1 : Funcion de deduccion de tipo de Voronoi
def type_deduction(a,ar):
	for i in range(len(ar)):
		temp = ar[i][0]
		for j in range(7):
			if j==6:
				if i+1 >= 7:
					return 7
				return i+1
			if temp[j]!=a[0][j]:
				break
	return 0
## 2 : Funcion que obtiene el shear strain promedio de cada tipo de Voronoi
def voronoi_shear(array,indices,shear,voro):
	ca = numpy.ascontiguousarray(voro).view([('', voro.dtype)] * voro.shape[1])
	indexes = numpy.argsort(indices)[::1]
	count = [0,0,0,0,0,0,0]
	avg_ss_voro = [0,0,0,0,0,0,0]
	for elemento in range (numofParticles):
		voro_type = type_deduction(ca[indexes[elemento]],array)
		temp_shear = shear[indexes[elemento]]
		if voro_type != 0:	
			avg_ss_voro[voro_type-1] = avg_ss_voro[voro_type-1] + temp_shear
			count[voro_type-1] = count[voro_type-1] + 1
	for i in range(len(avg_ss_voro)):
		avg_ss_voro[i] = avg_ss_voro[i] / count[i]
	return avg_ss_voro
## 3 : Funcion de calculo
def calculo_ovito(frame):
	ovito.dataset.anim.current_frame = frame

	node.compute()

	voro_indices = node.output["Voronoi Index"].array
	indices = node.output["Particle Identifier"].array
	shear_strain = node.output["Shear Strain"].array
	avg_ss_voro = voronoi_shear(arrs, indices, shear_strain, voro_indices)

	return avg_ss_voro
	
# ------------------------------------------------------
# DEFINIR ARCHIVO DONDE SE GUARDARAN LOS DATOS

outFile = open('outFile', 'w')

# ------------------------------------------------------
# LOOP DE CALCULO

for frame in range(0, ovito.dataset.anim.last_frame + 1):

	avg_ss_voro = calculo_ovito(frame)

	outFile.write('%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\n' % (frame*0.005, avg_ss_voro[0], avg_ss_voro[1], avg_ss_voro[2], avg_ss_voro[3], avg_ss_voro[4], avg_ss_voro[5]))

# ------------------------------------------------------
# FINALIZACION

outFile.close()
