import fileIO

ITER = 10
antNum = 1
rho = 0.9
alpha = 0.9

def stateToScore(state):	#一律以上方玩家為主
	score = 0
	for i in range(15):
		score += state[i+1][0]
		score += state[i+1][1]
	return score
def init(antNum):
	state = [[0,0] for i in range(31)]
	cnt1,cnt2 = 1,16
	for i in range(9):
		for j in range(9):
			if i+j < 5:
				state[cnt1] = [i,j]
				board[i][j] = cnt1		#1~15為玩家1的棋子
				cnt1 += 1
			elif i+j > 11:
				state[cnt2] = [i,j]
				board[i][j] = cnt2	#16~30為玩家2的棋子
				cnt2 += 1
	states = [state for i in range(antNum)]
	return states
def getMoveNet(state):
	move_net = []
	return move_net[]
def findNextPoints(state):	#尋找所有的下一步
	move_net = getMoveNet(state)	#尋找移動網路(00,01,10,11:5*5,5*4,4*5,4*4大小)
	targets = []
	for chess in range(15):		#對每個棋子尋找下一步
		#計算該棋子是屬於哪個移動網路中
		x = state[chess][0]
		y = state[chess][1]
		net_n = (x&1)*2 + (y&1)
		#計算該棋子在網路中是哪個節點
		point_from = (x>>1)*5+y>>1	#point_from = (x/2,y/2)->(a,b)->a*5+b	(2D->1D)
		#遍歷整個網路，紀錄哪些節點可以移動
		for i in range(5 - (x&1)):
			for j in range(5 - (y&1)):
				point_to = (i>>1)*5 + (j>>1)
				if move_net[net_n][point_from][point_to]:
					targets.append((chess,i,j))
	return targets	#移動哪個棋子，移動後位置
def calcScore(tau,state,targets):
	scores = []
	for target in targets:
		chess,x,y = target
		p1 = [state[i+1][0]*9 + state[i+1][1] for i in range(15)]
		p2 = [state[i+16][0]*9 + state[i+16][1] for i in range(15)]
		p1[chess] = x*9+y
		p1.sort()
		p2.sort()
		if !tau.has_key(p1+p2):
			tau[p1+p2] = stateToScore([0]+p1+p2)
		scores.append(tau[p1+p2])
	return scores
def weightChoice(weight): #加權隨機選取
	w = random.uniform(0,np.sum(weight))
	i = 0
	while w > 0:
		w -= weight[i]
		i += 1
	return i-1
def move(state,target):
	chess,i,j = target
	state[chess] = [i,j]
	return state
def localUpdate(tau,state):
	p1 = [state[i+1][0]*9 + state[i+1][1] for i in range(15)]
	p2 = [state[i+16][0]*9 + state[i+16][1] for i in range(15)]
	p1[chess] = x*9+y
	p1.sort()
	p2.sort()
	tau[p1+p2] *= (1-rho)
	tau[p1+p2] += rho*stateToScore([0]+p1+p2)
	return tau
def globalUpdate():
	return tau
def endGame(player,state):
	score = 0
	for i in range(15):
		score += state[i+player*15+1][0]
		score += state[i+player*15+1][1]
	if score == 40+player*160:
		return True
	return False
def train():
	#step 0 : 初始化費洛蒙(從檔案讀取或從頭開始)
	tau = loadModel()
	#step 1 : 訓練的世代數
	for iter in range(ITER):
		#step 2 : 讓10對螞蟻進行戰鬥，直到全部結束
		states = init(antNum)
		rec = [[]for i in range(antNum)]
		end_game_state = [False for i in range(antNum)]
		end_game_num = 0
		while end_game_num != antNum:
			#step 3 : 每一個戰場的螞蟻移動一步
			for ant in range(antNum):
				if end_game_state[ant]:	#如果對戰已經結束
					continue
				#step 4 : 螞蟻尋找所有可以走的下一步的狀態(所有鄰居)
				targets = findNextPoints(states[ant])
				
				#step 5 : 螞蟻計算這些下一步的分數
				scores = calcScore(tau,states[ant],targets)
				
				#step 6 : 螞蟻依照這些下一步的分數進行輪盤法選擇
				score = weightChoice(scores)
				target = targets[scores.index(score)]
				
				#step 7 : 螞蟻依照選擇結果進行移動
				states[ant] = move(states[ant],target)
				
				#step 8 : 螞蟻對於這個選擇進行更新tau'=(1-a)tau+a*tau0
				tau = localUpdate(tau,state)
				
				#step 9 : 紀錄並顯示本次移動的相關資訊
				#第幾隻螞蟻，第幾回合，移動選項數，移動哪個棋子，移動路徑，移動後分數
				rec[ant].append(states[ant])
				
				#step 10 : 判斷是否遊戲結束
				if endGame(state):
					end_game_state[ant] = True
					end_game_num += 1
				#step 11 : 將選項旋轉/鏡像，作為對手繼續選擇
		#step 12 : 依照對戰結果更新路徑分數tau'=(1-a)tau+a*(n+1)*tau0
		tau = globalUpdate()
		
		#step 13 : 儲存訓練結果
		if iter in [0,10,30,100,300,1000,3000,10000]:
			fileIO.saveRec(iter)
			fileIO.saveModel(iter)


















