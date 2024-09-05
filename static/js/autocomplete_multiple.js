{
  const autocompletes = document.querySelectorAll(
    "[data-autocomplete-multiple]"
  );

  autocompletes.forEach((e) => {
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
        const results = await fetch(
          `http://localhost:8000/tags/autocomplete?search=${e.target.value}`
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
          sugestionsContainer.appendChild(dropdownElement);

          dropdownElement.addEventListener("click", () => {
            selectOption(option, input, sugestionsContainer, selectedContainer);
          });
        });
      }, 600);
    });

    const selectedOptions = selectedContainer.querySelectorAll("[data-value]");

    selectedOptions.forEach((option) => {
      const checkbox = markCheckbox({ id: option.dataset.value }, input);
      const closeButton = option.querySelector("[data-remove]");
      closeButton.addEventListener("click", (e) => {
        e.target.closest("div").remove();
        checkbox.click();
      });
    });
  });

  function selectOption(option, input, sugestionsContainer, selectedContainer) {
    const tagOfSelectedItem = selectedContainer.querySelector(
      `[data-value='${option.id}']`
    );

    if (tagOfSelectedItem) {
      return;
    }

    const checkbox = markCheckbox(option, input);
    createSelectedItem(option, selectedContainer, checkbox);
    sugestionsContainer.innerHTML = "";
  }

  function markCheckbox(option, input) {
    const checkbox = document.createElement("input");

    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("name", "tags");
    checkbox.setAttribute("id", "id_tags");
    checkbox.setAttribute("value", option.id);

    input.append(checkbox);

    checkbox.click();

    return checkbox;
  }

  function createSelectedItem(option, selectedContainer, checkbox) {
    const optionContainer = document.createElement("div");
    optionContainer.classList.add(
      "bg-gray-500",
      "flex",
      "items-center",
      "gap-2",
      "px-4",
      "py-2",
      "rounded-lg",
      "text-white"
    );
    optionContainer.dataset.value = option.id;

    const nameElement = document.createElement("span");
    nameElement.innerText = option.title;

    const closeButton = document.createElement("span");
    closeButton.addEventListener("click", (e) => {
      e.target.closest("div").remove();
      checkbox.click();
    });
    closeButton.classList.add("text-xl", "cursor-pointer");
    closeButton.innerHTML = "&times;";

    optionContainer.append(nameElement);
    optionContainer.append(closeButton);

    selectedContainer.append(optionContainer);
  }
}
