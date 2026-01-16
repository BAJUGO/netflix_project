import {update_object} from "./funcs_updaters.js";

document.getElementById("update movie").addEventListener("click", event => {
    void update_object(event, "movie", movie_attrs)
})

let movie_attrs = ["title", "year_of_issue", "genre", "author_id", "description"]
