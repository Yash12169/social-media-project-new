document.addEventListener("DOMContentLoaded", function () {
    const themeContainer = document.getElementById("theme-container");
    const themeToggleLink = document.getElementById("theme-toggle-link");
    const sunIcon = document.getElementById("sun-icon");
    const moonIcon = document.getElementById("moon-icon");
  
    themeToggleLink.addEventListener("click", function (e) {
      e.preventDefault();
      toggleTheme();
    });
  
    function toggleTheme() {
      const body = document.body;
      if (body.classList.contains("light-theme")) {
        body.classList.remove("light-theme");
        body.classList.add("dark-theme");
        sunIcon.style.display = "none";
        moonIcon.style.display = "inline-block";
      } else {
        body.classList.remove("dark-theme");
        body.classList.add("light-theme");
        moonIcon.style.display = "none";
        sunIcon.style.display = "inline-block";
      }
    }
  });
  