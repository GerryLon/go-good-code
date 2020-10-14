package binary

import (
	"testing"
)

func TestIsLittleEndian(t *testing.T) {
	if !IsLittleEndian() {
		t.Errorf("not little endian")
	}
}
