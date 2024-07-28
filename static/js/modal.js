const actionButtons = document.querySelectorAll("[data-button-modal]");
const background = document.querySelector("[data-modal-background]");
const closeModal = document.querySelector("[data-close-modal]");
const modal = document.querySelector("[data-modal]");

const modalTitle = document.querySelector("#modal-title");
const modalText = document.querySelector("#modal-text");

const modalForm = document.querySelector("[data-modal-form]");
const cancelButton = document.querySelector("[data-form-cancel]");

function handleCloseModal() {
  background.classList.add("-z-10");
  background.classList.remove("z-50");
}

actionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    background.classList.remove("-z-10");
    background.classList.add("z-50");
    modalTitle.innerText = button.dataset.modalTitle;
    modalText.innerText = button.dataset.modalText;

    modalForm.setAttribute("action", `${button.dataset.noteId}`);
  });
});

modal.addEventListener("click", (e) => {
  e.stopPropagation();
});

cancelButton.addEventListener("click", (e) => {
  e.preventDefault();
  handleCloseModal();
});

closeModal.addEventListener("click", handleCloseModal);

background.addEventListener("click", handleCloseModal);
