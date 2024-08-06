{
  const icon = document.querySelector("#filters-icon");
  const filters = document.querySelector("#filters-container");
  const contentContainer = document.querySelector("#content-container");

  let size = filters.getBoundingClientRect().height;
  contentContainer.style.setProperty("--filters-height", size);

  icon.addEventListener("click", () => {
    size = filters.getBoundingClientRect().height;

    contentContainer.style.setProperty("transition", "all 200ms linear");
    contentContainer.style.setProperty("--filters-height", size);
    contentContainer.classList.toggle("close-filters");
  });
}
