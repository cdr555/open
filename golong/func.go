package main

import "fmt"

func main() {
	x,y := 5,6

	fmt.Println(add(x,y))
}
func add(x,y int) int {
	return x + y
}

