const sidebar = document.getElementById("table_layer");
const toggleBtn = document.getElementById("toggleSidebar");


// Toggle sidebar on button click
toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");

    if (sidebar.classList.contains("collapsed")) {
        toggleBtn.style.left = "10px";
        toggleBtn.textContent = "Show table";
    } else {
        toggleBtn.style.left = "165px";
        toggleBtn.textContent = "Hide";
    }
});
