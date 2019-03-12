/*
解題方法：使用hill climbing來進行
*/
#include "stdafx.h"
#include <iostream>
#include <time.h>
#include <fstream>
using namespace std;
#define ROUND 30				//要跑幾次round
#define ITER 100
void hillClimbing();
int main() {
	srand(time(NULL));
	hillClimbing();

	system("start D:\\plotxy.gp");
	system("pause");
	system("start D:\\01prob_hc.png");
	return 0;
}
void hillClimbing() {
	ofstream fout("D:\\01prob_hc.csv");	//檔案輸出位置
	int sol[210] = { 0 };			//紀錄搜尋結果
	for (int round = 0;round < ROUND;round++) {
		//初始化
		bool bin[100] = { 0 }, better[100] = { 0 };
		int dig = 0, maxdig = 0;
		for (int i = 0;i < 100;i++) {
			better[i] = rand()%2;
			maxdig += better[i];
		}
		//做500次iter
		for (int iter = 0;iter <= ITER;iter++) {
			//每10次iter紀錄結果
			if (iter % 10 == 0)
				sol[iter / 10] += maxdig;
			//隨機選擇一個bit進行0 1互換
			for (int i = 0;i < 100;i++)
				bin[i] = better[i];
			bin[rand() % 100] ^= 1;	//1^1=0, 0^1=1
			//計算該鄰居擁有的1數
			dig = 0;
			for (int i = 0;i < 100;i++)
				dig += bin[i];
			//如果是目前最好，將其替換
			if (dig > maxdig) {
				maxdig = dig;
				for (int i = 0;i < 100;i++)
					better[i] = bin[i];
			}
		}
	}
	//輸出結果(x,y)=(sol,iter)
	for (int iter = 0;iter < (ITER/10+1);iter++) {
		fout << iter * 10 << ' ' << (double)(sol[iter]) / ROUND << '\n';
	}
	fout.close();
}