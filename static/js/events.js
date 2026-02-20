const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortFilter = document.getElementById('sortFilter');
const eventGrid = document.getElementById('eventGrid');

async function updateGrid() {
  if (!window.eventsApiUrl || !eventGrid) return;
  const params = new URLSearchParams({
    q: searchInput?.value ?? '',
    category: categoryFilter?.value ?? 'all',
    sort: sortFilter?.value ?? 'date_asc',
  });
  const res = await fetch(`${window.eventsApiUrl}&${params.toString()}`);
  const events = await res.json();
  eventGrid.innerHTML = events
    .map(
      (event) => `
      <a class="card" href="/events/${event.id}?lang=${new URL(window.eventsApiUrl).searchParams.get('lang')}">
        <img src="${event.images[0]}" alt="${event.title}" />
        <div class="card-body">
          <span class="badge">${event.category}</span>
          <h3>${event.title}</h3>
          <p>${event.date} · ${event.time}</p>
        </div>
      </a>
    `,
    )
    .join('');
}

[searchInput, categoryFilter, sortFilter].forEach((el) => el?.addEventListener('input', updateGrid));
