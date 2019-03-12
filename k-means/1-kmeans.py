import random
import time
import numpy as np
from numba import jit

#讀取檔案
FILE , GROUP = "iris.csv" , 3
FILE , GROUP = "c20d6n1200000t.csv" , 20
pnum,dim = 0,0

#作者：中興大學資工所  賴誠( lcin1993@gmail.com )
#有任何問題或想法歡迎來信或由任何管道討論
#本程式碼歡迎任何人使用、複製、修改、研究與散布

def inputdata():
	data,label,labellist = [],[],[]			#資料、真實所屬群、群名稱
	for line in open(FILE,'r'):				#以"r"模式開啟檔案
		l = line.strip('\n').split(',')		#將讀取進來的資料依照逗號分割
		data.append(np.array([float(i) for i in l[:-1]]))	#加入data
		if l[-1] not in labellist:
			labellist.append(l[-1])
		label.append(labellist.index(l[-1]))
	return data,len(data),len(data[0]),label	#data,pnum,dim,label
	
@jit
def csum(c,p):
	for i in range(dim):
		c[i]+=p[i]
	return c
@jit
def calccenter(data,result):
	center = np.zeros((GROUP,dim),np.float)
	csize = np.zeros(GROUP,np.int)
	for i in range(pnum):
		center[ result[i] ] = csum(center[ result[i] ],data[i])
		csize[ result[i] ] += 1
	for j in range(GROUP):
		center[j] = center[j] / csize[j]
	return center,csize
@jit
def dissq(p,c):
	return np.sum((p-c)**2)
@jit
def rec(p,c):
	dmin = float("+inf")
	result = -1
	for j in range(GROUP):
		d = dissq(p,c[j])
		if dmin > d:
			dmin = d
			result = j
	return result
@jit
def reclassify(data,result,center):
	for i in range(pnum):
		result[i] = rec(data[i],center)
@jit
def calcsse(data,result,center):
	d=[0.0]*pnum
	for i in range(pnum):
		d[i] = dissq(data[i],center[result[i]])
	sse = np.sum(d)
	return sse

def kmeans(data,label):
	center = np.array(random.sample(data,GROUP))
	result = np.zeros(pnum,np.int)
	sse,sse0,dsse,iter = float("+inf"),float("+inf"),float("+inf"),0
	while dsse > 10e-3:
		iter = iter+1
		print("iter{0}:".format(iter))
		
		t = time.time()
		reclassify(data,result,center)			#重新分群
		center,csize = calccenter(data,result)	#重置中心
		sse = calcsse(data,result,center)		#計算sse
		print("\ttotal time:{0:.5f}".format(time.time()-t))

		dsse = 100 - 100.0*sse/sse0
		print("\tsse:{0:.5f}\tsse0:{1:.5f}\tdsse:{2:.5f}%".format(sse,sse0,dsse))
		sse0 = sse
		line = "\tsize:"
		for i in csize:
			line += "{0:7d}".format(i)
		print(line)
		print("")
	print("result:")
	line = "total\t"
	for i in range(GROUP):
		line += "{0:7d}".format(csize[i])
	print(line)
	
	line = "       \t"
	for i in range(GROUP):
		line += " pred{0:2d}".format(i)
	print(line)
	
	#step 5:印出混淆矩陣(預測與實際)並計算準確率
	a = [[0 for j in range(GROUP)]for i in range(GROUP)]
	acc = 0
	for i in range(pnum):
		a[ label[i] ][ result[i] ] += 1
	for i in range(GROUP):
		line = "true {0:2d}\t".format(i)
		for j in range(GROUP):
			line += "{0:7d}".format(a[i][j])
		print(line)
		acc += max(a[i])
	print("acc:{0:.5f}".format(acc*100.0/pnum))
if __name__ == "__main__":
	t = time.time()
	data,pnum,dim,label = inputdata()
	print("input time:{0:.5f}".format(time.time()-t))
	
	t = time.time()
	kmeans(data,label)
	print("total time:{0:.5f}".format(time.time()-t))
