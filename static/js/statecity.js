
const state = document.getElementById("id_state")
state.addEventListener("change", function () {
    let state_id = this.value;
    fetch("/get_cities/" + state_id)
        .then(res => res.json())
        .then(data => {
            let cityDropdown = document.getElementById("id_city");
            cityDropdown.innerHTML = "";
            data.forEach(city => {
                const option = document.createElement("option");
                option.value = city.id;
                option.textContent = city.city_name;
                cityDropdown.appendChild(option);
            });
        })
})