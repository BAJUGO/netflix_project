let everything = [
    {id: 1,
    name: "John",
    some_text: "Cool text"},
    {id: 2,
    name: "Mike",
    some_text: "Cooler  text"},
    {id: 3,
    name: "skiter",
    some_text: "COOOOOOOOL!!!"}
]


let every = everything.map(function(obj){
    return obj.name
})

let id_more_two = everything.filter(function(obj) {
    if (obj.id >= 2) {
        return obj
    }
}).map(function(todo) {
    return todo.id
})


if ((10 > 5 || 5 < 3) && 8 > 4) {
    console.log("hell")
} else {
    console.log("Not as hell but still")
}


console.log(every)
console.log(id_more_two)
