//text input elem
const searchInput = document.getElementById('searchInput');

//munro table rows
const rows = document.querySelectorAll('#mountainTable tbody tr');

//on input filter rows
searchInput.addEventListener('input', function () {
    const filter = searchInput.value.toLowerCase();
    rows.forEach(row => {
    const nameText = row.cells[0].textContent.toLowerCase();
    row.style.display = nameText.includes(filter) ? '' : 'none';
    });
});