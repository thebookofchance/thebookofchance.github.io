/* The Book of Chance v0.20: local-only publication title/topic filtering.
   No network requests, cookies, analytics, or personal-data persistence. */
(() => {
  'use strict';
  const scope = document.querySelector('#publication-catalogue');
  if (!scope) return;
  const field = document.getElementById('library-search');
  const controls = [...scope.querySelectorAll('[data-library-filter]')];
  const items = [...scope.querySelectorAll('[data-library-item]')];
  const groups = [...scope.querySelectorAll('[data-library-group]')];
  const result = scope.querySelector('[data-library-result]');
  const empty = scope.querySelector('[data-library-empty]');
  if (!field || !controls.length || !items.length || !groups.length || !result || !empty) return;

  let category = 'all';
  const normalize = value => value.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const update = () => {
    const terms = normalize(field.value.trim()).split(/\s+/).filter(Boolean);
    let matches = 0;
    items.forEach(item => {
      const inCategory = category === 'all' || category === item.dataset.category;
      const text = normalize(item.dataset.search || '');
      const show = inCategory && terms.every(term => text.includes(term));
      item.hidden = !show;
      if (show) matches++;
    });
    groups.forEach(group => {
      group.hidden = ![...group.querySelectorAll('[data-library-item]')].some(item => !item.hidden);
    });
    controls.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.libraryFilter === category));
    });
    empty.hidden = matches !== 0;
    if (terms.length || category !== 'all') {
      result.textContent = `${matches} publication${matches === 1 ? '' : 's'} match your selection`;
    } else {
      result.textContent = `Showing all ${matches} publications`;
    }
  };
  controls.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.libraryFilter;
    update();
  }));
  field.addEventListener('input', update);
  update();
})();
