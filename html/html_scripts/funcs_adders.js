import {mapping} from "./funcs_getters.js";


export async function add_object(event, object_type, list_of_attrs) {
    event.preventDefault()
    const attrs = list_of_attrs
    let future_body = {}
    for (let attr in attrs) {
        let el = document.getElementById(`new_${object_type}_${attrs[attr]}`)
        let attr_value
        if (el.type === "number") attr_value = el.valueAsNumber
        else attr_value = el.value
        if (!attr_value && attrs[attr] !== "description") {
            alert("All necessary fields must be filled!")
            return
        }
        future_body[attrs[attr]] = attr_value
    }

    fetch(`http://localhost:8000/${mapping[object_type]}/add_${object_type}`, {method: "POST",credentials: "include", body: JSON.stringify({new_body: future_body})}).then(response => {
        console.log(response)
    })
}