import sys,json,numpy as np,cv2
from PIL import Image
from scipy import ndimage as ni
SRC='/home/claude/dronespray/src/';OUT='/home/claude/dronespray/img/';PV=sys.argv[1]
exec(open('/home/claude/dronespray/tools/polys.py').read())
only=sys.argv[2:] or list(M)
for name in only:
    m=M[name];im=Image.open(SRC+m['f']+'.jpg').convert('RGB');WW=1800
    k=WW/1000;sm=im.resize((WW,int(im.height*WW/im.width)),Image.LANCZOS);a=np.array(sm)[...,::-1].copy()
    H,W=a.shape[:2];pts=lambda p:(np.array(p)*k).astype(np.int32)
    mask=np.full((H,W),cv2.GC_BGD,np.uint8)
    out=np.zeros((H,W),np.uint8);cv2.fillPoly(out,[pts(m['o'])],1)
    near=cv2.dilate(out,np.ones((9,9),np.uint8))
    mask[near>0]=cv2.GC_PR_BGD
    mask[out>0]=cv2.GC_PR_FGD
    for p in m.get('bg',[]):cv2.fillPoly(mask,[pts(p)],cv2.GC_BGD)
    for p in m.get('pbg',[]):cv2.fillPoly(mask,[pts(p)],cv2.GC_PR_BGD)
    for p in m['s']:cv2.fillPoly(mask,[pts(p)],cv2.GC_FGD)
    bm,fm=np.zeros((1,65)),np.zeros((1,65))
    cv2.grabCut(a,mask,None,bm,fm,6,cv2.GC_INIT_WITH_MASK)
    fg=(mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD)
    for p in m.get('add',[]):
        t=np.zeros((H,W),np.uint8);cv2.fillPoly(t,[pts(p)],1);fg|=t>0
    for p,w in m.get('lines',[]):
        t=np.zeros((H,W),np.uint8);cv2.polylines(t,[pts(p)],False,1,int(w*k));fg|=t>0
    for p in m.get('cut',[]):
        t=np.zeros((H,W),np.uint8);cv2.fillPoly(t,[pts(p)],1);fg&=t==0
    fg=ni.binary_opening(fg,iterations=2)
    lab,n=ni.label(fg);s=ni.sum(fg,lab,range(1,n+1));fg=np.isin(lab,1+np.where(s>=s.max()*0.004)[0])
    fg=ni.binary_fill_holes(fg)&~(ni.binary_opening(~fg,iterations=3)&~ni.binary_fill_holes(fg)) if False else fg
    # fill pin-holes only
    h=ni.binary_fill_holes(fg)&~fg;l2,n2=ni.label(h)
    if n2:
        z=ni.sum(h,l2,range(1,n2+1));fg|=np.isin(l2,1+np.where(z<120)[0])
    al=ni.gaussian_filter(fg.astype(float),1.3);al=np.clip((al-.55)*2.6+.5,0,1)
    res=Image.fromarray(np.dstack([np.array(sm),al*255]).astype('uint8'),'RGBA')
    bb=Image.fromarray((al>0.1).astype('uint8')*255).getbbox();p=12
    res=res.crop((max(bb[0]-p,0),max(bb[1]-p,0),min(bb[2]+p,W),min(bb[3]+p,H)))
    res.save(OUT+name+'.webp',quality=90,method=6)
    c=Image.new('RGB',res.size,(255,255,255));c.paste(res,mask=res.getchannel('A'));c.save(f'{PV}/r-{name}.png')
    print(name,res.size)
