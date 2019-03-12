import os
import time
from msvcrt import kbhit,getch

def print_at(r,c,s):	#左上角為(1,1)，在(r,c)位置顯示字串s
	print("\033[{0};{1}H{2}".format(r,c,s),end='')
	print("\033[36;0H",end='')

def showMenu():
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
				return int(key)

def showBoard(player,board,round):
	chess_text = "○⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⓿❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮"
	for i in range(9):		#往左下方向
		for j in range(9):	#往右下方向
			r = 2*(i+j)+2
			c = 16-2*(i-j)+2
			print_at(r,c,chess_text[board[i][j]])
			if i!=0 and j!=8:
				print_at(r,c+2,"－")
			if i!=8:
				print_at(r+1,c-1,"／")
			if j!=8:
				print_at(r+1,c+1,"＼")
	if player == 0:
		print_at(10,40,"輪到　player1　進行移動")
		print_at(18,40,"round:{0:3d}".format(round))
		print_at(26,40,"請　　player2　等待　　")
		print_at(36,1,"")
	else:
		print_at(10,40,"請　　player1　等待　　")
		print_at(18,40,"round:{0:3d}".format(round))
		print_at(26,40,"輪到　player2　進行移動")
		print_at(36,1,"")

def showState(player,state,round):
	board = [[0 for j in range(9)]for i in range(9)]
	for i in range(31):
		x = state[i][0]
		y = state[i][1]
		board[x][y] = i
	showBoard(player,board,round)
	
line = 0
def showMsg(msg):
	global line
	print_at(line+1,70, time.strftime( "%H:%M:%S", time.localtime() ) + msg)
	line += 1
	line %= 40
	print_at(line+1,70,"                                                  ")