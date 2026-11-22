#!/usr/bin/env python3
"""Build the Book of Chance's free fillable reflection PDFs.
Usage: python scripts/build_reflection_pdfs.py
Requires reportlab. Uses locally installed Liberation fonts for reproducible output.
Future commercial print production requires separate printer proof, page count,
bleed, binding, ISBN, and distribution decisions; these files are not a print quote.
"""
from pathlib import Path
import os, math, textwrap
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit

ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='scripts' else Path('/mnt/data/Book_of_Chance_Website_v0.8_STAGING')
OUT=ROOT/'files'/'reflection'
OUT.mkdir(parents=True,exist_ok=True)
FONTROOT=Path('/usr/share/fonts/truetype/liberation')
FONTMAP=[('BookSerif','LiberationSerif-Regular.ttf','Times-Roman'),('BookSerifBold','LiberationSerif-Bold.ttf','Times-Bold'),('BookSerifItalic','LiberationSerif-Italic.ttf','Times-Italic'),('BookSans','LiberationSans-Regular.ttf','Helvetica'),('BookSansBold','LiberationSans-Bold.ttf','Helvetica-Bold')]
for name,file,fallback in FONTMAP:
    path=FONTROOT/file
    if path.exists():
        pdfmetrics.registerFont(TTFont(name,str(path)))
    else:
        # Portable baseline for Windows/macOS builds without Liberation fonts.
        # The released files were generated with the explicitly defined TTFs.
        from reportlab.pdfbase.pdfmetrics import Font
        pdfmetrics.registerFont(Font(name,fallback,'WinAnsiEncoding'))
INK=HexColor('#26313b'); BLUE=HexColor('#286cb8'); MUTED=HexColor('#63717c'); LINE=HexColor('#d6dfdf'); PALE=HexColor('#f5f8fa'); PAPER=HexColor('#fffefb'); SOFT=HexColor('#f2f3ef')
PRACTICES={
 'chance':('The Reflection of Chance','DAILY PRACTICE','Notice before you judge',[
  ('What happened?','Describe an ordinary or meaningful moment without judging it.'),
  ('What was beyond my control?','Think of circumstances, timing, other people or chance.'),
  ('Where did I have a choice?','Notice what you chose, or what choice is still open.'),
  ('What did I learn or notice?','Uncertainty is an acceptable answer.'),
  ('What might become possible next?','A modest and compassionate next step, if any.')]),
 'action':('The Act of Possibility','PRACTICE OF ACTION','Offer without obligation',[
  ('Whose possibilities could I help widen?','Consider what they actually want, including their right to decline.'),
  ('What can I offer within my means?','Time, a skill, an introduction, attention or something else.'),
  ('What boundaries should I respect?','Think about consent, privacy and independence.'),
  ('What is one small step I could take?','Something achievable without demanding an outcome.'),
  ('What happened, if I wish to reflect later?','This part can wait until another day.')]),
 'week':('A Week of Possibilities','WEEKLY PRACTICE','Look back, carry forward',[
  ('What surprised me?','Something that did not unfold as expected.'),
  ('What did I learn about my circumstances?','What helped, limited or changed my options?'),
  ('Which choice am I glad I made?','Rest, asking for help and quiet choices all count.'),
  ('Where did another person make a difference?','Notice care and contributions that are easy to overlook.'),
  ('What could I carry forward?','An intention, not a guarantee or demand for perfection.')])
}

def bg(c,w,h,face='white'):
    c.setFillColor(PAPER if face=='warm' else HexColor('#ffffff'));c.rect(0,0,w,h,stroke=0,fill=1)

def lines_logo(c,x,y,size=82):
    # Decorative motif, not a replacement of the approved site emblem.
    c.saveState();c.setLineWidth(.9);c.setStrokeColor(BLUE)
    c.circle(x,y,size*.44,stroke=1,fill=0)
    c.setStrokeColor(INK)
    for k in (-2,-1,0,1,2):
        # clipped through an ornamental square to keep consistent bounds
        px=x-size*.39+k*size*.16
        c.line(px,y-size*.40,px+size*.80,y+size*.40)
    c.setStrokeColor(BLUE);c.line(x-size*.33,y+size*.33,x+size*.36,y-size*.36)
    c.restoreState()

