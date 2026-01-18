import {add_object} from "./funcs_adders.js";

document.getElementById("add_series_button").addEventListener('click', event => {
    void add_object(event, "series", series_attrs)
})

let series_attrs = ["title", "year_of_issue", "episodes", "seasons", "genre", "author_id", "description"]


