const Modal = class {
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
  }

  open() {
    this.background.classList.remove("-z-10");
    this.background.classList.add("z-50");
    this.element.querySelectorAll("input")[1]?.focus();
  }

  close() {
    this.background.classList.add("-z-10");
    this.background.classList.remove("z-50");
  }
};
