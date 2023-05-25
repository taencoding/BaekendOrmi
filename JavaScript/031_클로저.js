`
def
`

function one(x) {
    function two(y) {
        return x ** y
    }
    return two
}

let 승수2 = one(2)
let 승수3 = one(3)

console.log(승수2(3))
console.log(승수3(3))