document.getElementById("add_movie_button").addEventListener('click', add_movie)

async function add_movie(event) {
    event.preventDefault()
    const attrs = ["title", "year_of_issue", "genre", "author_id", "description"]
    let future_body = {}
    for (let attr in attrs) {
        let el = document.getElementById(`new_movie_${attrs[attr]}`)
        let attr_value
        if (el.type === "number") attr_value = el.valueAsNumber
        else attr_value = el.value
        future_body[attrs[attr]] = attr_value
    }

    fetch("http://localhost:8000/movies/add_movie", {method: "POST",credentials: "include", body: JSON.stringify({movie_body: future_body})}).then(response => {
        console.log(response)
    })
}


