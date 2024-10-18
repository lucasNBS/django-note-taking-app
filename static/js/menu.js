{
  const menuButton = document.querySelector("[data-menu-button]");
  const closeMenuButton = document.querySelector("[data-close-menu-button]");
  const menu = document.querySelector("[data-menu]");
  const background = document.querySelector("#menu-background");

  menuButton.addEventListener("click", () => {
    menu.classList.remove("max-lg:-translate-x-full");
    menu.classList.add("absolute", "h-screen", "z-40");
    background.classList.remove("-z-10");
    background.classList.add("z-40");
  });

  closeMenuButton.addEventListener("click", closeMenu);
  background.addEventListener("click", closeMenu);

  function closeMenu() {
    menu.classList.add("max-lg:-translate-x-full");
    menu.addEventListener(
      "transitionend",
      () => {
        menu.classList.remove("absolute", "h-screen", "z-40");
      },
      { once: true }
    );
    background.classList.add("-z-10");
    background.classList.remove("z-40");
  }
}
