{
  function createDropdownElement(option) {
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

    return dropdownElement;
  }

  function createCheckbox(optionId) {
    const checkbox = document.createElement("input");

    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("name", "tags");
    checkbox.setAttribute("id", "id_tags");
    checkbox.setAttribute("value", optionId);

    return checkbox;
  }

  function createSelectedItem(option, checkbox) {
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

    return optionContainer;
  }

  class AutocompleteMultiple {
    constructor(element) {
      this.element = element;
      this.input = element.querySelector("[data-autocomplete-multiple-input]");
      this.selectedOptionsContainer = element.querySelector(
        "[data-autocomplete-multiple-selected]"
      );
      this.sugestionsContainer = element.querySelector(
        "[data-autocomplete-multiple-sugestions]"
      );
      this.selectedOptions =
        this.selectedOptionsContainer.querySelectorAll("[data-value]");
      this.init();
    }

    init() {
      let timeout;
      this.input.addEventListener("keyup", () => {
        clearTimeout(timeout);
        this.sugestionsContainer.innerHTML = "";

        timeout = setTimeout(async () => await this.search(this.input), 600);
      });
      this.selectedOptions.forEach((option) => {
        this.selectInitialSelectedOptions(option);
      });

      document.addEventListener("click", (event) => {
        const clickedElement = event.target;
        if (
          !(
            clickedElement.dataset.autocompleteInput ||
            clickedElement.dataset.autocompleteSugestions
          )
        ) {
          this.sugestionsContainer.innerHTML = "";
        }
      });
    }

    async search(input) {
      const results = await fetch(
        `http://localhost:8000/tags/autocomplete?search=${input.value}`
      ).then((res) => res.json());

      results.forEach((option) => {
        const dropdownElement = createDropdownElement(option);
        this.sugestionsContainer.appendChild(dropdownElement);

        dropdownElement.addEventListener("click", () => {
          this.selectOption(option);
        });
      });
    }

    selectOption(option) {
      const tagOfSelectedItem = this.selectedOptionsContainer.querySelector(
        `[data-value='${option.id}']`
      );

      if (tagOfSelectedItem) {
        return;
      }

      const checkbox = this.markCheckbox(option.id);
      const selectedItem = createSelectedItem(option, checkbox);
      this.selectedOptionsContainer.append(selectedItem);
      this.sugestionsContainer.innerHTML = "";
    }

    selectInitialSelectedOptions(option) {
      const checkbox = this.markCheckbox(option.dataset.value);
      const closeButton = option.querySelector("[data-remove]");
      closeButton.addEventListener("click", (event) => {
        event.target.closest("div").remove();
        checkbox.click();
      });
    }

    // Selected option must have a checked checkbox to include its value in form
    markCheckbox(optionId) {
      const checkbox = createCheckbox(optionId);
      this.input.append(checkbox);
      checkbox.click();
      return checkbox;
    }
  }

  const autocompletes = document.querySelectorAll(
    "[data-autocomplete-multiple]"
  );

  autocompletes.forEach((autocomplete) => {
    new AutocompleteMultiple(autocomplete);
  });
}
