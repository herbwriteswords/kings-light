from PIL import Image, ImageDraw, ImageFont
import math, random
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets','sprites')+'/'
PAL={'.':(0,0,0,0),'o':(22,16,22),'1':(38,38,52),'2':(62,62,80),'3':(96,96,114),
'g':(246,196,68),'G':(255,246,190),'y':(190,124,40),'w':(92,58,32),'W':(152,102,54),
'm':(120,150,156),'M':(206,224,218),'k':(140,156,112),'K':(86,100,70),'c':(52,108,60),'s':(176,186,200)}
NOOUT=set('gG')  # glow pixels don't get outlined
class Spr:
    def __init__(s,w,h): s.w,s.h=w,h; s.p=[['.']*w for _ in range(h)]
    def set(s,x,y,c):
        x,y=int(round(x)),int(round(y))
        if 0<=x<s.w and 0<=y<s.h: s.p[y][x]=c
    def get(s,x,y): return s.p[y][x] if 0<=x<s.w and 0<=y<s.h else '.'
    def circ(s,cx,cy,r,c,ry=None):
        ry=ry or r
        for y in range(s.h):
            for x in range(s.w):
                if ((x-cx)/r)**2+((y-cy)/ry)**2<=1: s.p[y][x]=c
    def rect(s,x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1): s.set(x,y,c)
    def line(s,x0,y0,x1,y1,c):
        n=max(abs(x1-x0),abs(y1-y0),1)
        for i in range(n+1): s.set(x0+(x1-x0)*i/n,y0+(y1-y0)*i/n,c)
    def rows(s,rows,x0,y0):
        for y,r in enumerate(rows):
            for x,ch in enumerate(r):
                if ch!='.': s.set(x0+x,y0+y,ch)
    def outline(s):
        add=[]
        for y in range(s.h):
            for x in range(s.w):
                if s.p[y][x]=='.' and any(s.get(x+dx,y+dy) not in '.o' and s.get(x+dx,y+dy) not in NOOUT for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): add.append((x,y))
        for x,y in add: s.p[y][x]='o'
        return s
    def img(s):
        im=Image.new('RGBA',(s.w,s.h)); px=im.load()
        for y in range(s.h):
            for x in range(s.w): px[x,y]=PAL[s.p[y][x]]
        return im
F={}
# --- lightning bug 8x8, 3 frames
for i,r in enumerate([1.2,2.2,3.3]):
    s=Spr(8,8)
    for y in range(8):
        for x in range(8):
            d=math.hypot(x-3.5,y-3.5)
            if d<r and (d<r-1.2 or (x+y)%2==0): s.p[y][x]='g'
    s.rect(3,3,4,4,'G' if i else 'g')
    if i==2: s.set(2,3,'G'); s.set(5,4,'G'); s.set(3,5,'G'); s.set(4,2,'G')
    s.set(3,2,'w'); s.set(4,2,'w')
    F['bug%d'%i]=s.img()
# --- fog creature 48x32
def fog(t,blink=False):
    s=Spr(48,32)
    blobs=[(12,18,9),(24,13,11),(36,18,9),(18,22,8),(30,22,8),(6,23,5),(42,23,5)]
    for j,(x,y,r) in enumerate(blobs):
        ox=math.sin(t*2.1+j)*1.0; oy=math.cos(t*2.1+j*1.7)*1.0
        s.circ(x+ox,y+oy,r,'1')
    for y in range(32):
        for x in range(48):
            if s.p[y][x]=='1':
                above=s.get(x,y-2)=='.' or s.get(x-2,y-2)=='.'
                if s.get(x,y-1)=='.' or s.get(x-1,y-1)=='.' : s.p[y][x]='3'
                elif above: s.p[y][x]='2'
                elif y<20 and (x+y)%3==0: s.p[y][x]='2'
    # wispy bottom: dither
    for y in range(27,32):
        for x in range(48):
            if s.p[y][x]!='.' and (x+y+t)%2: s.p[y][x]='.'
    if blink:
        s.line(16,15,21,16,'y'); s.line(27,16,32,15,'y')
    else:
        s.rows(["o....","ggo..","gGGgo",".ggg."],16,13)
        s.rows(["....o","..ogg","ogGGg",".ggg."],28,13)
    s.line(20,22,23,21,'o'); s.line(24,21,28,22,'o'); s.set(19,23,'o'); s.set(29,23,'o')
    s.outline()
    for y in range(26,32):
        for x in range(48):
            if s.p[y][x]=='o': s.p[y][x]='.'
    return s.img()
