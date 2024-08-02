const icon = document.querySelector("#filters-icon");
const filters = document.querySelector("#filters-container");

icon.addEventListener("click", () => {
  filters.classList.toggle("close");
});
