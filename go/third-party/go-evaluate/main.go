package main

import (
	"fmt"

	"github.com/Knetic/govaluate"
)

func main() {
	expression, err := govaluate.NewEvaluableExpression("10 + 1");
	if err != nil {
		panic(err)
	}
	result, err := expression.Evaluate(nil);
	if err != nil {
		panic(err)
	}
	fmt.Println(result, result.(float64))
}
