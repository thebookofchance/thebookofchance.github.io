/* v0.26 — Page-by-page edition of the original Book of Chance web readings.
 * Local-only progress. JavaScript failure leaves original scrolling HTML readable.
 * A "page" is a viewport column, not a fixed printed page number.
 */
(() => {
  'use strict';
  const article=document.querySelector('.reading-article[data-reader-slug]');
  if (!article || article.querySelector('.book-pages-viewport')) return;
  const heading=article.querySelector(':scope > .chapter-heading');
  const body=article.querySelector(':scope > .reading-body');
  const oldPager=article.querySelector(':scope > .chapter-pager');
  if (!heading || !body || !oldPager) return;

  const slug=article.dataset.readerSlug;
  const slugOrder=[
    'note-on-this-edition','note-to-reader','introduction',
    'part-one','arrival','the-unfolding','fortune-and-hardship','the-open-future',
    'part-two','action-within-uncertainty','reflection-and-growth','hope','shared-fortune',
    'part-three','fellowship','the-living-world','stewardship','death-and-the-unknown',
    'afterword','note-on-the-fellowship','reader-resources','ways-of-reflecting','note-on-language','further-reading'
  ];
  const sectionNumber=Math.max(1,slugOrder.indexOf(slug)+1);
  const key='chance-page-v026-'+slug;
  const safeGet=k=>{try{return localStorage.getItem(k)}catch{return null}};
  const safeSet=(k,v)=>{try{localStorage.setItem(k,v)}catch{}};
  let saved={page:0,width:0,ratio:0};
  try {const v=JSON.parse(safeGet(key)||'null');if(v&&Number.isFinite(v.page))saved=v;}catch{}
  let page=0, total=1, active=false, raf=0, layoutWidth=0, layoutHeight=0;
  let turnDirection=0;

  const shell=document.createElement('div');shell.className='book-pages-shell';
  const viewport=document.createElement('div');viewport.className='book-pages-viewport';
  viewport.setAttribute('role','region');viewport.setAttribute('aria-label','One page at a time');
  viewport.setAttribute('tabindex','0');
  const flow=document.createElement('div');flow.className='book-pages-flow';
  flow.append(heading,body);viewport.append(flow);shell.append(viewport);
  article.insertBefore(shell,oldPager);

  const controls=document.createElement('nav');
  controls.className='book-pages-controls';
  controls.setAttribute('aria-label','Reading page controls');
  controls.innerHTML=`<button type="button" class="book-turn book-turn-prev" data-book-prev aria-label="Previous page">← <span>Previous</span></button>
    <div class="book-page-location"><strong data-book-page-counter aria-live="polite">Page 1 of 1</strong><span data-book-page-detail>Section ${sectionNumber} of ${slugOrder.length}</span></div>
    <button type="button" class="book-turn book-turn-next" data-book-next aria-label="Next page"><span>Next</span> →</button>`;
  article.insertBefore(controls,oldPager);
  const prev=controls.querySelector('[data-book-prev]');
  const next=controls.querySelector('[data-book-next]');
  const counter=controls.querySelector('[data-book-page-counter]');
  const detail=controls.querySelector('[data-book-page-detail]');
  const prevSection=oldPager.querySelector('.chapter-prev')?.getAttribute('href')||null;
  const nextSection=oldPager.querySelector('.chapter-next')?.getAttribute('href')||null;

  const title=heading.querySelector('.eyebrow')?.textContent?.trim()||`Section ${sectionNumber}`;
  const show=()=>{
    flow.style.transform=`translate3d(-${Math.round(page*layoutWidth)}px,0,0)`;
    counter.textContent=`Page ${page+1} of ${total}`;
    const percentage=Math.round((page+1)/Math.max(total,1)*100);
    detail.textContent=`${title} · ${percentage}% of this section`;
    prev.disabled=page===0&&!prevSection;
    next.disabled=page===total-1&&!nextSection;
    prev.title=page===0&&prevSection?'Previous section':'Previous page';
    next.title=page===total-1&&nextSection?'Next section':'Next page';
    viewport.setAttribute('aria-label',`${title}, page ${page+1} of ${total}`);
  };
  const save=()=>{
    safeSet(key,JSON.stringify({page,width:layoutWidth,ratio:total>1?page/(total-1):0}));
    safeSet('chance-last-slug',slug);
    const progress=Math.round((page+1)/Math.max(total,1)*100);
    const old=Number(safeGet('chance-read-'+slug)||0);
    safeSet('chance-read-'+slug,String(Math.max(old,progress)));
  };
  const measure=(initial=false)=>{
    if(!active)return;
    const w=Math.floor(viewport.getBoundingClientRect().width);
    const h=Math.floor(viewport.getBoundingClientRect().height);
    if(w<80||h<100)return;
    const oldRatio=total>1?page/(total-1):0;
    flow.style.width=w+'px';flow.style.height=h+'px';
    flow.style.columnWidth=w+'px';flow.style.columnGap='0px';
    layoutWidth=w;layoutHeight=h;
    // Count the columns created by the browser, instead of estimating from words.
    total=Math.max(1,Math.ceil((flow.scrollWidth-1)/w));
    if(initial){
      // Exact page when viewport width is unchanged; proportional position otherwise.
      page=Math.max(0,Math.min(total-1,
        Math.round(saved.width===w?saved.page:(saved.ratio||0)*(total-1))));
    } else if(turnDirection){
      page=turnDirection>0?0:total-1;turnDirection=0;
    } else {
      page=Math.max(0,Math.min(total-1,Math.round(oldRatio*(total-1))));
    }
    show();save();
  };
  const schedule=()=>{if(raf)cancelAnimationFrame(raf);raf=requestAnimationFrame(()=>{raf=0;measure();});};
  const move=delta=>{
    if(delta>0){
      if(page<total-1){page++;show();save();}
      else if(nextSection)location.href=nextSection;
    }else{
      if(page>0){page--;show();save();}
      else if(prevSection)location.href=prevSection;
    }
  };
  prev.addEventListener('click',()=>move(-1));
  next.addEventListener('click',()=>move(1));
  viewport.addEventListener('keydown',e=>{
    if(e.altKey||e.ctrlKey||e.metaKey)return;
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();move(1);}
    if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();move(-1);}
  });
  document.addEventListener('keydown',e=>{
    if(e.target===viewport || e.altKey||e.ctrlKey||e.metaKey)return;
    if(['BUTTON','A','INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName))return;
    if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();move(1)}
    if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();move(-1)}
  });
  let touch=null;
  viewport.addEventListener('touchstart',e=>{if(e.touches.length===1)touch={x:e.touches[0].clientX,y:e.touches[0].clientY}},{passive:true});
  viewport.addEventListener('touchend',e=>{
    if(!touch||e.changedTouches.length!==1)return;
    const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;touch=null;
    if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.4)move(dx<0?1:-1);
  },{passive:true});

  // Enable paging only after the original article has been safely placed in the new view.
  document.body.classList.add('book-paged-mode');
  active=true;
  requestAnimationFrame(()=>measure(true));
  const scaleButtons=[...document.querySelectorAll('[data-font-decrease],[data-font-increase]')];
  for(const button of scaleButtons)button.addEventListener('click',()=>requestAnimationFrame(schedule));
  window.addEventListener('resize',schedule,{passive:true});
  if(typeof ResizeObserver!=='undefined')new ResizeObserver(schedule).observe(viewport);
  for(const img of flow.querySelectorAll('img')){
    if(!img.complete){img.addEventListener('load',schedule,{once:true});img.addEventListener('error',schedule,{once:true});}
  }
  if(document.fonts?.ready)document.fonts.ready.then(schedule);
})();
