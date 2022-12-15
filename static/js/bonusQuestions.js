// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"

function getSortedItems(items, sortField, sortDirection) {
    let sorted
    if (sortDirection === "asc") {
        if (sortField === 'Title' || sortField === 'Description') {
            sorted = items.sort((a, b) => a[sortField].localeCompare(b[sortField]));
        } else {
            sorted = items.sort((a, b) => a[sortField] - b[sortField]);
        }
    } else {
        if (sortField === 'Title' || sortField === 'Description') {
            sorted = items.sort((a, b) => b[sortField].localeCompare(a[sortField]));
        } else {
            sorted = items.sort((a, b) => b[sortField] - a[sortField]);
        }
    }
    return sorted
}

// you receive an array of objects which you must filter by all its keys to have a value matching "filterValue"
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

let body = document.body;
body.style.backgroundColor = "white";

let table = document.getElementById("doNotModifyThisId_QuestionsTableBody");
table.style.fontSize = "15px";
let currentFontSize = parseFloat(window.getComputedStyle(table, null).fontSize);

function toggleTheme() {
    if (body.style.backgroundColor === "white") {
        body.style.backgroundColor = "grey";
    } else {
        body.style.backgroundColor = "white";
    }
}

function increaseFont() {
    if (currentFontSize < 15) {
        table.style.fontSize = ++currentFontSize + 'px';
  }
}

function decreaseFont() {
    console.log("decreaseFont")
    if (currentFontSize > 3) {
        table.style.fontSize = --currentFontSize + 'px';
  }
}