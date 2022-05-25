from sympy.parsing.sympy_parser import parse_expr
from math import *
import numpy as np

class Math_data():
	given_fcn = ""
	variables = None
	
	a_vec = None
	b_vec = None
	alfa = None
	beta = None
	gamma = None
	max_err = None
	max_iter = None
	
	iters = 0 
	x_iters = None
	x_plot = None
	f_iters = None
	e_iters = None
	x_vec_simpl = None
	
	def parse_fcn(self):
		correct=True
		err_mess = ""
		rdn = np.random.rand(5,1)
		try:
			fcn = parse_expr(self.given_fcn, transformations='all', local_dict=\
	{'x1':rdn.item(0), 'x2':rdn.item(1), 'x3':rdn.item(2), 'x4':rdn.item(3), 'x5':rdn.item(4)})
			res = eval(str(fcn))
		except:
			correct = False
			err_mess = "Błąd: nierozpoznane wyrażenie"
			return correct, err_mess
		vars = ['x1','x2','x3','x4','x5']
		count = [0,0]
		for elem in vars:
			if elem in self.given_fcn:
				count[0] += 1
		for elem in vars[0:count[0]]:
			if elem in self.given_fcn:
				count[1] += 1
		if not count[0] == count[1]:
			correct = False
			err_mess = "Błąd: nieprawidłowa kolejność zmiennych"
			return correct, err_mess
		if count[0] <= 1:
			correct = False
			err_mess = "Błąd: za mała ilość zmiennych (przynajmniej 2, maksymalnie 5)"
			return correct, err_mess
		self.variables = count[0]
		self.a_vec = np.zeros(self.variables)
		self.b_vec = np.zeros(self.variables)
		return correct, err_mess
	
	def check_params(self, labels):
		correct=True
		err_mess = "ok"
		#potem usunąć
		self.a_vec = np.zeros(self.variables)
		self.b_vec = np.zeros(self.variables)
		#koniec usunięcia
		i=0
		try:
			for elem in labels[0]:
				self.a_vec[i] = float(elem)
				i+=1
		except ValueError:
			correct=False
			err_mess = "Błąd konwersji paramatru a{:d} do liczby".format(i+1)
			return correct, err_mess
		i=0
		try:
			for elem in labels[1]:
				self.b_vec[i] = float(elem)
				i+=1
		except ValueError:
			correct=False
			err_mess = "Błąd konwersji paramatru b{:d} do liczby".format(i+1)
			return correct, err_mess
		params=["ε","L","α","β","γ"]
		try:
			i=0
			self.max_err = float(labels[2][0])
			i=1
			self.max_iter = int(labels[2][1])
			i=2
			self.alfa = float(labels[2][2])
			i=3
			self.beta = float(labels[2][3])
			i=4
			self.gamma = float(labels[2][4])
		except ValueError:
			correct=False
			err_mess = "Błąd konwersji paramatru {:s} do liczby".format(params[i])
			return correct, err_mess
		if not (self.max_err >0 and self.max_err <=0.001):
			correct=False
			err_mess = "Błąd wartości paramatru ε (dozwolony przedział: (0;0.001] )"
			return correct, err_mess
		if self.max_iter <=0:
			correct=False
			err_mess = "Błąd wartości paramatru L (musi byś to liczba całkowita dodatnia)"
			return correct, err_mess
		if self.alfa <=0:
			correct=False
			err_mess = "Błąd wartości paramatru α (musi byś to liczba dodatnia)"
			return correct, err_mess
		if not (self.beta >0 and self.beta <1):
			correct=False
			err_mess = "Błąd wartości paramatru β (musi byś to liczba z przedziału (0;1) )"
			return correct, err_mess
		if self.gamma <=0:
			correct=False
			err_mess = "Błąd wartości paramatru γ (musi byś to liczba dodatnia)"
			return correct, err_mess	
		return correct, err_mess
	
	def calc_Nelder_Meade(self):
		#dla bezpieczeństwa - czyścimy zmienne
		self.x_iters = None
		self.x_plot = None
		self.f_iters = None
		self.e_iters = None
		self.x_vec_simpl = None

		self.x_vec_simpl = np.zeros([self.variables+1,self.variables])
		#generacja losowego simpleksu
		for i in range(self.variables):
			rdn = np.random.rand(self.variables+1)*(self.b_vec[i]-self.a_vec[i])+self.a_vec[i]
			self.x_vec_simpl[:,i]=rdn
		#obliczenie wartości fcn
		res = np.zeros(self.variables+1)
		for i in range(self.variables+1):
			res[i] = self.calc_fcn(self.x_vec_simpl[i,:])
		#błąd do logu (jeszcze vec + fcn)
		self.e_iters = np.array([self.calc_err()])
		self.iters=1
		while self.iters <= self.max_iter and self.e_iters[-1] >= self.max_err :
			#szukanie min,max-1,max + wartości fcn
			tab = np.argsort(res)
			L=tab[0]
			res_L=res[L]
			H=tab[-1]
			res_H=res[H]
			H1=tab[-2]
			res_H1=res[H1]
			#wartości x_vec, fcn, x_plot do logów
			if self.iters ==1:
				self.x_iters = np.array([self.x_vec_simpl[L,:]])
				self.f_iters = np.array([res[L]])
				if self.variables ==2:
					elem = self.x_vec_simpl
					elem = np.append(elem,[self.x_vec_simpl[0,:]],axis=0)
					self.x_plot = np.array([elem])
					self.x_plot = np.append(self.x_plot,[elem],axis=0)
					self.x_plot = np.append(self.x_plot,[elem],axis=0)
			else:
				self.x_iters = np.append(self.x_iters, [self.x_vec_simpl[L,:]],axis=0)
				self.f_iters = np.append(self.f_iters, [res[L]])
				if self.variables ==2:
					elem = self.x_vec_simpl
					elem = np.append(elem,[self.x_vec_simpl[0,:]],axis=0)
					self.x_plot = np.append(self.x_plot,[elem],axis=0)
					
			#środek simpl bez x_H i fcn(x_H)
			x_c_simpl = self.x_vec_simpl.sum(axis=0) - self.x_vec_simpl[H,:]
			x_c_simpl = x_c_simpl / self.variables
			res_c = self.calc_fcn(x_c_simpl)
			# ODBICIE - punkt i fcn
			x_alfa = (1+self.alfa)*x_c_simpl - self.alfa*self.x_vec_simpl[H,:]
			res_alfa = self.calc_fcn(x_alfa)
			#jeżeli res_alfa < res_min
			if res_alfa < res_L:
				#ekspansja
				x_gamma = (1+self.gamma)*x_alfa - self.gamma*x_c_simpl
				res_gamma = self.calc_fcn(x_gamma)
				if res_gamma < res_L:
					self.x_vec_simpl[H,:] = x_gamma
					res[H] = res_gamma
				else:
					self.x_vec_simpl[H,:] = x_alfa
					res[H] = res_alfa
			#jeśli res_min < res_alfa < res_max1
			elif res_alfa >= res_L and res_alfa <= res_H1:
				self.x_vec_simpl[H,:] = x_alfa
				res[H] = res_alfa
			#jeśli res_alfa > res_max1
			else:
				if res_alfa < res_H:
					x_prim = x_alfa
					res_prim = res_alfa
				else:
					x_prim = self.x_vec_simpl[H,:]
					res_prim = res_H
				#kontrakcja
				x_beta = self.beta*x_prim + (1-self.beta)*x_c_simpl
				res_beta = self.calc_fcn(x_beta)
				if res_beta < res_H:
					self.x_vec_simpl[H,:] = x_beta
					res[H] = res_beta
				else:
					#zwężanie simpleksu
					for i in range(self.variables+1):
						if not i==L:
							self.x_vec_simpl[i,:] = \
									(self.x_vec_simpl[i,:]+self.x_vec_simpl[L,:])/2
							res[i] = self.calc_fcn(self.x_vec_simpl[i,:])
			#sprawdzenie, czy pkt w kostce
			for i in range(self.variables+1):
				corrected=False
				for j in range(self.variables):
					if self.x_vec_simpl[i,j] < self.a_vec[j]:
						corrected=True
						self.x_vec_simpl[i,j] = self.a_vec[j]
					if self.x_vec_simpl[i,j] > self.b_vec[j]:
						corrected=True
						self.x_vec_simpl[i,j] = self.b_vec[j]
				if corrected:
					res[i] = self.calc_fcn(self.x_vec_simpl[i,:])
			#błąd + uzupełnij logi
			self.e_iters = np.append(self.e_iters, [self.calc_err()])
			self.iters +=1
		#koniec pętli while
		tab = np.argsort(res)
		H=tab[-1]
		res_H=res[H]
		#wartości do logów
		self.x_iters = np.append(self.x_iters, [self.x_vec_simpl[L,:]],axis=0)
		self.f_iters = np.append(self.f_iters, [res[L]])
		if self.variables ==2:
			elem = self.x_vec_simpl
			elem = np.append(elem,[self.x_vec_simpl[0,:]],axis=0)
			self.x_plot = np.append(self.x_plot,[elem],axis=0)
			self.x_plot = np.append(self.x_plot,[elem],axis=0)
			self.x_plot = np.append(self.x_plot,[elem],axis=0)
		
	def calc_fcn(self, vec):
		dct={}
		for i in range(self.variables):
			dct['x{:d}'.format(i+1)] = vec[i]
		fcn = parse_expr(self.given_fcn, transformations='all', local_dict=dct)
		res = eval(str(fcn))
		return res
	
	def calc_err(self):
		max_err = 0
		for i in range(self.variables):
			for j in range(i+1,self.variables+1):
				diff_vec = self.x_vec_simpl[i,:] - self.x_vec_simpl[j,:]
				err = np.sqrt(np.sum(diff_vec**2))
				if err > max_err:
					max_err = err
		return max_err
	

