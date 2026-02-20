const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightboxImage');

if (lightbox && lightboxImage) {
  document.querySelectorAll('.gallery-item').forEach((item) => {
    item.addEventListener('click', () => {
      lightboxImage.src = item.src;
      lightbox.classList.remove('hidden');
    });
  });
  lightbox.addEventListener('click', () => lightbox.classList.add('hidden'));
}
