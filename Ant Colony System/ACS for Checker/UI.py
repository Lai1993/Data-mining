import os
import time
from msvcrt import kbhit,getch
import numpy as np
'''
print_at()
showMenu()
showBoard()
showState()
showMsg()
'''

net_size = 3
board_width = net_size*2-1
chess_num = net_size*(net_size+1)>>1
init_score = 8		#5:40	4:20	3:8
finish_score = 40	#5:200	4:100	3:40
#chess_text = "○①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯"	#5
#chess_text = "○①②③④⑤⑥⑦⑧⑨⑩❶❷❸❹❺❻❼❽❾❿"				#4
chess_text = "○①②③④⑤⑥❶❷❸❹❺❻"						#3
#low, high = 5,11	#9*9, 15chess
#low, high = 4,8	#7*7,10chess
low, high = 3,5	#5*5,6chess
def print_at(r,c,s):	#左上角為(1,1)，在(r,c)位置顯示字串s
	print("\033[{0};{1}H{2}\033[36;0H".format(r,c,s))

is_board_init = False
def showMenu():
	global is_board_init
	os.system("cls")
	print("跳棋AI v0.0，按下鍵盤的數字鍵進行選擇\n")
	print("0.訓練模式")
	print("1.對戰模式")
	print("2.重播模式")
	print("3.退出程式")
	while True:
		if kbhit():
			key = getch()
			if key in [b'0',b'1',b'2',b'3']:
				os.system("cls")
				print("\033[36;0H")
				is_board_init = False
				return int(key)

def boardInit():
	for i in range(board_width):
		for j in range(board_width):
			r = 2*(i+j)+2
			c = 16-2*(i-j)+2
			if i!=0 and j!=board_width-1:
				print_at(r,c+2,"－")
			if i!=board_width-1:
				print_at(r+1,c-1,"／")
			if j!=board_width-1:
				print_at(r+1,c+1,"＼")
	print_at(10,40,"　player1　")
	print_at(26,40,"　player2　")
def showBoard(player,board,round):
	for i in range(board_width):		#往左下方向
		for j in range(board_width):	#往右下方向
			r = 2*(i+j)+2
			c = 16-2*(i-j)+2
			ch = board[i][j]
			print_at(r,c,chess_text[ch])
	global is_board_init
	if not is_board_init:
		boardInit()
		is_board_init = True
	print_at(18,40,"round:{0:3d}".format(round))

def showState(player,state,round):
	board = np.zeros((board_width,board_width),np.int)
	for i in range(1+chess_num*2):
		x = state[i][0]
		y = state[i][1]
		board[x][y] = i
	showBoard(player,board,round)
	
line = 0
def showMsg(msg):
	global line
	print_at(line+1,70, time.strftime( "%H:%M:%S\t", time.localtime() ))
	print_at(line+1,80, msg)
	line += 1
	print_at(line+1,70,"     "*15)
	line %= 42

def pause():
	print("\033[35;0H")
	os.system("pause")