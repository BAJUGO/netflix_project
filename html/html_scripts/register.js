import {json_fetch} from "./funcs.js";

document.getElementById("register_form").addEventListener('submit', event => {
    event.preventDefault()
    let username_el = document.getElementById("username_input")
    let email_el = document.getElementById("email_input")
    let password_el = document.getElementById("password_input")

    fetch("http://localhost:8000/register", {method: "POST", credentials: "include",
        body: JSON.stringify({user_in_body: {visible_name: username_el.value, password: password_el.value, email: email_el.value}})}).then(response => {
        console.log(response)
        if (response.ok) {
            let form = new FormData()
            form.append("username", email_el.value)
            form.append("password", password_el.value)
            fetch("http://localhost:8000/create_token", {method: "POST", body: form, credentials: "include"}).then(response => {
                console.log(response)
                if (response.ok) {
                    window.location.href = 'main_page.html'
                }
                else {
                    console.log("Произошла ошибка! Попробуйте ещё раз")
                }})
        }
    })
})