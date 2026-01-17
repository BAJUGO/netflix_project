import {mapping} from "../getters/funcs_getters.js";
import {json_fetch} from "../funcs.js";

export async function update_object(event, object_type, list_of_attrs) {
    event.preventDefault()
    let id_el = document.getElementById(`update_${object_type}_id`)
    let id = id_el.valueAsNumber
    const attrs = list_of_attrs
    let future_body = {}
    for (let attr in attrs) {
        let el = document.getElementById(`update_${object_type}_${attrs[attr]}`)
        if (!el.value) {
            continue
        }
        let attr_value
        if (el.type === "number") attr_value = el.valueAsNumber
        else attr_value = el.value
        future_body[attrs[attr]] = attr_value
    }
    json_fetch(`http://localhost:8000/${mapping[object_type]}/${id}`, {method: "PATCH", credentials: "include", body: JSON.stringify({update_body: future_body})}).then(response => {
        console.log(response)
    })
    console.log("json_fetch на update был отправлен (во всяком случае была попытка)")
}