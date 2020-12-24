package main

import (
	"encoding/base64"
)

type  base64RawURLEncoding struct {
	args []interface{}
}

func (b base64RawURLEncoding) GetName() string {
	return "base64RawURLEncoding"
}

func (b base64RawURLEncoding) GetUsage() string {
	return "base64RawURLEncoding"
}

func (b base64RawURLEncoding) Do() (o Output) {
	if len(b.args) == 0 {
		return
	}

	i0 := b.args[0]
	if s, ok := i0.(string); ok {
		o.Str =  base64.RawURLEncoding.EncodeToString([]byte(s))
		return
	}

	return
}

// func base64RawURLEncoding(s string) string {
// 	return base64.RawURLEncoding.EncodeToString([]byte(s))
// }
