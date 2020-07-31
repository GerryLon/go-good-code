package binary

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsLittleEndian(t *testing.T) {
	assert.True(t, IsLittleEndian())
}
