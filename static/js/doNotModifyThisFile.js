// Please do not modify this file
const TABLE_FILTERS = {
    filter: "",
    criteria: "",
    direction: ""
}
const INITIAL_TABLE_DATA = {}

function getTableElements(headerId, bodyId) {
    const headings = getColumnNames(headerId)
    const rows = getRowValues(bodyId)
    const data = buildObjects(rows, headings)
    return data
}

function getColumnNames(headerId) {
    const tableHeader = document.getElementById(headerId)
    const headings = []
    for (let heading of tableHeader.children[0].children) {
        headings.push(heading.innerText.replace(' ', ''))
    }
    return headings
}

function getRowValues(bodyId, takeAllRows) {
    const tableBody = document.getElementById(bodyId)
    const rows = []
    for (let row of tableBody.children) {
        if (row.style.display !== "none") {
            const rowValues = []
            for (let cell of row.children) {
                rowValues.push(cell.innerText)
            }
            rows.push(rowValues)
        }
    }
    return rows
}

function buildObjects(values, names) {
    const result = []
    for (let value of values) {
        const item = {}
        for (let i=0; i<value.length; i++) {
            if (i < names.length   ) {
                item[names[i]] = value[i]
            } else {
                item[i] = value[i]
            }
        }
        result.push(item)
    }
    return result
}

function replaceTableRowsWith(newRows, tableBodyId, tableHeaderId) {
    const tableRows = document.getElementById(tableBodyId).children
    const headers = getColumnNames(tableHeaderId)
    const rowsNumber = tableRows.length
    for (let i=0; i<rowsNumber; i++) {
        if (i < newRows.length) {
            const columnsNumber = tableRows[i].children.length
            tableRows[i].style = "display:table-row"
            for (let j = 0; j < columnsNumber; j++) {
                if (j < Object.keys(newRows[i]).length && j < headers.length) {
                    const cell = tableRows[i].children[j]
                    const matchingValueWithCurrentCell = newRows[i][Object.keys(newRows[i])[j]]
                    cell.innerText = matchingValueWithCurrentCell
                }
            }
        } else {
            tableRows[i].style = "display:none"
        }
    }
}

function getAllTableItems(tableHeaderId, tableBodyId) {
    if (!INITIAL_TABLE_DATA[tableHeaderId]) {
        INITIAL_TABLE_DATA[tableHeaderId] = getTableElements(tableHeaderId, tableBodyId)
    }
    return [...INITIAL_TABLE_DATA[tableHeaderId]]
}

function sortEventHandler(e) {
    if (e.target.dataset["direction"] === "asc") {
        e.target.dataset["direction"] = "desc"
    } else {
        e.target.dataset["direction"] = "asc"
    }
    TABLE_FILTERS.criteria = e.target.innerText.replace(" ", "")
    TABLE_FILTERS.direction = e.target.dataset["direction"]
    const parentHeaderId = e.target.parentElement.parentElement.id
    const parentBodyId = e.target.parentElement.parentElement.nextElementSibling.id
    applyTableFilters(parentBodyId, parentHeaderId, TABLE_FILTERS)
}

function addTableOrderEventListeners(tableHeaderIds) {
    for (let tableHeaderId of tableHeaderIds) {
        const headers = document.getElementById(tableHeaderId)
        if (headers) {
            for (let header of headers.children) {
                header.addEventListener('click', sortEventHandler)
            }
        }
    }
}

function applyTableFilters(tableBodyId, tableHeaderId, tableFilters) {
    const items = getAllTableItems(tableHeaderId, tableBodyId)
    const filteredItems = getFilteredItems(items, tableFilters.filter)
    const sortedItems = getSortedItems(filteredItems, tableFilters.criteria, tableFilters.direction)
    console.log("sortedItems")
    console.log(sortedItems)
    replaceTableRowsWith(sortedItems, tableBodyId, tableHeaderId)
}

function filterInputHandler(e) {
    TABLE_FILTERS.filter = e.target.value
    const tableBodyId = e.target.dataset["tableBody"]
    const tableHeaderId = document.getElementById(tableBodyId).previousElementSibling.id
    applyTableFilters(tableBodyId, tableHeaderId, TABLE_FILTERS)
}

function addInputFilterEventListeners(inputIds) {
    for (let inputId of inputIds) {
        const input = document.getElementById(inputId)
        if (input) {
            input.addEventListener('input', filterInputHandler)
        }
    }
}

const tableHeaderIds = ["doNotModifyThisId_QuestionsTableHeader"]
addTableOrderEventListeners(tableHeaderIds)

const inputIds = ["doNotModifyThisId_QuestionsFilter"]
addInputFilterEventListeners(inputIds)

document.getElementById("theme-button").addEventListener("click", toggleTheme)
document.getElementById("increase-font-button").addEventListener("click", increaseFont)
document.getElementById("decrease-font-button").addEventListener("click", decreaseFont)
