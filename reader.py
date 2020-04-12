import numpy as np
import matplotlib.pyplot as plt
import interpolation

def import_data(filename):
	def extract(string):
		for i in range(len(string) - 1):
			if string[i] != ' ' and string[i + 1] == ' ':
				a = i + 1
			if string[i] == ' ' and string[i + 1] != ' ':
				b = i
		return(string[:a], string[b:].strip())

	metadata_raw = open(filename, 'r').readlines()[0:6]
	metadata = {}
	for i in range(len(metadata_raw)):
		point = extract(metadata_raw[i])
		if float(point[1])%1:
			metadata[point[0]] = float(point[1])
		else:
			metadata[point[0]] = int(point[1])

	Z = np.genfromtxt(filename, skip_header=len(metadata))
	x = np.arange(metadata['xllcorner'], metadata['xllcorner']+metadata['ncols']*metadata['cellsize'], metadata['cellsize'])
	y = np.arange(metadata['yllcorner'], metadata['yllcorner']+metadata['nrows']*metadata['cellsize'], metadata['cellsize'])
	X, Y = np.meshgrid(x, y)
	f = interpolation.bilinear(X, Y, Z)
	return X, Y, Z, f