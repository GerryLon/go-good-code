package main

import (
	"fmt"
	"net/url"

	"github.com/gorilla/schema"
)

type Person struct {
	Name  string `json:"name"`
	Phone string
	Location `json:"location"`
}
type Location struct {
	Country string `json:"country"`
	City string `json:"city"`
}

func main() {
	decoder := schema.NewDecoder()

	// 模拟url query参数: http.Request{}.Form
	queries := url.Values{
		"name": []string{"name value"},
		"phone": []string{"123"},
		"country": []string{"country value"},

		// // 模拟不存在的参数: panic: schema: invalid path "xxxxxxxx"
		// "xxxxxxxx": []string{"xxxxxxxx"},
	}
	p := Person{} // 模拟请求参数结构体

	err := decoder.Decode(&p, queries)
	if err != nil {
		panic(err)
	}

	fmt.Printf("request param: %+v\n", p)
}
