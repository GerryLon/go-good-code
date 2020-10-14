package errgroup

import (
	"context"
	"fmt"
	"log"
	"testing"
	"time"
)

// 运行结果说明
// 每三个一组(0,1,2; 3,4,5; ...), 每组顺序不定
// 到10的时候结束(因为出错了)
// === RUN   TestGroup
// 2
// 1
// 0
// 3
// 5
// 4
// 8
// 6
// 7
// 9
// 2020/10/14 10:10:03 too large number: 10
// --- PASS: TestGroup (4.00s)
// PASS
func TestGroup(t *testing.T) {
	g, ctx := WithContext(context.Background())
	g.Concurrency(3)

	for i := 0; i < 100; i++ {
		run(ctx, g, i)
	}

	err := g.Wait()
	log.Println(err)
}

func run(ctx context.Context, g *Group, i int) {
	g.Go(func() error {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			if i == 10 {
				return fmt.Errorf("too large number: %d", i)
			}
			fmt.Println(i)
			time.Sleep(time.Second)
			return nil
		}
	})
}

// whenErr: 决定传入的值是否会造成error
func randErr(i int, whenErr func(int) error) error {
	return whenErr(i)
}
