from PIL import Image, ImageDraw, ImageFont
import random
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets','sprites')+'/'
PAL={'.':(0,0,0,0),'o':(28,20,18),'s':(244,204,164),'S':(204,146,108),'h':(178,126,70),'H':(122,76,40),
'c':(92,150,78),'C':(52,108,60),'D':(30,66,42),'t':(160,108,62),'T':(104,66,38),'b':(72,46,30),
'g':(246,196,68),'G':(255,246,190),'f':(150,100,36)}
def norm(rows):
    return [(r+'.'*16)[:16] for r in rows]
DOWN=norm(["","","","","",
"......oooo......","....oohhhhoo....","...ohhhhhhhHo...","..ohhhhhhhhhHo..","..ohhhHhhhHHHo..",
"..ohHhhHhHhHHo..","..oHsssssssSHo..","..oHsosssosSHo..","..oSsssssssSSo..","...oSssSsssSo...",
"...oCoSSSSoDo...","..oCcCcCCCCDDo..",".ocCcCtttTCCDDo.",".ocCCotTtToCDDo.",".ocCCoTgTTToDDo.",
".ocCDottttToDDo.",".osCDottttToDso.",".ooCDottttTTDoo.","..oDDotttTTToo..","..ooooTTTTToo..."])
UP=norm(["","","","","",
"......oooo......","....oohhhhoo....","...ohhhhhhhHo...","..ohhhhhhhhhHo..","..ohhhhhhhhHHo..",
"..ohhhhhhhHHHo..","..ohHhhhhHHHHo..","..oHhHhhHHHHHo..","..oHHHhHHHHHHo..","...oHHHHHHHHo...",
"...oCccccCCDo...","..occoccCoCDDo..",".occcCooooCDDDo.",".occcCCCCCCDDDo.",".ocCCCCCCCCDDDo.",
".ocCCCCCCCDDDDo.",".osCCCCCCCDDDso.",".ooCCCCCCDDDDoo.","..oCCCCCDDDDDo..","..oooooooooooo.."])
LEFT=norm(["","","","","",
"......oooo......","....oohhhhoo....","...ohhhhhhhho...","..ohhhhhhhhhHo..","..ohhhhhhhHHHo..",
"..oHhhHhhHHHHo..","..ossshHhHHHHo..","..osossHHHHHHo..","..oSssssHHHHo...","...oSsssSHHo....",
"....oSSoCDDo....","...occcCCCDDo...","...occCCtCDDo...","...ocCCttCDDo...","...ocCTTTCDDo...",
"...ocCttCCDDo...","...osCttCCDDo...","...ooCtTCDDDo...","....oCTTCDDo....","....ooooooo....."])
LD={'A':["....oTTo.oTTo...","....oTbo.obbo...","....obbo.oooo...","....oooo........"],
    'S':["....oTTo.oTTo...","....oTbo.oTbo...","....obbo.obbo...","....oooo.oooo..."],
    'B':["....oTTo.oTTo...","....obbo.oTbo...","....oooo.obbo...",".........oooo..."]}
LS={'A':[".....oTooTo.....","....obo..obo....","...obbo..obbo...","...oooo..oooo..."],
    'S':["......oTTo......","......oTbo......",".....obbbo......",".....ooooo......"],
    'B':["......oTTo......","......oTTo......","......obbo......","......oooo......"]}
LANT=[".oo..","o..o.",".ooo.","ofGfo","oGGgo","oGGgo","ofgfo",".ooo."]
def blit(img,rows,x0,y0):
    px=img.load()
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            X,Y=x0+x,y0+y
            if ch!='.' and 0<=X<16 and 0<=Y<32: px[X,Y]=PAL[ch]
def frame(upper,legs,lant=None,front=True):
    im=Image.new('RGBA',(16,32),(0,0,0,0))
    if lant and not front: blit(im,LANT,*lant)
    blit(im,upper,0,0); blit(im,legs,0,25)
    if lant and front: blit(im,LANT,*lant)
    return im
F={}
sw={'A':-1,'S':0,'B':1}
for k in 'ASB':
    F['down'+k]=frame(DOWN,LD[k],(0,20+abs(sw[k])))
    F['up'+k]=frame(UP,LD[k],(11,20+abs(sw[k])),front=False)
    F['left'+k]=frame(LEFT,LS[k],(1+sw[k],20))
    F['right'+k]=F['left'+k].transpose(Image.FLIP_LEFT_RIGHT)
