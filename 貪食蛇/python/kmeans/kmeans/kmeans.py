import random
import time
FILE="D:\iris.txt"      #檔案位置
tstart = time.time()
#FILE="D:\c20d6n1200000t.txt"
GROUP=3
minsse = float("+inf")
def inputdata():    #輸入並處理數據
    data = []
    for i in open(FILE,'r'):                #讀取檔案
        data.append(i.split(',')[:-1])      #加入data
    return [[float(j) for j in i]for i in data]    #將最後一筆"\n"移除並轉成float
def calcdis(data,center):   #計算距離
    distance=[[0]*(len(center)) for i in range(len(data))]      #distance[len(data)][len(center)]   資料長度*中心數量
    for i in range(len(data)):              #用每一筆資料
        for j in range(GROUP):              #對每個中心
            for k in range(len(center[0])):   #的每個維度計算
                distance[i][j]+=pow(data[i][k]-center[j][k],2)
    return distance
#主程式
data = inputdata()          #輸入並處理數據
tmid = time.time()
print("讀取資料時間:",tmid-tstart)
for loop in range(5):     #做幾次k means
    print("loop%d:"%loop)
    tstart = time.time()
    center = [random.choice(data) for i in range(GROUP)]    #初始化中心點：隨機選三個點，不排除重複選到同一點的可能性
    sse0 = float("+inf")
    sse = 0
    iter = 0
    while sse0 > 10e-7 or iter < 10:                      #每次k means做幾次迭代
        tmid = time.time()
        iter = iter+1
        distance = calcdis(data,center)         #計算距離
        #分群、算sse
        group = [distance[i].index(min(distance[i])) for i in range(len(data))]    #將該資料的group指向距離平方最近的點
        elements = [0]*GROUP    #每個群的點數量
        sse0 = sse
        sse = 0
        for i in range(len(data)):
            elements[group[i]] += 1             #被該資料指到的group數量+1
            sse += min(distance[i])             #sse加上該距離平方
        if min(elements) == 0:
            print("第%d群為空，結束本次計算！"%elements.index(0))
            break
        #重置中心
        center = [[0]*len(center[0]) for i in range(GROUP)]

        for i in range(len(data)):              #先算所有點在四個座標軸的總和
            for j in range(len(data[0])):
                center[group[i]][j] += data[i][j]
        for i in range(len(center)):            #再將總和除上該群的點數來求質量中心
            for j in range(len(center[0])):
                center[i][j] = center[i][j]/elements[i]
        if sse0 !=0 :
            sse0 = 100 - (100*sse/sse0)
        print("\titer:",iter,"sse:",sse,"   \tdsse:",sse0,"%\tuse time:",time.time()-tmid)
    print("elements:",elements,"sse:",sse,"use time =",time.time()-tstart)
    if sse < minsse:
        minsse,mingroup,minelements,mincenter = sse,group,elements,center
#print("\nminsse=",minsse,"\ngroup=",mingroup,"\nelements=",minelements,"\ncenter=",mincenter)