class Modal {
  constructor(modal, background) {
    this.element = modal;
    this.background = background;
    this.closeButton = modal.querySelector("[data-modal-close]");
    this.cancelButton = modal.querySelector("[data-form-cancel]");
    this.init();
  }

  init() {
    this.element.addEventListener("click", (e) => {
      e.stopPropagation();
    });
    this.background.addEventListener("click", () => this.close());
    this.closeButton.addEventListener("click", () => this.close());
    this.cancelButton.addEventListener("click", (e) => {
      e.preventDefault();
      this.close();
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

const backgroundElement = document.querySelector("#modal-confirm-background");
const modalElement = document.querySelector("#modal-confirm");
const actionButtons = document.querySelectorAll("[data-button-modal]");

const modal = new Modal(modalElement, backgroundElement);

actionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    modal.element.querySelector("[data-modal-title]").innerText =
      button.dataset.modalTitle;
    modal.element.querySelector("[data-modal-text").innerText =
      button.dataset.modalText;
    modal.element.querySelector("[data-modal-form]").action =
      button.dataset.noteId;

    modal.open();
  });
});
