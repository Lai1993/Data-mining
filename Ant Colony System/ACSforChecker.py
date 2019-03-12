import UI
import train
import battle
import replay

if __name__ == "__main__":
	tau = {}
	while True:
		choice = UI.showMenu()
		if choice == 0:		#訓練模式
			tau = train.train(tau)
		elif choice == 1:	#對戰模式
			battle.battle(tau)
		elif choice == 2:	#重播模式(輸入完整檔名，重播比賽過程)
			replay.replay()
		elif choice == 3:	#退出程式
			break