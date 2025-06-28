func greet(person: String) -> String {
    let greeting = "hello,\(person)"
    return greeting
}
print(greet(person: "Anna"))

//无参数函数
func sayHelloWorld() -> String {
    return "hello,world"
}
print(sayHelloWorld())

//多参数函数
func Greet(person: String, alreadyGreeted: Bool) -> String {
    if alreadyGreeted {
        return "Hello again, \(person)!"
    } else {
        return greet(person: person)
    }
}
print(Greet(person: "Tim", alreadyGreeted: true))
// 打印 "Hello again, Tim!"

//无返回值函数
func nogreet(person: String) {
    print("Hello, \(person)!")
}
nogreet(person: "Dave")

//多重返回值函数
func minMax(array: [Int]) -> (min: Int, max: Int)? {
    if array.isEmpty { return nil }
    var currentMin = array[0]
    var currentMax = array[0]
    for value in array[1..<array.count] {
        if value < currentMin {
            currentMin = value
        } else if value > currentMax {
            currentMax = value
        }
    }
    return (currentMin, currentMax)
}
if let bounds = minMax(array: [8, -6, 2, 109, 3, 71]) {
print("min is \(bounds.min) and max is \(bounds.max)")}
// 打印 "min is -6 and max is 109"

//隐式返回的函数 如果函数的整个主体是一个表达式，则函数隐式返回该表达式
func greeting(for person: String) -> String {
    "Hello, \(person)!"
}
print(greeting(for: "Dave"))
//与上面的函数等价
func anotherGreeting(for person: String) -> String {
    return "Hello, " + person + "!"
}
print(anotherGreeting(for: "Dave"))
// 打印 "Hello, Dave!"

//函数参数标签和参数名称
func someFunction(firstParameterName: Int, secondParameterName: Int) {
    // 在函数体内，firstParameterName 和 secondParameterName 代表参数中的第一个和第二个参数值
}
someFunction(firstParameterName: 1, secondParameterName: 2)

//指定参数标签
func someFunction(argumentLabel parameterName: Int) {
    // 在函数体内，parameterName 代表参数值
}

someFunction(argumentLabel: 1)

//忽略参数标签
func someFunction(_ firstParameterName: Int, secondParameterName: Int) {
    // 在函数体内，firstParameterName 和 secondParameterName 代表参数中的第一个和第二个参数值
}
someFunction(1, secondParameterName: 2)

//默认参数值
func someFunction(parameterWithoutDefault: Int, parameterWithDefault: Int = 12) {
    // 在函数体内，parameterWithDefault 的值为 12
}
someFunction(parameterWithoutDefault: 3, parameterWithDefault: 6) // parameterWithDefault 使用默认值 6
someFunction(parameterWithoutDefault: 4) // parameterWithDefault 使用默认值 12

//可变参数
func arithmeticMean(_ numbers: Double...) -> Double {
    var total: Double = 0
    for number in numbers {
        total += number
    }
    return total / Double(numbers.count)
}
print(arithmeticMean(1, 2, 3, 4, 5))
// 返回 3.0, 是这 5 个数的平均数。
print(arithmeticMean(3, 8.25, 18.75))
// 返回 10.0, 是这 3 个数的平均数。

//输入输出参数
func swapTwoInts(_ a: inout Int, _ b: inout Int) {
    let temporaryA = a
    a = b
    b = temporaryA
}
var someInt = 3
var anotherInt = 107
swapTwoInts(&someInt, &anotherInt)
print("someInt is now \(someInt), and anotherInt is now \(anotherInt)")
// 打印 "someInt is now 107, and anotherInt is now 3"
