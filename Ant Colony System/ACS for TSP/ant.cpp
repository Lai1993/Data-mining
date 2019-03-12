#include "ant.h"

void ANT::setSize(void) {
	route.resize(pnum + 1);
	remain.resize(pnum);
	reset();
}
void ANT::reset(void) {
	path_len = 0.0;
	for (int i = 1;i < pnum + 1;i++) 
		route[i] = 0;
	route[0] = rand() % pnum;		//重新隨機起始點
	for (int i = 0;i < pnum;i++)
		remain[i] = 1;
	remain[route[0]] = 0;			//起點已走過不需包含
}
int ANT::findNextPoint(vector< vector<double> >&tau, int point_from, vector< vector<double> >&point_dist){
	vector<double>weight(pnum, 0.0);
	double total = 0.0, w = 0.0, maxw = 0.0;
	int point_to = 0;
	// 1. 依照費洛蒙計算累加權重
	for (int point = 0;point < pnum;point++)
		if (remain[point] == 1) {	//還沒走過
			w = tau[point_from][point] / pow(point_dist[point_from][point], beta);
			if (w > maxw) {		//找出最大weight的路徑
				maxw = w;
				point_to = point;
			}
			total += w;
			weight[point] = total;
		}
	double q = (double)rand() / RAND_MAX;
	if (q > q0) {	//探索(AS為100%探索)，否則為追隨(以最大值為目標)
		// 2. 將權重調整為 0.0 ~ 1.0 之間
		for (int point = 0;point < pnum;point++)
			weight[point] /= total;
		// 3. 依照權重隨機結果選擇下一個目標
		double p = (double)rand() / RAND_MAX;
		while (p > weight[point_to] || weight[point_to] == 0)
			point_to++;
	}
	return point_to;
}