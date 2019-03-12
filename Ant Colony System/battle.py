import random

import UI
import fileIO
import gameRule
import train
'''
battle()
getP1Move()
getP2Move()
'''
board_width = UI.board_width
net_size = UI.net_size
chess_num = UI.chess_num
finish_score = UI.finish_score
def battle(tau):
	state = gameRule.init()
	UI.showState(0,state,1)
	route = []
	round = 0	#回合數
	while True:									#每一個回合
		round += 1
		while True:
			target = getP1Move(state,tau)			#取得玩家1的移動target=(chess,x,y)
			if gameRule.isMovAble(0,state,target):			#若不可移動，則重新取得
				state = gameRule.move(0,state,target)	#移動棋子
				UI.showState(1,state,round)		#刷新畫面
				route.append(target)			#紀錄移動
				break
			UI.showMsg("你不能這麼做(chess{0}:({1},{2}))".format(target[0],target[1],target[2]))
			UI.pause()
		if gameRule.isEndGame(0,state):
			UI.showMsg("遊戲結束，恭喜玩家一獲勝")
			break

		while True:
			target = getP2Move(state)			#取得玩家2的移動target=(chess,x,y)
			if gameRule.isMovAble(1,state,target):			#若不可移動，則重新取得
				state = gameRule.move(1,state,target)	#移動棋子
				UI.showState(0,state,round)		#刷新畫面
				route.append(target)			#紀錄移動
				break
			UI.showMsg("你不能這麼做(chess{0}:({1},{2}))".format(target[0],target[1],target[2]))
		if gameRule.isEndGame(1,state):
			UI.showMsg("遊戲結束，恭喜玩家二獲勝")
			break
	# saveRec(fname)

def getP1Move(state,tau):
	#step 4 : 螞蟻尋找所有可以走的下一步的狀態(所有鄰居)
	targets = gameRule.findNextPoints(0,state)	#targets = [[chess,i,j]*n]
	
	#step 5 : 螞蟻計算這些下一步的分數
	scores,weight,fvalue = train.calcScore(0,tau,state,targets)
	#for target in targets:
	#	UI.showMsg(str(target))
	#step 6 : 螞蟻依照這些下一步的分數進行輪盤法選擇
	i = train.weightChoice(weight)
	target = targets[i]
	UI.print_at(12,40,"value:{0:5.1f}".format(fvalue[i]))
	return target

def getP1Move2(state,tau):
	#chess為player1/2的第幾個棋子
	chess = int(input())
	x = int(input())
	y = int(input())
	
	return (chess,x,y)
def getP2Move(state):
	#chess為player1/2的第幾個棋子
	while True:
		try:
			chess = int(input())
			x = state[chess+chess_num][0]
			y = state[chess+chess_num][1]
			mov = [[0,-1],[-1,0],[-1,1],[0,1],[1,0],[1,-1]]
			while True:
				i = int(input())
				if i == -1:
					break
				elif i < 6:
					x += mov[i][0]
					y += mov[i][1]
				elif i < 12:
					x += mov[i-6][0]*2
					y += mov[i-6][1]*2
			return (chess,x,y)
		except:
			UI.showMsg("輸入錯誤，請重新輸入")
			#if chess == 0:
			return False