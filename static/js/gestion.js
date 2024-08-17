document.addEventListener("DOMContentLoaded", function() {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var image = document.getElementById('imagen');
    canvas.width = image.width;
    canvas.height = image.height;
    
    // Dibuja la imagen en el lienzo al cargar la página
    ctx.drawImage(image, 0, 0);
    
    // Maneja el evento de escritura en el lienzo
    document.getElementById('texto').addEventListener('input', function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Borra el lienzo
        ctx.drawImage(image, 0, 0); // Vuelve a dibujar la imagen
        ctx.font = '20px Arial';
        ctx.fillText(this.value, 50, 50); // Dibuja el texto en el lienzo
    });
});
