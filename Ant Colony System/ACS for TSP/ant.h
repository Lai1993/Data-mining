#ifndef ANT_H
#define ANT_H

#include <vector>
#include "var_def.h"
using namespace std;

class ANT {
public:
	vector<int>route;					//紀錄螞蟻的路徑
	double path_len;				//紀錄螞蟻的移動距離
	vector<int>remain;					//紀錄螞蟻未走過的城市
	void setSize(void);
	void reset(void);
	int findNextPoint(
		vector< vector<double> >&tau,
		int point_from,
		vector< vector<double> >&point_dist);
};
#endif