// 结合 golang.org/x/sync/errgroup
// 即带有并发度控制 errgroup
package errgroup

import (
	"context"
	"sync"

	"github.com/GerryLon/good-code/go/pkg/semaphore"
)

// 复制自golang.org/x/sync/errgroup
// A Group is a collection of goroutines working on subtasks that are part of
// the same overall task.
//
// A zero Group is valid and does not cancel on error.
type Group struct {
	cancel func()

	// 控制最大并发数
	sema *semaphore.Semaphore

	wg sync.WaitGroup

	errOnce sync.Once
	err     error
}

// WithContext returns a new Group and an associated Context derived from ctx.
//
// The derived Context is canceled the first time a function passed to Go
// returns a non-nil error or the first time Wait returns, whichever occurs
// first.
func WithContext(ctx context.Context) (*Group, context.Context) {
	ctx, cancel := context.WithCancel(ctx)
	sema := semaphore.NewSemaphore(0) // 默认semaphore不起作用(permits: 0)
	return &Group{cancel: cancel, sema: sema}, ctx
}

func (g *Group) Concurrency(c int) *Group {
	g.sema = semaphore.NewSemaphore(c)
	return g
}

// Wait blocks until all function calls from the Go method have returned, then
// returns the first non-nil error (if any) from them.
func (g *Group) Wait() error {
	g.wg.Wait()
	if g.cancel != nil {
		g.cancel()
	}
	return g.err
}

// Go calls the given function in a new goroutine.
//
// The first call to return a non-nil error cancels the group; its error will be
// returned by Wait.
func (g *Group) Go(f func() error) {
	g.wg.Add(1)
	g.sema.Acquire()

	go func() {
		defer g.sema.Release()
		defer g.wg.Done()

		if err := f(); err != nil {
			g.errOnce.Do(func() {
				g.err = err
				if g.cancel != nil {
					g.cancel()
				}
			})
		}
	}()
}
