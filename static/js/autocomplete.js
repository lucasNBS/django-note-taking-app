{
  const autocomplete = document.querySelectorAll("[data-autocomplete]");

  autocomplete.forEach((e) => {
    const container = e;
    const input = e.querySelector("[data-autocomplete-input]");
    const sugestionsContainer = e.querySelector(
      "[data-autocomplete-sugestions]"
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
      if (e.target.readOnly) {
        return;
      }

      clearTimeout(timeout);
      sugestionsContainer.innerHTML = "";

      timeout = setTimeout(async () => {
        const foundTags = await fetch(
          `http://localhost:8000/folders/autocomplete?search=${e.target.value}`
        ).then((res) => res.json());

        foundTags.forEach((tag) => {
          const dropdownElement = document.createElement("div");
          dropdownElement.dataset.value = tag.id;
          dropdownElement.classList.add("p-2", "border-b-2", "border-gray-300");
          dropdownElement.innerText = tag.name;
          sugestionsContainer.append(dropdownElement);

          dropdownElement.addEventListener("click", () => {
            select(tag, input, container, sugestionsContainer);
          });
        });
      }, 600);
    });

    const selected = container.querySelector("[data-value]");

    const checkbox = selectOption({ id: selected.dataset.value }, input);
    input.value = selected.dataset.label;
    input.toggleAttribute("readonly");
    selected.addEventListener("click", (e) => {
      e.target.remove();
      input.toggleAttribute("readonly");
      input.value = "";
      checkbox.click();
    });
  });

  function select(tag, input, container, sugestionsContainer) {
    input.value = tag.name;
    input.toggleAttribute("readonly");
    const checkbox = selectOption(tag, input);
    createSelectedItem(input, container, checkbox);
    sugestionsContainer.innerHTML = "";
  }

  function selectOption(tag, input) {
    const checkbox = document.createElement("input");
    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("name", "folder");
    checkbox.setAttribute("id", "id_folder");
    checkbox.setAttribute("value", tag.id);

    input.append(checkbox);

    checkbox.click();

    return checkbox;
  }

  function createSelectedItem(input, container, checkbox) {
    const closeButton = document.createElement("span");
    closeButton.addEventListener("click", (e) => {
      e.target.remove();
      input.toggleAttribute("readonly");
      input.value = "";
      checkbox.click();
    });
    closeButton.classList.add("text-xl", "absolute", "right-2", "top-6px");
    closeButton.innerHTML = "&times;";

    container.append(closeButton);
  }
}
