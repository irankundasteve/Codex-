const faqSearch = document.getElementById('faqSearch');
faqSearch?.addEventListener('input', () => {
  const q = faqSearch.value.toLowerCase();
  document.querySelectorAll('.faq-item').forEach((item) => {
    item.style.display = item.querySelector('summary').textContent.toLowerCase().includes(q) ? '' : 'none';
  });
});
