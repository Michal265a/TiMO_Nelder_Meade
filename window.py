from functions import *
from plotting import *
import matplotlib
matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QTimer
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

	
class GlowneOkno(QWidget):
	def __init__(self):
		super().__init__()
		self.setFixedSize(600,685)
		self.setWindowTitle("Optymalizacja - Nelder-Meade")
		self.show()	
		self.show_0()
		
	list0 = [[],[],[],[]]#label,line,button,rules
	list1 = [[],[],[],[],[],[],[]]#label,ai,xi,bi,lab_param,lin_param,button
	list2 = [[],[],[]]#label,button,table
	shown=[False,False,False]
	err_label = [None,None]
	data = Math_data()
	plot = Plot_data()
	timer = QTimer()
	timer.setInterval(500)
	timer_conn = False

	def show_0(self):
		label = QLabel("Podaj wzór funkcji:",self)
		label.move(5,10)
		self.list0[0].append(label)
		
		line = QLineEdit("",self)
		line.move(140,5)
		line.setFixedWidth(350)
		self.list0[1].append(line)
		
		button = QPushButton("Zatwierdź",self)
		button.move(500,5)
		self.list0[2].append(button)
		self.list0[2][0].clicked.connect(self.but_zatwierdz)
		
		label = QLabel("Reguły wprowadzania funkcji:",self)
		label.move(5,35)
		self.list0[0].append(label)
		
		label = QLabel("- zmienne wprowadzać w kolejności: x1, x2, x3, x4, x5",self)
		label.move(215,35)
		self.list0[3].append(label)
		
		label = QLabel("- w miarę możliwości nie omijać znaku mnożenia (*)",self)
		label.move(215,55)
		self.list0[3].append(label)
		
		label = QLabel("- logarytm naturalny z a: ln(a), log(a)",self)
		label.move(215,75)
		self.list0[3].append(label)
		
		label = QLabel("- logarytm o podstawie a z b: log(b,a)",self)
		label.move(215,95)
		self.list0[3].append(label)
		
		label = QLabel("- wartość bezwzględna z a: abs(a)",self)
		label.move(215,115)
		self.list0[3].append(label)
		
		label = QLabel("- dozwolone użycie tylko nawiasów okrągłych ()",self)
		label.move(215,135)
		self.list0[3].append(label)
		
		for elem in self.list0:
			for lbl in elem:
				lbl.show()
		self.shown[0]=True
		
	def show_1(self):
		label = QLabel("Wykryto {:d} zmienne/ych".format(self.data.variables),self)
		label.move(5,180)
		self.list1[0].append(label)
		
		label = QLabel("Kostka (a ≤ x ≤ b):",self)
		label.move(5,200)
		self.list1[0].append(label)
		
		label = QLabel("Parametry:",self)
		label.move(305,200)
		self.list1[0].append(label)
		
		for i in range(self.data.variables):
			line = QLineEdit("-5",self)
			line.move(5,220+30*i)
			line.setFixedWidth(75)
			self.list1[1].append(line)
			
			label = QLabel("≤ x{:d} ≤".format(i+1),self)
			label.move(85,225+30*i)
			self.list1[2].append(label)
			
			line = QLineEdit("5",self)
			line.move(130,220+30*i)
			line.setFixedWidth(75)
			self.list1[3].append(line)
		
		params=["ε:","L:","α:","β:","γ:"]
		vals=["0.001","200","1","0.5","2"]
		for i in range(5):
			label = QLabel(params[i],self)
			label.move(325,225+30*i)
			self.list1[4].append(label)
			
			line = QLineEdit(vals[i],self)
			line.move(345,220+30*i)
			line.setFixedWidth(75)
			self.list1[5].append(line)
			
		button = QPushButton("Oblicz",self)
		button.move(500,190)
		self.list1[6].append(button)
		self.list1[6][0].clicked.connect(self.but_oblicz)
		
		for elem in self.list1:
			for lbl in elem:
				lbl.show()
		self.shown[1]=True
			
	def hide_1(self):
		for elem in self.list1:
			for lbl in elem:
				lbl.hide()
			for i in range(len(elem)):
				elem.pop()
		self.shown[1]=False
		
	def show_2(self):
		label = QLabel("Znaleziono rozwiązanie w {:d} krokach".format(self.data.iters-1),self)
		label.move(5,390)
		self.list2[0].append(label)
		
		solution = '['
		for i in range(self.data.variables):
			solution = solution + "{:.8f},".format(self.data.x_iters[-1,i])
		solution = solution[:-1]+']'
		label = QLabel("Znaleziony punkt: " + solution,self)
		label.move(5,410)
		self.list2[0].append(label)
		
		label = QLabel("Wartość funkcji: {:.8f}".format(self.data.f_iters[-1]),self)
		label.move(5,430)
		self.list2[0].append(label)
		
		label = QLabel("Wartość funkcji błędu: {:.8f}".format(self.data.e_iters[-1]),self)
		label.move(5,450)
		self.list2[0].append(label)
		
		if self.data.variables == 2:
			button = QPushButton("Pokaż wykres",self)
			button.move(480,390)
			self.list2[1].append(button)
			self.list2[1][0].clicked.connect(self.but_wykres)
		
		label = QLabel("Kolejne kroki algorytmu:",self)
		label.move(5,480)
		self.list2[0].append(label)
		
		table = QTableWidget(self.data.iters,3,self)
		table.setHorizontalHeaderLabels(["Punkt","Funkcja","Błąd"])
		table.setVerticalHeaderLabels(map(str,list(range(self.data.iters))))
		table.setColumnWidth(0,370)
		table.setColumnWidth(1,80)
		table.setColumnWidth(2,80)
		table.move(10,505)
		table.setFixedSize(580,170)
		for i in range(self.data.iters):
			text = '['
			for j in range(self.data.variables):
				text = text + "{:.6f},".format(self.data.x_iters[i,j])
			text = text[:-1]+']'
			table.setItem(i,0,QTableWidgetItem(text))
			text = "{:.5f}".format(self.data.f_iters[i].item())
			table.setItem(i,1,QTableWidgetItem(text))
			text = "{:.5f}".format(self.data.e_iters[i].item())
			table.setItem(i,2,QTableWidgetItem(text))		
		table.setEditTriggers(QTableWidget.NoEditTriggers)
		self.list2[2].append(table)
		
		for elem in self.list2:
			for lbl in elem:
				lbl.show()
		self.shown[2]=True
	
	def hide_2(self):
		for elem in self.list2:
			for lbl in elem:
				lbl.hide()
			for i in range(len(elem)):
				elem.pop()
		self.shown[2]=False
		
		
	def but_zatwierdz(self):
		if self.shown[2] is True:
			self.hide_2()
		if self.shown[1] is True:
			self.hide_1()
		for i in range(2):
			if self.err_label[i] is not None:
				self.err_label[i].hide()
				self.err_label[i] = None
		if self.timer.isActive():
			self.timer.stop()
		self.data.given_fcn = self.list0[1][0].text()
		corr, err = self.data.parse_fcn()
		if corr:
			self.show_1()
		else:
			self.err_label[0] = QLabel(err,self)
			self.err_label[0].move(50,160)
			self.err_label[0].setStyleSheet("color: red")
			self.err_label[0].show()
	
	def but_oblicz(self):
		if self.shown[2] is True:
			self.hide_2()
		if self.err_label[1] is not None:
			self.err_label[1].hide()
			self.err_label[1] = None
		if self.timer.isActive():
			self.timer.stop()
		#przepisanie param
		labels = [[],[],[]]#a,b,param
		for elem in self.list1[1]:
			labels[0].append(elem.text())
		for elem in self.list1[3]:
			labels[1].append(elem.text())
		for elem in self.list1[5]:
			labels[2].append(elem.text())
		corr, err = self.data.check_params(labels)
		if corr:
			self.data.calc_Nelder_Meade()
			self.show_2()
		else:
			self.err_label[1] = QLabel(err,self)
			self.err_label[1].move(50,370)
			self.err_label[1].setStyleSheet("color: red")
			self.err_label[1].show()

	def but_wykres(self):
		if self.timer.isActive():
			self.timer.stop()
		self.canvas = MplCanvas(self)
		#plot surface	
		self.plot.set_contour(self.data)
		lvl = np.linspace(self.plot.Z.min(),self.plot.Z.max(),31)
		self.canvas.ax.set_xlim(self.data.a_vec[0],self.data.b_vec[0])
		self.canvas.ax.set_ylim(self.data.a_vec[1],self.data.b_vec[1])
		l1 = self.canvas.ax.contourf(self.plot.X,self.plot.Y,self.plot.Z,levels=lvl)
		self.canvas.fig.colorbar(l1, ticks=lvl[::3])
		#plot
		self.plot.step=0
		#self.timer = None
		#self.timer = QTimer()
		#self.timer.setInterval(1000)
		if not self.timer_conn:
			self.timer.timeout.connect(self.update_plot)
			self.timer_conn=True
		self.timer.start()
		self.canvas.show()
		
	def update_plot(self):
		self.canvas.ax.cla()  # Clear the canvas.
		#surface
		lvl = np.linspace(self.plot.Z.min(),self.plot.Z.max(),31)
		self.canvas.ax.set_xlim(self.data.a_vec[0],self.data.b_vec[0])
		self.canvas.ax.set_ylim(self.data.a_vec[1],self.data.b_vec[1])
		self.canvas.ax.contourf(self.plot.X,self.plot.Y,self.plot.Z,levels=lvl)
		#line
		self.plot.set_step(self.data)
		self.canvas.ax.plot(self.plot.simpl_x, self.plot.simpl_y, 'k')
		self.canvas.draw()

