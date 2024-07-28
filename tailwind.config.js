/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "**/templates/**/*.html"],
  theme: {
    extend: {
      zIndex: {
        "-10": "-10",
      },
    },
  },
  plugins: [],
};
