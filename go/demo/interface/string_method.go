package main

import "fmt"

type App struct {
	Name string
}

// func (a App) String() string {
// 	return fmt.Sprintf("app: [%s]", a.Name)
// }

func (a *App) String() string {
	return fmt.Sprintf("app: [%s]", a.Name)
}
