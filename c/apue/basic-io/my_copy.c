#include <stdio.h>
#include <stdlib.h>

// ./my_copy src dst
int main(int argc, char const *argv[]) {
	FILE *fp_src, *fp_dst;
	int ch; // 读出的字符

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


	while (1) {
		ch = fgetc(fp_src);
		if (ch == EOF) {
			break;
		}
		if (fputc(ch, fp_dst) == EOF) {
			break;
		}
	}


	fclose(fp_src);
	fclose(fp_dst);

	return 0;
}
