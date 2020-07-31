package binary

import (
	"unsafe"
)

func IsLittleEndian() bool {
	var i int32 = 0x01020304
	firstByte := *((*byte)(unsafe.Pointer(&i)))
	return firstByte == 0x04
}


