(function () {
  var stored = localStorage.getItem("theme");
  var theme = stored === "light" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", theme);
})();

document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.getElementById("theme-toggle");
  if (!toggle) {
    return;
  }

  function sync() {
    var current = document.documentElement.getAttribute("data-theme");
    toggle.textContent = current === "dark" ? "Light Mode" : "Dark Mode";
  }

  toggle.addEventListener("click", function () {
    var current = document.documentElement.getAttribute("data-theme");
    var next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    sync();
  });

  sync();
});
