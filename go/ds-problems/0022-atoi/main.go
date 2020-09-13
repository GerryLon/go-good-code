/**
https://leetcode-cn.com/problems/string-to-integer-atoi/

8. 字符串转换整数 (atoi)
请你来实现一个 atoi 函数，使其能将字符串转换成整数。

首先，该函数会根据需要丢弃无用的开头空格字符，直到寻找到第一个非空格的字符为止。接下来的转化规则如下：

如果第一个非空字符为正或者负号时，则将该符号与之后面尽可能多的连续数字字符组合起来，形成一个有符号整数。
假如第一个非空字符是数字，则直接将其与之后连续的数字字符组合起来，形成一个整数。
该字符串在有效的整数部分之后也可能会存在多余的字符，那么这些字符可以被忽略，它们对函数不应该造成影响。
注意：假如该字符串中的第一个非空格字符不是一个有效整数字符、字符串为空或字符串仅包含空白字符时，则你的函数不需要进行转换，即无法进行有效转换。

在任何情况下，若函数不能进行有效的转换时，请返回 0 。

提示：

本题中的空白字符只包括空格字符 ' ' 。
假设我们的环境只能存储 32 位大小的有符号整数，那么其数值范围为 [−231,  231 − 1]。如果数值超过这个范围，请返回  INT_MAX (231 − 1) 或 INT_MIN (−231) 。


示例 1:

输入: "42"
输出: 42
示例 2:

输入: "   -42"
输出: -42
解释: 第一个非空白字符为 '-', 它是一个负号。
     我们尽可能将负号与后面所有连续出现的数字组合起来，最后得到 -42 。
示例 3:

输入: "4193 with words"
输出: 4193
解释: 转换截止于数字 '3' ，因为它的下一个字符不为数字。
示例 4:

输入: "words and 987"
输出: 0
解释: 第一个非空字符是 'w', 但它不是数字或正、负号。
     因此无法执行有效的转换。
示例 5:

输入: "-91283472332"
输出: -2147483648
解释: 数字 "-91283472332" 超过 32 位有符号整数范围。
     因此返回 INT_MIN (−231) 。
*/
package main

import "fmt"

func myAtoi(str string) int {
	if len(str) == 0 {
		return 0
	}

	r := 0
	sign := 1
	index := 0

	// 去除开始的空格
	for index < len(str) && str[index] == ' ' {
		index++
	}
	if index >= len(str) {
		return 0
	}

	// 确定正负号
	if str[index] == '+' || str[index] == '-' {
		if str[index] == '-' {
			sign = -1
		}
		index++ // 始终指向有效部分
	}
	if index >= len(str) {
		return 0
	}

	if str[index] < '0' || str[index] > '9' {
		// 空白跳过之后 不是正负号， 也不是数字
		return 0
	}

	min := -(1 << 31)
	max := (1 << 31) - 1
	for ; index < len(str); index++ {
		if str[index] < '0' || str[index] > '9' {
			break
		}
		digit := int(str[index] - '0')
		// 注意这里不能用 r*10 + digit > max来判断， 可能越界
		if r > (max-digit)/10 {
			if sign == 1 {
				return max
			}
			return min
		}
		r = r*10 + digit
	}

	return r * sign
}

func main() {
	r := myAtoi(" ")
	fmt.Println(r)
}
