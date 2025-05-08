let a : Int = 1
let b : Int = 2
let c : Int = 3

let d : Int = a + b + c

print(d)

let orangeAreOrange = true
let appleAreOrange = false
let turnipsAreDelicious = false

if turnipsAreDelicious {
    print("Mmm, tasty turnips!")
} else {
    print("Eww, turnips are horrible.")
}

//元组
let http404Error = (404, "Not Found")

let (statusCode, statusMessage) = http404Error

print("The status code is \(statusCode)")

let (justTheStatusCode, _) = http404Error

print("The status code is \(justTheStatusCode)")

let http200Status = (statusCode: 200, description: "OK")

print("The status code is \(http200Status.statusCode)")

//可选类型
let possibleNumber = "123"
let convertedNumber = Int(possibleNumber)

if let actualNumber = Int(possibleNumber) {
    print("The string \"\(possibleNumber)\" has an integer value of \(actualNumber)")
} else {
    print("The string \"\(possibleNumber)\" couldn't be converted to an integer")
}

print(convertedNumber)

//nil
var serverResponseCode: Int? = 404
//包含实际值int 404
serverResponseCode = nil
//不包含实际值nil
var surveyAnswer: String?
//surveyAnswer 自动设置为nil，在 Swift 中，nil 并非指针，而是特定类型值的缺失。任何类型的可选都可以被设置为 nil，而不仅仅是对象类型。
