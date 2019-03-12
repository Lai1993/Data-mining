# -*- coding: utf-8 -*-
import numpy as np
import random
import time
import copy
from numba import jit
from math import sqrt
#讀取檔案
FILE , GROUP = "iris.txt" , 3
FILE , GROUP = "c20d6n1200000t.txt" , 20

#作者：中興大學資工所  賴誠( lcin1993@gmail.com )
#有任何問題或想法歡迎來信或由任何管道討論
#本程式碼歡迎任何人使用、複製、修改、研究與散布

pnum , dim = 0 , 0          #資料筆數,特徵數
geno , popusize = 10 ,10       #世代數量,染色體數量
pm , cm = 0.05 , 1        #變異機率,變異常數
c = 2                       #標準差倍率

def inputdata():
	data,label,labellist = [],[],[]                         #資料
	for line in open(FILE,'r'):                             #以"r"模式開啟檔案
		l = line.strip('\n').split(',')                     #將讀取進來的資料依照逗號分割
		data.append(np.array([float(i) for i in l[:-1]]))   #加入data
		if l[-1] not in labellist:
			labellist.append(l[-1])
		label.append(labellist.index(l[-1]))
	return data,len(data),len(data[0]),label

def init(data): #將資料隨機分群，得到一些結果
	population = [[random.randint(0,GROUP-1) for j in range(pnum)]for i in range(popusize)]
	sse = np.zeros((popusize),np.float)
	
	for i in range(popusize):
		t = time.time()
		sse[i],csize = kmeans(data,population[i])
		print("i:{0}\tcsize:{1}\tsse:{2:.5f}\ttime:{3:.5f}".format(i,csize,sse[i],time.time()-t))
	return population,sse

def init2(data):    #將資料隨機取點，得到一些結果
	#隨機取20個點做為其初始中心
	center = np.array([random.sample(data,GROUP) for i in range(popusize)])
	
	#宣告變數
	population = np.zeros((popusize,pnum),np.int)
	sse = np.zeros((popusize),np.float)
	
	print("")
	for i in range(popusize):
		t = time.time()
		#以初始中心開始進行分群，得到初始結果
		sse[i],csize = reclassify(data,population[i],center[i])
		print("sse:{0:.5f}\ttime:{1:.5f}\tcsize:{2}".format(sse[i],time.time()-t,csize))
	print("")
		
	return population,sse
	
@jit
def selection(population,sse):
	#fitness value=SSE平均 - SSE + c*標準差
	fvalue = np.mean(sse) - sse + c*np.std(sse)
	#若fitness value<0，則將其設為0
	for i in range(popusize):
		if fvalue[i] < 0:
			fvalue[i] = 0
	#依照fitness value做輪盤式選擇，得到要被選出來的染色體
	p = weight_choice(fvalue)
	return population[p],p

def mutation(data,chromosome):
	newch = [0]*pnum                        #新的染色體的結果

	#計算其質量中心
	center,csize = calccenter(data,chromosome,type = 1)
	for i in range(pnum):
		#決定該基因是否進行變異
		if random.uniform(0,1) < pm:
			newch[i],center,csize = mut(data[i],center,csize,chromosome[i])
		else:
			newch[i] = chromosome[i]
	for k in range(GROUP):
		center[k] /= csize[k]
	
	return newch,csize#,center
@jit
def mut(point,center,csize,k0):
	p,d = [0]*GROUP,[0]*GROUP		#p:某個點被選到的機率 d:某個點距離所有群的距離
	#依照該點到各中心的距離，計算變異到各個群的機率
	for j in range(GROUP):
		d[j] = sqrt(dissq(point,center[j]/csize[j]))
	dmax = np.max(d)
	if d[k0] > 0:
		for j in range(GROUP):
			p[j] = cm*dmax - d[j]
		#selected from {1,2,...,K} according to the distribution {p1, p2, ..., pk}
		#將該點從原本的中心點扣掉，加入新的中心點
		#這裡的center是距離和，不是質心
		center[k0] -= point
		csize[k0] -= 1
		k = weight_choice(p)
		center[k] += point
		csize[k] += 1
	else:
		k = k0
	return k,center,csize

def kmeans(data,result):
	while True:
		#步驟一：計算中心點
		center,csize = calccenter(data,result)
		
		#步驟二：重新分群
		sse,csize = reclassify(data,result,center)
		
		if np.min(csize) != 0:
			break
		else:
			k = csize.index(0)
			print("\tempty cluster({0}):{1}".format(k,csize))
			i = random.randint(0,pnum-1)
			result[i] = k
	return sse,csize

