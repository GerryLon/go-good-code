#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

// 查看fopen最多能打开多少文件
//
// 可能的输出:
// fopen(): Too many open files
// max open files: 1020
int main() {
	FILE* fp = NULL;
	int count = 0;
	while (1) {
		fp = fopen("/etc/services", "r");
		if (!fp) {
			perror("fopen()");
			break;
		}
		count++;
	}
	
	printf("max open files: %d\n", count);

	return 0;
}

