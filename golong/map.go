package main

import "fmt"

func main() {
	person := make(map[string]string)
	person["name"] = "c"
	person["age"] = "20"
	fmt.Println(person)

	person2 := make(map[string]string)
	person2["name"] = "d"
	person2["age"] = "22"
	fmt.Println(person2)

	person3 := map[string]string{
		"name": "e",
		"age":  "24",
	}
	fmt.Println(person3)

	// 遍历map
	for key, value := range person3 {
		fmt.Println(key, value)
	}

	// // 删除map
	// delete(person3, "age")
	// fmt.Println(person3)

	// // 判断map是否存在
	// value, ok := person3["age"]
	// fmt.Println(value, ok)
	
}