# raise lantern
R=list(DOWN); R[21]=".ooCDottttToDso."; R[20]=".ooCDottttToDDo."
im=frame(R,LD['S'])
blit(im,["oso","oso","oso","oSo","oSo",".oo"],0,11)
blit(im,LANT,0,4)
F['raise']=im
# kneel: shift upper down 4, eyes closed, hands together, folded legs
K=list(DOWN); K[12]="..oHsSsssSsSHo.."; K[21]=".ooCDosstTToDoo."
im=Image.new('RGBA',(16,32),(0,0,0,0))
blit(im,["..obbTbbbbTbbo..","..oooooooooooo.."],0,29)
blit(im,K[5:25],0,9)
F['kneel']=im
order=[['downA','downS','downB'],['upA','upS','upB'],['leftA','leftS','leftB'],['rightA','rightS','rightB'],['raise','kneel']]
sheet=Image.new('RGBA',(48,160),(0,0,0,0))
for r,row in enumerate(order):
    for c,n in enumerate(row): sheet.paste(F[n],(c*16,r*32))
sheet.save(OUT+'dalton.png')
cols=[v for k,v in PAL.items() if k!='.']
assert len(cols)<=15
pp=Image.new('RGB',(len(cols)*32,32))
d=ImageDraw.Draw(pp)
for i,c in enumerate(cols): d.rectangle([i*32,0,i*32+31,31],fill=c[:3])
pp.save(OUT+'dalton_palette.png')
# background tile
def grass(w,h,seed=1):
    random.seed(seed); g=Image.new('RGB',(w,h),(70,128,62)); p=g.load()
    for _ in range(w*h//12):
        x,y=random.randrange(w),random.randrange(h); p[x,y]=random.choice([(86,146,70),(58,108,54)])
    return g
S=8
names=[n for row in order for n in row]
pv=Image.new('RGB',(len(names[:7])*20*S, 2*44*S))
bg=grass(pv.width//S,pv.height//S).resize(pv.size,Image.NEAREST); pv.paste(bg)
d=ImageDraw.Draw(pv)
try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except: font=ImageFont.load_default()
for i,n in enumerate(names):
    cx=(i%7)*20*S+2*S; cy=(i//7)*44*S+2*S
    pv.paste(F[n].resize((16*S,32*S),Image.NEAREST),(cx,cy),F[n].resize((16*S,32*S),Image.NEAREST))
    d.text((cx,cy+33*S),n,fill=(255,240,200),font=font,stroke_width=2,stroke_fill=(20,30,20))
pv.save(OUT+'dalton_preview.png')
seq=['A','S','B','S']; gifs=[]
for k in seq:
    g=grass(4*20,36).resize((80*S,36*S),Image.NEAREST)
    for j,dn in enumerate(['down','up','left','right']):
        f=F[dn+k].resize((16*S,32*S),Image.NEAREST); g.paste(f,(j*20*S+2*S,2*S),f)
    gifs.append(g.convert('P',palette=Image.ADAPTIVE))
gifs[0].save(OUT+'dalton_walk.gif',save_all=True,append_images=gifs[1:],duration=160,loop=0)
# mockup
m=grass(240,160,7); p=m.load(); random.seed(3)
for y in range(160):
    for x in range(240):
        if abs(x-120-int(10*__import__('math').sin(y/20)))<18 or (60<y<92 and x<130):
            p[x,y]=random.choice([(176,138,90),(164,126,80),(186,150,100)])
d=ImageDraw.Draw(m)
for tx,ty in [(20,10),(200,20),(30,110),(210,120),(180,70)]:
    d.ellipse([tx-14,ty-14,tx+14,ty+10],fill=(28,70,40),outline=(20,40,26)); d.ellipse([tx-10,ty-12,tx+6,ty+2],fill=(44,96,52))
    d.rectangle([tx-2,ty+8,tx+2,ty+18],fill=(90,58,34))
dx,dy=112,64; lx,ly=dx+2,dy+24
ov=Image.new('RGBA',(240,160),(10,20,40,90)); od=ImageDraw.Draw(ov)
for r,a in [(44,40),(32,25),(22,0),(12,0)]: od.ellipse([lx-r,ly-r,lx+r,ly+r],fill=(255,210,110,a))
m=Image.alpha_composite(m.convert('RGBA'),ov); m.alpha_composite(F['downS'],(dx,dy))
for fx,fy in [(150,40),(160,52),(140,30)]: m.putpixel((fx,fy),(255,250,170,255))
m.convert('RGB').resize((960,640),Image.NEAREST).save(OUT+'dalton_mockup.png')
