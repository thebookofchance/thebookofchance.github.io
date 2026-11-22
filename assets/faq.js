/* Questions About Chance v0.23. All filtering is local; no requests or storage. */
(() => {
  'use strict';
  const root=document.getElementById('faq-explorer');
  if(!root)return;
  const search=document.getElementById('faq-search');
  const clear=document.getElementById('faq-clear');
  const buttons=[...root.querySelectorAll('[data-faq-filter]')];
  const questions=[...root.querySelectorAll('[data-faq-question]')];
  const groups=[...root.querySelectorAll('[data-faq-group]')];
  const results=document.getElementById('faq-results');
  const empty=document.getElementById('faq-empty');
  let filter='all';
  const normalise=s=>String(s).toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'');
  const apply=()=>{
    const terms=normalise(search.value.trim()).split(/\s+/).filter(Boolean);
    let matches=0;
    questions.forEach(el=>{
      const inCategory=filter==='all'||filter===el.dataset.category;
      const haystack=normalise(el.dataset.search||'');
      const shown=inCategory && terms.every(t=>haystack.includes(t));
      el.hidden=!shown;
      if(shown)matches++;
    });
    groups.forEach(group=>{group.hidden=![...group.querySelectorAll('[data-faq-question]')].some(el=>!el.hidden);});
    buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.faqFilter===filter)));
    empty.hidden=matches!==0;
    results.textContent=(terms.length||filter!=='all') ? `${matches} question${matches===1?'':'s'} match your selection` : 'Showing all 26 questions';
    clear.hidden=!search.value;
  };
  buttons.forEach(button=>button.addEventListener('click',()=>{filter=button.dataset.faqFilter;apply();}));
  search.addEventListener('input',apply);
  clear.addEventListener('click',()=>{search.value='';search.focus();apply();});
  const openTarget=()=>{
    const id=decodeURIComponent(location.hash.slice(1));
    if(!/^q\d{2}$/.test(id))return;
    const target=document.getElementById(id);
    if(!target||!questions.includes(target))return;
    filter='all';search.value='';apply();target.open=true;
  };
  window.addEventListener('hashchange',openTarget);
  apply();openTarget();
})();
