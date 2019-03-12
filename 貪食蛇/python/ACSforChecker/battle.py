import UI
import fileIO

def init():
	state = [[0,0] for i in range(31)]
	cnt1,cnt2 = 1,16
	for i in range(9):
		for j in range(9):
			if i+j < 5:
				state[cnt1] = [i,j]
				cnt1 += 1
			elif i+j > 11:
				state[cnt2] = [i,j]
				cnt2 += 1
	UI.showState(0,state,1)
	return state

def battle():
	state = init()
	route = []
	round = 0	#回合數
	while True:											#每一個回合
		round += 1
		while True:
			target = getP1Move(state)					#取得玩家1的移動target=(chess,x,y)
			if movAble(0,state,target):		#若不可移動，則重新取得
				state = move(0,state,target)	#移動棋子
				UI.showState(1,state,round)	#刷新畫面
				route.append(target)					#紀錄移動
				break
			UI.showMsg("你不能這麼做")
		if endGame2(0,state):
			UI.showMsg("遊戲結束，恭喜玩家一獲勝")
			break

		while True:
			target = getP2Move(state)					#取得玩家2的移動target=(chess,x,y)
			if movAble(1,state,target):		#若不可移動，則重新取得
				state = move(1,state,target)	#移動棋子
				UI.showState(0,state,round)	#刷新畫面
				route.append(target)					#紀錄移動
				break
			UI.showMsg("你不能這麼做")
		if endGame2(1,state):
			UI.showMsg("遊戲結束，恭喜玩家二獲勝")
			break
	# saveRec(fname)

def getP1Move(state):
	#chess為player1/2的第幾個棋子
	chess = int(input())
	route = []
	while True:
		i = int(input())
		if i == -1:
			break
		route+=[i]
	return chess+1,route

def getP2Move(state):
	#chess為player1/2的第幾個棋子
	chess = int(input())
	route = []
	while True:
		i = int(input())
		if i == -1:
			break
		route+=[i]
	return chess+1,route


def movAble(player, state, target):
	chess, route = target
	mov = [[0, -1], [-1, 0], [-1, 1], [0, 1], [1, 0], [1, -1]]
	count = 0
	# 在不動到現有state的情況下，紀錄目前計算到哪個位置，並用目前位置計算接下來的移動是否符合規則
	i = [] # 儲存紀錄，目的地的x座標
	j = [] # 儲存紀錄，目的地的y座標
	block_i = [] # 儲存紀錄，要跳的障礙物x座標
	block_j = [] # 儲存紀錄，要跳的障礙物座標
	for x in route:
		if (x < 6): # 用走的
			if len(route) == 1:      # 如果走一步
				i = state[player * 15 + chess][0] + mov[route[0]][0] # 目的地的x座標
				j = state[player * 15 + chess][1] + mov[route[0]][1] # 目的地的y座標
				for y in range(len(state)):
					if (i == state[y][0]) & (j == state[y][1]):      # 如果目的地位置上有棋子
						return False                                 # 則不允許移動
			else:                    # 如果走超過一步
				return False         # 則不允許移動
		else:  # 用跳的
			Ju = 0  # 判斷中間是否有棋可跳(初始:障礙物座標上沒棋子)
			Em = 1  # 判斷該位置是否有棋子(初始:目的地座標上沒棋子)
			if count == 0: # 跳第一步時
				blo_i = state[player * 15 + chess][0] + mov[x - 6][0] # 在當前位置時，要跳的障礙物x座標
				blo_j = state[player * 15 + chess][1] + mov[x - 6][1] # 在當前位置時，要跳的障礙物y座標
				block_i.append(blo_i)        # 儲存障礙物的x座標
				block_j.append(blo_j)        # 儲存障礙物的y座標
				a = state[player * 15 + chess][0] + mov[x - 6][0] * 2 # 在當前位置時，目的地的x座標
				b = state[player * 15 + chess][1] + mov[x - 6][1] * 2 # 在當前位置時，目的地的x座標
			else:          # 跳第一步以後
				# 用前一步跳完的位置，計算下一步的障礙物和目的地的座標
				blo_i = i[count - 1] + mov[x - 6][0]    # 在當前位置時，要跳的障礙物x座標
				blo_j = j[count - 1] + mov[x - 6][1]    # 在當前位置時，要跳的障礙物y座標
				block_i.append(blo_i)
				block_j.append(blo_j)
				a = i[count - 1]
				b = j[count - 1]
			# 判斷下一步的障礙物和目的地是否符合規則
			for y in range(len(state)):
				if (blo_i == state[y][0]) & (blo_j == state[y][1]):  # 障礙物的座標上有棋子
					Ju = 1  # 中間有棋可跳
				if (a == state[y][0]) & (b == state[y][1]):          # 目的地的座標上有棋子
					Em = 0  # 目的地位置存在著棋子
			if (Ju == 1) & (Em == 1):
				i.append(a) # 儲存目的地的x座標
				j.append(b) # 儲存目的地的座標
			else:
				return False
			count = count + 1
	return True

def move(player,state,target):
	chess,route = target
	mov = [[0,-1],[-1,0],[-1,1],[0,1],[1,0],[1,-1]]
	for pto in route:
		if pto < 6:
			state[player*15+chess][0]+=mov[pto][0]
			state[player*15+chess][1]+=mov[pto][1]
		elif pto < 12:
			state[player*15+chess][0]+=mov[pto-6][0]*2
			state[player*15+chess][1]+=mov[pto-6][1]*2
	return state

def endGame2(player,state):
	score = 0
	for i in range(15):
		score += state[i+player*15+1][0]
		score += state[i+player*15+1][1]
	if score == 40+player*160:
		return True
	return False
def endGame(player,state,step):
	end = 0 # 結束判斷
	if step > 20:                                # 雙方走過一定的步數後，才開始檢查比賽是否結束，此定為雙方各下10次後
		if player == 0:                          # 玩家一，檢查下方棋盤是否填滿
			for i in range(5):                   # 8, 7, 6, 5, 4
				for j in range(8, 3+i, -1):      # 8 ~ (4, 5, 6, 7, 8, 9)
					l = [8-i, j]
					if state.count(l) == 0:      # 當有一個位置沒有放置棋子時，則不能結束遊戲
						end = 1                  # end = 1 代表遊戲 未結束
			if end == 1:
				return False
			if end == 0:
				return True

		if player == 1:                          # 玩家二，檢查上方棋盤是否填滿
			for i in range(4, -1, -1):
				for j in range(i+1):
					l = [4-i, j]
					if state.count(l) == 0:      # 當有一個位置沒有放置棋子時，則不能結束遊戲
						end = 1                  # end = 1 代表遊戲 未結束
			if end == 1:
				return False
			if end == 0:
				return True

	else:                                        # 特定步數內，一律當作遊戲沒結束
		return False

def saveRec(fname):
	return False