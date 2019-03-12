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
	route[0] = rand() % pnum;		//���s�H���_�l�I
	for (int i = 0;i < pnum;i++)
		remain[i] = 1;
	remain[route[0]] = 0;			//�_�I�w���L���ݥ]�t
}
int ANT::findNextPoint(vector< vector<double> >&tau, int point_from, vector< vector<double> >&point_dist){
	vector<double>weight(pnum, 0.0);
	double total = 0.0, w = 0.0, maxw = 0.0;
	int point_to = 0;
	// 1. �̷ӶO���X�p��֥[�v��
	for (int point = 0;point < pnum;point++)
		if (remain[point] == 1) {	//�٨S���L
			w = tau[point_from][point] / pow(point_dist[point_from][point], beta);
			if (w > maxw) {		//��X�̤jweight�����|
				maxw = w;
				point_to = point;
			}
			total += w;
			weight[point] = total;
		}
	double q = (double)rand() / RAND_MAX;
	if (q > q0) {	//����(AS��100%����)�A�_�h���l�H(�H�̤j�Ȭ��ؼ�)
		// 2. �N�v���վ㬰 0.0 ~ 1.0 ����
		for (int point = 0;point < pnum;point++)
			weight[point] /= total;
		// 3. �̷��v���H�����G��ܤU�@�ӥؼ�
		double p = (double)rand() / RAND_MAX;
		while (p > weight[point_to] || weight[point_to] == 0)
			point_to++;
	}
	return point_to;
}