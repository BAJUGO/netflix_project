import {initPage, initClearButtons, create_content_on_page} from "./funcs.js";
import {get_all_objects, get_object_by_id} from "./funcs_getters.js";

let init_Page = initPage()
initClearButtons(".clear_ul_button")


let form_for_author_by_id = document.getElementById("form_for_author_by_id")
form_for_author_by_id.addEventListener('submit', event => {
    void get_object_by_id("author", event)
})

let form_for_all_authors = document.getElementById("form_for_all_authors")
form_for_all_authors.addEventListener('submit', event => {
    void get_all_objects("author", event)
})


