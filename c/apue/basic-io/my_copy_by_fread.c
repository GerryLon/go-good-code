#include <stdio.h>
#include <stdlib.h>

#define BUF_SIZE 64

int main(int argc, char const *argv[]) {
	FILE *fp_src, *fp_dst;
	char buffer[BUF_SIZE];
	int n = 0;

	if (argc != 3) {
		fprintf(stderr, "Usage: %s src dst\n", argv[0]);
		exit(1);
	}

	fp_src = fopen(argv[1], "r");
	if (!fp_src) {
		perror("fopen() source");
		exit(1);
	}

	fp_dst = fopen(argv[2], "w");
	if (!fp_dst) {
		fclose(fp_src);
		perror("fopen() destination");
		exit(1);
	}


	while ((n = fread(buffer, 1, BUF_SIZE, fp_src)) > 0) {
		fwrite(buffer, 1, n, fp_dst);
	}

	fclose(fp_src);
	fclose(fp_dst);

	return 0;
}
