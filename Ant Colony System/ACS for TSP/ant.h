#ifndef ANT_H
#define ANT_H

#include <vector>
#include "var_def.h"
using namespace std;

class ANT {
public:
	vector<int>route;					//�������ƪ����|
	double path_len;				//�������ƪ����ʶZ��
	vector<int>remain;					//�������ƥ����L������
	void setSize(void);
	void reset(void);
	int findNextPoint(
		vector< vector<double> >&tau,
		int point_from,
		vector< vector<double> >&point_dist);
};
#endif