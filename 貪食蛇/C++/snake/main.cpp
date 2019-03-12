/*
解題方法：使用與上個狀態的差異解題
*/
#include "stdafx.h"
#include <iostream>
#include <time.h>
int main() {
	time_t start = clock(), use = time(NULL);
	bool bin[100] = { 0 };
	char binscr[101] = { 0 };
	for (int i = 0;i < 100;i++) {
		binscr[i] = '0';
	}
	int nowdig = 0, maxdig = 0;
	int i = 0;
	while (true) {
		printf("%s(%2d/%2d)\n", binscr, nowdig, maxdig);
		i = 99;
		while (bin[i]) {
			binscr[i] = '0';
			bin[i] ^= 1;
			i--;
			nowdig--;
			if (i < 0)
				break;
		}
		nowdig++;
		binscr[i] = '1';
		bin[i] ^= 1;
		if (nowdig > maxdig) {
			maxdig = nowdig;
			use = clock() - start;
			printf("find more bit! use %3ld min %3ld.%3ld sec\n", (long)(use / 60000), (long)((use % 60000) / 1000), (long)(use % 1000));
			if (use > 3600000)
				break;
		}
	}
	system("pause");
	return 0;
}