def line_text(c,text,x,y,maxwidth,font='BookSans',size=8,leading=12,color=MUTED):
    c.setFillColor(color);c.setFont(font,size)
    for i,lin in enumerate(simpleSplit(text,font,size,maxwidth)):
        c.drawString(x,y-i*leading,lin)
    return y-max(1,len(simpleSplit(text,font,size,maxwidth)))*leading

def pageframe(c,w,h,category,index=None):
    bg(c,w,h)
    left=49 if w<500 else 52
    c.setStrokeColor(LINE);c.setLineWidth(.7);c.line(left,h-49,w-left,h-49)
    c.setFillColor(BLUE);c.setFont('BookSansBold',8.2);c.drawString(left,h-38,'THE BOOK OF CHANCE')
    c.setFillColor(MUTED);c.setFont('BookSans',7.6);c.drawRightString(w-left,h-38,category.upper())
    c.line(left,43,w-left,43)
    c.setFillColor(MUTED);c.setFont('BookSans',7.1);c.drawString(left,29,'THE REFLECTION JOURNAL · H')
    if index is not None:c.drawRightString(w-left,29,f'{index:02d}')

def field(c,name,x,y,w,h,print_edition=False,lines=True):
    if print_edition:
        c.setStrokeColor(LINE);c.setLineWidth(.5)
        for j in range(max(2,round(h/18))):
            ly=y+9+j*18
            if ly<y+h-2:c.line(x,ly,x+w,ly)
    else:
        # Fillable AcroForm fields. All content is saved in the user's PDF by their viewer.
        c.acroForm.textfield(name=name,tooltip=name.replace('_',' '),x=x,y=y,width=w,height=h,
          borderStyle='solid',borderWidth=.7,borderColor=LINE,fillColor=PALE,
          textColor=INK,forceBorder=True,fontName='Helvetica',fontSize=10,
          fieldFlags='multiline')

def question(c,num,title,hint,x,top,w,box_h,fieldname,print_edition=False,fontsize=10.7):
    c.setFillColor(BLUE);c.setFont('BookSansBold',8)
    c.drawString(x,top-2,f'{num:02d}')
    c.setFillColor(INK);c.setFont('BookSerif',fontsize)
    title_lines=simpleSplit(title,'BookSerif',fontsize,w-30)
    for i,t in enumerate(title_lines): c.drawString(x+27,top-2-i*13,t)
    hint_top=top-17-13*(len(title_lines)-1)
    hint_bottom=line_text(c,hint,x+27,hint_top,w-28,'BookSans',7.4,10)
    y=hint_bottom-box_h-6
    field(c,fieldname,x+27,y,w-27,box_h,print_edition)
    return y-17

def cover(c,w,h,tag,title,subtitle,edition='DIGITAL · FILLABLE PDF'):
    bg(c,w,h,'warm');m=49
    c.setFillColor(BLUE);c.rect(m,h-66,34,2,fill=1,stroke=0)
    c.setFont('BookSansBold',8.5);c.drawString(m,h-90,'THE BOOK OF CHANCE')
    c.setFillColor(MUTED);c.setFont('BookSans',8);c.drawRightString(w-m,h-90,tag)
    lines_logo(c,w*.67,h*.69,min(w*.46,185))
    c.setFillColor(INK);c.setFont('BookSerif',min(35,w*.078))
    ypos=h*.49
    for ln in title.split('\n'):
        c.drawString(m,ypos,ln);ypos-=43 if w>500 else 37
    c.setStrokeColor(BLUE);c.setLineWidth(2);c.line(m,ypos+8,m+74,ypos+8)
    ypos-=20
    line_text(c,subtitle,m,ypos,w-2*m,'BookSerifItalic',12,17,INK)
    c.setFillColor(MUTED);c.setFont('BookSans',8.3);c.drawString(m,71,edition)
    c.setFont('BookSerifItalic',11);c.drawRightString(w-m,71,'By H')
    c.setStrokeColor(LINE);c.line(m,60,w-m,60)
    c.showPage()

