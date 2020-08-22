/**
 * https://www.nowcoder.com/practice/22f9d7dd89374b6c8289e44237c70447?tpId=46&tags=&title=&diffculty=0&judgeStatus=0&rp=1
 *
	计算逆波兰式（后缀表达式）的值
	运算符仅包含"+","-","*"和"/"，被操作数可能是整数或其他表达式
	例如：
	  ["2", "1", "+", "3", "*"] -> ((2 + 1) * 3) -> 9
	  ["4", "13", "5", "/", "+"] -> (4 + (13 / 5)) -> 6
 */
package main

import (
	"fmt"
	"strconv"
)

func eval(a, b int, op string) int {
	switch op {
	case "+":
		return a+b
	case "-":
		return a-b
	case "*":
		return a*b
	case "/":
		return a / b
	}
	return 0
}

func isOp(t string) bool {
	switch t {
	case "+", "-", "*", "/":
		return true
	default:
		return false
	}
}

func evalRPN(tokens []string ) int {
	// write code here
	stack := make([]int, 0)
	var firstNumber, secondNumber, tmpResult int

	for _, t := range tokens  {
		if isOp(t) { // 遇到操作符， 取栈顶两个元素， 注意顺序
			secondNumber = stack[0]
			firstNumber = stack[1]
			stack = stack[2:]
			tmpResult = eval(firstNumber, secondNumber, t)

			// 遇到运算符， 取出栈顶两个数， 运算结果入栈
			stack = append([]int{tmpResult}, stack...)
		} else {
			firstNumber, _ = strconv.Atoi(t)
			// 遇到数字就入栈
			stack = append([]int{firstNumber}, stack...)
		}
	}
	// 正常的话， 此时栈中应该只有一个元素， 就是最终的结果
	return stack[0]
}

func main()  {
	fmt.Println(evalRPN([]string{"2", "1", "+", "3", "*"}) == 9)
	fmt.Println(evalRPN([]string{"4", "13", "5", "/", "+"}) == 6)
}
