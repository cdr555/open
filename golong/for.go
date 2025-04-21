package main

import "fmt"

func main() {
	var age int = 18
	// age := 18 简写
	if age >= 18 {
		fmt.Println("You are an adult")
	} else {
		fmt.Println("You are not an adult")
	}

	// 循环
	for i := 0; i < 10; i++ {
		fmt.Println(i)
	}
	
}
