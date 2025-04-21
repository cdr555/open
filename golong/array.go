package main

import "fmt"

func main() {
	var numbers [5]int
	numbers[0] = 1
	numbers[1] = 2
	numbers[2] = 3
	numbers[3] = 4
	numbers[4] = 5

	fmt.Println(numbers[3])

	EvenNumbers := [5]int{2, 4, 6, 8, 10}
	fmt.Println(EvenNumbers[2])

	// 数组长度
	fmt.Println(len(EvenNumbers))

	// 数组遍历
	for i := 0; i < len(EvenNumbers); i++ {
		fmt.Println(EvenNumbers[i])
	}

	// 数组遍历2
	for index, value := range EvenNumbers {
		fmt.Println(index, value)
	}

	// 数组切片
	slice := EvenNumbers[1:3]
	fmt.Println(slice)

	slice2 := make([]int, 5)
	fmt.Println(slice2)

	copy(slice2, slice)
	fmt.Println(slice2)
    
	// 数组切片
	numberslice := []int{1, 2, 3, 4, 5}
	fmt.Println(numberslice)

	numberslice = append(numberslice, 6, 7, 8, 9, 10)
	fmt.Println(numberslice)

}