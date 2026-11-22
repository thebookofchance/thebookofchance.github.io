/* Guided Reading Journey 0.24: no analytics, network calls or answer storage. */
(() => {
  'use strict';
  const root = document.querySelector('[data-journey-root]');
  if (!root) return;
  const routes = [...root.querySelectorAll('[data-journey-panel]')];
  const choices = [...document.querySelectorAll('[data-journey-choice]')];
  const valid = new Map(routes.map(route => [route.id, route]));
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function updateProgress(route) {
    if (!route) return;
    const checks = [...route.querySelectorAll('[data-journey-check]')];
    checks.forEach(check => check.closest('[data-journey-stop]')?.classList.toggle('v24-explored', check.checked));
    const count = checks.filter(check => check.checked).length;
    const target = route.querySelector('[data-journey-progress-text]');
    if (target) target.textContent = `${count} of ${checks.length} explored`;
  }

  function activate(id, opts = {}) {
    const route = valid.get(id);
    routes.forEach(panel => panel.classList.toggle('v24-active', panel === route));
    choices.forEach(choice => {
      const selected = choice.dataset.journeyChoice === id;
      choice.classList.toggle('v24-selected', selected);
      if (selected) choice.setAttribute('aria-current', 'true');
      else choice.removeAttribute('aria-current');
    });
    root.classList.toggle('v24-has-selection', Boolean(route));
    if (route) updateProgress(route);
    if (route && opts.scroll) {
      route.scrollIntoView({behavior: prefersReducedMotion.matches ? 'auto' : 'smooth', block: 'start'});
      if (opts.focus) route.querySelector('h2')?.focus({preventScroll:true});
    }
  }

  root.classList.add('v24-js-ready');
  choices.forEach(choice => {
    choice.addEventListener('click', event => {
      const id = choice.dataset.journeyChoice;
      if (!valid.has(id)) return;
      event.preventDefault();
      if (window.location.hash !== `#${id}`) window.history.pushState(null, '', `#${id}`);
      activate(id, {scroll:true, focus:true});
    });
  });
  root.querySelectorAll('[data-journey-check]').forEach(check => {
    check.addEventListener('change', () => updateProgress(check.closest('[data-journey-panel]')));
  });
  root.querySelectorAll('[data-journey-reset]').forEach(button => {
    button.addEventListener('click', () => {
      const route = button.closest('[data-journey-panel]');
      route?.querySelectorAll('[data-journey-check]').forEach(check => {check.checked = false;});
      updateProgress(route);
    });
  });
  document.querySelectorAll('[data-journey-back]').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      window.history.pushState(null, '', '#choose-a-path');
      activate(null);
      document.getElementById('choose-a-path')?.scrollIntoView({behavior: prefersReducedMotion.matches ? 'auto' : 'smooth', block:'start'});
      document.getElementById('choose-path-heading')?.setAttribute('tabindex','-1');
      document.getElementById('choose-path-heading')?.focus({preventScroll:true});
    });
  });
  window.addEventListener('hashchange', () => activate(decodeURIComponent(window.location.hash.slice(1)), {scroll:true}));
  window.addEventListener('popstate', () => activate(decodeURIComponent(window.location.hash.slice(1)), {scroll:true}));
  const initial = decodeURIComponent(window.location.hash.slice(1));
  activate(initial);
  if (valid.has(initial)) window.requestAnimationFrame(() => valid.get(initial).scrollIntoView({block:'start'}));
})();
