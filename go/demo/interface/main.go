package main

import (
	"fmt"
	"unsafe"
)

func basic() {
	var i interface{}
	var r = func() *int {
		return nil
	}()
	i = r
	fmt.Printf("%T\n", r)
	fmt.Println(i == nil, r == nil)
}

// I'm , 3 years old
// I'm , 4 years old
func fn_receiver() {
	var a Animal
	a.Name("lion")
	a.Age(3)
	fmt.Println(a)

	b := &Animal{}
	b.Name("tiger")
	b.Age(4)
	fmt.Println(b)
}

func pointer_vs_value_receiver() {
	var p People
	p = Gopher{}
	p.Say("go go go!")

	p = &PHPer{}
	p.Say("php!")
}

func get_dynamic_type_and_value() {
	var a interface{} = nil

	var b interface{} = (*int)(nil)

	var x int = 5
	var c interface{} = (*int)(&x)

	ia := *(*iface)(unsafe.Pointer(&a))
	ib := *(*iface)(unsafe.Pointer(&b))
	ic := *(*iface)(unsafe.Pointer(&c))

	// {0 0} {4851360 0} {4851360 824634175152}
	// true
	fmt.Println(ia, ib, ic)
	fmt.Println(*(*int)(unsafe.Pointer(ic.data)) == x)
}

func main() {
	// basic()
	// fn_receiver()
	// pointer_vs_value_receiver()
	get_dynamic_type_and_value()
}
