export async function custom_response(url, options = {}, to_json = true) {
    let body = undefined
    let headers = options.headers

    if (options.form) {
        body = options.form
    } else if (options.body) {
        body = options.body
        headers["Content-Type"] = "application/json"
    }

    let resp = await fetch(url, {
        ...options,
        headers,
        body,
        method: options.method ?? "GET"
    })
    if (to_json) return resp.json()
    return resp

}


export function create_content_on_page(value, id_of_ul) {

    let ul_to_changed = document.getElementById(id_of_ul)
    let li_to_add = document.createElement("li")
    let main_element = document.createElement("h1")
    let sub_ul = document.createElement("ul")
    if (value["detail"]) {
        main_element.innerText = "This object wasn't found"
        sub_ul.innerHTML = value["detail"]
        li_to_add.appendChild(main_element)
        li_to_add.appendChild(sub_ul)
        ul_to_changed.appendChild(li_to_add)
        return
    }
    main_element.innerText = value["title"] ?? value["name"]
    li_to_add.appendChild(main_element)



    for (let obj in value) {
        if (obj === "title" || obj === "name") continue;
        let object = document.createElement("li")
        object.innerText = `${obj} - ${value[obj]}`
        sub_ul.appendChild(object)
    }
    li_to_add.appendChild(sub_ul)
    ul_to_changed.appendChild(li_to_add)
    ul_to_changed.appendChild(document.createElement("hr"))


}


export async function initPage() {
    let response = await fetch("http://localhost:8000/initPage", {credentials: "include"})
    if (!response.ok) {
        window.location.href = "../html_pages/login_page.html"
    }
}


export function initClearButtons(class_ob_clearer_button) {
    document.querySelectorAll(class_ob_clearer_button).forEach(button => {
        button.onclick = function () {
            console.log("Нажали на кнопку с целью:", button.getAttribute("data-target"));
            const target_id = button.getAttribute("data-target");
            document.getElementById(target_id).innerText = ''

        };
    });
}