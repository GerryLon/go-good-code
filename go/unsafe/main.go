package main

import (
	"fmt"
	"reflect"
	"unsafe"

	"github.com/GerryLon/good-code/go/unsafe/unsafe_model"
)

func unsafe_basic() {
	type Programmer struct {
		name string
		age uint8
	}

	p := Programmer{"gerrylon", 18}
	fmt.Println(p) // {gerrylon 18}

	// name是结构体的第一个成员, 和结构体地址相同, 所以下面两句都行
	// name := (*string)(unsafe.Pointer(&p))
	name := (*string)(unsafe.Pointer(&p.name))
	*name = "gl"

	// 结构体的起始地址, 加上age字段的偏移, 也就是age的地址
	age := (*uint8)(unsafe.Pointer(uintptr(unsafe.Pointer(&p)) + unsafe.Offsetof(p.age)))
	*age = 19
	fmt.Println(p) // {gl 19}

	// 直接取得age字段的地址
	age = (*uint8)(unsafe.Pointer(&p.age))
	*age = 20
	fmt.Println(p) // {gl 20}
}

func unsafe_change_private_field() {
	p := unsafe_model.Programmer{}
	fmt.Println(p) // { 0}

	// p.name = "gl" // Unresolved reference 'name'

	name := (*string)(unsafe.Pointer(&p))
	*name = "gl"
	fmt.Println(p) // {gl 0}

	// unsafe.Sizeof("") 即name字段的占的内存大小
	age := (*uint8)(unsafe.Pointer(uintptr(unsafe.Pointer(&p)) + unsafe.Sizeof("")))
	*age = 19
	fmt.Println(p) // {gl 19}
}

func string2bytes(s string) []byte {
	str := (*reflect.StringHeader)(unsafe.Pointer(&s))
	by := reflect.SliceHeader{
		Data: str.Data,
		Len:  str.Len,
		Cap:  str.Len,
	}
	return *(*[]byte)(unsafe.Pointer(&by))
}


func bytes2string(bs []byte) string {
	by := (*reflect.SliceHeader)(unsafe.Pointer(&bs))

	str := reflect.StringHeader{
		Data: by.Data,
		Len:  by.Len,
	}
	return *(*string)(unsafe.Pointer(&str))
}

func stringAndBytesTransformationTest() {
	s := "hello world"
	fmt.Println(s == bytes2string(string2bytes(s)))
}

func main() {
	// unsafe_basic()
	// unsafe_change_private_field()
	stringAndBytesTransformationTest()
}
