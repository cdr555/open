//函数类型
func addTwoInts(_ a: Int, _ b: Int) -> Int {
    return a + b
}
//使用函数类型
let mathFunction: (Int, Int) -> Int = addTwoInts
print("Result: \(mathFunction(2, 3))")
// 打印 "Result: 5"

//函数类型作为参数类型
func printMathResult(_ mathFunction: (Int, Int) -> Int, _ a: Int, _ b: Int) {
    print("Result: \(mathFunction(a, b))")
}
printMathResult(addTwoInts, 3, 5)
// 打印 "Result: 8"

//函数类型作为返回类型
func stepForward(_ input: Int) -> Int {
    return input + 1
}
func stepBackward(_ input: Int) -> Int {
    return input - 1
}

func chooseStepFunction(backward: Bool) -> (Int) -> Int {
    return backward ? stepBackward : stepForward
}

var currentValue = 3
let moveNearerToZero = chooseStepFunction(backward: currentValue > 0)

print("Counting to zero:")
// Counting to zero:
while currentValue != 0 {
    print("\(currentValue)... ")
    currentValue = moveNearerToZero(currentValue)
}
print("zero!")

//嵌套函数
func ChooseStepFunction(backward: Bool) -> (Int) -> Int {
    func stepForward(input: Int) -> Int { return input + 1 }
    func stepBackward(input: Int) -> Int { return input - 1 }
    return backward ? stepBackward : stepForward
}
var CurrentValue = -4
let MoveNearerToZero = ChooseStepFunction(backward: CurrentValue > 0)
// MoveNearerToZero 现在引用了嵌套的 stepForward() 函数
while CurrentValue != 0 {
    print("\(CurrentValue)... ")
    CurrentValue = MoveNearerToZero(CurrentValue)
}
print("zero!")
// -4...
// -3...
// -2...
// -1...
// zero!