for i in range(3): F['fog%d'%i]=fog(i)
F['fog_blink']=fog(0,True)
# --- mirror 32x48
def mirror(stage):
    s=Spr(32,48)
    s.circ(16,8,12,'W',7); s.rect(4,8,27,45,'W')
    s.circ(16,9,9,'w',4); s.rect(7,9,24,42,'w')
    if stage<2:
        s.circ(16,10,8,'m',3.5); s.rect(8,10,23,41,'m')
        for k in range(0,36,9):
            for i in range(11):
                x,y=int(9+k//3+i*0.5),int(40-k-i)
                if s.get(x,y)=='m': s.set(x,y,'M')
        cr=[(16,22,9,12),(16,22,23,15),(16,22,12,38),(16,22,21,36),(16,22,8,26)]
        if stage==1: cr+= [(16,22,20,9),(16,22,23,28),(12,38,8,41),(9,12,10,20)]
        for a in cr: s.line(*a,'o')
        if stage==1:
            s.circ(16,22,3,'G'); s.set(16,22,'G')
    elif stage==2:
        s.rect(8,10,23,41,'1')
        for x,y in [(10,30),(20,14),(14,38),(22,26),(12,18)]: s.rows(["Mm","mM"],x,y)
    else:
        s.rect(8,10,23,41,'1')
        s.rows(["Mm.","mmM"],9,37); s.rows([".M","Mm"],20,38)
    # ornaments
    s.rows(["..y..",".yWy.","yWgWy",".yWy.","..y.."],14,1)
    for x,y in [(5,12),(26,12),(5,44),(26,44)]: s.set(x,y,'y')
    s.rect(4,45,27,46,'w')
    s.outline()
    im=s.img()
    if stage==2:
        pass
    return im
for i in range(4): F['mirror%d'%i]=mirror(i)
# shards flying overlay for stage 2 (outside frame)
d=F['mirror2'].load()
for x,y in [(1,8),(30,16),(2,30),(29,36),(15,0)]:
    d[x,y]=PAL['M']; 
    if y+1<48: d[x,y+1]=PAL['m']
# --- mirrorbeast 32x32
def beast(t,hurt=False):
    s=Spr(32,32); b=t
    s.circ(16,14+b,10,'c',9)                       # hood
    s.rect(7,16+b,25,30,'c'); s.circ(16,30,10,'c',3)
    s.circ(16,15+b,7,'k',6)                       # face
    s.rows(["k...","kk..","kkk.",".kkk"],4,9+b); s.rows(["...k","..kk",".kkk","kkk."],24,9+b)  # ears
    for ex in (12,20):
        s.circ(ex,14+b,2.6,'M'); s.set(ex,14+b,'o'); s.set(ex+1,14+b,'o' if not hurt else 'M')
    s.line(9,11+b,13,10+b,'K'); s.line(19,10+b,23,11+b,'K')  # brows
    s.rect(13,19+b,19,20+b,'o'); s.set(14,21+b,'M'); s.set(18,21+b,'M'); s.set(14,19+b,'M'); s.set(18,19+b,'M')
    s.rect(9,7+b,23,8+b,'K')  # hood shadow on face top
    s.circ(16,8+b,8,'c',3)
    for y in range(32):
        for x in range(32):
            if s.p[y][x]=='c' and x>20 and (x+y)%2: s.p[y][x]='K' if False else 'c'
            if s.p[y][x]=='c' and x>21: s.p[y][x]='1'
    cx=1-t
    for hx in (6+cx,23-cx):  # claws
        s.rect(hx,22,hx+3,24,'k'); 
        for k in range(4): s.set(hx+k,25+(k%2),'M')
    s.outline()
    if hurt:
        for y in range(32):
            for x in range(32):
                if s.p[y][x] in 'kcK1': s.p[y][x]='M' if (x+y)%2 else 'G'
    return s.img()
F['beast0']=beast(0); F['beast1']=beast(1); F['beast_hurt']=beast(0,True)
# --- sword 16x16
def sword(glow):
    s=Spr(16,16)
    for i in range(9): s.set(5+i,10-i,'s'); s.set(6+i,10-i,'M'); s.set(5+i,9-i,'s')
    s.line(2,9,6,13,'y'); s.set(4,11,'g')
    s.line(3,12,1,14,'w'); s.set(2,13,'W'); s.set(0,15,'g')
    s.outline()
    if glow:
        for y in range(16):
            for x in range(16):
                if s.p[y][x]=='.' and x+y>=12 and x>=4 and any(s.get(x+a,y+b)=='o' for a,b in((1,0),(-1,0),(0,1),(0,-1))): s.p[y][x]='g'
        for i in range(0,9,2): s.set(6+i,10-i,'G')
    return s.img()
F['sword']=sword(0); F['sword_glow']=sword(1)
# --- placeholders
s=Spr(16,16); s.circ(8,9,5,'W',4); s.circ(11,6,3,'W'); s.set(14,6,'y'); s.set(11,5,'o'); s.circ(6,10,3,'w',2); s.line(3,12,1,14,'w'); s.outline(); F['bird_ph']=s.img()
s=Spr(32,32); s.circ(15,18,9,'W',5); s.circ(24,10,4,'W',3); s.rect(23,12,25,16,'W')
for x in (9,12,18,21): s.rect(x,22,x,29,'w')
s.line(23,7,21,2,'w'); s.line(26,7,28,2,'w'); s.set(25,10,'o'); s.circ(15,19,6,'y',2); s.outline(); F['deer_ph']=s.img()
BF=[["mm.o.mm.","mMmwmMm.","mmmwmmm.",".MmwmM..",".MMwMM..","...w...."],
    ["..mmo...","..mMw...","..mmw...","..Mmw...","..MMw...","...w...."]]
for i in range(2):
    s=Spr(8,8); s.rows(BF[i],0,1); s.outline(); F['bfly%d'%i]=s.img()

def h(x,y,t=0): return ((x*73856093)^(y*19349663)^(t*83492791))%97/97.0
# ---- v2 fog: noise shading, creeping ground tendrils
def fog2(t,blink=False):
    s=Spr(48,32)
    blobs=[(14,15,9,8),(25,11,10,8),(35,15,8,7),(24,19,15,6),(10,22,9,4),(38,22,9,4)]
    for j,(x,y,rx,ry) in enumerate(blobs):
        s.circ(x+math.sin(t*2.1+j)*1.2,y+math.cos(t*2.1+j*1.7),rx,'1',ry)
    for x in range(48):   # ground tendrils
        top=24+int(2*math.sin(x/4+t*1.3))
        for y in range(top,30):
            if h(x,y,t)<0.75-(y-top)*0.15 and 2<x<46: s.p[y][x]='1'
    for y in range(32):
        for x in range(48):
            if s.p[y][x]!='1': continue
            e1=s.get(x,y-1)=='.' or s.get(x-1,y)=='.'; e2=s.get(x,y-2)=='.' or s.get(x-2,y-1)=='.'
            n=h(x,y,t)
            if e1 and y<24: s.p[y][x]='3'
            elif (e2 and y<24) or (y<16 and n<0.25): s.p[y][x]='2'
            elif y>=24 and n<0.3: s.p[y][x]='2'
    if blink:
        s.line(16,15,21,16,'y'); s.line(27,16,32,15,'y')
    else:
        s.rows(["o....","ggo..","gGGgo",".ggg."],16,13)
        s.rows(["....o","..ogg","ogGGg",".ggg."],28,13)
    s.line(20,22,23,21,'o'); s.line(24,21,28,22,'o'); s.set(19,23,'o'); s.set(29,23,'o')
    s.outline()
    for y in range(22,32):
        for x in range(48):
            if s.p[y][x]=='o': s.p[y][x]='.'
    return s.img()
for i in range(3): F['fog%d'%i]=fog2(i)
F['fog_blink']=fog2(0,True)
# ---- v2 mirror shards: bigger triangles
def shard(s,x,y,flip=0):
    rows=["M...","Mm..","Mmm.","mmmm"] if not flip else ["mmmM",".mmM","..mM","...M"]
    s.rows(rows,x,y)
def mirror2(stage):
    s=Spr(32,48)
    s.circ(16,8,12,'W',7); s.rect(4,8,27,45,'W'); s.circ(16,9,9,'w',4); s.rect(7,9,24,42,'w')
    s.circ(16,10,8,'1',3.5); s.rect(8,10,23,41,'1')
    if stage==2:
        for i,(x,y) in enumerate([(9,13),(18,18),(11,27),(19,33),(13,36)]): shard(s,x,y,i%2)
    else:
        for x,y in [(9,38),(20,39)]: shard(s,x,y,x>15)
    s.rows(["..y..",".yWy.","yWgWy",".yWy.","..y.."],14,1)
    for x,y in [(5,12),(26,12),(5,44),(26,44)]: s.set(x,y,'y')
    s.rect(4,45,27,46,'w'); s.outline(); return s.img()
F['mirror2']=mirror2(2); F['mirror3']=mirror2(3)
big=Image.new('RGBA',(48,56)); big.alpha_composite(F['mirror2'],(8,4))
sp=Spr(48,56)
for i,(x,y) in enumerate([(0,6),(42,14),(1,34),(43,40),(22,0)]): shard(sp,x,y,i%2)
sp.outline(); big.alpha_composite(sp.img()); F['mirror2']=big
for k in ('mirror0','mirror1','mirror3'):
    c=Image.new('RGBA',(48,56)); c.alpha_composite(F[k],(8,4)); F[k]=c
# ---- v2 mirrorbeast: twisted Dalton
def beast2(t,hurt=False):
    s=Spr(32,32); b=t
    s.circ(16,13+b,11,'c',10); s.circ(16,27,13,'c',6); s.rect(4,20,27,31,'c')
    s.rows(["k..","kk.",".kk"],2,12+b); s.rows(["..k",".kk","kk."],27,12+b)   # ears out of hood
    s.circ(16,15+b,8,'1',7)                     # hood opening
    s.circ(16,16+b,6.5,'k',6)                   # face
    for x in range(10,23):                      # hair fringe (Dalton's)
        s.set(x,10+b+(x%3==0),'W');
        if x%2: s.set(x,11+b,'w')
    s.set(9,12+b,'w'); s.set(23,12+b,'w')
    for ex in (13,19):
        s.circ(ex,15+b,2.4,'M'); s.set(ex,15+b,'o'); s.set(ex,16+b,'o')
    s.line(10,13+b,14,12+b,'K'); s.line(18,12+b,22,13+b,'K')  # brows angled (twisted)
    s.rect(14,19+b,18,21+b,'o'); s.set(14,19+b,'M'); s.set(18,19+b,'M'); s.set(15,21+b,'M'); s.set(17,21+b,'M')
    s.set(12,19+b,'K'); s.set(20,19+b,'K')
    for y in range(32):
        for x in range(32):
            if s.p[y][x]=='c' and x-0.25*y>18: s.p[y][x]='K'
            elif s.p[y][x]=='c' and x+0.2*y<9: s.p[y][x]='c'
    cx=1-t
    for hx in (8+cx,20-cx):
        s.rect(hx,24,hx+3,26,'k')
        for k in range(4): s.set(hx+k,27+(k%2),'M')
    s.outline()
    if hurt:
        for y in range(32):
            for x in range(32):
                if s.p[y][x] in 'kcK1Ww': s.p[y][x]='M' if (x+y)%2 else 'G'
    return s.img()
F['beast0']=beast2(0); F['beast1']=beast2(1); F['beast_hurt']=beast2(0,True)
# ---- v2 sword glow: clean
def sword2(glow):
    s=Spr(16,16)
    for i in range(9):
        s.set(5+i,10-i,'s'); s.set(6+i,10-i,'G' if glow else 'M'); s.set(5+i,9-i,'M' if glow else 's')
    s.line(2,9,6,13,'y'); s.set(4,11,'g'); s.line(3,12,1,14,'w'); s.set(2,13,'W'); s.set(0,15,'g')
    s.outline()
    if glow:
        for x,y in [(15,0),(14,0),(15,1),(11,1),(9,3),(4,10)]: 
            if s.get(x,y) in '.o': s.set(x,y,'G' if (x+y)%2 else 'g')
    return s.img()
F['sword']=sword2(0); F['sword_glow']=sword2(1)
# ---- sword in grass 16x32
def sword_grass(glow):
    s=Spr(16,32)
    s.rect(7,10,8,26,'s'); s.set(8 if not glow else 7,12,'M')
    for y in range(11,26,2): s.set(8,y,'G' if glow else 'M')
    s.rect(4,8,11,9,'y'); s.set(7,8,'g'); s.rect(7,3,8,7,'w'); s.set(7,4,'W'); s.rect(6,1,9,2,'g'); s.set(7,1,'G')
    for x in range(1,15):
        ht=4+int(h(x,3)*6)
        for y in range(31-ht,31): s.set(x+(1 if y<31-ht+2 and x%2 else 0),y,'c' if (x+y)%3 else 'K')
    s.outline()
    if glow:
        for x,y in [(4,1),(11,2),(3,6),(12,7),(5,12),(10,14)]: s.set(x,y,'g' if (x+y)%2 else 'G')
    return s.img()
F['sword_grass']=sword_grass(0); F['sword_grass_glow']=sword_grass(1)
# ---- bird 16x16 (songbird on branch), 2 frames (sing)
def bird(sing):
    s=Spr(16,16)
    s.circ(7,8,4.5,'W',3.5); s.circ(10,5,3,'W',2.6); s.circ(7,9,3,'y',2)  # body, head, warm breast
    s.line(2,9,0,12,'w'); s.line(3,10,1,12,'w')       # tail
    s.circ(6,7,3,'w',1.5)                            # wing
    s.set(11,4,'o')
    if sing: s.set(13,4,'y'); s.set(13,6,'y'); s.set(12,5,'.')
    else: s.set(13,5,'y'); s.set(14,5,'y')
    s.set(6,12,'w'); s.set(9,12,'w')
    s.line(0,13,15,13,'w'); s.line(0,14,15,14,'W'); s.set(13,12,'c'); s.set(14,12,'c'); s.set(2,12,'c')
    s.outline()
    if sing: s.set(15,2,'g'); s.set(14,1,'g')
    return s.img()
F['bird0']=bird(0); F['bird1']=bird(1)
# ---- young doe 32x32, 2 frames (ear flick)
def doe(f):
    s=Spr(32,32)
    s.circ(13,17,8,'W',4.5)                        # body
    s.rect(19,9,22,17,'W')                         # neck
    s.circ(22,8,3.5,'W',3); s.circ(25,9,2.5,'W',1.8)  # head, muzzle
    s.set(27,9,'o'); s.set(22,7,'o')
    s.rows(["WW..","yWWW","..WW"],15,3-f); s.rows(["..WW","WWWy","WW.."],24,3)  # big doe ears
    for x,dx in [(7,0),(10,1),(16,0),(19,-1)]:
        for y in range(21,30): s.set(x+(dx if y>25 else 0),y,'W')
        s.set(x+dx,29,'o')
    s.circ(13,20,5,'y',1.5)                        # pale belly
    s.circ(11,15,5,'w',1.5) if False else None
    for y in range(13,22):
        for x in range(5,22):
            if s.get(x,y)=='W' and y<15 and x<18: s.p[y][x]='W'
    for (x,y) in [(9,15),(12,14),(15,15),(11,17)]: s.set(x,y,'y')   # fawn spots
    s.set(5,14,'y'); s.set(4,13,'W')               # tail
    s.outline(); return s.img()
F['doe0']=doe(0); F['doe1']=doe(1)
# ---- gold butterfly 8x8, 2 frames
BF2=[[".gg..gg.","gGgogGg.","gggoggg.",".gyoyg..",".yy.yy..","...o...."],
     ["..gogg..","..gGGg..","..ggog..","..yyo...","..yy....","...o...."]]
for i in range(2):
    s=Spr(8,8); s.rows(BF2[i],0,1); F['bfly%d'%i]=s.img()
for k in ['bird_ph','deer_ph']: F.pop(k,None)
# sheet + preview
names=list(F)
colors=set()
for im in F.values():
    for c in im.get_flattened_data():
        if c[3]: colors.add(c)
assert len(colors)<=15,len(colors)
S=8; cellw=52; cellh=62
cols=6
pv=Image.new('RGB',(cols*cellw*S,((len(names)+cols-1)//cols)*cellh*S),(18,22,34))
d=ImageDraw.Draw(pv)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
for i,n in enumerate(names):
    im=F[n].resize((F[n].width*S,F[n].height*S),Image.NEAREST)
    x=(i%cols)*cellw*S+S; y=(i//cols)*cellh*S+S
    pv.paste(im,(x,y),im); d.text((x,y+57*S),n,fill=(240,230,200),font=font)
pv.save(OUT+'creatures_preview.png')
# anim gif
seqs=[['bug0','bug1','bug2','bug1'],['bird0','bird1','bird0','bird1'],['doe0','doe0','doe1','doe0'],['bfly0','bfly1','bfly0','bfly1'],['sword_grass','sword_grass_glow','sword_grass','sword_grass_glow'],['fog0','fog1','fog2','fog_blink'],['mirror0','mirror1','mirror2','mirror3'],['beast0','beast1','beast0','beast_hurt'],['sword','sword_glow','sword','sword_glow']]
fr=[]
for k in range(4):
    g=Image.new('RGB',((len(seqs))*50*4,58*4),(18,22,34))
    for j,sq in enumerate(seqs):
        im=F[sq[k]]; im=im.resize((im.width*4,im.height*4),Image.NEAREST); g.paste(im,(j*200+4,4),im)
    fr.append(g.convert('P',palette=Image.ADAPTIVE))
fr[0].save(OUT+'creatures_anim.gif',save_all=True,append_images=fr[1:],duration=280,loop=0)

def glow(m,cx,cy,R,col=(255,206,110),strength=0.55,dark=0.0):
    p=m.load()
    for y in range(m.height):
        for x in range(m.width):
            r,g_,b_=p[x,y][:3]
            if dark: r,g_,b_=r*(1-dark),g_*(1-dark),b_*(1-dark*0.6)
            dd=math.hypot(x-cx,y-cy)/R; a=max(0,1-dd)**2*strength
            p[x,y]=(int(r+(col[0]-r)*a),int(g_+(col[1]-g_)*a),int(b_+(col[2]-b_)*a),255)
# soaked palette swap for Dalton
dsheet=Image.open(OUT+'dalton.png').convert('RGBA'); px=dsheet.load()
for y in range(dsheet.height):
    for x in range(dsheet.width):
        r,g_,b_,a=px[x,y]
        if a and (r,g_,b_) not in [(246,196,68),(255,243,176),(255,246,190)] and r+g_+b_<700:
            px[x,y]=(int(r*0.72),int(g_*0.76),int(b_*0.86+12),a)
dsheet.save(OUT+'dalton_soaked.png')
# night fog mockup
random.seed(5); m=Image.new('RGB',(240,160),(24,44,34)); p=m.load()
for _ in range(2500):
    x,y=random.randrange(240),random.randrange(160); p[x,y]=random.choice([(30,54,40),(20,36,30)])
dd=ImageDraw.Draw(m)
for y in range(160):
    for x in range(100,140):
        if abs(x-120-int(6*math.sin(y/25)))<12: p[x,y]=random.choice([(70,58,44),(62,50,40)])
for tx,ty in [(30,30),(200,30),(40,120),(205,115),(70,70),(175,80)]:
    dd.ellipse([tx-18,ty-18,tx+18,ty+12],fill=(14,32,24)); dd.rectangle([tx-2,ty+10,tx+2,ty+22],fill=(36,26,20))
m=m.convert('RGBA'); dal=Image.open(OUT+'dalton.png').crop((16,0,32,32))
dx,dy=112,104; lx,ly=dx+2,dy+24
glow(m,lx,ly,48)
m.alpha_composite(F['fog0'],(96,46)); m.alpha_composite(dal,(dx,dy))
for x,y,i in [(150,70,2),(160,84,1),(80,90,2),(140,96,0),(66,60,1)]: m.alpha_composite(F['bug%d'%i],(x,y))
m.convert('RGB').resize((960,640),Image.NEAREST).save(OUT+'creatures_mockup.png')
print(len(colors),'colors')

# page 9 dusk path mockup
random.seed(9); m=Image.new('RGB',(240,160),(44,74,60)); p=m.load()
for _ in range(3000):
    x,y=random.randrange(240),random.randrange(160); p[x,y]=random.choice([(52,86,66),(36,62,50)])
for y in range(160):
    for x in range(80,170):
        if abs(x-125-int(14*math.sin(y/30)))<14+y//16: p[x,y]=random.choice([(104,88,64),(94,78,58)])
dd=ImageDraw.Draw(m)
for tx,ty in [(20,20),(222,24),(30,130),(214,128)]:
    dd.ellipse([tx-22,ty-20,tx+22,ty+14],fill=(26,52,42)); dd.rectangle([tx-2,ty+12,tx+2,ty+26],fill=(56,38,26))
dd.line([(10,46),(70,40)],fill=(70,48,30),width=3)
m=m.convert('RGBA')
glow(m,0,0,1,strength=0,dark=0.25)
dal=Image.open(OUT+'dalton.png').crop((16,32,32,64))
dx,dy=118,96
glow(m,dx+13,dy+24,44)
m.alpha_composite(F['bird1'],(36,27)); m.alpha_composite(F['doe0'],(176,62))
m.alpha_composite(F['bfly0'],(160,112)); m.alpha_composite(dal,(dx,dy))
m.convert('RGB').resize((960,640),Image.NEAREST).save(OUT+'path_mockup.png')
