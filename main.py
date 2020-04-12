import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import reader

# Number of particles
n = 30
# Number of dimensions
m = 2
# Function
x, y, z, f = reader.import_data('datasets/everest_closeup.asc')
# Boundaries
b = np.array([[x[0,0], x[0,-1]], [y[0,0], y[-1,0]]])
# Inertia param
w = 0.12
# Local search param
c1 = 0.04
# Global search param
c2 = 0.06
# The optimum of the function
z_max = np.max(z)

# Init particles
X = np.random.rand(n, m)
V = np.random.rand(n, m)*w
for i in range(n):
	for j in range(m):
		X[i][j]=X[i][j]*(b[j][1]-b[j][0])+b[j][0]

# Init general
pbest = X
gbest = pbest[np.where(f(*pbest.T) == np.max(f(*X.T)))[0][0]]
fig, ax = plt.subplots(nrows=1, ncols=2)
points = ax[0].plot(*X.T, 'x')
gbest_hist = [f(*gbest)]
gbest_plot = ax[1].plot([0], [0])
zmax_plot = ax[1].plot([0], [0])

# Search function
def func(t):
	global X
	global V
	global pbest
	global gbest
	global points
	global gbest_hist
	global gbest_plot
	global zmax_plot

	r1 = np.random.rand(n, m)
	r2 = np.random.rand(n, m)
	mask = np.array([f(*X.T) > f(*pbest.T) for i in range(m)]).T
	pbest = X*(mask) + pbest*(1 - mask)
	bestloc_id = np.where(f(*pbest.T) == np.max(f(*pbest.T)))[0][0]
	bestloc = X[bestloc_id]
	gbest = pbest[bestloc_id]
	V = w*V + c1*r1*(pbest - X) + c2*r2*(gbest - X)
	X = X + V
	points.pop(0).remove()
	gbest_plot.pop(0).remove()
	zmax_plot.pop(0).remove()
	points = ax[0].plot(*X.T, 'x', c='white')
	gbest_hist += [f(*gbest)]
	gbest_plot = ax[1].plot(gbest_hist, c='black', label='Global best found')
	zmax_plot = ax[1].plot([0, len(gbest_hist)-1], [z_max, z_max], c='red', label='Optimum')
	ax[1].set_title("gbest, location = ({}, {})".format(np.round(bestloc[0], 2), np.round(bestloc[1], 2)))
	ax[1].legend()
	ax[0].set_xlim([b[0][0], b[0][1]])
	ax[0].set_ylim([b[1][0], b[1][1]])
	fig.savefig(str(t)+'.png', dpi=300)

# Init of plot
ax[0].contourf(x, y, z, levels=12, cmap=cm.inferno)
fig.suptitle("Particle Swarm Algorithm")
ax[0].set_title("Search space")
ax[1].set_title("gbest")
ax[1].grid()

# Search runs here for k iterations
k = 100
for i in range(k+1):
	func(i)