import re,base64,os
import os
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+os.sep;s=open(D+'src.html',encoding='utf8').read()
mt={'webp':'image/webp','jpg':'image/jpeg','svg':'image/svg+xml','png':'image/png'}
cache={}
def uri(n):
    if n not in cache:
        b=open(D+'img/'+n,'rb').read();cache[n]=f'data:{mt[n.rsplit(".",1)[1]]};base64,'+base64.b64encode(b).decode()
    return cache[n]
missing=set()
def rep(m):
    n=m.group(1)
    if not os.path.exists(D+'img/'+n):missing.add(n);return m.group(0)
    return uri(n)
# put each image once in a JS map, reference by key, to avoid duplicating base64
names=sorted(set(re.findall(r'img/([\w.-]+\.(?:webp|jpg|svg|png))',s)))
for n in names:
    if not os.path.exists(D+'img/'+n):missing.add(n)
have=[n for n in names if n not in missing]
print('missing',missing)
mapjs='const IMGDATA={'+','.join(f'"img/{n}":"{uri(n)}"' for n in have)+'};\nconst IU=p=>IMGDATA[p]||p;\n'
# JS strings 'img/..' -> IU('img/..')
s=re.sub(r"'(img/[\w.-]+\.(?:webp|jpg|svg|png))'",lambda m:f"IU('{m.group(1)}')" if m.group(1)[4:] in have else m.group(0),s)
# template literals src="img/..." inside JS
s=re.sub(r'src="(img/[\w.-]+\.(?:webp|jpg|svg|png))"',lambda m:'src="${IU(\''+m.group(1)+'\')}"' if m.group(1)[4:] in have else m.group(0),s)
s=s.replace('<script>\n','<script>\n'+mapjs,1)
# static HTML outside <script>: use the data URI directly
a,b=s.split('<script>',1)
a=re.sub(r'src="\$\{IU\(\'(img/[\w.-]+)\'\)\}"',lambda m:'src="'+uri(m.group(1)[4:])+'"',a)
s=a+'<script>'+b
s=re.sub(r"url\(fonts/([\w.-]+\.woff)\)",lambda m:'url(data:font/woff;base64,'+base64.b64encode(open(D+'fonts/'+m.group(1),'rb').read()).decode()+')',s)
open(D+'index.html','w',encoding='utf8').write(s);print(len(s)//1024,'KB')
