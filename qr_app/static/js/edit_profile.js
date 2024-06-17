document.addEventListener('DOMContentLoaded', function () {
    const messageBox = document.querySelector('.message-success');
    if (messageBox) {
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 5000); // Oculta el mensaje después de 5 segundos
    }
});
