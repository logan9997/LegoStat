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
    document.getElementById('search-suggestions').classList.remove('d-none')
} 

function create_new_search_suggestion(id, name) {
    let suggestions_container = document.getElementById('search-suggestions')
    suggestions_container.insertAdjacentHTML('beforeend', 
    `
    <div class="position-relative search-suggestion" style="width: 15rem; height: 4.8rem; display: flex; ">
        <img src="${window.location.origin + `/static/App/items/${id}.png`}" alt="" style="width: 4rem; height: 4rem; margin: 0.3rem 0.5rem">
        <div style="display: flex; flex-direction: column; width:10rem; padding: 0 0.7rem 0;">
            <span class="text-max-two-lines">${name}</span>
            <a href="${window.location.origin}/item/${id}" class="bottom-0 position-absolute mb-1">${id}</a>
        </div>
    </div>
    `
    )
}

function clear_search_suggestions() {
    let suggestions_container = document.getElementById('search-suggestions')
    suggestions_container.innerHTML = ''
}

function update_graph(metric_label) {
    for (let i = 0; i < graph.data.datasets.length; i ++) {
        if (graph.data.datasets[i].label == metric_label) {
            if (graph.data.datasets[i].hidden == false) {
                graph.data.datasets[i].hidden = true
            } else {
                graph.data.datasets[i].hidden = false
            }
        }
    }
    graph.update()
}

function check_checkboxes(checkboxes) {
    for (let i = 0; i < checkboxes.length; i ++) {
        checkboxes[i].checked = true
    }
}

function change_graph_layout(number) {
    if (number == 'four') {
        for (let i = 0; i < 4; i ++) {
            new Chart()
        }
    }
}

function update_graph_date() {

    let start_slider = document.getElementById('start-date-slider')
    let end_slider = document.getElementById('end-date-slider')
    let start_date_range_text = document.getElementById('start-date-range-text')
    let end_date_range_text = document.getElementById('end-date-range-text')

    var start_value = parseInt(start_slider.value)
    var end_value = parseInt(end_slider.value)

    for (let i = 0; i < graph.data.datasets.length; i ++) {
        graph.data.datasets[i].data = []
        for (let j = start_value; j < end_value; j ++) {
            graph.data.datasets[i].data.push(data_arrays[i][j])
        }
    }

    graph.data.labels = []
    for (let j = start_value; j < end_value; j ++) {
        graph.data.labels.push(dates[j])
    }
    graph.update()

    start_date_range_text.innerHTML = dates[start_value]
    end_date_range_text.innerHTML = dates[end_value-1]
}

function update_focus_item(item) {
    var new_id = item.getElementsByClassName('item-id')[0].innerHTML    
    var new_name = item.getElementsByClassName('item-name')[0].innerHTML

    var focus_item_container = document.getElementById('focus-item')
    focus_item_container.getElementsByClassName('item-id')[0].innerHTML = new_id
    focus_item_container.getElementsByClassName('item-name')[0].innerHTML = new_name
    focus_item_container.getElementsByClassName('item-image')[0].src = `/static/App/items/${new_id}.png`

    var item_index = parseInt(
        item.getElementsByClassName('trending-item-index')[0].innerHTML
    )

    document.getElementById('avg-price-new').innerHTML = `
        Average Price (New) : £${trending_items[item_index].avg_price_new}
    `
    document.getElementById('avg-price-used').innerHTML = `
        Average Price (Used) : £${trending_items[item_index].avg_price_used}
    `
    document.getElementById('total-quantity-new').innerHTML = `
        Total Quantity (New) :  ${trending_items[item_index].total_quantity_new}
    `
    document.getElementById('total-quantity-used').innerHTML = `
        Total Quantity (Used) : ${trending_items[item_index].total_quantity_used}
    `

    var metric = JSON.parse(document.getElementById('graph-metrics').textContent)[0]   
    graph.data.datasets[0].data = trending_items[item_index][`graph_${metric}`]
    graph.data.labels = trending_items[item_index].graph_dates
    graph.update()
}