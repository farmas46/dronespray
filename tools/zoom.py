import sys,numpy as np
from PIL import Image,ImageDraw
# usage: zoom.py P name src x0 y0 x1 y1
P,n,x0,y0,x1,y1=sys.argv[1],sys.argv[2],*map(int,sys.argv[3:7])
i=Image.open(f'{P}/w-{n}.png');z=1000/(x1-x0)*1.0
c=i.crop((x0,y0,x1,y1)).resize((1000,int((y1-y0)*z)),Image.LANCZOS);d=ImageDraw.Draw(c)
st=20
for x in range((x0//st+1)*st,x1,st):
    X=(x-x0)*z;d.line([(X,0),(X,c.height)],fill=(255,0,255) if x%100==0 else (0,255,255));d.text((X+1,1),str(x),fill=(255,255,255),stroke_width=1,stroke_fill=0)
for y in range((y0//st+1)*st,y1,st):
    Y=(y-y0)*z;d.line([(0,Y),(c.width,Y)],fill=(255,0,255) if y%100==0 else (0,255,255));d.text((1,Y+1),str(y),fill=(255,255,255),stroke_width=1,stroke_fill=0)
c.save(f'{P}/z-{n}.png')
