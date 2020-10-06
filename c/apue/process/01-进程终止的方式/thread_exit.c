#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pthread.h>

// 线程要执行的代码
void *run(void * arg) {
	puts("run in new thread");
	pthread_exit((void *)9527);
}

int main() {
	pthread_t tid;
	int err;
	void *retval;

	err = pthread_create(&tid, NULL, run, NULL);
	if (err) {
		fprintf(stderr, "pthread_create(), err: %s\n", strerror(err));
		exit(1);
	}

	// 待纯种返回， 并取得其返回值
	err = pthread_join(tid, &retval);
	if (err) {
		fprintf(stderr, "pthread_join(), err: %s\n", strerror(err));
		exit(1);
	}
	printf("new thread retval: %d\n", (int)retval);

	exit(0);
}
