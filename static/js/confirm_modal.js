{
  const backgroundElement = document.querySelector("#modal-confirm-background");
  const modalElement = document.querySelector("#modal-confirm");
  const openModalButtons = document.querySelectorAll("[data-confirm-modal]");

  const modal = new Modal(modalElement, backgroundElement);

  const cancelButton = modal.element.querySelector("[data-form-cancel]");

  cancelButton.addEventListener("click", (e) => {
    e.preventDefault();
    modal.close();
  });

  function openModalWithSelectedInstanceData() {
    modal.element.querySelector("[data-modal-title]").innerText =
      button.dataset.modalTitle;
    modal.element.querySelector("[data-modal-text]").innerText =
      button.dataset.modalText;
    modal.element.querySelector("[data-modal-form]").action =
      button.dataset.url;
    modal.open();
  }

  openModalButtons.forEach((button) => {
    button.addEventListener("click", openModalWithSelectedInstanceData);
  });
}
