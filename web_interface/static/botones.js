function redirigirBoton(url) {
    const botones = document.querySelectorAll('button');
    botones.forEach(boton => boton.disabled = true);
    window.location.href = url;
}