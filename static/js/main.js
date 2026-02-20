const menuButton = document.getElementById('hamburger');
const mainNav = document.getElementById('mainNav');
if (menuButton && mainNav) {
  menuButton.addEventListener('click', () => mainNav.classList.toggle('open'));
}
