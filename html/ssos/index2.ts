class Person {
    name: string;
    age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }

    whoami() {
        console.log(`${this.name}, and my age is ${this.age}`);
    }
}


class BadPerson extends Person {
    bad_things: string[] = []

    constructor(name: string, age: number, bad_things: string[] = []) {
        super(name, age);
        //this.name = "Cool boy"
        this.bad_things = bad_things
    }

    whoami() {
        super.whoami()
        console.log("By the wat, I am bad person. My bad stufs are: \n ", this.bad_things)
    }

    //! EVEN IF THIS METHOD WON'T BE TYPED, METHOD WOULD INHERIT!
}


const dima: BadPerson = new BadPerson("Dima", 14, ["smoking"])

dima.whoami()

const not_dima: string = "Dima"


type OneOfPerson = Person | BadPerson
type GoodBadOk = "Good" | "Bad" | "Ok"


function CheckOnPerson(person: OneOfPerson): any {
    return person.whoami()
}

console.log(CheckOnPerson(dima))


const variables: string = "Something"


const list_of_variables: string[] = ["a", "b", "c"]

list_of_variables.forEach((letter: string):any => {
    console.log(letter)
})


type StrList = Array<string>
type IntList = Array<number>

const list_str: StrList = ["dima", "not_dima"]
const list_int: IntList = [1,2,3,4,5]


console.log(list_str)
console.log(list_int)

let character: number = 1

character = 4

console.log(character)



declare function something(arg: 1 | 2 | 3): void;
let one: number = 1

//something(one)

