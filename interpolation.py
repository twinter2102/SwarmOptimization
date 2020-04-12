import numpy as np

def bilinear(X, Y, Z):
	k = X[0,1] - X[0,0]
	m = Y[1,0] - Y[0,0]
	def f(x_global, y_global):
		i, j = ((x_global - X[0,0]) // k).astype(np.int), ((y_global - Y[0,0]) // k).astype(np.int)
		Z0 = (1/k)*(Z[j,i+1] - Z[j,i])*(x_global - X[j,i]) + Z[j,i]
		Z1 = (1/k)*(Z[j+1,i+1] - Z[j+1,i])*(x_global - X[j,i]) + Z[j+1,i]
		return (1/m)*(Z1-Z0)*(y_global - Y[j,i]) + Z0
	return f