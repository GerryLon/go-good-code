package pb

import (
	"math/rand"
	"testing"
	"time"
)

func TestPB(t *testing.T) {
	var bar Bar
	bar.NewOption(0, 100)
	for i := 0; i <= 100; i++ {
		time.Sleep(50 * time.Millisecond)
		bar.Play(int64(i))
	}
	bar.Finish()

	var bar2 Bar
	bar2.NewOptionWithGraph(0, 100, "#")
	for i := 0; i <= 100; i++ {
		time.Sleep(time.Duration(rand.Intn(50)) * time.Millisecond)
		bar2.Play(int64(i))
	}
	bar2.Finish()
}
