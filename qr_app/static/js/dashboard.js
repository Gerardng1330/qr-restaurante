document.addEventListener("DOMContentLoaded", function() {
    const editIcons = document.querySelectorAll(".edit-icon");
    const popup = document.getElementById("edit-popup");
    const closeBtn = popup.querySelector(".close");

    editIcons.forEach(icon => {
        icon.addEventListener("click", () => {
            popup.classList.remove("hidden");
        });
    });

    closeBtn.addEventListener("click", () => {
        popup.classList.add("hidden");
    });

    window.addEventListener("click", (event) => {
        if (event.target == popup) {
            popup.classList.add("hidden");
        }
    });
});
