import time
import random
import numpy as np

import fileIO
import gameRule
import UI

ITER = 10000
antNum = 20
rho = 0.1
alpha = 0.1

board_width = UI.board_width
chess_num = UI.chess_num
init_score = UI.init_score
finish_score = UI.finish_score
def stateToScore(pstate):	#輸入該玩家的狀態，給出初始分數
	score = 0
	for i in range(chess_num):
		score += int(pstate[i]/board_width)
		score += pstate[i]%board_width
	return score
def calcScore(player,tau,state,targets):
	scores = []		#固定值，做為每個狀態的初始費洛蒙
	fvalue = []		#費洛蒙，用來計算權重
	weight = []		#權重
	for target in targets:
		chess,x,y = target	#chess = 1~30
		p1 = [state[i+1][0]*board_width + state[i+1][1] for i in range(chess_num)]
		p2 = [state[i+1+chess_num][0]*board_width + state[i+1+chess_num][1] for i in range(chess_num)]
		if player == 0:
			p1[chess-1] = x*board_width + y
			p1.sort()
			p2.sort()
			if tau.__contains__(str(p1+p2)):
				#tau[str(p1+p2)] = stateToScore(p1)
				fvalue.append(tau[str(p1+p2)])
			else:
				fvalue.append(stateToScore(p1))
			scores.append(stateToScore(p1))
		else:
			p2[chess-1] = x*board_width + y
			p1.sort()
			p2.sort()
			fvalue.append(stateToScore(p2))
			scores.append(stateToScore(p2))
	threshold = np.mean(fvalue) - np.std(fvalue)
	fvalue_mean = np.mean(fvalue)
	weight = [0 if value < threshold else 2**(value-fvalue_mean) for value in fvalue]
	return scores,weight,fvalue
def weightChoice(weight): #加權隨機選取
	w = random.uniform(0,np.sum(weight))
	i = 0
	while w > 0:
		w -= weight[i]
		i += 1
	return i-1
#@jit
def mirror(state):
	for i in range(chess_num*2):
		state[i+1]=[board_width-1-state[i+1][0],board_width-1-state[i+1][1]]
	return state
def localUpdate(player,tau,state):
	p1 = [state[i+1][0]*9 + state[i+1][1] for i in range(chess_num)]
	p2 = [state[i+1+chess_num][0]*9 + state[i+1+chess_num][1] for i in range(chess_num)]
	p1.sort()
	p2.sort()
	if player == 0:
		if tau.__contains__(str(p1+p2)):	#不存在就設為tau0
			tau[str(p1+p2)] *= (1-rho)
			tau[str(p1+p2)] += rho*stateToScore(p1)
	else:
		if tau.__contains__(str(p2+p1)):
			tau[str(p2+p1)] *= (1-rho)
			tau[str(p2+p1)] += rho*stateToScore(p2)
	return tau
def globalUpdate(tau,rec,round,score):
	if round > 320:
		return tau
	player = 0
	step = 1
	round = (round>>1)+1
	iswin = score[0]>score[1]
	wins = abs(score[0]-score[1])
	for state in rec:
		#print(player,step,round)
		p1 = [state[i+1][0]*board_width + state[i+1][1] for i in range(chess_num)]
		p2 = [state[i+1+chess_num][0]*board_width + state[i+chess_num][1] for i in range(chess_num)]
		p1.sort()
		p2.sort()
		if not tau.__contains__(str(p1+p2)):	#不存在就設為tau0
			tau[str(p1+p2)] = stateToScore(p1)
		#tau[str(p1+p2)] = 0.9*tau[str(p1+p2)]+0.1*(tau[str(p1+p2)]-round+step-(score[player]<score[player^1]))
		#tau[str(p1+p2)] = 0.9*tau[str(p1+p2)]+0.1*(tau[str(p1+p2)]*wins**iswin)
		tau[str(p1+p2)] = 0.9*tau[str(p1+p2)]+0.1*(finish_score-round+step)#-(score[player] < finish_score))
		#tau[str(p1+p2)] += ((score[player] > score[player^1])-(score[player] < score[player^1]))/round
		step += player
		player ^= 1
	#UI.pause()
	return tau
