document.addEventListener("DOMContentLoaded", function() {
    const openModalButton = document.getElementById('openModalButton');
    const modal = document.getElementById('modal');
    const closeModalButton = document.getElementById('closeModalButton');

    // Mostrar y ocultar modal
    openModalButton.addEventListener('click', function() {
        modal.classList.remove('hidden');
    });

    closeModalButton.addEventListener('click', function() {
        modal.classList.add('hidden');
    });
});
