import numpy as np
import UI

board_width = UI.board_width
net_size = UI.net_size
chess_num = UI.chess_num
finish_score = UI.finish_score
low, high = UI.low, UI.high
def init():
	state = [[0,0] for i in range(1+chess_num*2)]
	cnt1,cnt2 = 1,1+chess_num
	for i in range(board_width):
		for j in range(board_width):
			if i+j < low:######
				state[cnt1] = [i,j]
				cnt1 += 1
			elif i+j > high:####
				state[cnt2] = [i,j]
				cnt2 += 1
	return state
def linkNet(move_net,board):
	mov = [[0,-1],[-1,0],[-1,1],[0,1],[1,0],[1,-1]]
	#將可連接的相鄰兩點設為1(有向圖)
	for x in range(board_width):
		for y in range(board_width):
			net_n = (x&1)*2 + (y&1)
			#六個方向檢查
			for dir in mov:
				x1,y1 = x + dir[0], y + dir[1]
				x2,y2 = x+dir[0]*2, y+dir[1]*2
				if x2 >=0 and x2 <board_width and y2 >=0 and y2 <board_width:	#邊界確認
					#障礙物必須要有棋子，目的地不能有棋子
					if board[x1][y1] != 0 and board[x2][y2] == 0:
						i1 = (x >>1) * (net_size-(net_n&1)) + (y >>1)
						i2 = (x2>>1) * (net_size-(net_n&1)) + (y2>>1)
						move_net[net_n][i1][i2] = True
						#顯示可移動的目的地(一步)
						#r = 2*(x2+y2)+2
						#c = 16-2*(x2-y2)+2
						#UI.print_at(r,c,"Ｘ")
						#UI.showMsg(str((board[x][y],x,y,x2,y2)))
	#UI.pause()
	return move_net
#@jit
def iterNet(move_net):
	#將所有連通點串在一起
	is_change = True
	while is_change:
		is_change = False
		# at net n, from [i,j] to [j,k]
		for net in range(4):
			n = len(move_net[net])
			for i in range(n):
				for j in range(n):
					if move_net[net][i][j]:	#若i j相連
						for k in range(n):
							if not move_net[net][i][k]:		#原本i k不相連
								if move_net[net][j][k]:
									move_net[net][i][k] = True
									is_change = True
	return move_net
#@jit
def getMoveNet(state):
	#初始化移動網路
	mov = [[0,-1],[-1,0],[-1,1],[0,1],[1,0],[1,-1]]
	move_net = [[]for net in range(4)]
	#move_net = [[],[],[],[]]
	for net in range(4):
		n = (net_size-(net>>1))*(net_size-(net&1))
		move_net[net] = [[False for j in range(n)]for i in range(n)]
		#move_net[net] = np.zeros((n,n),np.bool)
	#首先將state轉換成board
	board = np.zeros((board_width,board_width),np.int)
	#board = [[0 for y in range(9)]for x in range(9)]
	for chess in range(1+chess_num*2):
		x = state[chess][0]
		y = state[chess][1]
		board[x][y] = chess
	#將可連接的相鄰兩點設為1(有向圖)
	move_net = linkNet(move_net,board)
	#將所有連通點串在一起
	move_net = iterNet(move_net)
	#轉換為2D座標系
	arr = [[False for p2 in range(board_width**2)]for p1 in range(board_width**2)]
	#arr = np.zeros((81,81),np.bool)
	for net in range(4):
		n = len(move_net[net])	#25 20 20 16
		for i in range(n):
			for i2 in range(n):
				if move_net[net][i][i2]:
					net_y = net_size-(net&1)	#y方向的大小
					x,y = int(i/net_y)*2+(net>>1),i%net_y*2+(net&1)
					x1,y1 = int(i2/net_y)*2+(net>>1),i2%net_y*2+(net&1)
					arr[x*board_width+y][x1*board_width+y1] = True
	#加入移動
	for chess in range(chess_num*2):
		x = state[chess+1][0]
		y = state[chess+1][1]
		for dir in mov:
			x1,y1 = x + dir[0], y + dir[1]
			if x1 >=0 and x1 <board_width and y1 >=0 and y1 <board_width:	#邊界確認
				if board[x1][y1] == 0:
					arr[x*board_width+y][x1*board_width+y1] = True
	return arr
#@jit
def findNextPoints(player,state):
	move_net = getMoveNet(state)
	mov = [[0,-1],[-1,0],[-1,1],[0,1],[1,0],[1,-1]]
	targets = []
	for chess in range(chess_num):
		x = state[chess + player*chess_num + 1][0]
		y = state[chess + player*chess_num + 1][1]
		for x1 in range(board_width):
			for y1 in range(board_width):
				if move_net[x*board_width+y][x1*board_width+y1]:
					targets.append((chess+1,x1,y1))
	return targets
def isMovAble(player,state,target):
	chess,x1,y1 = target
	x = state[chess + player*chess_num][0]
	y = state[chess + player*chess_num][1]
	move_net = getMoveNet(state)
	#UI.showMsg(str((x,y))+str((x1,y1)))
	#UI.pause()
	if move_net[x*board_width+y][x1*board_width+y1]:
		return True
	return False
#@jit
def move(player,state,target):
	chess,x,y = target
	state[chess + player*chess_num] = [x,y]
	return state
#@jit
def isEndGame(player,state):
	score = 0
	for i in range(chess_num):
		score += state[i+player*chess_num+1][0]
		score += state[i+player*chess_num+1][1]
	if score == UI.init_score:####
		return True
	return False