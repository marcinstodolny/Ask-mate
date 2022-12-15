// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    // console.log(items)
    // console.log(sortField)
    // console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    let filtered_items = []
        for (let i=0; i<items.length; i++) {
            if (items[i]['Title'].includes(filterValue)) {
                filtered_items.push(items[i])
            }
            else if (filterValue[0] === "!" && !(filterValue.substring(1,13) === "Description:") && !(items[i]['Title'].includes(filterValue.substring(1,filterValue.length)))) {
                filtered_items.push(items[i])
            }
            else if (filterValue.substring(0,12) === "Description:" && (items[i]['Description'].includes(filterValue.substring(12,filterValue.length)))) {
                filtered_items.push(items[i])
            }
            else if (filterValue.substring(0,13) === "!Description:" && !(items[i]['Description'].includes(filterValue.substring(13,filterValue.length)))) {
                filtered_items.push(items[i])
            }
    }

    return filtered_items
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}