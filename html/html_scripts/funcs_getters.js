import {create_content_on_page, custom_response} from "./funcs.js";

const mapping = {
    movie: "movies",
    series: "series",
    author: "authors",
    user: "users"
}


export async function get_object_by_id(object_type, event){
    event.preventDefault()
    document.getElementById("clear_ul_1").click()
    let id = document.getElementById(`${object_type}_id`)
    custom_response(`http://localhost:8000/${mapping[object_type]}/${id.value}`, {
        method: "GET",
        credentials: "include"
    }).then(response => {
        create_content_on_page(response, "ul_1")
        console.log(response)

    })
    id.value = ''
}

export async function get_all_objects(object_type, event) {
    event.preventDefault()
    document.getElementById("clear_ul_2").click()
    const path = mapping[object_type]
    custom_response(`http://localhost:8000/${path}/get_${path}`, {
        method: "GET",
        credentials: "include"
    }).then(response => {
        for (let object_number in response) {
            create_content_on_page(response[object_number], "ul_2")
        }
    })
}