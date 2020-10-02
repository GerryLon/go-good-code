#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[]) {
	if (argc != 2) {
		fprintf(stderr, "Usage %s filename\n", argv[0]);
		exit(1);
	}

	FILE *fp;
	int count = 0;

	fp = fopen(argv[1], "r");
	if (!fp) {
		perror("fopen()");
		exit(1);
	}

	while (fgetc(fp) != EOF) {
		count++;
	}

	// format like `wc -c filename`
	printf("%d %s\n", count, argv[1]);

	return 0;
}