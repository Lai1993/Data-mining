// ACOforTSP.cpp: 定義主控台應用程式的進入點。
#include "stdafx.h"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <ctime>
#include <random>
#include <vector>

#include "var_def.h"
#include "ant.h"
#define FILE1 "D://eil51.txt"
#define FILE2 "D://ans.csv"

using namespace std;

double getSolByGreedy(vector< vector<double> >&point_dist);
int main(int argc,char* argv[]){
	vector<double> iter_opt(ITER,0.0);			//每個round第iter世代的最佳解
	vector<double> iter_sum(ITER,0.0);			//每個round第iter世代的平均
	vector<double> local_opt(ROUND,0.0);		//每個round的最佳解
	vector<int> local_opt_route(pnum, 0);		//路徑
	vector<int> global_opt_route(pnum, 0);		//路徑
	double global_opt = 0.0;					//整支程式的最佳解
	double global_sum = 0.0;					//平均值
	double global_sumsq = 0.0;					//標準差
	srand(time(NULL));
	// 0. 讀取與處理資料
	ifstream fin(FILE1);
	ofstream fout(FILE2);
	vector< vector<double> > point_coord(pnum,vector<double>(2));
	for (int point = 0;point < pnum;point++)
		fin >> point_coord[point][0] >> point_coord[point][1];
	// 1. 初始設定
		// 1-1 計算各點之間的距離
	vector< vector<double> >point_dist(pnum, vector<double>(pnum));
	for (int i = 0;i < pnum;i++)
		for (int j = 0;j < pnum;j++)
			point_dist[i][j] = (int)(sqrt(
				pow(point_coord[i][0] - point_coord[j][0], 2) +		//(x1 - x2)^2
				pow(point_coord[i][1] - point_coord[j][1], 2))+ 0.5);		//(y1 - y2)^2
		// 1-2 用greedy找一個還不錯的解，並設定初始費洛蒙
	double tau0 = 1.0 / getSolByGreedy(point_dist);
	vector< vector<double> >tau(pnum, vector<double>(pnum,tau0));	//pnum * pnum set tau0
		// 1-3 初始化螞蟻
	int point_from,point_to;
	vector<ANT> ant(antNum);
	for (int antID = 0;antID < antNum;antID++)
		ant[antID].setSize();
	// 2. 循環次數，總共ROUND次循環
	for (int round = 0;round < ROUND;round++) {
		cout << "round:" << round + 1 << endl;
		// 3. 迭代次數，總共迭代ITER次
		for (int iter = 0; iter < ITER;iter++) {
			// 4. 重置螞蟻內部資訊
			for (int antID = 0;antID < antNum;antID++)
				ant[antID].reset();
			// 5. 每隻螞蟻各自尋找下一個點
			for (int point = 0;point < pnum;point++) {
				for (int antID = 0;antID < antNum;antID++) {
					// 5-1 對每隻螞蟻尋找下個目標
					point_from = ant[antID].route[point];
					if (point < pnum-1)
						point_to = ant[antID].findNextPoint(tau, point_from, point_dist);
					else		//最後一個點為起點
						point_to = ant[antID].route[0];
					// 5-2 更新路徑和剩餘點，螞蟻行走距離
					ant[antID].route[point + 1] = point_to;
					ant[antID].path_len += point_dist[point_from][point_to];
					ant[antID].remain[point_to] = 0;
					// 5-3 更新螞蟻走過路徑的費洛蒙(局部更新)
					tau[point_from][point_to] *= (1 - rho);		//(1)
					tau[point_from][point_to] += rho * tau0;	//(2)
					// (1)(2)	ACS
					// (1)		ACS with delta tau =0
					// None		ACS without local-updating or AS
					tau[point_to][point_from] = tau[point_from][point_to];
				}
			}
			// 6-1 更新最佳解(per iter)
			for (int antID = 0; antID < antNum;antID++)	//update local opt
				if (ant[antID].path_len < local_opt[round] || local_opt[round] == 0.0) {
					local_opt[round] = ant[antID].path_len;
					for (int point = 0;point < pnum + 1;point++)
						local_opt_route[point] = ant[antID].route[point];
					cout << "iter:" << setw(4) << iter + 1
						<< "\tlocal_opt:" << setw(7) << local_opt[round] << endl;
				}
			if(local_opt[round] < iter_opt[iter] || iter_opt[iter] == 0.0)
				iter_opt[iter] = local_opt[round];				//update iter opt
			iter_sum[iter] += local_opt[round];				//update iter avg
			// 7. 路徑揮發費洛蒙
			for (int point_from = 0;point_from < pnum;point_from++)
				for (int point_to = 0;point_to < pnum;point_to++)
					tau[point_from][point_to] *= (1 - alpha);
			// 8-1 螞蟻散發費洛蒙(AS)
			/*for (int antID = 0;antID < antNum;antID++) {
				for (int i = 0;i < pnum;i++) {
					point_from = ant[antID].route[i];
					point_to = ant[antID].route[i + 1];
					tau[point_from][point_to] += 100 / ant[antID].path_len;
					tau[point_to][point_from] = tau[point_from][point_to];
				}
			}*/
			// 8-2 螞蟻散發費洛蒙(ACS)
			for (int point = 0;point < pnum;point++) {
				point_from = local_opt_route[point];
				point_to = local_opt_route[point+1];
				tau[point_from][point_to] += 1.0 / local_opt[round];
				tau[point_to][point_from] = tau[point_from][point_to];
			}
		}
		// 6-2 更新最佳解(per round)
		if (local_opt[round] < global_opt || global_opt == 0.0) {			//update global opt
			global_opt = local_opt[round];
			for (int point = 0;point<pnum + 1;point++)
				global_opt_route[point] = local_opt_route[point];
		}
		global_sum += local_opt[round];
		global_sumsq += pow(local_opt[round], 2.0);
		cout << "opt:" << setw(7) << global_opt;
		cout << "\tavg:" << setw(7) << global_sum / (double)(round + 1);
		cout << "\t SD:" << setw(7) << pow(global_sumsq / (double)(round + 1) - pow(global_sum / (double)(round + 1), 2), 0.5) << endl;
		// 9. 重置部分變數
		for (int point_from = 0;point_from < pnum;point_from++)
			for (int point_to = 0;point_to < pnum;point_to++)
				tau[point_from][point_to] = tau0;
	}
	// 9. 顯示結果
	cout << "gloal best route:" << endl;
	for (int point = 0;point < pnum + 1;point++) 
		cout << setw(3) << global_opt_route[point];
	cout << endl;
	//   長條圖：各種模式的(opt, avg, sd)
	fout << "opt,avg,SD\n" << global_opt << "," << global_sum / (double)(ROUND)
		 << "," << pow(global_sumsq / (double)(ROUND)-pow(global_sum / (double)(ROUND), 2), 0.5) << endl;
	fout << "opt,avg,round,coord_x,coord_y\n";
	for (int iter = 0;iter < ITER;iter++) {
		// 折線圖(iter*len)：各種模式的opt, avg
		fout << iter_opt[iter] << "," << iter_sum[iter] / (double)(ROUND);
		//  Y散佈圖：每個round的path len
		if (iter < ROUND)
			fout << "," << local_opt[iter];
		// XY散佈圖：各種模式的opt route(coord)
		if (iter < pnum + 1)
			fout << "," << point_coord[global_opt_route[iter]][0] << "," << point_coord[global_opt_route[iter]][1];
		fout << endl;
	}
	system("pause");
	return 0;
}
double getSolByGreedy(vector< vector<double> >&point_dist){
	double len = 0.0; // 位移
	vector<int>remain(pnum,0); // 記錄走過位置
	// 隨機初始城市位置
	int ori_city = rand() % pnum;
	int city = ori_city;
	remain[city] = 1;
	for (int i = 0;i < pnum - 1;i++) {
		double min = 99999999.0;
		// 尋找距離目前城市的最近城市(不是自己且沒有走過)
		for (int j = 0;j < pnum;j++)
			if (point_dist[city][j] < min && remain[j] == 0) {
				min = point_dist[city][j];
				city = j;
			}
		// 計算位移、更新走過的位置
		len += min;
		remain[city] = 1;
		cout << setw(5) << city;
	}
	cout << endl;
	len += point_dist[ori_city][city];
	cout << "len:" << len << endl;
	return len;
}