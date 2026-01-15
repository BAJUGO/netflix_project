import {create_content_on_page, custom_response, initPage, initClearButtons} from "./funcs.js";
import {get_all_objects, get_object_by_id} from "./funcs_getters.js";

let init_Page = initPage()
initClearButtons(".clear_ul_button")


let form_for_movie_by_id = document.getElementById("form_for_movie_by_id")
form_for_movie_by_id.addEventListener('submit', (event) => {
    void get_object_by_id("movie", event)
})

let form_for_all_movies = document.getElementById("form_for_all_movies")
form_for_all_movies.addEventListener('submit', event => {
    void get_all_objects("movie", event)
})





