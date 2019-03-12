#coding:utf-8
import numpy as np
import random
import time
import math
from numba import jit
from pyspark import SparkContext
FILE,MaxGROUP = "iris.csv" , 3
#FILE,MaxGROUP = "c20d6n1200000t.csv" , 20
NowGROUP = 1

#作者：中興大學資工所  賴誠( lcin1993@gmail.com )
#有任何問題或想法歡迎來信或由任何管道討論
#本程式碼歡迎任何人使用、複製、修改、研究與散布


def inputdata():
	data = sc.textFile(FILE).map( lambda line:np.array([float(i) for i in line.split(',')[:-1]]) ).cache()
	return data
@jit
def calcgd(point,center):
	d=[0.0]*2
	for i in range(2):
		d[i] = np.sum((point-center[i])**2)
	g = int(d[0] > d[1])*1
	mind = d[g]
	return (g,(mind,point,1))
def kmeans(data):
	tkm0 = time.time()
	center = np.array(data.takeSample(False,2,1))
	iter = 0
	sse0,sse,dsse = float("+inf"),[float("+inf")]*2,float("+inf")
	while dsse > 10e-3:# or iter < 10:
		tkm1 = time.time()
		iter += 1
		sse0 = sse
		a1 = data.map(lambda point:(calcgd(point,center))).cache()
		tkm2 = time.time()
		a2 = a1.reduceByKey(lambda p1,p2:((p1[0]+p2[0]),p1[1]+p2[1],p1[2]+p2[2] )).collect()	#計算sse、質心總和、點數
		newgroup = [a2[0][1][1],a2[1][1][1]]
		tkm3 = time.time()
		sse=[a2[0][1][0],a2[1][1][0]]
		center = np.array([a2[0][1][1],a2[1][1][1]])
		for i in range(len(center)):
			for j in range(len(center[0])):
				center[i][j] /= a2[i][1][2]
		dsse = 100 - 100.0*((sse[0]+sse[1])/(sse0[0]+sse0[1]))
		tkm4 = time.time()
		print("iter={0}\tgroup={1}\tsse={2}\tdsse={3}%".format(iter,(a2[0][1][2],a2[1][1][2]),sse,dsse))
		print("calcgd={0}\treduceByKey={1}\tcalccenter={2}\titer time={3}".format(tkm2-tkm1,tkm3-tkm2,tkm4-tkm3,tkm4-tkm1))
	a3 = a1.filter(lambda (g,(mind,p,c)):g==0).map(lambda (g,(mind,p,c)):p).collect()
	a4 = a1.filter(lambda (g,(mind,p,c)):g==1).map(lambda (g,(mind,p,c)):p).collect()
	newgroup = [a3,a4]
	print("reduce time:{0}".format(time.time()-tkm4))
	return newgroup,sse
if __name__ == "__main__":
	sc = SparkContext()
	tstart =time.time()
	data = inputdata()
	data2 = data.collect()
	Pnum,Dimen = len(data2),len(data2[0])	
	print("Pnum:{0} Dimen:{1}".format(Pnum,Dimen))
	group_list = [data2] 
	sse = [float("+inf")]
	print("load time:{0}".format(time.time()-tstart))
	while NowGROUP < MaxGROUP:
		print("loop %2d:"%NowGROUP)
		tmid = time.time()
		t = sse.index(max(sse))
		g = sc.parallelize(group_list[t])#,int(math.sqrt(len(group_list[t]))))
		newgroup,newsse = kmeans(g)
		group_list[t] = newgroup[0]
		group_list.append(newgroup[1])
		sse[t] = newsse[0]
		sse.append(newsse[1])
		print("final group:{0}	use time:{1}".format([len(i) for i in group_list],time.time()-tmid))
		NowGROUP += 1
	totalsse=0.0
	for s in sse:
		totalsse += s
	print("sse:{0}\ttotalsse:{1}\ttotal time:{2}".format(sse,totalsse,time.time()-tstart))
	print([len(i) for i in group_list])
	sc.stop()
