#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[]) {
	if (argc != 2) {
		fprintf(stderr, "Usage %s filename\n", argv[0]);
		exit(1);
	}

	FILE *fp;

	fp = fopen(argv[1], "r");
	if (!fp) {
		perror("fopen()");
		exit(1);
	}

	fseek(fp, 0, SEEK_END);

	// format like `wc -c filename`
	printf("%ld %s\n", ftell(fp), argv[1]);

	fclose(fp);

	return 0;
}

