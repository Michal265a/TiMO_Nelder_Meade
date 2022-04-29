from functions import *
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Plot_data():
	X = None
	Y = None
	Z = None
	simpl_x = None
	simpl_y = None
	step=0
	
	def set_contour(self, data):
		x = np.linspace(data.a_vec[0],data.b_vec[0],25)
		y = np.linspace(data.a_vec[1],data.b_vec[1],25)
		self.X, self.Y = np.meshgrid(x,y)
		self.Z = np.zeros(self.X.shape)
		for i in range(x.shape[0]):
			for j in range(y.shape[0]):
				vec = np.array([self.X[i,j],self.Y[i,j]])
				self.Z[i,j] = data.calc_fcn(vec)
	
	def set_step(self, data):
		self.simpl_x = data.x_plot[self.step,:,0]
		self.simpl_y = data.x_plot[self.step,:,1]
		self.step = (self.step+1)%(data.x_plot.shape[0])
		

class MplCanvas(FigureCanvas):
	def __init__(self, parent=None,):
		self.fig = Figure(figsize=(8,6), dpi=100)
		self.ax = self.fig.add_subplot(111)
		super(MplCanvas, self).__init__(self.fig)
		self.setWindowTitle("Wykres")


