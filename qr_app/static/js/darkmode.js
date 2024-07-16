document.addEventListener("DOMContentLoaded", function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav.sidebar');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = body.querySelector(".mode-text");

    // Handle sidebar toggle
    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("close");
    });

    // Check for saved 'darkMode' in localStorage
    const currentMode = localStorage.getItem('darkMode');
    if (currentMode === 'enabled') {
        body.classList.add('dark');
        modeText.innerText = "Light mode";
    } else {
        modeText.innerText = "Dark mode";
    }

    // Handle dark mode toggle
    modeSwitch.addEventListener("click", () => {
        body.classList.toggle("dark");
        if (body.classList.contains("dark")) {
            localStorage.setItem('darkMode', 'enabled');
            modeText.innerText = "Light mode";
        } else {
            localStorage.setItem('darkMode', 'disabled');
            modeText.innerText = "Dark mode";
        }
    });
});
