import {add_object} from "./funcs_adders.js";

document.getElementById("add_author_button").addEventListener('click', event => {
    void add_object(event, "author", author_attrs)
})

let author_attrs = ["name", "age"]



