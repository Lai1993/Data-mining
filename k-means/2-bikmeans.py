#coding:utf-8
import numpy as np
import random
import time
from numba import jit
#讀取檔案
FILE , MaxGROUP = "iris.csv" , 3
FILE , MaxGROUP = "c20d6n1200000t.csv" , 20
NowGROUP = 1

#作者：中興大學資工所  賴誠( lcin1993@gmail.com )
#有任何問題或想法歡迎來信或由任何管道討論
#本程式碼歡迎任何人使用、複製、修改、研究與散布

pnum , dim = 0 , 0          #資料筆數,特徵數

def inputdata():
	data,label,labellist = [],[],[]                         #資料
	for line in open(FILE,'r'):                             #以"r"模式開啟檔案
		l = line.strip('\n').split(',')                     #將讀取進來的資料依照逗號分割
		data.append(np.array([float(i) for i in l[:-1]]))   #加入data
		if l[-1] not in labellist:
			labellist.append(l[-1])
		label.append(labellist.index(l[-1]))
	return data,len(data),len(data[0]),label
	
@jit
def dissq(p,c):
	return np.sum((p-c)**2)
	
@jit
def calcgsc(data,center):
	d = [0.0,0.0]
	sse = [0.0,0.0]
	size = [0,0]
	result = [0]*len(data)
	newcenter = np.zeros((2,dim),np.float)
	for i in range(len(data)):
		d[0] = dissq(data[i],center[0])
		d[1] = dissq(data[i],center[1])
		k = 0 if d[0] < d[1] else 1
		result[i] = k
		sse[k] += d[k]
		newcenter[k] += data[i]
		size[k] += 1
	for i in range(dim):
		newcenter[0][i] /= size[0]
		newcenter[1][i] /= size[1]
	return result,sse,newcenter
	
def kmeans(data,label):
	center = random.sample(data,2)	#隨機選兩個點作為中心點
	sse,sse0,dsse,iter = [float("+inf")]*2,float("+inf"),float("+inf"),0
	while dsse > 10e-3:
		iter += 1
		group,sse,center = calcgsc(data,center)
		dsse = 100 - 100.0*((sse[0]+sse[1])/sse0)
		sse0 = sse[0] + sse[1]
	glist=[[],[]]
	llist=[[],[]]
	for p in range(len(data)):
		glist[group[p]].append(data[p])
		llist[group[p]].append(label[p])
	return glist,sse,llist
	
if __name__ == "__main__":
	t0 = time.time()
	data,pnum,dim,label = inputdata()
	group_list = [data] #每個群包含的點的座標，一開始全部都在一群
	label_list = [label]
	sse = [float("+inf")]
	print("load time:{0:.5f}".format(time.time()-t0))
	
	while NowGROUP < MaxGROUP:
		tmid = time.time()
		t = sse.index(max(sse))	#從當前的群中，選出最大SSE的群
		#將其用kmeans分為兩群
			#newgroup為兩個群的點的座標
			#newsse為兩個群的點各自對其中心的距離平方和
		newgroup,newsse,newlist = kmeans(group_list[t],label_list[t])
		#將分開的兩群分別加入原本的位置與最末端
		group_list[t] = newgroup[0]
		group_list.append(newgroup[1])
		sse[t] = newsse[0]
		sse.append(newsse[1])
		label_list[t] = newlist[0]
		label_list.append(newlist[1])
		print("cluster:{0}\tuse time:{1:.5f}".format(NowGROUP+1,time.time()-tmid))
		print("size:{0}".format([len(i) for i in group_list]))
		a = [[0 for j in range(MaxGROUP)]for i in range(NowGROUP+1)]
		acc = 0
		print("result:")
		for i in range(NowGROUP+1):
			for j in label_list[i]:
				a[i][j] +=1
		for i in range(NowGROUP+1):
			line = ""
			for j in range(MaxGROUP):
				line += "{0:7d}".format(a[i][j])
			print(line)
			acc += max(a[i])
		print("acc:{0:.5f} %".format(acc*100.0/pnum))
		print("")
		NowGROUP += 1
	totalsse=0.0
	for s in sse:
		totalsse += s
	print("total sse:",totalsse,"\t total time:",time.time()-t0)
