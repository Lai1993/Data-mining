#coding:utf-8
import numpy as np
import random
import time
import math
from numba import jit
from pyspark import SparkContext
FILE,GROUP = "iris.csv" , 3
#FILE,GROUP = "c20d6n1200000t.csv" , 20

#作者：中興大學資工所  賴誠( lcin1993@gmail.com )
#有任何問題或想法歡迎來信或由任何管道討論
#本程式碼歡迎任何人使用、複製、修改、研究與散布

pnum,dim = 0,0
#spark-submit --master local[*] --driver-memory 8G --executor-memory 8g bikmeans-spark.py

def inputdata():
	data,label,labellist = [],[],[]                         #資料
	for line in open(FILE,'r'):                             #以"r"模式開啟檔案
		l = line.strip('\n').split(',')                     #將讀取進來的資料依照逗號分割
		data.append(np.array([float(i) for i in l[:-1]]))   #加入data
		if l[-1] not in labellist:
			labellist.append(l[-1])
		label.append(labellist.index(l[-1]))
	return data,len(data),len(data[0]),label
	
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

if __name__ == "__main__":
	sc = SparkContext()
	data,pnum,dim,label = inputdata()
	t0 = time.time()
	data2 = sc.parallelize(data)
	center = np.array(random.sample(data,GROUP))
	for i in range(10):
		print("iter:{0:2d}".format(i+1))
		t = time.time()
		
		result = data2.map(lambda point:(reassign(point,center)))
		center0 = result.reduceByKey(lambda (p1,c1,se1),(p2,c2,se2):(p1+p2,c1+c2,se1+se2)).collect()
		
		print("use time:{0:.5f}".format(time.time()-t))
		line=""
		sse = 0.0
		for k in range(GROUP):
			center[k] = center0[k][1][0]/center0[k][1][1]
			line += "{0:7d}".format(center0[k][1][1])
			sse += center0[k][1][2]
		print(line)
		print("sse:{0:.5f}".format(sse))
	a = [[0 for j in range(GROUP)]for i in range(GROUP)]
	acc = 0
	result0 = result.collect()
	for i in range(pnum):
		a[ label[i] ][ result0[i][0] ] += 1
	for i in range(GROUP):
		line = "true {0:2d}\t".format(i)
		for j in range(GROUP):
			line += "{0:7d}".format(a[i][j])
		print(line)
		acc += max(a[i])
	print("acc:{0:.5f}".format(acc*100.0/pnum))
	print("total use time:{0:.5f} second".format(time.time()-t0))
	
