#!/usr/bin/env python3
"""The Book of Chance: reproducible companion journal series, v0.9.
Three different journaling experiences; four cover/edition files plus a
printer-oriented manuscript proof. All releases are free digital PDFs.
This tool only touches files/reflection and assets/journals.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.lib.pagesizes import A4
import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'files/reflection';OUT.mkdir(parents=True,exist_ok=True)
IMAGES=ROOT/'assets/journals';IMAGES.mkdir(parents=True,exist_ok=True)
W,H=432,648
INK=HexColor('#202b34'); BLUE=HexColor('#1b70cf'); FAINT=HexColor('#d8dde0'); GREY=HexColor('#6d7680'); IVORY=HexColor('#fffefd'); SOFT=HexColor('#f5f8fa'); NIGHT=HexColor('#101317')
FONTDIR=Path('/usr/share/fonts/truetype/liberation')
for fn,real in [('S','LiberationSerif-Regular.ttf'),('SB','LiberationSerif-Bold.ttf'),('SI','LiberationSerif-Italic.ttf'),('N','LiberationSans-Regular.ttf'),('NB','LiberationSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(fn,str(FONTDIR/real)))

PRACTICES={
'chance':('THE REFLECTION OF CHANCE','Notice what happened without making uncertainty a verdict.',[
 ('What happened?','A moment worth noticing, ordinary or extraordinary.'),
 ('What was not mine to choose?','Circumstances, timing, limits, or other people.'),
 ('Where did a choice remain?','A response I made, or a choice still open.'),
 ('What can I understand differently?','Perhaps a pattern, a kindness, or something I do not know.'),
 ('What could be possible now?','A gentle next step; sometimes rest is enough.')]),
'action':('THE ACT OF POSSIBILITY','Consider an offer of help that respects autonomy.',[
 ('Whose possibilities might I widen?','Begin with what they have said they need, not assumptions.'),
 ('What can I offer freely?','Attention, a skill, an introduction, time, or something else.'),
 ('What boundaries matter?','Consent, privacy, capacity, and their right to say no.'),
 ('What is a small, realistic step?','An offer, not a promise to control the result.'),
 ('What did I notice afterward?','Return later, if you wish, without keeping score.')]),
'week':('A WEEK OF POSSIBILITIES','Take the longer view, without grading your week.',[
 ('What surprised me?','An encounter, change, delay, discovery or quiet moment.'),
 ('What shaped my circumstances?','What helped, constrained or complicated the week?'),
 ('Where did I exercise choice?','Including restraint, rest, and asking for help.'),
 ('Who affected my path?','Care, cooperation, kindness or friction.'),
 ('What is worth carrying forward?','An intention, a question, an appreciation.')]),
'annual':('THE TURNING OF CHANCE','Return to a longer view of a changing life.',[
 ('What changed around me?','Circumstances, relationships, opportunities, and losses.'),
 ('What did I learn about my choices?','Consider the information and means I actually had.'),
 ('Who shared this part of my story?','The support I received and offered, without measuring worth.'),
 ('What can I release?','A rigid expectation, an unhelpful judgment, a burden.'),
 ('Where might I make room next?','An open possibility, not a demand or prediction.')]),
'follow':('AFTER THE ACT','Look back on a choice without evaluating a person.',[
 ('What did I offer?','Keep other people anonymous or ask permission to name them.'),
 ('What did the other person choose?','Their response belonged to them, including declining.'),
 ('What was beyond my control?','An outcome is not a moral score.'),
 ('What did I notice or learn?','About care, capacity, assumptions and boundaries.'),
 ('What, if anything, would I change?','A next invitation or simply a different understanding.')]),
'weekdaily':('A WEEK IN VIEW','Look for patterns in ordinary days.',[
 ('What changed in my circumstances?','Conditions that made some things easier or harder.'),
 ('When was I gentle with myself?','A pause, a boundary, or accepting uncertainty.'),
 ('What gave me something to appreciate?','A moment need not be productive to matter.'),
 ('Who helped shape my days?','The people and relationships around me.'),
 ('What question do I want to carry?','No answer is required today.')])
}


def fill(c,col):c.setFillColor(col)
def stroke(c,col):c.setStrokeColor(col)
def txt(c,x,y,s,font='N',size=9,color=INK):
    fill(c,color);c.setFont(font,size);c.drawString(x,y,s)
def wrap(c,x,y,text,width,font='N',size=9,lead=14,color=INK):
    arr=simpleSplit(text,font,size,width)
    for i,s in enumerate(arr):txt(c,x,y-i*lead,s,font,size,color)
    return y-len(arr)*lead

def thread_art(c,x,y,w,h,dark=False,variant='confluence'):
    """Vector sweeps derived from the intersecting paths language of the book cover."""
    c.saveState()
    schemes = [HexColor('#a1aab1'), HexColor('#30383e'), BLUE, HexColor('#c4cbd2'), HexColor('#48535b'), HexColor('#cdd4d9')]
    if dark: schemes=[HexColor('#697178'), HexColor('#e1e8eb'), BLUE, HexColor('#46525b'), HexColor('#bfcad2'),HexColor('#384550')]
    c.setLineWidth(.8)
    for i,clr in enumerate(schemes):
        p=c.beginPath(); bend=i*7.5
        if variant=='confluence':
            p.moveTo(x-24, y+h*.68+bend*.3)
            p.curveTo(x+w*.28,y+h*.98-bend, x+w*.38,y+h*.08+bend, x+w+24,y+h*.32-bend*.12)
        elif variant=='daily':
            p.moveTo(x-24,y+h*.30+bend*.5)
            p.curveTo(x+w*.34,y+h*.02+bend,x+w*.61,y+h*.96-bend,x+w+24,y+h*.70-bend*.3)
        else:
            p.moveTo(x-24,y+h*.70+bend*.3)
            p.curveTo(x+w*.25,y+h*.06+bend,x+w*.60,y+h*.99-bend,x+w+24,y+h*.26-bend*.2)
        stroke(c,clr);c.drawPath(p)
    # Reciprocal arc gives the sense of one life crossing another.
    for i in range(4):
        c.setLineWidth(.7)
        stroke(c,[schemes[0],schemes[2],schemes[1],schemes[3]][i])
        p=c.beginPath();off=i*12
        p.moveTo(x-14,y+h*.26-off*.3)
        p.curveTo(x+w*.26,y+h*.06+off,x+w*.61,y+h*.92-off*.6,x+w+25,y+h*.76+off*.12)
        c.drawPath(p)
    c.restoreState()

class Journal:
    def __init__(self,path,title,subtitle,tag='COMPANION VOLUME',edition='Light Edition',dark=False,kind='main',print_proof=False):
        self.path=Path(path);self.title=title;self.subtitle=subtitle;self.tag=tag;self.edition=edition;self.dark=dark;self.kind=kind;self.print_proof=print_proof
        self.c=canvas.Canvas(str(self.path),pagesize=(W,H),pageCompression=1)
        self.c.setTitle(title+' | The Book of Chance')
        self.c.setAuthor('H')
        self.c.setSubject('A Book of Chance companion publication for private reflection')
        self.p=0;self.nfield=0
    def new(self,cat='JOURNAL'):
        self.p+=1;c=self.c;fill(c,IVORY);c.rect(0,0,W,H,fill=1,stroke=0)
        if self.p>1:
            stroke(c,FAINT);c.setLineWidth(.6);c.line(48,H-48,W-48,H-48)
            txt(c,48,H-37,'THE BOOK OF CHANCE','NB',7.5,INK)
            c.setFont('N',7.1);fill(c,GREY);c.drawRightString(W-48,H-37,cat.upper())
            c.line(48,43,W-48,43)
            txt(c,48,28,self.title.upper()+'  /  H','N',6.4,GREY)
            c.setFont('N',7);c.drawRightString(W-48,28,str(self.p).zfill(2))
        return c
    def end(self):self.c.showPage()
    def cover(self):
        c=self.new();dark=self.dark
        bg=NIGHT if dark else IVORY;primary=IVORY if dark else INK
        fill(c,bg);c.rect(0,0,W,H,stroke=0,fill=1)
        txt(c,52,576,'THE BOOK OF CHANCE','NB',9,primary)
        txt(c,52,559,self.tag,'N',7.6,BLUE if not dark else HexColor('#60a6ef'))
        stroke(c,BLUE);c.setLineWidth(1.2);c.line(52,541,85,541)
        # large, gracious typographic cover analogous to The Book of Chance
        title_words={'main':['The','REFLECTION','JOURNAL'],'daily':['The','DAILY','REFLECTION','JOURNAL'],'action':['The','POSSIBILITY','JOURNAL']}[self.kind]
        size1=30 if self.kind=='daily' else 35
        txt(c,52,495,'The','SI',27,primary)
        y=446
        for word in title_words[1:]:
            size=35 if len(word)>=10 else 44
            if self.kind=='daily':size=32 if len(word)>9 else 40
            txt(c,50,y,word,'S',size,primary);y-=43 if self.kind=='daily' else 54
        # motif occupies centre of cover with subtler palette like the book
        v={'main':'confluence','daily':'daily','action':'action'}[self.kind]
        thread_art(c,23,165,385,188,dark=dark,variant=v)
        # lower subtitle separates type from strands
        text_y=119
        y=wrap(c,52,text_y,self.subtitle,310,'SI',12.3,17,primary)
        stroke(c,BLUE);c.setLineWidth(1);c.line(52,77,82,77)
        txt(c,52,55,'FREE DIGITAL EDITION  ·  FILLABLE PDF' if not self.print_proof else 'PRINT INTERIOR STUDY', 'N',7.3,GREY if not dark else HexColor('#a7b0b9'))
        c.setFont('S',20);fill(c,primary);c.drawRightString(W-51,54,'H')
        self.end()
    def normal(self,category='GUIDE'):
        return self.new(category)
    def intro(self,intro,how=None):
        c=self.normal('BEFORE YOU BEGIN')
        txt(c,49,552,'A NOTE TO THE READER','NB',8.2,BLUE)
        txt(c,49,507,'A place to return to.','S',26)
        y=466
        chunks=[intro,'A page may be left blank. Pause, skip an entry, or close the journal whenever reflection stops being helpful. There is no score and no required daily practice.',
          'Your entries are stored in the PDF you save, not sent to this website. Save in a private folder; on shared or public devices, avoid sensitive details and delete downloaded or temporary copies when finished.']
        if how:chunks.append(how)
        chunks.append('Check that your PDF reader can save a short test entry. Printed pages and shared backups can also reveal private words. If reflection becomes distressing, take a break and seek support if needed.')
        for block in chunks:
            y=wrap(c,50,y,block,330,'N',10,16,INK)-25
        self.end()
    def contents(self,sections):
        c=self.normal('CONTENTS')
        txt(c,49,555,'A GUIDE TO THIS VOLUME','NB',8,BLUE)
        txt(c,49,511,'Find your own rhythm.','S',26)
        y=453
        for i,(head,desc,page) in enumerate(sections,1):
            stroke(c,FAINT);c.line(49,y+22,383,y+22)
            txt(c,50,y,f'{i:02}', 'SI',19,BLUE)
            txt(c,92,y+3,head,'S',15)
            y2=wrap(c,92,y-18,desc,259,'N',8.5,13,GREY)
            fill(c,GREY);c.setFont('N',7.5);c.drawRightString(383,y+4,str(page).zfill(2))
            y-=86
        txt(c,50,81,'You may begin anywhere. This is not a programme to complete.','SI',10.5,GREY)
        self.end()
    def note(self,kicker,heading,paras,ending=''):
        c=self.normal('A PAUSE')
        txt(c,49,551,kicker,'NB',8,BLUE)
        y=493
        for ln in heading.split('\n'):
            txt(c,49,y,ln,'S',28);y-=35
        y-=29
        for para in paras:
            y=wrap(c,50,y,para,327,'N',10,17,INK)-23
        if ending:
            stroke(c,BLUE);c.setLineWidth(1);c.line(49,160,80,160)
            wrap(c,49,131,ending,320,'SI',13,19,INK)
        thread_art(c,246,44,153,85,variant='confluence')
        self.end()
    def section(self,no,title,desc,art='confluence'):
        c=self.normal('PART '+no)
        txt(c,50,545,'PART '+no+'  /  A RETURNING PRACTICE','NB',8,BLUE)
        y=461
        for line in title.split('\n'):
            txt(c,49,y,line,'S',32);y-=39
        y-=21
        wrap(c,50,y,desc,293,'SI',12.5,20,INK)
        thread_art(c,180,81,235,205,variant=art)
        self.end()
    def _field(self,name,x,y,w,h):
        if self.print_proof:
            stroke(self.c,FAINT);self.c.setLineWidth(.65)
            yy=y+15
            while yy<y+h-2:
                self.c.line(x,yy,x+w,yy);yy+=18
            return
        self.c.acroForm.textfield(name=name,tooltip=name.replace('_',' ').strip(),x=x,y=y,width=w,height=h,
            borderStyle='solid',borderWidth=.6,borderColor=FAINT,fillColor=SOFT,textColor=INK,forceBorder=True,
            fontName='Helvetica',fontSize=10,fieldFlags='multiline')
        self.nfield+=1
    def _q(self,key,num,y,label,hint,box_h=105):
        c=self.c
        txt(c,51,y,f'{num:02}', 'NB',9,BLUE)
        title_lines=simpleSplit(label,'S',13,298)
        for i,line in enumerate(title_lines):txt(c,81,y-i*15,line,'S',13,INK)
        text_bottom=y-20-(len(title_lines)-1)*15
        wrap(c,81,text_bottom,hint,292,'N',8.4,12,GREY)
        field_y=text_bottom-box_h-18
        self._field(key,81,field_y,295,box_h)
        return field_y-19
    def entry(self,key,entryno,label=None):
        name,_,qs=PRACTICES[key]; entryname=label or {'chance':'The Reflection of Chance','action':'The Act of Possibility','week':'A Week of Possibilities','annual':'The Turning of Chance','follow':'After the Act','weekdaily':'A Week in View'}[key]
        for side,subset in ((1,qs[:3]),(2,qs[3:])):
            c=self.normal('ENTRY  /  '+name)
            txt(c,51,553,'ENTRY '+str(entryno).zfill(2)+'  /  '+str(side)+' OF 2','NB',8,BLUE)
            txt(c,50,519,entryname,'S',21)
            txt(c,50,495,'DATE OR MOMENT  ·  OPTIONAL','NB',7.1,GREY)
            if side==1:
                self._field(f'{key}_{entryno}_date',240,488,137,21)
                if entryno==1:txt(c,51,469,'SKIP ANY QUESTION  ·  PAUSE WHEN YOU WISH','N',6.8,GREY)
            else:
                stroke(c,FAINT);c.line(240,488,377,488)
            y=451
            for j,(prompt,hint) in enumerate(subset,(1 if side==1 else 4)):
                if side==1:
                    y=self._q(f'{key}_{entryno}_q{j}',j,y,prompt,hint,80)
                else:
                    y=self._q(f'{key}_{entryno}_q{j}',j,y,prompt,hint,91)
            if side==2:
                txt(c,81,149,'A SPACE FOR WHAT DOES NOT FIT THE QUESTIONS','NB',7,GREY)
                self._field(f'{key}_{entryno}_free',81,66,295,71)
            self.end()
    def open_page(self,n):
        c=self.normal('AN OPEN PAGE')
        txt(c,50,549,'YOUR OWN WORDS  /  '+str(n).zfill(2),'NB',8,BLUE)
        txt(c,49,512,'An open page.','S',25)
        wrap(c,50,481,'A question, an observation, an image, a silence. Use this space as you wish.',319,'SI',11,16,GREY)
        self._field(f'open_{n}',51,80,326,371)
        self.end()
    def closing(self):
        c=self.normal('RETURN WHEN YOU WISH')
        txt(c,49,549,'A FINAL NOTE','NB',8,BLUE)
        txt(c,49,495,'Nothing to prove.','S',29)
        txt(c,49,458,'Something to notice.','S',23)
        y=402
        for para in ['You need not finish every page or arrive at a satisfying conclusion. This journal was made to accompany your life, not to measure it.',
                     'A reflection can remain private. An act of possibility can be small. A week can be difficult and still contain moments worth keeping.',
                     'When chance brings you back to these pages, begin again wherever you are.']:
            y=wrap(c,50,y,para,327,'N',10,17,INK)-24
        thread_art(c,90,76,310,115,variant='confluence')
        txt(c,50,66,'THROUGH CHANCE, WE MEET.  THROUGH CHOICE, WE GROW.','NB',6.6,GREY)
        self.end()
    def save(self):self.c.save()


def core(path,dark=False,print_proof=False):
    j=Journal(path,'The Reflection Journal','Three practices for chance, choice, and the lives we share.',edition='Dark Edition' if dark else 'Light Edition',dark=dark,kind='main',print_proof=print_proof)
    j.cover()
    j.intro('The Reflection Journal brings three practices from The Book of Chance into everyday life: noticing circumstances, considering an act of possibility, and reflecting across a week. Each gives a different way to attend to a life already in progress.')
    j.contents([('Notice','The Reflection of Chance: begin with circumstances and choice.',5),('Offer','The Act of Possibility: a respectful offer within your means.',17),('Review','A Week of Possibilities: a longer view without a score.',27),('Return','The Turning of Chance and open pages.',38)])
    j.note('BEFORE THE FIRST ENTRY','Chance, choice,\nand kindness.',[
        'Some things happen beyond our choosing. Our responses still matter, but we should not confuse uncertainty with personal failure.',
        'The questions in this journal are invitations. You may answer one, several, or none. A peaceful ordinary moment has as much right to these pages as a difficult decision.',
        'Growth need not be measured. You may return to the same question with a different understanding, or decide that the question no longer serves you.'
    ],'What might become possible if I looked with a little more care?')
    j.section('I','The Reflection\nof Chance','Begin by noticing what shaped a moment, and what could be chosen within it.','confluence')
    for i in range(1,6):j.entry('chance',i)
    j.note('BETWEEN PRACTICES','What is already\nworth keeping?',[
       'Not every reflection has to become a plan. Some experiences matter simply because they were lived.',
       'You may name something ordinary: a warm meal, someone listening, a brief pause, or an unexpected view. Appreciation is not a demand to be grateful for hardship.'
    ],'Let a moment be enough.')
    j.section('II','The Act of\nPossibility','Consider what you can offer without taking responsibility for another person\'s choices.','action')
    for i in range(1,5):j.entry('action',i)
    j.note('BETWEEN PRACTICES','Care needs\nboundaries.',[
      'An offer has meaning because it can be accepted or declined. Giving does not create a debt of gratitude, agreement, or access.',
      'A thoughtful action may be to ask, to listen, to leave space, or to do nothing until you understand what the other person wants.'
    ],'Offer what you can. Allow the other person to choose.')
    j.section('III','A Week of\nPossibilities','Look across several days for patterns that a single moment could not reveal.','daily')
    for i in range(1,6):j.entry('week',i)
    j.section('IV','The Turning\nof Chance','An occasional longer reflection on the changes we inherit and the lives we shape.','confluence')
    for i in range(1,3):j.entry('annual',i,label='The Turning of Chance')
    j.note('BEFORE YOU CLOSE','No final\naccounting.',[
       'A year need not resolve into a lesson. Some years are endured, some are shared, and some are quieter than we expected.',
       'If you wish, use the following open pages for a thought that belongs to none of the practices. You can also leave them untouched.'
    ],'The notebook serves the life, not the other way around.')
    for i in range(1,5):j.open_page(i)
    j.closing();assert j.p==48,(j.p,path)
    j.save();return j.p,j.nfield


def daily(path):
    j=Journal(path,'The Daily Reflection Journal','A gentle practice of noticing, without judgment or a score.',tag='FOCUSED COMPANION  /  01',kind='daily')
    j.cover()
    j.intro('This focused journal gives you quiet room for the Reflection of Chance. Use it after an ordinary day, a difficult moment, or whenever a question returns. The daily rhythm is an option, not a requirement.','After a few entries, a weekly overview can help you notice a pattern without turning life into a performance review.')
    j.contents([('Begin here','Fourteen two-page reflections for any day or moment.',4),('Look back','Two gentle weekly reviews.',32),('Write freely','Open pages with no prescribed questions.',36)])
    for i in range(1,15):j.entry('chance',i)
    for i in range(1,3):j.entry('weekdaily',i,label='A Week in View')
    for i in range(1,5):j.open_page(i)
    j.closing();assert j.p==40,(j.p,path)
    j.save();return j.p,j.nfield


def possibility(path):
    j=Journal(path,'The Possibility Journal','A thoughtful record of offers, care, consent, and shared chances.',tag='FOCUSED COMPANION  /  02',kind='action')
    j.cover()
    j.intro('This focused journal is for anyone who wants to turn reflection toward others. An Act of Possibility might be an introduction, a useful skill, a conversation, or a small task offered freely. There is no expectation to act every day.','Keep the people whose lives intersect yours safe: seek consent, preserve privacy, and do not document private information without permission.')
    j.contents([('Before an offer','A short guide to consent, capacity, and dignity.',4),('Acts of possibility','Twelve guided occasions to notice or offer care.',5),('Return later','Three follow-up reflections on what unfolded.',29),('Open pages','Space for questions, notes, or ideas.',35)])
    j.note('A PRACTICE OF CARE','Not a ledger\nof good deeds.',[
      'The value of an action is not measured by how impressive it looks. It cannot purchase another person\'s gratitude, loyalty, or attention.',
      'Ask what is wanted. Stay within your means. Be ready to hear no. Never make someone\'s hardship a story you publish without permission.'
    ],'What would respectful help look like from their point of view?')
    for i in range(1,13):j.entry('action',i)
    for i in range(1,4):j.entry('follow',i,label='After the Act')
    for i in range(1,6):j.open_page(i)
    j.closing();assert j.p==40,(j.p,path)
    j.save();return j.p,j.nfield


def preview(pdf,name):
    p=fitz.open(pdf);page=p[0]
    pix=page.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False)
    from PIL import Image
    from io import BytesIO
    image=Image.open(BytesIO(pix.tobytes('png'))).convert('RGB')
    image.save(IMAGES/(name+'.webp'),'WEBP',quality=86,method=6)
    p.close()

if __name__=='__main__':
    made={}
    files={
        'The_Reflection_Journal_Fillable.pdf':lambda p:core(p),
        'The_Reflection_Journal_Dark_Fillable.pdf':lambda p:core(p,dark=True),
        'The_Daily_Reflection_Journal_Fillable.pdf':daily,
        'The_Possibility_Journal_Fillable.pdf':possibility,
        'The_Reflection_Journal_Print_Layout_Proof.pdf':lambda p:core(p,print_proof=True)
    }
    for name,fn in files.items():made[name]=fn(OUT/name)
    for file,name in [('The_Reflection_Journal_Fillable.pdf','reflection-light'),('The_Reflection_Journal_Dark_Fillable.pdf','reflection-dark'),('The_Daily_Reflection_Journal_Fillable.pdf','daily'),('The_Possibility_Journal_Fillable.pdf','possibility')]:preview(OUT/file,name)
    print('Generated',made)
