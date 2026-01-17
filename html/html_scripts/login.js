import {json_fetch} from "./funcs.js";

async function isLogined() {
    fetch("http://localhost:8000/initPage", {credentials: "include"}).then(resp => {
        if (resp.ok) {
            window.location.href = "../html_pages/main_pages/main_page.html"
        }})
}
//* ДВОЙНОЙ ЗАПРОС ОТПРАВЛЯЕТСЯ ИМЕННО ИЗ-ЗА ЭТОЙ ФУНКЦИИ! ЕСЛИ НУЖНО УБРАТЬ - УБЕРИ ЕЁ

await isLogined()

let baseApi = "http://localhost:8000"

let myButton = document.getElementById('button_button');

let loginButton = document.getElementById('login_button')

let password = document.getElementById("password_input")

let email = document.getElementById("email_input")

let hidden_h1 = document.getElementById("hidden_h1")

let login_form = document.getElementById("login_form")

myButton.addEventListener('click', function () {
    alert('Кнопка была нажата!');
});

myButton.addEventListener('mouseover', function () {
    myButton.style.color = "red"
})

myButton.addEventListener('mouseout', function () {
    myButton.style.color = "white"
})

login_form.addEventListener("submit", loginUser)


// const form = new FormData()
// form.append("username", "user1@example.com")
// form.append("password", "kiril12AZ")
//
//
// json_fetch("http://localhost:8000/create_token", {method: "POST", form}).then(response => {
//     console.log(response)
// })


async function loginUser(event) {
    event.preventDefault()
    let form = new FormData()
    form.append("username", email.value)
    form.append("password", password.value)

    email.value = ''
    password.value = ''
    fetch("http://localhost:8000/create_token", {method: "POST", body: form, credentials: "include"}).then(response => {
    console.log(response)
    if (response.ok) {
        window.location.href = '../html_pages/main_pages/main_page.html'
    }
    else {
        console.log("Неудачная попытка авторизации! Попробуйте ещё раз")
    }})
}





