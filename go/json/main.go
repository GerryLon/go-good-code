package main

import (
	"encoding/json"
	"fmt"
)

type ST struct {
	String string `json:"name"`
	Int *int `json:"int"`
	Slice []string `json:"slice"`
}

func main() {
	i := 1
	slice := []string{"aa", "bb"}
	st := ST{
		String: "hello",
		Int: &i,
		Slice: slice,
	}
	bytes, err := json.MarshalIndent(st, "", "  ")
	if err != nil {
		panic(err)
	}

	// {
	// 	"name": "hello",
	// 	"int": 1,
	// 	"slice": [
	// 		"aa",
	// 		"bb"
	// 	]
	// }
	fmt.Printf("%s\n", bytes)

	st2 := ST{}
	err = json.Unmarshal(bytes, &st2)
	if err != nil {
		panic(err)
	}
	// hello 1 [aa bb]
	fmt.Println(st2.String, *st2.Int, st2.Slice)

	var st3 ST
	err = json.Unmarshal([]byte(`{ "int": 0 }`), &st3)
	if err != nil {
		panic(err)
	}

	// {String: Int:0xc00010c180 Slice:[]}, false
	fmt.Printf("%+v, %v\n", st3, st3.Int == nil)

	var st4 ST
	err = json.Unmarshal([]byte(`{}`), &st4)
	if err != nil {
		panic(err)
	}

	// {String: Int:<nil> Slice:[]}, true
	fmt.Printf("%+v, %v\n", st4, st4.Int == nil)

	// 结论:
	// 指针类型的字段 可通过nil来判断 json串有没有相应的字段
	// slice类型的字段, 会自动make, 不用提前:st.Slice = make(...)
}
