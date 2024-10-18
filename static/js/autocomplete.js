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
    checkbox.setAttribute("name", "folder");
    checkbox.setAttribute("id", "id_folder");
    checkbox.setAttribute("value", optionId);

    return checkbox;
  }

  class Autocomplete {
    constructor(element) {
      this.element = element;
      this.input = element.querySelector("[data-autocomplete-input]");
      this.sugestionsContainer = element.querySelector(
        "[data-autocomplete-sugestions]"
      );
      this.unselectOptionButton = element.querySelector("[data-value]");
      this.init();
    }

    init() {
      let timeout;
      this.input.addEventListener("keyup", () => {
        if (this.input.readOnly) {
          return;
        }

        clearTimeout(timeout);
        this.sugestionsContainer.innerHTML = "";

        timeout = setTimeout(async () => await this.search(this.input), 600);
      });
      this.unselectOptionButton.addEventListener("click", () => {
        this.unselectOption(this.unselectOptionButton);
      });
      this.checkbox = this.selectOption({
        title: this.unselectOptionButton.dataset.label,
        id: this.unselectOptionButton.dataset.value,
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
        `http://localhost:8000/folders/autocomplete?search=${input.value}`
      ).then((res) => res.json());

      results.forEach((option) => {
        const dropdownElement = createDropdownElement(option);
        this.sugestionsContainer.append(dropdownElement);

        dropdownElement.addEventListener("click", () => {
          this.selectOption(option, true);
        });
      });
    }

    selectOption(option, shouldCreateNewUnselectOptionButton = false) {
      this.input.value = option.title;
      this.input.setAttribute("readonly", "true");
      const checkbox = createCheckbox(option.id);
      this.input.append(checkbox);
      checkbox.click();
      if (shouldCreateNewUnselectOptionButton) {
        this.createNewUnselectOptionButton();
      }
      this.sugestionsContainer.innerHTML = "";
      return checkbox;
    }

    createNewUnselectOptionButton() {
      const newUnselectOptionButton = document.createElement("span");
      newUnselectOptionButton.classList.add(
        "text-xl",
        "absolute",
        "right-2",
        "top-6px",
        "cursor-pointer"
      );
      this.unselectOptionButton = newUnselectOptionButton;

      newUnselectOptionButton.addEventListener("click", () => {
        this.unselectOption(this.unselectOptionButton);
      });
      newUnselectOptionButton.innerHTML = "&times;";

      this.element.append(newUnselectOptionButton);
    }

    unselectOption(unselectOptionButton) {
      unselectOptionButton.remove();
      this.input.removeAttribute("readonly");
      this.input.value = "";
      this.checkbox.click();
    }
  }

  const autocompletes = document.querySelectorAll("[data-autocomplete]");

  autocompletes.forEach((autocomplete) => {
    new Autocomplete(autocomplete);
  });
}
