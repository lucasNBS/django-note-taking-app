{
  const backgroundElement = document.querySelector("#modal-form-background");
  const modalElement = document.querySelector("#modal-form");
  const openModalButtons = document.querySelectorAll("[data-form-modal]");

  const modal = new Modal(modalElement, backgroundElement);

  function validateModalData() {
    const input = modal.element.querySelector("input#id_title");

    if (input.value.length > 50) {
      const error = this.element.querySelector("[data-modal-error]");
      error.classList.remove("h-0");
      return false;
    }

    return true;
  }

  modal.element.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    const is_valid = validateModalData();
    if (is_valid) {
      e.target.submit();
    }
  });

  function openModalWithSelectedInstanceData(button) {
    modal.element.querySelector("[data-modal-title]").innerText =
      button.dataset.modalTitle;
    modal.element
      .querySelector("input#id_title")
      .setAttribute("value", button.dataset.modalValue);
    modal.element.querySelector("[data-modal-form]").action =
      button.dataset.url;
    modal.open();
  }

  openModalButtons.forEach((button) => {
    button.addEventListener("click", () =>
      openModalWithSelectedInstanceData(button)
    );
  });
}