def train(tau):
	#step 0 : 初始化費洛蒙(從檔案讀取或從頭開始)
	#tau = fileIO.loadModel()
	init_state = gameRule.init()
	time_start = time.clock()
	total_round = 0
	#step 1 : 訓練的世代數
	for iter in range(ITER):
		#step 2-1 : 進行初始化，包含起始狀態、移動紀錄、回合數、是否結束，結束狀態
		states = [[chess for chess in init_state] for ant in range(antNum)]
		rec = [[]for i in range(antNum)]
		round = 0	#回合數，任一玩家移動一次都算一個回合
		end_game_state = [False for i in range(antNum)]
		end_game_num = 0
		p1win = 0
		score = [[0.0,0.0]for ant in range(antNum)]
		value = [[0.0,0.0]for ant in range(antNum)]
		end_round = [0 for ant in range(antNum)]
		UI.showState(0,states[0],round)
		#UI.pause()
		#step 2-2 : 讓10對螞蟻進行戰鬥，直到全部結束
		while end_game_num != antNum:
			#step 3 : 每一個戰場的螞蟻移動一步
			for ant in range(antNum):
				if end_game_state[ant]:	#如果對戰已經結束
					continue
				#step 4 : 螞蟻尋找所有可以走的下一步的狀態(所有鄰居)
				targets = gameRule.findNextPoints(round&1,states[ant])	#targets = [[chess,i,j]*n]
				#UI.showMsg("round:{0:4d}, node:{1:3d}".format(round,len(targets)))
				#step 5 : 螞蟻計算這些下一步的分數
				scores,weight,fvalue = calcScore(round&1,tau,states[ant],targets)
				
				#step 6 : 螞蟻依照這些下一步的分數進行輪盤法選擇
				i = weightChoice(weight)
				target = targets[i]
				score[ant][round&1] = scores[i]
				value[ant][round&1] = fvalue[i]
				
				#step 7 : 螞蟻依照選擇結果進行移動
				states[ant] = gameRule.move(round&1,states[ant],target)
				
				#step 8 : 螞蟻對於這個選擇進行更新tau'=(1-a)tau+a*tau0
				#tau = localUpdate(round&1,tau,states[ant])
				
				#step 9 : 紀錄並顯示本次移動的相關資訊
				#step 10 : 將選項旋轉，作為對手繼續選擇
				#chess,x,y = target
				if round&1 == 0:		#實際為玩家一行動時
					if ant == 0:
						UI.showState(0,states[ant],round+1)
						UI.print_at(11,40,"score:{0:3d}".format(score[ant][0]))
						UI.print_at(12,40,"value:{0:5.1f}".format(value[ant][0]))
					#rec[ant].append((chess,x,y))
					rec[ant].append([coord for coord in states[ant]])
					states[ant] = mirror(states[ant])
				else:
					states[ant] = mirror(states[ant])
					if ant == 0:
						UI.showState(0,states[ant],round+1)
						UI.print_at(27,40,"score:{0:3d}".format(score[ant][1]))
						UI.print_at(28,40,"value:{0:5.1f}".format(value[ant][1]))
					#rec[ant].append((chess+15,8-x,8-y))
					rec[ant].append([coord for coord in states[ant]])
				#需要state score 
				#step 11 : 判斷是否遊戲結束
				#if round%40 == 39:
				#	UI.pause()
				if gameRule.isEndGame(round&1,states[ant]) or round > 320:
					end_game_state[ant] = True
					end_game_num += 1
					end_round[ant] = round
					if round&1 == 0:
						p1win += 1
					UI.showMsg("player{0:2d}-{1} win! score:{2} round:{3:4d}".format(ant,1+(round&1),score[ant],round))
					#UI.pause()
			round += 1
			total_round += 1
		#step 12 : 依照對戰結果更新路徑分數
		tausize = len(tau)
		for ant in range(antNum):
			tau = globalUpdate(tau,rec[ant],end_round[ant],score[ant])
		#UI.showMsg("iter:{0:4d}/{1} player{2} win! score:{3} use round:{4:4d} tausize:{5}/{6:.0f}/{7:3d} tpr:{8:.2f}"\
		#.format(iter,ant,1+(round&1),score[ant],round,len(tau),len(tau)/(iter+1),len(tau)-tausize,(time.clock()-time_start)*1000/total_round))
		UI.showMsg("iter:{0:5d} total round:{1:4d} tausize:{2:7d}/{3:3d}({4:4d}) tpr:{5:.2f} win%:{6:3.2f}    "\
		.format(iter,np.sum(end_round),len(tau),len(tau)-tausize\
		,np.sum(end_round)-len(tau)+tausize,(time.clock()-time_start)*1000/total_round,p1win*100/antNum))
	UI.pause()
		#step 13 : 儲存訓練結果
		#if iter in [0,10,30,100,300,1000,3000,10000]:
		#	fileIO.saveRec(iter)
		#	fileIO.saveModel(iter)
	return tau


















