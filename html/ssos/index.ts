const attr: string = "Dima";
const number = 4;
const sss: string = "swd";

console.log(`${attr}, is ${number} years old`)

function add(x: number, y: number): number { //number after : it is "=> int"
    return x + y;
}

const x = 4
const y = 4

console.log(add(x, y));

//* next

const numbers: number[] = [1, 2, 3, 4, 5]

console.log(numbers);
console.log(numbers[1])

const strings: string[] = ["a", "b", "c"];

console.log(strings);
console.log(strings[1])

strings.push("d")
console.log(strings)

const additional_string: string[] = ["e", "f", "g"]
console.log(`The length of 'strings' = ${strings.length}`)

if (strings.includes("a")) {
    console.log(`strings does have 'a'`);
}

const user = {
    name: "Alice",
    age: 3
}
console.log(user);
console.log(user.name);
console.log(user["name"])

const lambdafunc = (a: number, b: number): number => a + b

const another_way_of_lambdafunc = (a: number, b: number): number => {
    return a + b
}


console.log(lambdafunc(1, 5));

console.log(another_way_of_lambdafunc(1, 5));

//* next


const lamb = (a: number, b: number): string => {
    if (a > b) {
        return `${a} is more than ${b}`
    } else if (a === b) {
        return `${a} is equal to ${b}`
    } else {
        return `${a} is smaller than ${b}`
    }
};

function same_function(a: number, b: number): string {
    if (a > b) {
        return `${a} is more than ${b}`
    } else if (a === b) {
        return `${a} is equal to ${b}`
    } else {
        return `${a} is equal to ${b}`
    }
}

console.log(lamb(5, 5))


strings.forEach((name_of_attr: string): undefined => {
    console.log(name_of_attr);
})

for (const number of numbers) {
    console.log(number);
}

class Player {
    name: string = "Anonymous";
    age: number = 18;
    skill_level: string = "ok"

    constructor(name: string, age: number, skill_level: string = "ok") {
        this.name = name;
        this.age = age;
        this.skill_level = skill_level;
    }

    introduce() {
        return `${this.name} is ${this.age} years old`;
    }
}


const alice: Player = new Player("Alice", 14, "normal")


//* next

function calculate_smth(price: number, tax: number = 0.05, extra_tax: number = 0) {
    if (extra_tax) return price + (price * tax) + extra_tax;
    return price;
}

console.log(calculate_smth(10, undefined, 5));


interface Player_interface {
    name: string;
    age: number;
}

function AcceptPlayer(player: Player) {
    return `${player.name} is a ${player.age} years old`;
}


const alice_interface: Player_interface = {name: "Alice", age: 4}

console.log(alice); // full class => Player {{ name: 'Alice', age: 4 }

//console.log(alice.introduce());

console.log(alice_interface); // just an object => { name: 'Alice', age: 4 }

console.log(AcceptPlayer(alice)) // This Alice is appropriate item, even if it isn't an interface
// In addition, interface has no attribute skill_level, but class does. Nevertheless, function works!

function countLength(obj: string | string[] | number[]) {
    return `Length of object is ${obj.length}`
}

console.log(countLength("numbers"))


