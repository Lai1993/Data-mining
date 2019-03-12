#coding:utf-8
import numpy as np
import random
import time
import math
from numba import jit
from pyspark import SparkContext
#讀取檔案
FILE,GROUP = "iris.txt" , 3
FILE,GROUP = "c20d6n1200000t.txt" , 20

#作者：中興大學資工所  賴誠( lcin1993@gmail.com )
#有任何問題或想法歡迎來信或由任何管道討論
#本程式碼歡迎任何人使用、複製、修改、研究與散布

#spark-submit --master local[*] --driver-memory 6G --executor-memory 6g gka-spark.py

pnum , dim = 0 , 0			#資料筆數,特徵數
geno , popusize = 10 ,10		#世代數量,染色體數量
pm , cm = 0.05 , 1			#變異機率,變異常數
c = 2						#標準差倍率

def inputdata():
	data,label,labellist = [],[],[]                         #資料
	for line in open(FILE,'r'):                             #以"r"模式開啟檔案
		l = line.strip('\n').split(',')                     #將讀取進來的資料依照逗號分割
		data.append(np.array([float(i) for i in l[:-1]]))   #加入data
		if l[-1] not in labellist:
			labellist.append(l[-1])
		label.append(labellist.index(l[-1]))
	return data,len(data),len(data[0]),label

def init():
	center = [np.array(random.sample(data0,GROUP)) for i in range(popusize)]
	population,sse = [0]*popusize,[0]*popusize
	for i in range(popusize):
		#population[popusize](k,(point,count,se))
		t = time.time()
		population[i] = data.map(lambda point:reassign(point,center[i]))
		sse[i] = population[i].map(lambda (k,(p,c,d)):d).reduce(lambda d1,d2:d1+d2)
		print("sse:{0:.5f}\tuse time:{1:.5f}".format(sse[i],time.time()-t))
	return population,sse,center

def selection(population,sse):
	fvalue = np.mean(sse) - sse + c*np.std(sse)
	#若fitness value<0，則將其設為0
	for i in range(popusize):
		if fvalue[i] < 0:
			fvalue[i] = 0
	#依照fitness value做輪盤式選擇，得到要被選出來的染色體
	p = weight_choice(fvalue)
	return population[p],p

def mutation(k,point,se,center):
	d,p = [0.0]*GROUP,[0.0]*GROUP
	if random.uniform(0,1) < pm:
		for i in range(GROUP):
			d[i] = dissq(point,center[i])
		dmax = np.max(d)
		if d[k] > 0:
			p = cm*dmax - d
			#selected from {1,2,...,K} according to the distribution {p1, p2, ..., pk}
			k = weight_choice(p)
			se = d[k]
	return (k,(point,1,se))

def reassign(p,c):
	dmin = float("+inf")
	for i in range(GROUP):
		d = dissq(p,c[i])
		if dmin > d:
			dmin = d
			k = i
	return (k,(p,1,dmin))
@jit
def dissq(p,c):
	return np.sum((p-c)**2)
@jit
def weight_choice(weight): #加權隨機選取
	w = random.uniform(0,np.sum(weight))
	i = 0
	while w > 0:
		w -= weight[i]
		i += 1
	return i-1

if __name__ == "__main__":
	sc = SparkContext()
	#step 0:輸入資料
	t = time.time()
	data0,pnum,dim,label = inputdata()
	data = sc.parallelize(data0)
	print("load data:{0:.5f} second".format(time.time()-t))

	#step 1:初始化第0世代
	t0 = time.time()
	population,sse,center = init()
	print("init time:{0:.5f} second".format(time.time()-t0))

	#step 2:預設最佳解
	bestsse,bestcsize = float("+inf"),[0]*GROUP
	for i in range(geno):
		print("geno:{0}".format(i+1))

		#step 3:依照sse選出一染色體作為下一世代的母群體
		t = time.time()
		chromosome,p = selection(population,sse)
		print("select chromosome:{0}\tsse:{1:.5f}\tuse time:{2:.5f}".format(p,sse[p],time.time()-t))

		for j in range(popusize):
			print("\tchromosome:{0}".format(j+1))
			
			#step 4-1:將這個選出來的染色體進行變異成為新的世代
			t = time.time()
			population[j] = chromosome.map(lambda (k,(point,count,se)):mutation(k,point,se,center[p]))

			#step 4-2:重新計算質量中心
			center0 = population[j].reduceByKey(lambda (p1,c1,se1),(p2,c2,se2):(p1+p2,c1+c2,se1+se2)).collect()
			line = "\t"
			for k in range(GROUP):
				center[j][k] = center0[k][1][0]/center0[k][1][1]
				line += "{0:7d}".format(center0[k][1][1])
			print("\tmutation time:  {0:3.5f} second".format(time.time()-t))
			print(line)
			
			#step 5:將新的分群結果進行k-means的 1-step 分群
			while True:
				#step 5-1:依照mutation得到的質心進行分群
				t = time.time()
				population[j] = data.map(lambda point:reassign(point,center[j]))

				#step 5-2:計算sse
				t = time.time()
				center0 = population[j].reduceByKey(lambda (p1,c1,se1),(p2,c2,se2):(p1+p2,c1+c2,se1+se2)).collect()
				print("\tk-means time:   {0:3.5f} second".format(time.time()-t))
				#break	#debug
				if len(center0) == GROUP:	#沒有空群就直接跳出
					break
				else:	#當有空群時，隨機取點作為新的中心
					print("\tempty group")
					csize = [0]*GROUP
					for k in range(len(center0)):
						csize[k] = center0[k][1][1]
						center[j][k] = center0[k][1][0]/center0[k][1][1]
					for k in range(GROUP - len(center0)):
						np.array(center[j].tolist().append(random.sample(data0,1)[0]))
			line="\t"
			sse[j] = 0.0
			csize = [0]*GROUP
			for k in range(GROUP):
				center[j][k] = center0[k][1][0]/center0[k][1][1]
				line += "{0:7d}".format(center0[k][1][1])
				sse[j] += center0[k][1][2]
				csize[k] = center0[k][1][1]
			#step 6:比較是否有比較好
			if sse[j] < bestsse:
				best = population[j].map(lambda (k,(point,count,se)):k).collect()
				bestsse = sse[j]
				bestcsize = csize
			print("\t{0}".format(csize))
			print("\tsse:{0:.5f}".format(sse[j]))
			print("")
	print("best population sse:{0:.5f}".format(bestsse))
	print("result:")
	line = "total\t"
	for i in range(GROUP):
		line += "{0:7d}".format(bestcsize[i])
	print(line)
	
	line = "       \t"
	for i in range(GROUP):
		line += " pred{0:2d}".format(i)
	print(line)
	
	#step 5:印出混淆矩陣(預測與實際)並計算準確率
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