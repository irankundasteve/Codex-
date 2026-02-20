const mediaGrid = document.getElementById('mediaGrid');
const mediaCategory = document.getElementById('mediaCategory');
const mediaType = document.getElementById('mediaType');
const loadMore = document.getElementById('loadMore');

let visibleCount = 6;
function applyFilters() {
  if (!mediaGrid) return;
  const cards = [...mediaGrid.querySelectorAll('.media-card')];
  let shown = 0;
  cards.forEach((card) => {
    const categoryOk = !mediaCategory || mediaCategory.value === 'all' || card.dataset.category === mediaCategory.value;
    const typeOk = !mediaType || mediaType.value === 'all' || card.dataset.type === mediaType.value;
    const visible = categoryOk && typeOk && shown < visibleCount;
    card.style.display = visible ? '' : 'none';
    if (categoryOk && typeOk) shown += 1;
  });
}
mediaCategory?.addEventListener('change', () => { visibleCount = 6; applyFilters(); });
mediaType?.addEventListener('change', () => { visibleCount = 6; applyFilters(); });
loadMore?.addEventListener('click', () => { visibleCount += 6; applyFilters(); });
applyFilters();
