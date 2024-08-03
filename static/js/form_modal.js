{
  class Modal {
    constructor(modal, background) {
      this.element = modal;
      this.background = background;
      this.closeButton = modal.querySelector("[data-modal-close]");
      this.init();
    }

    init() {
      this.element.addEventListener("click", (e) => {
        e.stopPropagation();
      });
      this.background.addEventListener("click", () => this.close());
      this.closeButton.addEventListener("click", () => this.close());
      this.element.querySelector("form").addEventListener("submit", (e) => {
        e.preventDefault();

        const input = modal.element.querySelector("input#id_name");

        if (input.value.length > 50) {
          const error = this.element.querySelector("[data-modal-error]");
          error.classList.remove("h-0");
          return;
        }

        e.target.submit();
      });
    }

    open() {
      this.background.classList.remove("-z-10");
      this.background.classList.add("z-50");
    }

    close() {
      this.background.classList.add("-z-10");
      this.background.classList.remove("z-50");
    }
  }

  const backgroundElement = document.querySelector("#modal-form-background");
  const modalElement = document.querySelector("#modal-form");
  const actionButtons = document.querySelectorAll("[data-form-modal]");

  const modal = new Modal(modalElement, backgroundElement);

  actionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      modal.element.querySelector("[data-modal-title]").innerText =
        button.dataset.modalTitle;
      modal.element
        .querySelector("input#id_name")
        .setAttribute("value", button.dataset.modalValue);
      modal.element.querySelector("[data-modal-form]").action =
        button.dataset.url;
      modal.open();
    });
  });
}
