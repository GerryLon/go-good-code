package main

import (
	"fmt"
	"unsafe"
)

type Programmer struct {
	name string
	age uint8
}

func main() {
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
