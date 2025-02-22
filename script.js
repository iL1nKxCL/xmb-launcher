// script.js
let currentIndex = 0;
const menuItems = document.querySelectorAll('.xmb-item');

// Función para actualizar el estado de selección
function updateSelection() {
    menuItems.forEach((item, index) => {
        item.classList.remove('selected');
        if (index === currentIndex) {
            item.classList.add('selected');
        }
    });
}

// Manejo de la navegación por teclado
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        // Mover a la derecha
        currentIndex = (currentIndex + 1) % menuItems.length;
    } else if (event.key === 'ArrowLeft') {
        // Mover a la izquierda
        currentIndex = (currentIndex - 1 + menuItems.length) % menuItems.length;
    }
    updateSelection();
});

// Inicializar la selección al cargar la página
updateSelection();
