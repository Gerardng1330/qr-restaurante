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
document.addEventListener('DOMContentLoaded', function() {
    const openModalButton = document.getElementById('openModalButton');
    const closeModalButton = document.getElementById('closeModalButton');
    const modal = document.getElementById('modal');

    openModalButton.addEventListener('click', function() {
        modal.classList.remove('hidden');
    });

    closeModalButton.addEventListener('click', function() {
        modal.classList.add('hidden');
    });

    // Lógica para el popup de edición
    const editIcons = document.querySelectorAll('.edit-icon');
    const editPopup = document.getElementById('edit-popup');
    const closeEditPopupButton = editPopup.querySelector('.close');

    editIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            editPopup.classList.add('open');
        });
    });

    closeEditPopupButton.addEventListener('click', function() {
        editPopup.classList.remove('open');
    });
});