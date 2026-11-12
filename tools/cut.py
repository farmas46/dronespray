import numpy as np,sys
from PIL import Image
from scipy import ndimage as ni
S,PV=sys.argv[1:3];O='/home/claude/dronespray/img/'
HOLES={'ds600':[14,41,46,50,51,52,54],'ds300':[6,31,32],'ds200':[3,4],'ds110':[3,12,14,15]}
st=np.ones((3,3))
for name,f in [('ds600','ds600.jpg'),('ds300','ds300-800.jpg'),('ds200','ds200-800.jpg'),('ds110','ds110-800.jpg')]:
    a=np.asarray(Image.open(f'{S}/{f}').convert('RGB')).astype(float);m=a.max(2);sc=a.shape[1]/800
    low=m<=4
    lab,_=ni.label(ni.binary_opening(low,structure=st,iterations=3))
    e=list(set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0})
    bg=ni.binary_dilation(np.isin(lab,e),structure=st,iterations=4,mask=low)
    lab1,_=ni.label(ni.binary_opening(low,structure=st,iterations=1))
    bg|=ni.binary_dilation(np.isin(lab1,HOLES[name]),structure=st,iterations=2,mask=low)
    # eat the near-black fringe around the outline, a limited distance only
    bg=ni.binary_dilation(bg,structure=st,iterations=int(round(3*sc)),mask=m<=30)
    bg=ni.binary_dilation(bg,structure=st,iterations=1)
    al=ni.gaussian_filter((~bg).astype(float),0.8*sc**.5)
    al=np.clip((al-.5)*2.2+.5,0,1)
    im=Image.fromarray(np.dstack([a,al*255]).astype('uint8'),'RGBA')
    bb=im.getchannel('A').point(lambda v:255 if v>16 else 0).getbbox();p=int(max(a.shape)*.015)
    im=im.crop((max(bb[0]-p,0),max(bb[1]-p,0),min(bb[2]+p,im.width),min(bb[3]+p,im.height)))
    im.save(O+name+'.webp',quality=90,method=6)
    for col,suf in [((255,255,255),'w'),((255,0,200),'m')]:
        c=Image.new('RGB',im.size,col);c.paste(im,mask=im.getchannel('A'));c.save(f'{PV}/{name}-{suf}.png')
    print(name,im.size)
n=['ds600','ds300','ds200','ds110']
for suf in 'wm':
    I=[Image.open(f'{PV}/{x}-{suf}.png') for x in n];H=620;I=[i.resize((int(i.width*H/i.height),H)) for i in I]
    o=Image.new('RGB',(sum(i.width for i in I),H));x=0
    for i in I:o.paste(i,(x,0));x+=i.width
    o.save(f'{PV}/sheet-{suf}.png')
