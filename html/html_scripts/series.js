import {initPage, initClearButtons, create_content_on_page} from "./funcs.js";
import {get_all_objects, get_object_by_id} from "./funcs_getters.js";

let init_Page = initPage()
initClearButtons(".clear_ul_button")


let form_for_series_by_id = document.getElementById("form_for_series_by_id")
form_for_series_by_id.addEventListener('submit', event => {
    void get_object_by_id("series", event)
})

let form_for_all_series = document.getElementById("form_for_all_series")
form_for_all_series.addEventListener('submit', event => {
    void get_all_objects("series", event)
})





