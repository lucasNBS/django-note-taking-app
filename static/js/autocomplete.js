{
  const autocompletes = document.querySelectorAll("[data-autocomplete]");

  autocompletes.forEach((e) => {
    const autocomplete = e;
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
        const results = await fetch(
          `http://localhost:8000/folders/autocomplete?search=${e.target.value}`
        ).then((res) => res.json());

        results.forEach((option) => {
          const dropdownElement = document.createElement("div");

          dropdownElement.classList.add(
            "p-2",
            "border-b-2",
            "border-gray-300",
            "cursor-pointer",
            "hover:bg-gray-300"
          );
          dropdownElement.dataset.value = option.id;
          dropdownElement.innerText = option.title;
          sugestionsContainer.append(dropdownElement);

          dropdownElement.addEventListener("click", () => {
            selectOption(option, input, autocomplete, sugestionsContainer);
          });
        });
      }, 600);
    });

    const selectedOptionCloseButton =
      autocomplete.querySelector("[data-value]");

    const checkbox = markCheckbox(
      { id: selectedOptionCloseButton.dataset.value },
      input
    );
    input.value = selectedOptionCloseButton.dataset.label;
    input.setAttribute("readonly", "true");
    selectedOptionCloseButton.addEventListener("click", (e) => {
      e.target.remove();
      input.removeAttribute("readonly");
      input.value = "";
      checkbox.click();
    });
  });

  function selectOption(option, input, autocomplete, sugestionsContainer) {
    input.value = option.title;
    input.setAttribute("readonly", "true");
    const checkbox = markCheckbox(option, input);
    createSelectedItem(input, autocomplete, checkbox);
    sugestionsContainer.innerHTML = "";
  }

  function markCheckbox(option, input) {
    const checkbox = document.createElement("input");

    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("name", "folder");
    checkbox.setAttribute("id", "id_folder");
    checkbox.setAttribute("value", option.id);

    input.append(checkbox);

    checkbox.click();

    return checkbox;
  }

  function createSelectedItem(input, autocomplete, checkbox) {
    const closeButton = document.createElement("span");
    closeButton.addEventListener("click", (e) => {
      e.target.remove();
      input.removeAttribute("readonly");
      input.value = "";
      checkbox.click();
    });
    closeButton.classList.add(
      "text-xl",
      "absolute",
      "right-2",
      "top-6px",
      "cursor-pointer"
    );
    closeButton.innerHTML = "&times;";

    autocomplete.append(closeButton);
  }
}
