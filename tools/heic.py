import struct,subprocess,sys,io
from PIL import Image
def boxes(b,s,e):
    while s+8<=e:
        n,t=struct.unpack('>I4s',b[s:s+8]);h=8
        if n==1:n=struct.unpack('>Q',b[s+8:s+16])[0];h=16
        elif n==0:n=e-s
        yield t.decode('latin1'),s+h,s+n;s+=n
def kids(b,s,e):return {t:(a,z) for t,a,z in boxes(b,s,e)}
def conv(path,out):
    b=open(path,'rb').read()
    top=kids(b,0,len(b));ms,me=top['meta'];M=kids(b,ms+4,me)
    pitm=struct.unpack('>H',b[M['pitm'][0]+4:M['pitm'][0]+6])[0]
    # iinf
    a,z=M['iinf'];ver=b[a];p=a+4+(2 if ver==0 else 4);types={}
    for t,s,e in boxes(b,p,z):
        v=b[s];iid=struct.unpack('>H',b[s+4:s+6])[0];types[iid]=b[s+8:s+12].decode('latin1')
    # iloc
    a,z=M['iloc'];v=b[a];p=a+4;x=b[p];y=b[p+1];p+=2
    os_,ls,bs,ix=x>>4,x&15,y>>4,y&15
    rd=lambda n,q:int.from_bytes(b[q:q+n],'big') if n else 0
    cnt=rd(2,p);p+=2;loc={}
    for _ in range(cnt):
        iid=rd(2,p);p+=2
        cm=0
        if v==1:cm=rd(2,p)&15;p+=2
        p+=2;base=rd(bs,p);p+=bs;ec=rd(2,p);p+=2;ex=[]
        for _ in range(ec):
            if v==1 and ix:p+=ix
            o=rd(os_,p);p+=os_;l=rd(ls,p);p+=ls;ex.append((base+o+(M['idat'][0] if cm==1 else 0),l))
        loc[iid]=ex
    # iref dimg
    tiles=[]
    for t,s,e in boxes(b,M['iref'][0]+4,M['iref'][1]):
        fr=rd(2,s)
        if t=='dimg' and fr==pitm:
            c=rd(2,s+2);tiles=[rd(2,s+4+2*i) for i in range(c)]
    # props
    P=kids(b,*M['iprp']);co=list(boxes(b,*P['ipco']));ip=P['ipma'];v2=b[ip[0]];fl=b[ip[0]+3]&1;p=ip[0]+4;n=rd(4,p);p+=4;assoc={}
    for _ in range(n):
        iid=rd(2,p);p+=2;c=b[p];p+=1;L=[]
        for _ in range(c):
            if fl:L.append(rd(2,p)&0x7fff);p+=2
            else:L.append(b[p]&0x7f);p+=1
        assoc[iid]=L
    def prop(iid,typ):
        for k in assoc.get(iid,[]):
            if k and co[k-1][0]==typ:return co[k-1]
    grid=b[loc[pitm][0][0]:loc[pitm][0][0]+loc[pitm][0][1]]
    rows,cols=grid[2]+1,grid[3]+1
    wide=grid[1]&1
    W,H=struct.unpack('>II',grid[4:12]) if wide else struct.unpack('>HH',grid[4:8])
    def annexb(iid):
        _,s,e=prop(iid,'hvcC');q=s+22;na=b[q];q+=1;out=b''
        ln=(b[s+21]&3)+1
        for _ in range(na):
            q+=1;c=rd(2,q);q+=2
            for _ in range(c):
                l=rd(2,q);q+=2;out+=b'\0\0\0\1'+b[q:q+l];q+=l
        for o,l in loc[iid]:
            q=o
            while q<o+l:
                k=rd(ln,q);q+=ln;out+=b'\0\0\0\1'+b[q:q+k];q+=k
        return out
    canvas=None
    for i,t in enumerate(tiles):
        r=subprocess.run(['ffmpeg','-v','error','-f','hevc','-i','-','-frames:v','1','-f','image2pipe','-c:v','png','-'],input=annexb(t),capture_output=True)
        im=Image.open(io.BytesIO(r.stdout)).convert('RGB')
        if canvas is None:tw,th=im.size;canvas=Image.new('RGB',(tw*cols,th*rows))
        canvas.paste(im,((i%cols)*tw,(i//cols)*th))
    canvas=canvas.crop((0,0,W,H))
    rot=prop(pitm,'irot')
    if rot:canvas=canvas.rotate(90*(b[rot[1]]&3),expand=True)
    canvas.save(out,quality=95);print(out,canvas.size,len(tiles))
if __name__=='__main__':conv(*sys.argv[1:3])
