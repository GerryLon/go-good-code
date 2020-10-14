package semaphore

import (
	"fmt"
	"testing"
	"time"
)

func TestSemaphore(t *testing.T) {
	// 现象: 一次打印三个数
	s := NewSemaphore(3)

	for i := 0; ; i++ {
		s.Acquire()
		go func(i int) {
			defer s.Release()
			// 0 1 2
			// 3 4 5
			// ...
			// 一组内的顺序不一定, 但是都是三个三个一组
			fmt.Println(i)
			time.Sleep(time.Second)
		}(i)
	}
	select {}
}
