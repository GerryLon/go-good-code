package main

import (
	"fmt"
	"runtime"
	"sync"
)

func main() {
	runtime.GOMAXPROCS(1)
	wg := &sync.WaitGroup{}
	const N = 256
	wg.Add(N)
	ch := make(chan string, N)
	for i := 0; i < N/2; i++ {
		go func() {
			defer wg.Done()
			// fmt.Println("A:", i)
			ch <- fmt.Sprintf("A: %d", i)
		}()
	}

	for i := 0; i < N/2; i++ {
		go func(i int) {
			defer wg.Done()
			// fmt.Println("B:", i)
			ch <- fmt.Sprintf("B: %d", i)
		}(i)
	}

	wg.Wait()
	close(ch)

	for s := range ch {
		fmt.Println(s)
	}
}
