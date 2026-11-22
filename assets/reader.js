/* The Book of Chance v0.25 Reading Room.
 * All chapter HTML comes from this site's published reading pages; no remote API.
 * Saves only book/section/page on this browser, with a visible clear control.
 */
(() => {
  'use strict';
  const all=window.BOC_READER_BOOKS;
  const app=document.getElementById('reader-app');
  if (!app || !all) return;
  const get=s=>app.querySelector(s);
  const nodes={select:get('[data-reader-book]'),cover:get('[data-reader-cover]'),title:get('[data-reader-title]'),kind:get('[data-reader-kind]'),
    original:get('[data-reader-original]'),toc:get('[data-reader-toc]'),aside:get('[data-reader-aside]'),flow:get('[data-reader-flow]'),
    viewport:get('[data-reader-viewport]'),caption:get('[data-reader-section-caption]'),counter:get('[data-reader-count]'),
    status:get('[data-reader-page-status]'),location:get('[data-reader-location]'),prev:get('[data-reader-prev]'),next:get('[data-reader-next]')};
  let book=null,sectionIndex=0,pageIndex=0,pageCount=1,textSize=18,frame=0,ready=false,savingSuspended=false;
  const safeGet=k=>{try{return localStorage.getItem(k)}catch{return null}};
  const safeSet=(k,v)=>{try{localStorage.setItem(k,v)}catch{}};
  const safeRemove=k=>{try{localStorage.removeItem(k)}catch{}};
  const storeKey=id=>'boc-reading-room-v25-'+id;
  const keys=Object.keys(all);
  const preferred=new URLSearchParams(window.location.search).get('book');
  keys.forEach(key=>{
    const o=document.createElement('option');o.value=key;o.textContent=all[key].title;
    nodes.select.append(o);
  });
  function current(){return book.sections[sectionIndex]}
  function remember(){
    if(!book || !ready || savingSuspended)return;
    safeSet(storeKey(book.id),JSON.stringify({section:sectionIndex,page:pageIndex}));
    safeSet('boc-reading-room-v25-last',book.id);
  }
  function urlUpdate(){
    try{
      const url=new URL(location.href);url.searchParams.set('book',book.id);
      history.replaceState(null,'',url);
    }catch{}
  }
  function renderControls(){
    nodes.counter.textContent=`Page ${pageIndex+1} of ${pageCount}`;
    nodes.status.textContent=`Page ${pageIndex+1} of ${pageCount} · Section ${sectionIndex+1} of ${book.sections.length}`;
    nodes.location.textContent='Reading place saved on this device';
    nodes.prev.disabled=pageIndex===0&&sectionIndex===0;
    nodes.next.disabled=pageIndex>=pageCount-1&&sectionIndex>=book.sections.length-1;
    [...nodes.toc.querySelectorAll('button')].forEach((button,i)=>{
      if (i===sectionIndex){button.setAttribute('aria-current','true');button.setAttribute('aria-label',`Current section: ${book.sections[i].title}`)}
      else{button.removeAttribute('aria-current');button.removeAttribute('aria-label')}
    });
  }
  function position(){
    const width=Math.max(1,Math.floor(nodes.viewport.clientWidth));
    nodes.flow.style.columnWidth=width+'px';nodes.flow.style.columnGap='0px';
    nodes.flow.style.width=width+'px';nodes.flow.style.height=nodes.viewport.clientHeight+'px';
    // A real CSS column is a page. Count columns at the current viewport/font size.
    const scroll=nodes.flow.scrollWidth;
    pageCount=Math.max(1,Math.ceil((scroll-1)/width));
    pageIndex=Math.max(0,Math.min(pageCount-1,pageIndex));
    nodes.flow.style.transform=`translate3d(-${pageIndex*width}px,0,0)`;
    renderControls();remember();
  }
  function recalc(){
    if(frame)cancelAnimationFrame(frame);
    frame=requestAnimationFrame(()=>{frame=0;position()});
  }
  function drawSection(i,p=0){
    if(!book)return;
    sectionIndex=Math.max(0,Math.min(book.sections.length-1,i));
    pageIndex=p;
    const segment=current();
    nodes.flow.replaceChildren();
    // Authored, build-time-verified HTML, not user input.
    nodes.flow.innerHTML=segment.html;
    nodes.caption.textContent=segment.title;
    nodes.original.href=segment.source || book.original;
    nodes.original.textContent='Open this section in the original edition ↗';
    nodes.flow.scrollLeft=0;
    recalc();
    nodes.flow.querySelectorAll('img').forEach(img=>{
      if(img.complete) return;
      img.addEventListener('load',recalc,{once:true});
      img.addEventListener('error',recalc,{once:true});
    });
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(recalc);
  }
  function drawBook(id,loadSaved=true){
    savingSuspended=false;
    book=all[id]||all['book-of-chance'];
    ready=false;
    nodes.select.value=book.id;nodes.cover.src=book.cover;nodes.cover.alt=`Cover of ${book.title}`;
    nodes.title.textContent=book.title;nodes.kind.textContent=book.kind;
    nodes.toc.replaceChildren();
    book.sections.forEach((seg,i)=>{
      const button=document.createElement('button');button.type='button';
      button.textContent=`${String(i+1).padStart(2,'0')} · ${seg.title}`;
      button.addEventListener('click',()=>{savingSuspended=false;drawSection(i,0);if(window.innerWidth<940)toggleContents(true)});
      nodes.toc.append(button);
    });
    let state={section:0,page:0};
    if(loadSaved){try{
      const stored=JSON.parse(safeGet(storeKey(book.id))||'null');
      if(stored && Number.isSafeInteger(stored.section)&&Number.isSafeInteger(stored.page))state=stored;
    }catch{}}
    textSize=Number(safeGet('boc-reading-room-v25-textsize'))||18;
    textSize=Math.max(15,Math.min(23,textSize));
    nodes.flow.style.setProperty('--v25-reader-font',textSize+'px');
    ready=true;
    drawSection(state.section,state.page);urlUpdate();
  }
  function move(delta){
    if(!book)return;
    savingSuspended=false;
    if(delta>0){
      if(pageIndex<pageCount-1){pageIndex++;position()}
      else if(sectionIndex<book.sections.length-1)drawSection(sectionIndex+1,0);
    }else{
      if(pageIndex>0){pageIndex--;position()}
      else if(sectionIndex>0)drawSection(sectionIndex-1,Number.MAX_SAFE_INTEGER);
    }
  }
  function toggleContents(forceClosed){
    const collapsed=typeof forceClosed==='boolean'?forceClosed:nodes.aside.dataset.collapsed!=='true';
    nodes.aside.dataset.collapsed=String(collapsed);
    app.querySelectorAll('[data-reader-toggle]').forEach(b=>{
      b.setAttribute('aria-expanded',String(!collapsed));
      if(b.closest('.v25-aside-title'))b.textContent=collapsed?'Show':'Hide';
    });
  }
  app.querySelectorAll('[data-reader-toggle]').forEach(b=>b.addEventListener('click',()=>toggleContents()));
  nodes.prev.addEventListener('click',()=>move(-1));nodes.next.addEventListener('click',()=>move(1));
  nodes.select.addEventListener('change',e=>drawBook(e.target.value));
  get('[data-reader-smaller]').addEventListener('click',()=>changeSize(-1));
  get('[data-reader-larger]').addEventListener('click',()=>changeSize(1));
  function changeSize(d){
    textSize=Math.max(15,Math.min(23,textSize+d));
    nodes.flow.style.setProperty('--v25-reader-font',textSize+'px');
    safeSet('boc-reading-room-v25-textsize',String(textSize));
    get('[data-reader-smaller]').disabled=textSize<=15;
    get('[data-reader-larger]').disabled=textSize>=23;
    pageIndex=0;recalc();
  }
  get('[data-reader-clear]').addEventListener('click',()=>{
    if(!book)return;
    savingSuspended=true;
    safeRemove(storeKey(book.id));safeRemove('boc-reading-room-v25-last');
    drawSection(0,0);
    // Start over without immediately re-saving the cleared position.
    safeRemove(storeKey(book.id));nodes.location.textContent='Reading place cleared on this device';
  });
  document.addEventListener('keydown',event=>{
    if(!book||event.altKey||event.ctrlKey||event.metaKey)return;
    const tag=document.activeElement?.tagName;
    if(['INPUT','SELECT','TEXTAREA'].includes(tag))return;
    if(event.key==='ArrowRight'||event.key==='PageDown'){event.preventDefault();move(1)}
    if(event.key==='ArrowLeft'||event.key==='PageUp'){event.preventDefault();move(-1)}
    if(event.key==='Escape'&&window.innerWidth<940)toggleContents(true);
  });
  window.addEventListener('resize',recalc,{passive:true});
  if(typeof ResizeObserver!=='undefined')new ResizeObserver(recalc).observe(nodes.viewport);
  // When a link points to the reading room with a book query, open that title.
  const selected=keys.includes(preferred)?preferred:(safeGet('boc-reading-room-v25-last')||'book-of-chance');
  drawBook(selected);
  if(window.innerWidth<940)toggleContents(true);
  get('[data-reader-smaller]').disabled=textSize<=15;
  get('[data-reader-larger]').disabled=textSize>=23;
})();
