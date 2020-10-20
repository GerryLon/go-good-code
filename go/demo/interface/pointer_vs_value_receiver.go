package main

import "fmt"

type People interface {
	Say(string)
}

type Gopher struct {
}

// cannot use Gopher literal (type Gopher) as type People in assignment:
// Gopher does not implement People (Say method has pointer receiver)
// func (g *Gopher) Say(s string) {
// 	fmt.Println(s)
// }

func (g Gopher) Say(s string) {
	fmt.Println(s)
}

type PHPer struct{}

func (P PHPer) Say(s string) {
	fmt.Println(s)
}
