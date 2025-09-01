
const sidebar = document.getElementById("table_layer");
const toggleBtn = document.getElementById("toggleSidebar");

toggleBtn.addEventListener("click", () => {
sidebar.classList.toggle("collapsed");

// Optional: move the toggle button with the sidebar
if (sidebar.classList.contains("collapsed")) {
    toggleBtn.style.left = "10px";  // adjust position when collapsed
    toggleBtn.textContent = "Show table";
} else {
    toggleBtn.style.left = "170px";
    toggleBtn.textContent = "Hide table";
}
});