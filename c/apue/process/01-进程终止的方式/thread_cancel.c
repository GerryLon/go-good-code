#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h> // sleep


static void *run1(void *arg) {
	printf("thread 1 start\n");
	int i = 0;
	while (1) {
		i++;
		// 在不包含取消点，但是又需要取消点的地方创建一个取消点，
		// 以便在一个没有包含取消点的执行代码线程中响应取消请求
		pthread_testcancel();

		// 如果不用pthread_testcancel， 也可以用sleep
		// sleep(1);
	}

	pthread_exit((void *)10000);
}

int main() {
	pthread_t tid1;
	int err;
	void *retval;

	err = pthread_create(&tid1, NULL, run1, (void *)1);
	if (err) {
		fprintf(stderr, "pthread_create() 1 err: %s\n", strerror(err));
		exit(1);
	}

	sleep(1);
	err = pthread_cancel(tid1);
	if (err) {
		fprintf(stderr, "pthread_cancel() 1 err: %s\n", strerror(err));
		exit(1);
	}

	err = pthread_join(tid1, &retval);
	if (err) {
		fprintf(stderr, "pthread_join() 1 err: %s\n", strerror(err));
		exit(1);
	}
	printf("thread 1 retval: %d\n", (int)retval);

	exit(0);
}
