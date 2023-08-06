function show_search_suggestions(input) {
    clear_search_suggestions()

    const max_suggestions = 10
    let item_ids = JSON.parse(document.getElementById('all-item-ids').textContent)
    let item_names = JSON.parse(document.getElementById('all-item-names').textContent)
    let matches = 0

    let input_value = input.value.toLowerCase()

    if (input_value != '') {
        for (let i = 0; i < item_names.length; i ++) {
            if (
                item_names[i].toLowerCase().includes(input_value) ||
                item_ids[i].includes(input_value)
            ) {
                matches += 1
                create_new_search_suggestion(item_ids[i], item_names[i])
            }
            if (matches >= max_suggestions) {
                break
            }
        }
    }
} 

function create_new_search_suggestion(id, name) {
    let suggestions_container = document.getElementById('search-suggestions')
    suggestions_container.insertAdjacentHTML('beforeend', 
    `
    <div class="position-relative search-suggestion" style="width: 15rem; height: 4.8rem; display: flex; ">
        <img src="" alt="" style="width: 4rem; height: 4rem; margin: 0.3rem 0.5rem">
        <div style="display: flex; flex-direction: column; width:10rem; padding: 0 0.7rem 0;">
            <span class="text-max-two-lines">${name}</span>
            <a href="" class="bottom-0 position-absolute mb-1">${id}</a>
        </div>
    </div>
    `
    )
}

function clear_search_suggestions() {
    let suggestions_container = document.getElementById('search-suggestions')
    suggestions_container.innerHTML = ''
}