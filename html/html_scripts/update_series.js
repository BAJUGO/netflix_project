import {update_object} from "./funcs_updaters.js";

document.getElementById("update series").addEventListener("click", event => {
    void update_object(event, "series", series_attrs)
})

let series_attrs = ["title", "year_of_issue", "episodes", "seasons", "genre", "author_id", "description"]