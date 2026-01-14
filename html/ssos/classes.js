class Player {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    introduce() {
        return `My name is ${this.name}. My age is ${this.age}.`;
    }
}


const Alice = new Player("Alice", 14)

console.log(Alice.name)
console.log(Alice.age)


function calculate_price({price, tax = 0.05, extra_tax = 0}) {
    return price + (price * tax) + extra_tax;
}

console.log(calculate_price({price: 100, extra_tax: 3}));



