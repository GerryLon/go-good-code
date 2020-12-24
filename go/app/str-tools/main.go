package main

import (
	"flag"
	"fmt"
	"os"
)

var (
	name string
	value string
)

func main() {
	flag.StringVar(&name, "name", "", "tool name")
	flag.StringVar(&value, "value", "", "tool args")
	flag.Parse()

	var tools []ITool
	tools = append(tools, base64RawURLEncoding{args: []interface{}{value}})

	if len(os.Args) == 1 {
		listTools(tools)
		os.Exit(1)
	}

	match := false
	for _, v := range tools {
		if v.GetName() == name {
			match = true
			o := v.Do()
			s := o.String()
			fmt.Println(s)
			return
		}
	}

	if !match {
		fmt.Printf("no such tool: %v\n", name)
		os.Exit(1)
	}
}

func listTools(tools []ITool) {
	fmt.Println("Usage: ")
	for _, v := range tools {
		fmt.Printf("%s, usage: %s\n", v.GetName(), v.GetUsage())
	}
	fmt.Println()
}



