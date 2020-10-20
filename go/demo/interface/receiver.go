package main

import "fmt"

type Animal struct {
	name string
	age int
}

func (a Animal) Name(name string)  {
	a.name = name
}

func (a *Animal) Age(age int)  {
	a.age = age
}


func (a Animal) String() string {
	return fmt.Sprintf("I'm %s, %d years old", a.name, a.age)
}




