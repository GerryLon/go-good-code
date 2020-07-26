package main

// func restriction_demo1() {
// 	i := 3
// 	p := &i
// 	p++ // Invalid operation: p++ (non-numeric type *int)
// 	p = &i + 5 // Invalid operation: &i + 5 (mismatched types *int and untyped int)
// }

// func restriction_demo2() {
// 	i := 3
// 	var f *float64
// 	f = &i // Cannot use '&i' (type *int) as type *float64
// }

// func restriction_demo3() {
// 	var i int64 = 1
// 	var f float64 = 1.0
// 	pi, pf := &i, &f
//
// 	pi == pf // Invalid operation: pi == pf (mismatched types *int64 and *float64)
// 	pi != pf // Invalid operation: pi != pf (mismatched types *int64 and *float64)
// }
