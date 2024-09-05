{
  const backgroundElement = document.querySelector("#modal-form-background");
  const modalElement = document.querySelector("#modal-form");
  const actionButtons = document.querySelectorAll("[data-form-modal]");

  const modal = new Modal(modalElement, backgroundElement);

  modal.element.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();

    const input = modal.element.querySelector("input#id_title");

    if (input.value.length > 50) {
      const error = this.element.querySelector("[data-modal-error]");
      error.classList.remove("h-0");
      return;
    }

    e.target.submit();
  });

  actionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      modal.element.querySelector("[data-modal-title]").innerText =
        button.dataset.modalTitle;
      modal.element
        .querySelector("input#id_title")
        .setAttribute("value", button.dataset.modalValue);
      modal.element.querySelector("[data-modal-form]").action =
        button.dataset.url;
      modal.open();
    });
  });
}
