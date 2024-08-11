{
  const autocomplete = document.querySelectorAll(
    "[data-autocomplete-multiple]"
  );

  autocomplete.forEach((e) => {
    const input = e.querySelector("[data-autocomplete-multiple-input]");
    const selectedContainer = e.querySelector(
      "[data-autocomplete-multiple-selected]"
    );
    const sugestionsContainer = e.querySelector(
      "[data-autocomplete-multiple-sugestions]"
    );

    document.addEventListener("click", (e) => {
      const clickedElement = e.target;
      if (
        !(
          clickedElement.dataset.autocompleteInput ||
          clickedElement.dataset.autocompleteSugestions
        )
      ) {
        sugestionsContainer.innerHTML = "";
      }
    });

    let timeout;
    input.addEventListener("keyup", (e) => {
      clearTimeout(timeout);
      sugestionsContainer.innerHTML = "";

      timeout = setTimeout(async () => {
        const foundTags = await fetch(
          `http://localhost:8000/tags/autocomplete?search=${e.target.value}`
        ).then((res) => res.json());

        foundTags.forEach((tag) => {
          const dropdownElement = document.createElement("div");
          dropdownElement.dataset.value = tag.id;
          dropdownElement.classList.add("p-2", "border-b-2", "border-gray-300");
          dropdownElement.innerText = tag.name;
          sugestionsContainer.append(dropdownElement);

          dropdownElement.addEventListener("click", () => {
            addTag(tag, input, sugestionsContainer, selectedContainer);
          });
        });
      }, 600);
    });

    const selectedTags = selectedContainer.querySelectorAll("[data-value]");

    selectedTags.forEach((tag) => {
      const checkbox = selectOption({ id: tag.dataset.value }, input);
      const closeButton = tag.querySelector("[data-remove]");
      closeButton.addEventListener("click", (e) => {
        e.target.closest("div").remove();
        checkbox.click();
      });
    });
  });

  function addTag(tag, input, sugestionsContainer, selectedContainer) {
    const tagOfSelectedItem = selectedContainer.querySelector(
      `[data-value='${tag.id}']`
    );

    if (tagOfSelectedItem) {
      return;
    }

    const checkbox = selectOption(tag, input);
    createSelectedItem(tag, selectedContainer, checkbox);
    sugestionsContainer.innerHTML = "";
  }

  function selectOption(tag, input) {
    const checkbox = document.createElement("input");
    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("name", "tags");
    checkbox.setAttribute("id", "id_tags");
    checkbox.setAttribute("value", tag.id);

    input.append(checkbox);

    checkbox.click();

    return checkbox;
  }

  function createSelectedItem(tag, selectedContainer, checkbox) {
    const tagContainer = document.createElement("div");
    tagContainer.classList.add(
      "bg-gray-500",
      "flex",
      "items-center",
      "gap-2",
      "px-4",
      "py-2",
      "rounded-lg",
      "text-white"
    );
    tagContainer.dataset.value = tag.id;

    const nameElement = document.createElement("span");
    nameElement.innerText = tag.name;

    const closeButton = document.createElement("span");
    closeButton.addEventListener("click", (e) => {
      e.target.closest("div").remove();
      checkbox.click();
    });
    closeButton.classList.add("text-xl");
    closeButton.innerHTML = "&times;";

    tagContainer.append(nameElement);
    tagContainer.append(closeButton);

    selectedContainer.append(tagContainer);
  }
}
