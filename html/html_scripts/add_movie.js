import {custom_response} from "./funcs.js";



document.getElementById("add_movie_button").addEventListener('click', add_movie)

async function add_movie(event) {
    event.preventDefault()
    const attrs = ["title", "year_of_issue", "genre", "author_id", "description"]
    const future_body = {}
    for (let attr in attrs) {
        console.log(attr)
        let attr_value = document.getElementById(`new_movie_${attrs[attr]}`)

        future_body[attr] = `${attr_value.value}`
    }

    fetch("http://localhost:8000/movies/add_movie", {method: "POST", body: JSON.stringify({movie_in: future_body}), credentials: "include" }).then(response => {
        console.log(response)
    })
}