def single_worksheet(path,key):
    title,tag,subtitle,qs=PRACTICES[key]
    w,h=A4; c=canvas.Canvas(str(path),pagesize=A4,pageCompression=1)
    c.setTitle(f'{title} — Fillable Reflection Worksheet | The Book of Chance')
    c.setAuthor('H · The Book of Chance')
    pageframe(c,w,h,'FILLABLE WORKSHEET',1)
    m=55
    c.setFillColor(BLUE);c.setFont('BookSansBold',8.5);c.drawString(m,h-76,tag)
    c.setFont('BookSerif',29);c.setFillColor(INK);c.drawString(m,h-108,title)
    line_text(c,subtitle+'. Take your time; there is no correct response.',m,h-132,w-2*m,'BookSans',9.1,12)
    c.setFillColor(INK);c.setFont('BookSans',8);c.drawString(m,h-166,'DATE / MOMENT (OPTIONAL)')
    field(c,key+'_date',m+151,h-173,w-2*m-151,21)
    top=h-203
    for i,(q,hint) in enumerate(qs,1):
        top=question(c,i,q,hint,m,top,w-2*m,60,f'{key}_q{i}',fontsize=12)
    c.setFillColor(MUTED);c.setFont('BookSans',7.5)
    c.drawString(m,56,'Free to use · Private by default · Save a copy in your PDF reader to keep your writing.')
    c.save()

def intro_journal(c,w,h):
    pageframe(c,w,h,'HOW TO USE',2)
    x=49
    c.setFillColor(BLUE);c.setFont('BookSansBold',8.5);c.drawString(x,h-85,'A NOTE BEFORE YOU BEGIN')
    c.setFillColor(INK);c.setFont('BookSerif',25);c.drawString(x,h-122,'A place to return to.')
    p=['This journal is not a record of achievement. It is a place to notice what you did not choose, where you could act, and whose lives meet your own.',
       'Use any practice in any order. You can leave questions unanswered. Some days a few words are enough.',
       'The fillable edition contains editable text boxes. Open it in a PDF reader that supports forms and save a new copy when you have finished. You can also print the pages and write by hand.',
       'Your writing belongs to you. No entries are submitted to the Fellowship. Do not include other people\'s private details without permission.']
    y=h-158
    for item in p:y=line_text(c,item,x,y,w-98,'BookSans',9.2,15,INK)-17
    c.setFillColor(BLUE);c.setFont('BookSansBold',8);c.drawString(x,y-5,'THREE RETURNING PRACTICES')
    y-=31
    for num,name,desc in [('01','The Reflection of Chance','For a moment, a day or a difficult question.'),('02','The Act of Possibility','For an offer of care within your means.'),('03','A Week of Possibilities','For a longer view of the days behind you.')]:
        c.setFillColor(BLUE);c.setFont('BookSerifItalic',17);c.drawString(x,y,num)
        c.setFillColor(INK);c.setFont('BookSerif',13.5);c.drawString(x+44,y,name)
        c.setFillColor(MUTED);c.setFont('BookSans',8.4);c.drawString(x+44,y-18,desc)
        y-=62
    c.showPage()

def divider(c,w,h,tag,title,desc,page_num):
    pageframe(c,w,h,tag,page_num);x=49
    c.setFillColor(BLUE);c.setFont('BookSansBold',8.5);c.drawString(x,h-102,tag)
    ypos=h-163
    for t in title.split('\n'):
        c.setFillColor(INK);c.setFont('BookSerif',31);c.drawString(x,ypos,t);ypos-=38
    c.setStrokeColor(BLUE);c.setLineWidth(1.6);c.line(x,ypos,x+69,ypos)
    line_text(c,desc,x,ypos-31,w-98,'BookSerifItalic',12,18,INK)
    lines_logo(c,w*.65,h*.31,125)
    c.showPage()