@jit
def calccenter(data,result,type = 0): #質心計算：輸入資料集、分群結果；輸出三個群的中心
	#宣告變數
	center = np.zeros((GROUP,dim),np.float)
	csize = [0]*GROUP
	
	#將該群所有點加總起來
	for i in range(pnum):
		center[ result[i] ] = csum(center[ result[i] ],data[i])
		csize[ result[i] ] += 1
	#若type=1，則不做平均
	if type == 1:
		return center,csize
	#取平均
	for i in range(GROUP):
		for j in range(dim):
			center[i][j] /= csize[i]
	return center,csize

@jit
def reclassify(data,result,center):
	#宣告變數
	sse = 0.0
	csize = [0]*GROUP
	#對每個點，選擇距離最近的中心點做為分群結果
	for i in range(pnum):
		result[i],d = rec(data[i],center)
		sse += d
		csize[result[i]]+=1
	return sse,csize
		
@jit
def rec(p,c):
	dmin = float("+inf")
	result = -1
	#計算距離，選最小值
	for j in range(GROUP):
		d = dissq(p,c[j])
		if dmin > d:
			dmin = d
			result = j
	return result,dmin
	
@jit
def csum(c,p):  #將c p兩個陣列加起來
	for i in range(dim):
		c[i]+=p[i]
	return c
	
@jit
def calcsse(data,result,center):
	#計算其SSE
	d=[0.0]*pnum
	for i in range(pnum):
		d[i] = dissq(data[i],center[result[i]])
	sse = np.sum(d)
	return sse

@jit
def dissq(p,c):
	#計算p c兩點的距離
	return np.sum((p-c)**2)
	
@jit
def weight_choice(weight): #加權隨機選取
	w = random.uniform(0,np.sum(weight))
	i = 0
	while w > 0:
		w = w - weight[i]
		i += 1
	return i-1
	
if __name__ == "__main__":
	#step 0:讀取資料
	t0 = time.time()
	data,pnum,dim,label = inputdata()
	print("input data:{0:.5f} sec".format(time.time()-t0))
	
	#step 1:初始化第0世代
	population , sse = init2(data)
	
	#step 2:預設最佳解為第0條染色體
	best,bestsse = population[0],float("inf")
	
	for i in range(geno):
		print("geno: {0:2d}".format(i+1))
		#step 3:依照sse選出一染色體作為下一世代的母群體
		t = time.time()
		chromosome,p = selection(population,sse)
		print("select chromosome:{0}\tuse time:{1:.5f}".format(p,time.time()-t))
		
		for i in range(popusize):
			print("\tchromosome:{0}".format(i))
			
			#step 4:將這個選出來的染色體進行變異成為新的世代
			t = time.time()
			population[i],csize = mutation(data,chromosome)
			print("\tmutation  csize:{0}\ttime:{1:.5f}".format(csize,time.time()-t))
			
			#step 5:將新的分群結果進行k-means的 1-step 分群
			t = time.time()
			sse[i],csize = kmeans(data,population[i])
			print("\tkmeans    csize:{0}\ttime:{1:.5f}".format(csize,time.time()-t))
			
			#step 6:比較是否有比較好
			if sse[i] < bestsse:
				best = copy.deepcopy(population[i])
				bestsse = sse[i]
				bestcsize = csize
			print("\tsse:{0:.5f}\n".format(sse[i]))
	#step 7:印出最好結果與sse
	print("result:\nsse:{0:.5f}".format(bestsse))
	line = "total\t"
	for i in range(GROUP):
		line += "{0:7d}".format(bestcsize[i])
	print(line)
	
	line = "       \t"
	for i in range(GROUP):
		line += " pred{0:2d}".format(i)
	print(line)
	
	#step 8:印出混淆矩陣(預測與實際)並計算準確率
	a = [[0 for j in range(GROUP)]for i in range(GROUP)]
	acc = 0
	for i in range(pnum):
		a[ best[i] ][ label[i] ] += 1
		#a[ label[i] ][ best[i] ] += 1
	for i in range(GROUP):
		line = " act {0:2d}\t".format(i)
		for j in range(GROUP):
			line += "{0:7d}".format(a[j][i])
		print(line)
		acc += max(a[i])
	print("acc:{0:.5f}".format(acc*100.0/pnum))
	print("total use time:{0:.5f} second".format(time.time()-t0))
