package main

import "fmt"

func main() {
	age := 18
	switch age {
	case 10:
		fmt.Println("You are an child")
	case 19:
		fmt.Println("You are a teenager")
	case 20:
		fmt.Println("You are an adult")
	default:
		fmt.Println("no match")
	}
}