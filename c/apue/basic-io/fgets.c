#include <stdio.h>
#include <stdlib.h>

#define BUF_SIZE 5

int main(int argc, char const *argv[]) {
	if (argc != 2) {
		fprintf(stderr, "Usage %s filename\n", argv[0]);
		exit(1);
	}

	int count = 0;
	FILE *fp;
	char buffer[BUF_SIZE];
	
	fp = fopen(argv[1], "r");
	if (!fp) {
		perror("fopen()");
		exit(1);
	}

	while (fgets(buffer, BUF_SIZE, fp)) {
		count++;
		printf("count: %d, %s", count, buffer);
	}

	return 0;
}
