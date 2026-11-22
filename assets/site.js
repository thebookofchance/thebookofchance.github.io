/* The Book of Chance: local-only preferences, never contact-server or collect user data. */
(() => {
  'use strict';
  const get = (k, d = null) => {try {let v=localStorage.getItem(k);return v===null?d:v;}catch {return d;}};
  const put = (k, v) => {try {localStorage.setItem(k, v);}catch {}};
  const doc = document.documentElement;

  const setTheme = theme => {
    doc.dataset.theme = theme === 'dark' ? 'dark' : 'light';
    put('chance-theme', doc.dataset.theme);
    document.querySelectorAll('[data-theme-toggle]').forEach(b=>{
      b.setAttribute('aria-label', `Switch to ${doc.dataset.theme==='light'?'dark':'light'} mode`);
      b.title = `Switch to ${doc.dataset.theme==='light'?'dark':'light'} mode`;
    });
  };
  setTheme(get('chance-theme','light'));
  document.querySelectorAll('[data-theme-toggle]').forEach(btn=>btn.addEventListener('click',()=>setTheme(doc.dataset.theme==='dark'?'light':'dark')));
  const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('.main-nav');
  if(menu&&nav){menu.addEventListener('click',()=>{let expanded=menu.getAttribute('aria-expanded')==='true';menu.setAttribute('aria-expanded',String(!expanded));menu.setAttribute('aria-label',expanded?'Open navigation':'Close navigation');nav.classList.toggle('open',!expanded);});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false')}));}

  // Persistence is confined to the user's browser. No registration, analytics or tracking.
  const article=document.querySelector('[data-reader-slug]');
  const allReadingSlugs=['arrival','the-unfolding','fortune-and-hardship','the-open-future','action-within-uncertainty','reflection-and-growth','hope','shared-fortune','fellowship','the-living-world','stewardship','death-and-the-unknown'];
  if(article){
    const slug=article.dataset.readerSlug;
    let scale=Number(get('chance-font-scale','1'))||1;
    const fontDecrease=document.querySelector('[data-font-decrease]'),fontIncrease=document.querySelector('[data-font-increase]');
    const applyScale=()=>{scale=Math.max(.89,Math.min(1.28,Math.round(scale*100)/100));doc.style.setProperty('--reader-scale',String(scale));put('chance-font-scale',String(scale));if(fontDecrease)fontDecrease.disabled=scale<=.89;if(fontIncrease)fontIncrease.disabled=scale>=1.28;};
    if(fontDecrease)fontDecrease.addEventListener('click',()=>{scale-=.1;applyScale()});
    if(fontIncrease)fontIncrease.addEventListener('click',()=>{scale+=.1;applyScale()});
    applyScale();
    const bookmark=document.querySelector('[data-bookmark]');
    const bookmarkKey='chance-bookmark-'+slug;
    const renderBookmark=()=>{if(!bookmark)return;const on=get(bookmarkKey)==='true';bookmark.setAttribute('aria-pressed',String(on));bookmark.querySelector('span').textContent=on?'Bookmarked':'Bookmark';bookmark.firstChild.textContent=on?'★ ':'☆ ';};
    if(bookmark){bookmark.addEventListener('click',()=>{put(bookmarkKey,String(get(bookmarkKey)!=='true'));renderBookmark()});renderBookmark();}
    const fill=document.querySelector('[data-progress-fill]');
    let ticking=false;
    const updateProgress=()=>{
      const top=article.getBoundingClientRect().top+window.scrollY;
      const height=article.offsetHeight;
      let amount=Math.max(0,Math.min(100,100*((window.scrollY+window.innerHeight*.7-top)/Math.max(height,1))));
      if(fill)fill.style.width=amount+'%';
      if(allReadingSlugs.includes(slug)) {
        const old=Number(get('chance-read-'+slug,'0'))||0;
        put('chance-read-'+slug,String(Math.round(Math.max(old,amount))));
      }
      put('chance-last-slug',slug);
      ticking=false;
    };
    window.addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(updateProgress)}},{passive:true});
    window.addEventListener('resize',updateProgress);
    updateProgress();
  }

  const continueLink=document.querySelector('[data-continue-reading]');
  if(continueLink){
    const last=get('chance-last-slug');
    if(last&&/^[a-z0-9-]+$/.test(last)){
      continueLink.href=last+'/';continueLink.innerHTML='Continue reading <span aria-hidden="true">→</span>';
    }
    const count=allReadingSlugs.filter(slug=>Number(get('chance-read-'+slug,'0'))>=85).length;
    const status=document.querySelector('[data-reading-status]');
    if(status){status.textContent=count?`${count} of 12 readings completed on this device.`:'Your place is saved only on this device.';}
  }

  const input=document.getElementById('book-search'),results=document.getElementById('search-results'),toc=document.getElementById('book-toc');
  if(input&&results&&toc){
    let index=null, delay=0;
    const show=async()=>{
      const q=input.value.trim().toLocaleLowerCase();
      if(q.length<2){results.hidden=true;toc.hidden=false;results.replaceChildren();return;}
      if(!index){
        try{const response=await fetch('../search-index.json');if(!response.ok)throw new Error('Search index unavailable');index=await response.json()}catch{results.hidden=false;results.textContent='Search is available when the site is served from a website or local server.';return;}
      }
      const terms=q.split(/\s+/).filter(Boolean);
      const found=index.filter(s=>terms.every(term=>(s.title+' '+s.text).toLocaleLowerCase().includes(term))).slice(0,15);
      results.replaceChildren();results.hidden=false;toc.hidden=true;
      const summary=document.createElement('p');summary.textContent=`${found.length} result${found.length===1?'':'s'}${found.length===15?' (showing first 15)':''}`;results.append(summary);
      found.forEach(s=>{
        const a=document.createElement('a');a.href=s.slug+'/';a.className='search-result';
        const title=document.createElement('strong');title.textContent=s.title;
        const excerpt=document.createElement('span');const lower=s.text.toLocaleLowerCase();const i=lower.indexOf(terms[0]);
        const start=Math.max(0,(i>=0?i:0)-95);excerpt.textContent=(start?'…':'')+s.text.slice(start,start+250)+(s.text.length>start+250?'…':'');
        a.append(title,excerpt);results.append(a);
      });
    };
    input.addEventListener('input',()=>{clearTimeout(delay);delay=setTimeout(show,130)});
  }

  const coverButtons=[...document.querySelectorAll('[data-cover-choice]')],coverImg=document.getElementById('selected-print-cover');
  if(coverButtons.length&&coverImg){
    const choose=kind=>{const good=kind==='dark'?'dark':'light';coverImg.src='../assets/covers/'+good+'-cover.webp';coverImg.alt=(good==='dark'?'Dark':'Light')+' Edition book cover';coverButtons.forEach(b=>{const on=b.dataset.coverChoice===good;b.classList.toggle('selected',on);b.setAttribute('aria-pressed',String(on));});};
    choose(get('chance-print-cover','light'));
    coverButtons.forEach(b=>b.addEventListener('click',()=>choose(b.dataset.coverChoice)));
    document.getElementById('save-cover-choice')?.addEventListener('click',()=>{
      const kind=coverButtons.find(b=>b.getAttribute('aria-pressed')==='true')?.dataset.coverChoice||'light';
      put('chance-print-cover',kind);
      const status=document.getElementById('cover-save-status');
      if(status)status.textContent=`${kind==='light'?'Light':'Dark'} cover saved on this device. This is not a reservation or order; no details were submitted.`;
    });
  }
})();
