import {mapping} from "./funcs_getters.js";
import {json_fetch} from "./funcs.js";

let movie_id_el = document.getElementById('movie_id')
let series_id_el = document.getElementById('series_id')
let author_id_el = document.getElementById('author_id')


document.getElementById("form_for_deleting_movie").addEventListener('submit', event => {
    event.preventDefault()
    void delete_obj("movie", movie_id_el.value)
    movie_id_el.value = ''
})
document.getElementById("form_for_deleting_series").addEventListener('submit', event => {
    event.preventDefault()
    void delete_obj("series", series_id_el.value)
    series_id_el.value = ''
})

document.getElementById("form_for_deleting_author").addEventListener('submit', event => {
    event.preventDefault()
    void delete_obj("author", author_id_el.value)
    author_id_el.value = ''
})



async function delete_obj(obj_type, obj_id) {
    json_fetch(`http://localhost:8000/${mapping[obj_type]}/${obj_id}`, {method: "DELETE", credentials: "include"}).then(response => {
        console.log(response)
    })
}
