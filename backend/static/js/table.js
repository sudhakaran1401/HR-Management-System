function initTableControls(tableId, defaultRows = 5) {
    const input = document.getElementById("globalSearch");
    const table = document.getElementById(tableId);

    if (!table) return;

    function getRows() {
        return Array.from(table.querySelectorAll("tbody tr"));
    }

    let currentPage = 1;
    let rowsPerPage = defaultRows;
    let filteredRows = getRows();

    const pageInfo = document.getElementById(tableId + "_pageInfo");
    const prevBtn = document.getElementById(tableId + "_prev");
    const nextBtn = document.getElementById(tableId + "_next");
    const rowsSelect = document.getElementById(tableId + "_rowsPerPage");

    function renderTable() {
        const allRows = getRows();

        const totalRows = filteredRows.length;
        const totalPages = Math.ceil(totalRows / rowsPerPage) || 1;

        if (currentPage > totalPages) currentPage = totalPages;

        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        allRows.forEach(row => row.style.display = "none");

        filteredRows.slice(start, end).forEach(row => {
            row.style.display = "table-row";
        });

        if (pageInfo) {
            pageInfo.innerText = `${start + 1}–${Math.min(end, totalRows)} of ${totalRows}`;
        }

        if (prevBtn) prevBtn.disabled = currentPage === 1;
        if (nextBtn) nextBtn.disabled = currentPage === totalPages;
    }

    function applyFilter() {
        const value = input ? input.value.toLowerCase() : "";

        filteredRows = getRows().filter(row =>
            row.innerText.toLowerCase().includes(value)
        );

        currentPage = 1;
        renderTable();
    }

    if (input) input.addEventListener("keyup", applyFilter);

    if (rowsSelect) {
        rowsSelect.addEventListener("change", function () {
            rowsPerPage = parseInt(this.value);
            currentPage = 1;
            renderTable();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            currentPage--;
            renderTable();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            currentPage++;
            renderTable();
        });
    }

    renderTable();
}


// AUTO INIT
document.addEventListener("DOMContentLoaded", function () {
    const tables = document.querySelectorAll("[data-pagination='report']");

    tables.forEach(table => {
        const tableId = table.id;
        const rows = table.getAttribute("data-rows") || 5;

        if (tableId) {
            initTableControls(tableId, parseInt(rows));
        }
    });
});