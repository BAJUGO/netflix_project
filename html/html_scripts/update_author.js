import {update_object} from "./funcs_updaters.js";

document.getElementById("update author").addEventListener("click", event => {
    void update_object(event, "author", author_attrs)
})

let author_attrs = ["name", "age"]