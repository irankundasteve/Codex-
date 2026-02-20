const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightboxImage');
const lightboxVideo = document.getElementById('lightboxVideo');

if (lightbox) {
  document.querySelectorAll('.gallery-item').forEach((item) => {
    item.addEventListener('click', () => {
      const card = item.closest('.media-card');
      const type = card?.dataset.type || 'image';
      const src = card?.dataset.src || item.src;
      if (type === 'video') {
        lightboxImage.classList.add('hidden');
        lightboxVideo.classList.remove('hidden');
        lightboxVideo.src = src;
      } else {
        lightboxVideo.classList.add('hidden');
        lightboxVideo.src = '';
        lightboxImage.classList.remove('hidden');
        lightboxImage.src = src;
      }
      lightbox.classList.remove('hidden');
    });
  });
  lightbox.addEventListener('click', () => {
    lightbox.classList.add('hidden');
    if (lightboxVideo) lightboxVideo.src = '';
  });
}
