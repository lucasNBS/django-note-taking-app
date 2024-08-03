{
  const forms = document.querySelectorAll("form[data-favorite-note]");

  forms.forEach((form) => {
    const checkbox = form.querySelector("input[type='checkbox']");
    const star = form.querySelector("i[data-star]");

    star.addEventListener("click", () => {
      checkbox.toggleAttribute("checked");

      form.submit();
    });
  });
}
