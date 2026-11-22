/* The Book of Chance — private reflection workspace (v0.7).
   No network calls, cookies, analytics, external storage or automatic persistence.
   Answers are held only in the current tab until the visitor downloads or prints. */
(() => {
  'use strict';

  const templates = {
    chance: {
      title: 'The Reflection of Chance',
      questions: [
        ['What happened?', 'Describe an ordinary or meaningful moment without judging it.'],
        ['What was beyond my control?', 'Think about circumstance, timing, other people or chance.'],
        ['Where did I have a choice?', 'What did you choose, or what choice is still open?'],
        ['What did I learn or notice?', 'Uncertainty is an acceptable answer.'],
        ['What might become possible next?', 'Consider one modest, compassionate next step, if any.']
      ]
    },
    action: {
      title: 'The Act of Possibility',
      questions: [
        ['Whose possibilities could I help widen?', 'Think about what they actually want, including their right to decline.'],
        ['What can I offer within my means?', 'Time, a skill, a useful introduction, listening or another appropriate act.'],
        ['What boundaries should I respect?', 'Consider consent, privacy and the other person’s independence.'],
        ['What is one small step I could take?', 'Choose an achievable action without requiring a particular result.'],
        ['What happened, if I wish to reflect later?', 'You can leave this blank until later.']
      ]
    },
    week: {
      title: 'A Week of Possibilities',
      questions: [
        ['What surprised me?', 'Something that did not unfold as you expected.'],
        ['What did I learn about my circumstances?', 'What helped, limited or changed your options?'],
        ['Which choice am I glad I made?', 'Rest, asking for help and other quiet choices all count.'],
        ['Where did another person make a difference?', 'Notice people whose help may have been easy to overlook.'],
        ['What could I carry forward?', 'An intention, not a guarantee or demand for perfection.']
      ]
    }
  };
  const form = document.getElementById('chance-reflection-form');
  const select = document.getElementById('reflection-mode');
  const questions = document.getElementById('reflection-questions');
  const status = document.getElementById('reflection-status');
  const weeklyData = document.getElementById('chance-weekly-prompts');
  if (!form || !select || !questions || !status || !weeklyData) return;

  function setStatus(message) { status.textContent = message; }
  function hasWriting() { return [...questions.querySelectorAll('textarea')].some(x => x.value.trim()); }
  function buildTemplate(key) {
    const template = templates[key];
    if (!template) return;
    questions.replaceChildren();
    template.questions.forEach(([q, hint], i) => {
      const box = document.createElement('div');
      box.className = 'reflection-field';
      const label = document.createElement('label');
      const id = `reflection-answer-${i + 1}`;
      label.htmlFor = id;
      label.textContent = `${i + 1}. ${q}`;
      const desc = document.createElement('p');
      desc.id = `reflection-hint-${i + 1}`;
      desc.textContent = hint;
      const textarea = document.createElement('textarea');
      textarea.id = id;
      textarea.name = `reflection_answer_${i + 1}`;
      textarea.rows = 3;
      textarea.maxLength = 9000;
      textarea.setAttribute('aria-describedby', desc.id);
      textarea.placeholder = 'Your thoughts…';
      box.append(label, desc, textarea);
      questions.append(box);
    });
    select.value = key;
    setStatus(`Ready: ${template.title}. Your writing stays in this tab.`);
    document.getElementById('reflection-blank-pdf')?.setAttribute('href', {chance:'../files/reflection/The_Reflection_of_Chance_Fillable.pdf',action:'../files/reflection/The_Act_of_Possibility_Fillable.pdf',week:'../files/reflection/A_Week_of_Possibilities_Fillable.pdf'}[key]);
  }

  function askChange(next) {
    if (next === select.dataset.active) return;
    if (hasWriting() && !window.confirm('Switching templates will clear the answers in this tab. Download them first if you want to keep them. Continue?')) {
      select.value = select.dataset.active;
      return;
    }
    select.dataset.active = next;
    buildTemplate(next);
  }
  select.dataset.active = 'chance';
  buildTemplate('chance');
  select.addEventListener('change', () => askChange(select.value));
  document.querySelectorAll('[data-pick-template]').forEach(b => b.addEventListener('click', () => {
    const next = b.getAttribute('data-pick-template');
    askChange(next);
    document.getElementById('reflection-workspace')?.scrollIntoView({behavior:'smooth', block:'start'});
    select.focus({preventScroll:true});
  }));

  // Print the current typed responses in the journal's editorial style.
  // Visitors can choose "Save as PDF" in the browser print dialog. This
  // does not upload their private answers or require any third-party library.
  const pdfFiles = {
    chance: '../files/reflection/The_Reflection_of_Chance_Fillable.pdf',
    action: '../files/reflection/The_Act_of_Possibility_Fillable.pdf',
    week: '../files/reflection/A_Week_of_Possibilities_Fillable.pdf'
  };
  function updateBlankLink() {
    const link=document.getElementById('reflection-blank-pdf');
    if (link) {
      link.href=pdfFiles[select.dataset.active];
      link.setAttribute('aria-label',`Download blank fillable PDF: ${templates[select.dataset.active].title}`);
    }
  }
  updateBlankLink();
  select.addEventListener('change',updateBlankLink);
  document.querySelectorAll('[data-pick-template]').forEach(button => button.addEventListener('click',updateBlankLink));
  document.getElementById('reflection-print')?.addEventListener('click', () => {
    document.getElementById('reflection-print-sheet')?.remove();
    const sheet=document.createElement('article');
    sheet.id='reflection-print-sheet';
    sheet.setAttribute('aria-label','Printable reflection');
    const eyebrow=document.createElement('div');
    eyebrow.className='print-sheet-eyebrow';
    eyebrow.textContent='THE BOOK OF CHANCE / A PRIVATE REFLECTION';
    const heading=document.createElement('h1');
    heading.textContent=templates[select.dataset.active].title;
    const subtitle=document.createElement('p');
    subtitle.className='print-sheet-subtitle';
    subtitle.textContent='The Reflection Journal · By H · '+new Date().toLocaleDateString();
    sheet.append(eyebrow,heading,subtitle);
    [...questions.querySelectorAll('textarea')].forEach((input,i) => {
      const section=document.createElement('section');
      section.className='print-answer';
      const question=document.createElement('h2');
      question.textContent=`${i+1}. ${templates[select.dataset.active].questions[i][0]}`;
      const answer=document.createElement('p');
      answer.textContent=input.value.trim() || '—';
      section.append(question,answer);
      sheet.append(section);
    });
    const footer=document.createElement('p');
    footer.className='print-sheet-footer';
    footer.textContent='Private by default. No one is required to share this reflection.';
    sheet.append(footer);document.body.append(sheet);
    setStatus('Choose “Save as PDF” or a printer in the browser print dialog. For an editable PDF form, use the blank fillable worksheet instead.');
    window.print();
  });
  document.getElementById('reflection-clear')?.addEventListener('click', () => {
    if (hasWriting() && !window.confirm('Clear the answers from this tab? This cannot be undone.')) return;
    questions.querySelectorAll('textarea').forEach(x => {x.value='';});
    setStatus('Answers cleared. Nothing was submitted or saved.');
  });
  form.addEventListener('submit', ev => ev.preventDefault());

  // Deterministic 12-question cycle: updates on local Monday, no tracking.
  let items=[];
  try { items=JSON.parse(weeklyData.textContent); } catch { return; }
  if (!Array.isArray(items) || !items.length) return;
  const title=document.querySelector('[data-weekly-title]');
  const question=document.querySelector('[data-weekly-question]');
  const action=document.querySelector('[data-weekly-action]');
  const period=document.querySelector('[data-weekly-period]');
  const now=new Date();
  const monday = new Date(now.getFullYear(),now.getMonth(),now.getDate()-(now.getDay()+6)%7);
  const day=24*60*60*1000;
  const diff=Math.round((Date.UTC(monday.getFullYear(),monday.getMonth(),monday.getDate())-Date.UTC(2026,10,23))/day);
  let index=((Math.floor(diff/7)%items.length)+items.length)%items.length;
  let isArchive=false;
  const start=monday.toLocaleDateString(undefined,{day:'numeric',month:'short',year:'numeric'});
  const update = () => {
    const item=items[index];
    if (title) title.textContent=item.title;
    if (question) question.textContent=item.question;
    if (action) action.textContent=item.practice;
    if (period) period.textContent=isArchive ? 'From the twelve-question archive · The featured question updates each Monday.' : `Week beginning ${start} · From a twelve-question cycle that repeats.`;
  };
  update();
  document.querySelector('[data-next-weekly]')?.addEventListener('click',() => {
    index=(index+1)%items.length;
    isArchive=true;
    update();
  });
})();
