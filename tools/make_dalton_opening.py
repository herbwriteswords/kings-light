# Opening scene: no-lantern Dalton, bed, wake-up sequence. Same palette as dalton.png
import math, random
from PIL import Image, ImageDraw, ImageFont
import make_dalton as MD
PAL=MD.PAL; OUT=MD.OUT
def ed(rows,y,x,ch):
    r=list(rows[y]); r[x]=ch; rows[y]=''.join(r)
def arms(base,dirn,ph):
    r=list(base)
    if dirn in('down','up'):
        L,R=1,14
        # ph -1: left hand up/back, right hand down/forward
        for x in (L,R): ed(r,21,x,'o' if ph else r[21][x])
        if ph:
            a,b=(L,R) if ph<0 else (R,L)
            ed(r,20,a,'s'); ed(r,22,b,'s'); ed(r,21,a,'C' if a==L else 'D'); ed(r,21,b,'C' if b==L else 'D')
            ed(r,23,b,'o')
    else:  # side: hand at col4 row21; swing fwd/back
        ed(r,21,4,'c')
        hx={-1:3,0:4,1:7}[ph]; hy={-1:21,0:21,1:22}[ph]
        ed(r,hy,hx,'s')
        if hx==3: ed(r,21,2,'o'); ed(r,20,3,'o'); ed(r,22,3,'o')
    return r
def frame(upper,legs):
    im=Image.new('RGBA',(16,32)); MD.blit(im,upper,0,0); MD.blit(im,legs,0,25); return im
F={}
B={'down':MD.DOWN,'up':MD.UP,'left':MD.LEFT}
ph={'A':-1,'S':0,'B':1}
for d,base in B.items():
    for k in 'ASB':
        F[d+k]=frame(arms(base,d,ph[k]),(MD.LS if d=='left' else MD.LD)[k])
for k in 'ASB': F['right'+k]=F['left'+k].transpose(Image.FLIP_LEFT_RIGHT)
breath=list(MD.DOWN[:5])+['']+list(MD.DOWN[5:16])+list(MD.DOWN[17:])
F['idle0']=frame(MD.DOWN,MD.LD['S']); F['idle1']=frame(MD.norm(breath),MD.LD['S'])
order=[['idle0','idle1'],['downA','downS','downB'],['upA','upS','upB'],['leftA','leftS','leftB'],['rightA','rightS','rightB']]
sh=Image.new('RGBA',(48,160))
for r,row in enumerate(order):
    for c,n in enumerate(row): sh.paste(F[n],(c*16,r*32))