def journal_practice_pages(c,w,h,key,roundnum,page_num,print_edition=False):
    title,tag,subtitle,qs=PRACTICES[key]
    for half,subset in enumerate((qs[:3],qs[3:]),1):
        pageframe(c,w,h,title,page_num);page_num+=1;x=49
        c.setFillColor(BLUE);c.setFont('BookSansBold',8.0)
        c.drawString(x,h-84,f'ENTRY {roundnum:02d}  /  PART {half} OF 2')
        c.setFillColor(INK);c.setFont('BookSerif',21)
        c.drawString(x,h-112,title)
        c.setFont('BookSans',7.7);c.setFillColor(MUTED)
        c.drawString(x,h-137,'DATE (OPTIONAL)')
        field(c,f'{key}_{roundnum:02d}_date_{half}',x+109,h-145,w-2*x-109,19,print_edition)
        t=h-169
        for i,(q,hint) in enumerate(subset,start=(1 if half==1 else 4)):
            box=79 if half==1 else 127
            t=question(c,i,q,hint,x,t,w-2*x,box,f'{key}_{roundnum:02d}_q{i}',print_edition,fontsize=11.0)
        c.showPage()
    return page_num

def journal(path,print_edition=False):
    w,h=432,648 # 6x9 inches, a plausible future paperback interior trim size
    c=canvas.Canvas(str(path),pagesize=(w,h),pageCompression=1)
    c.setTitle(('Print layout proof' if print_edition else 'Fillable edition')+' — The Reflection Journal | The Book of Chance')
    c.setAuthor('H · The Book of Chance')
    cover(c,w,h,'REFLECTION PRACTICES','The Reflection\nJournal','Three practices for chance, choice, and the lives we share.', 'PRINT LAYOUT PROOF · NOT A PRINT-READY MASTER' if print_edition else 'FREE DIGITAL EDITION · FILLABLE PDF')
    intro_journal(c,w,h)
    page=3
    for key,rounds,tag,title,desc in [
        ('chance',4,'PART I · NOTICE','The Reflection\nof Chance','Observe your circumstances, your choices, and the next possibilities without demanding certainty.'),
        ('action',3,'PART II · OFFER','The Act of\nPossibility','Support others voluntarily, with consent, respect, and no expectation of repayment.'),
        ('week',4,'PART III · RETURN','A Week of\nPossibilities','Look back on what surprised you, what others contributed, and what you can carry forward.')]:
        divider(c,w,h,tag,title,desc,page);page+=1
        for i in range(1,rounds+1):
            page=journal_practice_pages(c,w,h,key,i,page,print_edition)
    pageframe(c,w,h,'CLOSING REFLECTION',page)
    x=49
    c.setFillColor(BLUE);c.setFont('BookSansBold',8);c.drawString(x,h-85,'NO FINISH LINE')
    c.setFillColor(INK);c.setFont('BookSerif',25);c.drawString(x,h-121,'What might be possible?')
    y=line_text(c,'You may return to any question, cross out an answer, or begin a new notebook. Reflection is a practice, not a verdict.',x,h-146,w-98,'BookSans',9.1,15,INK)
    field(c,'closing_reflection',x,120,w-98,248,print_edition)
    c.setFillColor(MUTED);c.setFont('BookSans',8);c.drawString(x,79,'Free digital edition · The Book of Chance · by H')
    c.save()

if __name__=='__main__':
    for k,filename in [('chance','The_Reflection_of_Chance_Fillable.pdf'),('action','The_Act_of_Possibility_Fillable.pdf'),('week','A_Week_of_Possibilities_Fillable.pdf')]:
        single_worksheet(OUT/filename,k)
    # Journal series v0.9 is built by the separate, publication-specific script.
    from build_journal_series import core, daily, possibility, preview
    core(OUT/'The_Reflection_Journal_Fillable.pdf')
    core(OUT/'The_Reflection_Journal_Dark_Fillable.pdf',dark=True)
    daily(OUT/'The_Daily_Reflection_Journal_Fillable.pdf')
    possibility(OUT/'The_Possibility_Journal_Fillable.pdf')
    core(OUT/'The_Reflection_Journal_Print_Layout_Proof.pdf',print_proof=True)
    for file,name in [('The_Reflection_Journal_Fillable.pdf','reflection-light'),('The_Reflection_Journal_Dark_Fillable.pdf','reflection-dark'),('The_Daily_Reflection_Journal_Fillable.pdf','daily'),('The_Possibility_Journal_Fillable.pdf','possibility')]:preview(OUT/file,name)
    for p in OUT.glob('*.pdf'):
        print(p.name, f'{p.stat().st_size/1024:.1f} KiB')
