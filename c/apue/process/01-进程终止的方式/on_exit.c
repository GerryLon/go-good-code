#include <stdio.h>
#include <stdlib.h>

// on_exit
static void exit_handler(int status, void *arg) {
	printf("exit status: %d, arg: %s\n", status, (char *)arg);
}

// atexit
static void exit_handler2() {
	printf("exit_handler2()\n");
}

// atexit
static void exit_handler3() {
	printf("exit_handler3()\n");
}

int main() {
	char* reason = "some reason";
	int i;

	char strs[3][80];

	for (i = 0; i < 3; i++) {
		sprintf(strs[i], "[%d] %s", i, reason);
		// 注意： 为了逻辑清晰， 忽略了检查返回值
		on_exit(exit_handler, strs[i]);
	}


	// 注意： 为了逻辑清晰， 忽略了检查返回值
	atexit(exit_handler2);
	atexit(exit_handler3);

	// exit_handler3()
	// exit_handler2()
	// exit status: 233, arg: �
	// exit status: 233, arg:
	// exit status: 233, arg:
	// return (233);

	// exit_handler3()
	// exit_handler2()
	// exit status: 233, arg: [2] some reason
	// exit status: 233, arg: [1] some reason
	// exit status: 233, arg: [0] some reason
	exit(233);
}
