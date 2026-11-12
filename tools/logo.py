import numpy as np,cv2
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
A='/mnt/user-data/attachments/8755a5ab-8e08-56d5-bbcc-ac48ae9f9946/'
INK='#1a1a1a';GOLD='#e6cf86'
def gray(p):
    c=Image.open(p).convert('RGBA');w=Image.new('RGBA',c.size,'white');w.alpha_composite(c);return np.asarray(w.convert('L')).astype(np.uint8)
def bbox(m):
    y,x=np.where(m);return x.min(),y.min(),x.max()+1,y.max()+1
def trace(g,up,thr,sx,sy,ox,oy,blur=0.0,eps=0.5,minarea=0):
    b=cv2.resize(g,None,fx=up,fy=up,interpolation=cv2.INTER_CUBIC)
    if blur:b=cv2.GaussianBlur(b,(0,0),blur)
    _,m=cv2.threshold(b,thr,255,cv2.THRESH_BINARY_INV)
    cs,_=cv2.findContours(m,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE);d=[]
    for c in cs:
        if cv2.contourArea(c)<minarea:continue
        c=cv2.approxPolyDP(c,eps,True).reshape(-1,2).astype(float)
        if len(c)<3:continue
        c=(c+.5)/up
        P=[(ox+x*sx,oy+y*sy) for x,y in c]
        d.append('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in P)+'Z')
    return ''.join(d)
wide=gray(A+'409c89b6-image.png');st=gray(A+'a8b78a05-image.png')
L=bbox(wide[:,:440]<120);print('left',L)
sb=bbox(st<128);print('stacked',sb)
s=(L[2]-L[0])/(sb[2]-sb[0]);print('scale',s)
stacked=trace(st[sb[1]:sb[3],sb[0]:sb[2]],3,128,s,s,L[0],L[1],blur=1.2,eps=.7,minarea=20)
# right panel measures
H=wide[:,495:];hm=H<110
rows=np.where(hm.sum(1)>0)[0];print('rows',rows.min(),rows.max())
head_end=None
# heading = rows above the gold rule
g=np.asarray(Image.open(A+'409c89b6-image.png').convert('RGB')).astype(int)
gold=(g[...,0]-g[...,2]>25)&(g[...,0]>180)
gy=np.where(gold[:,495:].sum(1)>100)[0];print('gold y',gy.min(),gy.max());gx=np.where(gold[gy.min():gy.max()+1].sum(0)>0)[0];gx=gx[gx>495];print('gold x',gx.min(),gx.max())
top=wide[:gy.min()-2,495:]<128;hb=bbox(top);hb=(hb[0]+495,hb[1],hb[2]+495,hb[3]);print('heading',hb)
W=st[sb[1]:sb[3],sb[0]:sb[2]]
ink=W<128
r=np.where(ink[480:].sum(1)>0)[0]+480
# find text rows in the wordmark
prof=ink.sum(1)>0;runs=[];i=0
while i<len(prof):
    if prof[i]:
        j=i
        while j<len(prof) and prof[j]:j+=1
        runs.append((i,j));i=j
    else:i+=1
print('rows',runs)
big=[x for x in runs if x[1]-x[0]>120 and x[0]>350][:2];print(big)
def letters(row):
    m=ink[row[0]:row[1]];c=m.sum(0)>0;o=[];i=0
    while i<len(c):
        if c[i]:
            j=i
            while j<len(c) and c[j]:j+=1
            o.append(m[:,i:j]);i=j
        else:i+=1
    return o
dr=letters(big[0]);sp=letters(big[1]);print(len(dr),len(sp),[x.shape for x in dr+sp])
C=big[0][1]-big[0][0];SW=int(round(C*.29))
G_={'P':sp[1],'R':sp[2],'E':dr[4],'S':sp[0],'N':dr[3]}
def rect(w):
    return np.zeros((C,w),bool)
def poly(w,ps):
    t=np.zeros((C,w),np.uint8);cv2.fillPoly(t,[np.array(ps,np.int32)],1);return t>0
I_=rect(SW);I_[:]=True
Tw=int(C*1.06);T_=rect(Tw);T_[:int(C*.27)]=True;T_[:,(Tw-SW)//2:(Tw+SW)//2]=True
Xw=int(C*1.14);b=int(C*.33)
X_=poly(Xw,[(0,0),(b,0),(Xw,C),(Xw-b,C)])|poly(Xw,[(Xw-b,0),(Xw,0),(b,C),(0,C)])
Mw=int(C*1.32);d=int(C*.30)
M_=rect(Mw);M_[:,:SW]=True;M_[:,Mw-SW:]=True
M_|=poly(Mw,[(0,0),(d,0),(Mw//2,int(C*.60)),(Mw-d,0),(Mw,0),(Mw,int(C*.28)),(Mw//2+d//3,C-int(C*.08)),(Mw//2-d//3,C-int(C*.08)),(0,int(C*.28))])
O_=dr[2].copy();gw=O_.shape[1]
O_[int(C*.28):int(C*.50),gw-SW-4:]=False
O_[int(C*.50):int(C*.72),int(gw*.52):gw]=True
O_[int(C*.72):,gw-SW:]=O_[int(C*.72):,gw-SW:]
Yw=int(C*1.16);b2=int(C*.33);mid=Yw//2;st2=SW//2;ym=int(C*.58)
Y_=poly(Yw,[(0,0),(b2,0),(mid,int(C*.34)),(Yw-b2,0),(Yw,0),(mid+st2,ym),(mid+st2,C),(mid-st2,C),(mid-st2,ym)])
G_.update(Y=Y_,I=I_,T=T_,X=X_,M=M_,G=O_)
gap=int(C*.17)
lines=['PRE','MIXING','SYSTEMS']
hp=[]
k=(hb[2]-hb[0])/(sum(G_[c].shape[1] for c in 'SYSTEMS')+6*gap);ky=32/C;CAP=32;pitch=(hb[3]-hb[1]-CAP)/2;print('cap',CAP)
for n,t in enumerate(lines):
    tot=sum(G_[c].shape[1] for c in t)+gap*(len(t)-1)
    can=np.zeros((C+40,tot+40),np.uint8);x=20
    for c in t:
        g_=G_[c];can[20:20+g_.shape[0],x:x+g_.shape[1]][g_]=255;x+=g_.shape[1]+gap
    can=cv2.erode(can,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)));can=cv2.GaussianBlur(can,(0,0),2.0)
    hp.append(trace(255-can,2,128,k,ky,hb[0]-20*k,hb[1]+n*pitch-20*ky,blur=0,eps=.6,minarea=30))
heading=''.join(hp)
HR=hb[0]+max(sum(G_[c].shape[1] for c in t)+gap*(len(t)-1) for t in lines)*k
bot=wide[gy.max()+3:,495:]<190;tb=bbox(bot);print('tag',tb[0]+495,tb[1]+gy.max()+3,tb[2]+495,tb[3]+gy.max()+3)
vr=(wide[:,440:495]<150);vx=np.where(vr.sum(0)>100)[0];vy=np.where(vr.sum(1)>0)[0];print('vrule x',vx.min()+440,vx.max()+440,'y',vy.min(),vy.max())
f=TTFont('/usr/share/fonts/truetype/google-fonts/Poppins-Light.ttf');gs=f.getGlyphSet();cm=f.getBestCmap();upm=f['head'].unitsPerEm;cap=f['OS/2'].sCapHeight
def text(t,x0,x1,base,capH):
    k=capH/cap;adv=[gs[cm[ord(c)]].width*k for c in t];sp=(x1-x0-sum(adv))/(len(t)-1);x=x0;o=[]
    for c,a in zip(t,adv):
        if c!=' ':
            p=SVGPathPen(gs,ntos=lambda v:f'{v:.2f}');gs[cm[ord(c)]].draw(TransformPen(p,(k,0,0,-k,x,base)));o.append(p.getCommands())
        x+=a+sp
    return ''.join(o)
tx0=tb[0]+495;tx1=tb[2]+495;ty0=tb[1]+gy.max()+3;ty1=tb[3]+gy.max()+3
capH=13;l1=text('FOR AGRICULTURAL',tx0,tx1,ty0+capH,capH);l2=text('SPRAYING DRONES',tx0,tx1-14,ty1,capH)
vb=f'{L[0]-2} {L[1]-2} {tx1-L[0]+4} {L[3]-L[1]+4}'
vr_=f'<rect x="{vx.min()+440}" y="{vy.min()}" width="2" height="{vy.max()-vy.min()+1}" fill="{INK}"/>'
gr=f'<rect x="{gx.min()}" y="{gy.min()}" width="{gx.max()-gx.min()+1}" height="4" fill="{GOLD}"/>'
full=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="DroneSpray Pre-Mixing Systems for agricultural spraying drones"><path fill="{INK}" fill-rule="evenodd" d="{stacked}{heading}"/><path fill="{INK}" d="{l1}{l2}"/>{vr_}{gr}</svg>'
open('/home/claude/dronespray/img/logo-full.svg','w').write(full)
vbh=f'{L[0]-2} {L[1]-2} {HR-L[0]+4:.1f} {L[3]-L[1]+4}'
hdr=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vbh}" role="img" aria-label="DroneSpray Pre-Mixing Systems"><path fill="{INK}" fill-rule="evenodd" d="{stacked}{heading}"/>{vr_}</svg>'
open('/home/claude/dronespray/img/logo-header.svg','w').write(hdr)
vbs=f'{L[0]-2} {L[1]-2} {L[2]-L[0]+4} {L[3]-L[1]+4}'
open('/home/claude/dronespray/img/logo-stacked.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vbs}" role="img" aria-label="DroneSpray Pre-Mixing Systems"><path fill="{INK}" fill-rule="evenodd" d="{stacked}"/></svg>')
