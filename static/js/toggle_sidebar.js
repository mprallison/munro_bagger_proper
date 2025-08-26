  const sidebar = document.getElementById('mountainTable');
  const toggleButton = document.getElementById('toggleSidebar');

  toggleButton.addEventListener('click', function () {
    if (sidebar.style.transform === 'translateX(-140px)') {
      sidebar.style.transform = 'translateX(0)';
      toggleButton.style.left = '150px';
      toggleButton.textContent = 'Hide table';
    } else {
      sidebar.style.transform = 'translateX(-140px)';
      toggleButton.style.left = '10px';
      toggleButton.textContent = 'Show table';
    }
  });

export function search_sidebar() {
  document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById('searchInput');
    const rows = document.querySelectorAll('#mountainTable tbody tr');
    searchInput.addEventListener('input', function () {
      const filter = searchInput.value.toLowerCase();
      rows.forEach(row => {
        const nameText = row.cells[0].textContent.toLowerCase();
        row.style.display = nameText.includes(filter) ? '' : 'none';
      });
    });
  });
}