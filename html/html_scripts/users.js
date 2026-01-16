import {json_fetch} from "./funcs.js";


document.getElementById("get_all_users_button").addEventListener('click', event=> {
    event.preventDefault()
    let ul = document.getElementById("ul_for_users")

    json_fetch("http://localhost:8000/users/get_users", {credentials: "include"}).then(response => {
        for (let user in response) {
            let new_li = document.createElement("li")
            new_li.innerText = response[user]
            ul.appendChild(new_li)

        }
        console.log(response)
    })
})