sh.save(OUT+'dalton_nolantern.png')
# ---------- canvas helper
class C:
    def __init__(s,w,h): s.w,s.h=w,h; s.p=[['.']*w for _ in range(h)]
    def set(s,x,y,c):
        if 0<=x<s.w and 0<=y<s.h: s.p[y][x]=c
    def get(s,x,y): return s.p[y][x] if 0<=x<s.w and 0<=y<s.h else '.'
    def rect(s,x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1): s.set(x,y,c)
    def rows(s,rows,x0,y0):
        for y,r in enumerate(rows):
            for x,ch in enumerate(r):
                if ch!='.': s.set(x0+x,y0+y,ch)
    def outline(s):
        add=[(x,y) for y in range(s.h) for x in range(s.w) if s.p[y][x]=='.' and any(s.get(x+a,y+b) not in '.o' for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
        for x,y in add: s.p[y][x]='o'
        return s
    def img(s):
        im=Image.new('RGBA',(s.w,s.h)); px=im.load()
        for y in range(s.h):
            for x in range(s.w): px[x,y]=PAL[s.p[y][x]]
        return im
# ---------- bed 32x48 (base: frame+mattress+pillow, no blanket)
def bed_base():
    s=C(32,48)
    s.rect(2,0,29,7,'t'); s.rect(2,0,29,0,'f'); s.rect(3,2,28,6,'T')       # headboard
    for x in (2,29): s.rect(x,0,x,45,'t')                                 # posts
    s.rect(1,0,3,2,'f'); s.rect(28,0,30,2,'f')
    s.rect(3,7,28,44,'G'); s.rect(3,7,28,8,'S')                           # mattress (sheet)
    for y in range(9,44,4): s.rect(3,y,28,y,'G')
    s.rect(7,8,24,14,'G'); s.rect(7,14,24,14,'S'); s.rect(7,8,7,14,'S'); s.rect(24,8,24,14,'S')  # pillow
    s.rect(2,44,29,47,'t'); s.rect(3,45,28,46,'T'); s.rect(2,47,29,47,'b') # footboard
    return s
def blanket(s,top,lump=0,ruffle=0,turned=False):
    s.rect(3,top,28,43,'C')
    for y in range(top,44):
        for x in range(3,29):
            if x in(3,4) or y>41: s.set(x,y,'D')
            elif (x+y)%8==0 or (x-y)%8==0: s.set(x,y,'c')   # quilt diamonds
    s.rect(3,top,28,top+1,'c' if not turned else 'G')
    if turned: s.rect(3,top+2,28,top+2,'S')
    if lump:   # body lump highlight
        for y in range(top+2,top+22):
            w=5+lump-(1 if y>top+16 else 0)
            for x in range(16-w,16+w):
                if s.get(x,y)=='C' and x<16-w+2: s.set(x,y,'c')
                elif s.get(x,y) in 'C' and x>16+w-3: s.set(x,y,'D')
    for i in range(ruffle):
        x=8+i*6; s.set(x,top,'.'); s.set(x+1,top+1,'D')
base=bed_base()
bedimg=base.outline().img()
made=bed_base(); blanket(made,16,turned=True); made=made.outline().img()
bs=Image.new('RGBA',(64,48)); bs.paste(bedimg,(0,0)); bs.paste(made,(32,0)); bs.save(OUT+'bed.png')
# ---------- Dalton in-bed bits
HEAD_SLEEP=["..oooooo..",".ohhhhhho.","ohhhHhhHHo","ohHhhhHHHo","oHssssssHo","oSsSsSsSSo",".oSsssSSo.","..oooooo.."]  # eyes closed
HEAD_TURN =["..oooooo..",".ohhhhhho.","ohhHhhHHHo","oHhhhHHHHo","oHHssssHHo","oHSsSsSSSo",".oHSssSSo.","..oooooo.."]
def wake_canvas(): return Image.new('RGBA',(48,48))
def layer(draw):
    s=C(32,48); draw(s); return s
W=[]
def compose(fn, dal=None, dpos=None):
    im=wake_canvas()
    s=C(32,48); fn(s); s.outline()
    im.alpha_composite(s.img(),(0,0))
    if dal is not None: im.alpha_composite(dal,dpos)
    return im
def body(rows_from,rows_to,img=None):
    img=img or F['idle0']; return img.crop((0,rows_from,16,rows_to))
# 0,1 sleep breathe
W.append(compose(lambda s:(s.rows(HEAD_SLEEP,11,7),blanket(s,18))))
W.append(compose(lambda s:(s.rows(HEAD_SLEEP,11,7),blanket(s,19))))
# 2,3 stirring (head turns, blanket ruffles, arm out)
W.append(compose(lambda s:(s.rows(HEAD_TURN,12,7),blanket(s,19,ruffle=2))))
W.append(compose(lambda s:(s.rows(HEAD_SLEEP,10,8),blanket(s,18,ruffle=3),s.rows(["oso","oso","oso"],17,21))))
# 4,5,6 sitting up, blanket sliding to waist
def sit(y_body,top):
    def f(s): blanket(s,top,turned=True)
    im=wake_canvas()
    bb=C(32,48); f(bb); bb.outline()
    up=F['idle0'].crop((0,4,16,25))
    im.alpha_composite(bed_base().outline().img() if False else Image.new('RGBA',(1,1)),(0,0))
    im.alpha_composite(up,(8,y_body)); im.alpha_composite(bb.img().crop((0,top-1,32,48)),(0,top-1))
    return im
W.append(sit(8,22)); W.append(sit(5,25)); W.append(sit(4,28))
# 7 legs swung over the right edge (sitting on edge), 8 stepping out, 9 standing beside
def edge():
    im=wake_canvas(); bb=C(32,48); blanket(bb,30,turned=True,ruffle=2); bb.outline()
    im.alpha_composite(bb.img().crop((0,29,32,48)),(0,29))
    im.alpha_composite(F['idle0'].crop((0,4,16,29)),(20,10))
    return im
W.append(edge())
def out(fr,x):
    im=wake_canvas(); bb=C(32,48); blanket(bb,30,turned=True,ruffle=2); bb.outline()
    im.alpha_composite(bb.img().crop((0,29,32,48)),(0,29)); im.alpha_composite(fr,(x,12)); return im
W.append(out(F['rightA'],29)); W.append(out(F['idle0'],32))
ws=Image.new('RGBA',(48*len(W),48))
for i,w in enumerate(W): ws.paste(w,(i*48,0))
ws.save(OUT+'dalton_wakeup.png')
# full composite frames (bed under overlay)
def comp(i):
    im=Image.new('RGBA',(48,48)); im.alpha_composite(bedimg,(0,0)); im.alpha_composite(W[i]); return im
# ---------- preview 8x
S=8; font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
names=list(F)
pv=Image.new('RGB',(max(10*20*S,5*52*S),2*40*S+ 2*56*S),(46,38,34)); d=ImageDraw.Draw(pv)
for i,n in enumerate(['idle0','idle1']+[a+b for a in('down','up','left','right') for b in 'ASB']):
    x=(i%10)*20*S+2*S; y=(i//10)*40*S+S; im=F[n].resize((128,256),Image.NEAREST); pv.paste(im,(x,y),im)
    d.text((x,y+33*S),n,fill=(255,240,200),font=font)
labels=['sleep1','sleep2','stir1','stir2','sit1','sit2','sit3','legs over','step out','stand']
for i in range(len(W)):
    x=(i%5)*52*S+S; y=80*S+(i//5)*56*S; im=comp(i).resize((384,384),Image.NEAREST); pv.paste(im,(x,y),im)
    d.text((x,y+49*S),labels[i],fill=(255,240,200),font=font)
pv.save(OUT+'opening_preview.png')
# ---------- gif
seq=[(0,400),(1,400),(0,400),(1,400),(0,400),(1,600),(2,220),(3,220),(2,220),(3,300),(4,200),(5,200),(6,350),(7,300),(8,220),(9,800)]
frames=[];durs=[]
for i,t in seq:
    g=Image.new('RGB',(48,48),(120,86,56)); g.paste(comp(i),(0,0),comp(i)); frames.append(g.resize((384,384),Image.NEAREST)); durs.append(t)
frames[0].save(OUT+'dalton_wakeup.gif',save_all=True,append_images=frames[1:],duration=durs,loop=0)
# ---------- bedroom mockup
m=Image.new('RGB',(240,160),(122,86,54)); dd=ImageDraw.Draw(m); random.seed(4)
dd.rectangle([0,0,239,40],fill=(176,150,112)); dd.rectangle([0,38,239,42],fill=(96,64,40))  # back wall + trim
for y in range(43,160,8): dd.line([(0,y),(239,y)],fill=(98,68,42))
for y in range(43,160,8):
    off=random.randrange(0,40)
    for x in range(off,240,40): dd.line([(x,y),(x,y+7)],fill=(98,68,42))
dd.rectangle([150,6,190,34],fill=(96,64,40)); dd.rectangle([153,9,187,31],fill=(210,232,240)); dd.line([(170,9),(170,31)],fill=(96,64,40)); dd.line([(153,20),(187,20)],fill=(96,64,40))
dd.ellipse([96,100,170,140],fill=(140,52,44)); dd.ellipse([102,104,164,136],fill=(170,80,56))
dd.rectangle([20,20,44,46],fill=(110,74,44)); dd.rectangle([22,22,42,24],fill=(140,96,58))  # shelf/dresser
dd.rectangle([200,60,220,76],fill=(110,74,44))
m=m.convert('RGBA')
# morning light beam from window
p=m.load()
for y in range(34,160):
    for x in range(240):
        t=(y-34); x0=153+t*0.35; x1=187+t*0.6
        if x0<=x<=x1 and y<130:
            r,g,b,a=p[x,y]; k=0.22*(1-t/96)
            p[x,y]=(int(r+(255-r)*k),int(g+(236-g)*k),int(b+(190-b)*k),255)
m.alpha_composite(comp(9),(48,34))
m.convert('RGB').resize((960,640),Image.NEAREST).save(OUT+'opening_mockup.png')
print('ok',len(W))
