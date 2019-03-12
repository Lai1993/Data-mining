import UI
import train
import battle
import replay

if __name__ == "__main__":
	while True:
		choice = UI.showMenu()
		if choice == 0:		#訓練模式
			train.train()
		elif choice == 1:	#對戰模式
			battle.battle()
		elif choice == 2:	#重播模式(輸入完整檔名，重播比賽過程)
			replay.replay()
		elif choice == 3:	#退出程式
			break