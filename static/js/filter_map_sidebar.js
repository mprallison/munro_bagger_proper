import { addMapMarkers } from '/static/js/populate_markers.js';

const idFilter = document.getElementById('idFilter');
const rows = document.querySelectorAll('#mountainTable tbody tr');

// Build the dropdown dynamically from unique IDs in the first cell
const uniqueIds = new Set();
rows.forEach(row => {
  uniqueIds.add(row.cells[0].id);
});

var idList = Array.from(uniqueIds);
idList = idList.filter(item => item !== "gap");
idList.sort().reverse();

idList.forEach(id => {
  const option = document.createElement('option');
  option.value = id;
  option.textContent = id;
  idFilter.appendChild(option);
});

const countDisplay = document.getElementById('countDisplay');

let filterMunroIds = window.filterMunroIds;

// Filter rows when dropdown changes
idFilter.addEventListener('change', () => {
  const filter = idFilter.value.trim();
  
  let visibleCount = 0;
  let filterMunroIds = [];

  rows.forEach(row => {
    const rowId = row.cells[0].id;
    const match = filter === '' || rowId === filter;
    row.style.display = match ? '' : 'none';
    if (match) {
      visibleCount++
      filterMunroIds.push(row.cells[0].getAttribute('data-munro-id'))
    };
  });
  // Replace the text inside the existing span
  //dont display for all total
  if (visibleCount === 282)
    {countDisplay.textContent = "";}
  else {
  countDisplay.textContent = visibleCount;
  }

  const locations = window.locations.filter(item => filterMunroIds.includes(item.munro_id));

  addMapMarkers(locations);

});