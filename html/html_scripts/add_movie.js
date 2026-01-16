import {add_object} from "./funcs_adders.js";

document.getElementById("add_movie_button").addEventListener('click', event => {
    void add_object(event, "movie", movie_attrs)
})

let movie_attrs = ["title", "year_of_issue", "genre", "author_id", "description"]



