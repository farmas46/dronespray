import json,math
p='/home/claude/dronespray/src.html';s=open(p,encoding='utf8').read()
def r(a,b):
    global s
    assert s.count(a)==1,a[:70];s=s.replace(a,b)
C=[('es',40.4,-3.7),('it',41.9,12.5),('lv',56.95,24.1),('gb',51.5,-0.13),('de',52.5,13.4),('fr',48.86,2.35),('hr',45.8,15.98),('ie',53.35,-6.26)]
HQ=(39.64,22.42)
def pr(lat,lon):
    x=(lon+12)*math.cos(math.radians(48))*22; y=(60-lat)*22
    return round(x+20,1),round(y+20,1)
hx,hy=pr(*HQ)
pts={c:pr(a,b) for c,a,b in C}
arcs=''.join(f'<path class="nw-arc" style="animation-delay:{k*0.12:.2f}s" d="M{hx} {hy} Q{(hx+x)/2:.1f} {min(hy,y)-60:.1f} {x} {y}"/>' for k,(c,(x,y)) in enumerate(pts.items()))
dots=''.join(f'<g class="nw-pt" data-c="{c}"><circle cx="{x}" cy="{y}" r="5"/><circle class="halo" cx="{x}" cy="{y}" r="11"/><text x="{x+10}" y="{y-9}">${{t.nw.c.{c}}}</text></g>' for c,(x,y) in pts.items())
grid=''.join(f'<circle cx="{gx}" cy="{gy}" r="1"/>' for gx in range(20,520,22) for gy in range(20,500,22))
svg=f'<svg class="nw-map" viewBox="0 0 520 500" role="img" aria-label="${{t.nw.mapL}}"><g class="nw-grid">{grid}</g>{arcs}{dots}<g class="nw-hq"><circle cx="{hx}" cy="{hy}" r="7"/><circle class="halo" cx="{hx}" cy="{hy}" r="16"/><text x="{hx+12}" y="{hy+18}">${{t.nw.hq}}</text></g></svg>'
codes=['es','it','lv','gb','de','fr','hr','ie']
fn=r"""function network(){const t=T[lang],n=t.nw;
  return `<section class="nw-hero"><div class="wrap"><div class="nw-copy"><span class="eyebrow">${n.eye}</span><h1>${n.h}</h1><p>${n.p}</p><div class="nw-stats"><div><b>8</b><span>${n.sCountries}</span></div><div><b>1</b><span>${n.sHq}</span></div></div><div class="btn-row"><a class="btn" href="#contact" data-subject="2">${n.cta} →</a><a class="btn ghost" href="${WA()}" target="_blank" rel="noopener">WhatsApp</a></div></div>SVGMAP</div></section>
<section class="band white"><div class="wrap"><div class="head"><span class="eyebrow">${n.listEye}</span><h2>${n.listH}</h2><p>${n.listP}</p></div><div class="nw-grid-list">${CODES.map(c=>`<a class="nw-c" href="#contact" data-subject="2" data-country="${n.c[c]}"><span class="nw-code">${c.toUpperCase()}</span><span class="nw-name">${n.c[c]}</span><span class="nw-st">${n.avail}</span><span class="nw-go">${n.find} →</span></a>`).join('')}</div></div></section>
<section class="band"><div class="wrap"><div class="head"><h2>${n.howH}</h2></div><ol class="dl-steps nw-steps">${n.steps.map((x,k)=>`<li><span class="num">0${k+1}</span><h3>${x[0]}</h3><p>${x[1]}</p></li>`).join('')}</ol></div></section>
<section class="nw-cta"><div class="wrap"><div><h2>${n.ctaH}</h2><p>${n.ctaP}</p></div><div class="btn-row"><a class="btn" href="#dealers">${t.dl.nav} →</a><a class="btn ghost" href="#contact" data-subject="2">${t.contact}</a></div></div></section>`}
""".replace('SVGMAP',svg)
r("function accCards(list,dup){","const CODES="+json.dumps(codes)+";\n"+fn+"function accCards(list,dup){")
r("'accessories','dealers','contact'].includes(h)","'accessories','dealers','network','contact'].includes(h)")
r("view==='dealers'?dealers():","view==='dealers'?dealers():view==='network'?network():")
r("+ln('dealers',t.dl.nav,view==='dealers')","+ln('network',t.nw.nav,view==='network')+ln('dealers',t.dl.nav,view==='dealers')")
r('<li><a href="#dealers">${t.dl.nav}</a></li>','<li><a href="#network">${t.nw.nav}</a></li><li><a href="#dealers">${t.dl.nav}</a></li>')
r("if(a.dataset.product)form.product=a.dataset.product;","if(a.dataset.product)form.product=a.dataset.product;if(a.dataset.country){form.country=a.dataset.country;form.msg=T[lang].nw.msg(a.dataset.country)}")
N={
'el':dict(nav='Δίκτυο',eye='Διεθνές δίκτυο',h='Δίκτυο συνεργατών στο εξωτερικό',p='Τα συστήματα DroneSpray ταξιδεύουν από τη Λάρισα σε όλη την Ευρώπη. Επικοινωνήστε μαζί μας και θα σας φέρουμε σε επαφή με τον συνεργάτη της χώρας σας.',sCountries='Χώρες εξαγωγής',sHq='Έδρα στην Ελλάδα',cta='Βρείτε συνεργάτη',mapL='Χάρτης χωρών εξαγωγής DroneSpray',hq='Λάρισα',
 listEye='Πού βρισκόμαστε',listH='Οι χώρες μας',listP='Επιλέξτε τη χώρα σας. Θα σας απαντήσουμε και θα σας κατευθύνουμε στον πλησιέστερο συνεργάτη.',avail='Ενεργό δίκτυο',find='Βρείτε συνεργάτη',
 c=dict(es='Ισπανία',it='Ιταλία',lv='Λετονία',gb='Ηνωμένο Βασίλειο',de='Γερμανία',fr='Γαλλία',hr='Κροατία',ie='Ιρλανδία'),
 howH='Πώς λειτουργεί',steps=[['Επικοινωνία','Μας στέλνετε μήνυμα από τη φόρμα ή στο WhatsApp, με τη χώρα σας.'],['Κατεύθυνση','Σας φέρνουμε σε επαφή με τον συνεργάτη που εξυπηρετεί την περιοχή σας.'],['Εξυπηρέτηση','Παραλαβή, εκπαίδευση και υποστήριξη από κοντά.']],
 ctaH='Η χώρα σας δεν είναι στη λίστα;',ctaP='Το δίκτυο μεγαλώνει. Γίνετε ο πρώτος συνεργάτης της DroneSpray στη χώρα σας.'),
'en':dict(nav='Network',eye='International network',h='Our partner network abroad',p='DroneSpray systems travel from Larissa across Europe. Contact us and we will put you in touch with the partner in your country.',sCountries='Export countries',sHq='Headquarters in Greece',cta='Find a partner',mapL='Map of DroneSpray export countries',hq='Larissa',
 listEye='Where we are',listH='Our countries',listP='Choose your country. We will reply and direct you to the nearest partner.',avail='Active network',find='Find a partner',
 c=dict(es='Spain',it='Italy',lv='Latvia',gb='United Kingdom',de='Germany',fr='France',hr='Croatia',ie='Ireland'),
 howH='How it works',steps=[['Contact','Send us a message through the form or WhatsApp, with your country.'],['Referral','We connect you with the partner serving your area.'],['Service','Delivery, training and local support.']],
 ctaH='Your country is not listed?',ctaP='The network is growing. Become the first DroneSpray partner in your country.'),
'es':dict(nav='Red',eye='Red internacional',h='Nuestra red de distribuidores en el extranjero',p='Los sistemas DroneSpray viajan desde Larisa a toda Europa. Contáctenos y le pondremos en contacto con el distribuidor de su país.',sCountries='Países de exportación',sHq='Sede en Grecia',cta='Buscar distribuidor',mapL='Mapa de países de exportación de DroneSpray',hq='Larisa',
 listEye='Dónde estamos',listH='Nuestros países',listP='Elija su país. Le responderemos y le dirigiremos al distribuidor más cercano.',avail='Red activa',find='Buscar distribuidor',
 c=dict(es='España',it='Italia',lv='Letonia',gb='Reino Unido',de='Alemania',fr='Francia',hr='Croacia',ie='Irlanda'),
 howH='Cómo funciona',steps=[['Contacto','Envíenos un mensaje por el formulario o WhatsApp, indicando su país.'],['Derivación','Le ponemos en contacto con el distribuidor de su zona.'],['Servicio','Entrega, formación y asistencia cercana.']],
 ctaH='¿Su país no aparece?',ctaP='La red está creciendo. Sea el primer distribuidor de DroneSpray en su país.'),
'it':dict(nav='Rete',eye='Rete internazionale',h='La nostra rete di partner all’estero',p='I sistemi DroneSpray viaggiano da Larissa in tutta Europa. Contattateci e vi metteremo in contatto con il partner del vostro paese.',sCountries='Paesi di esportazione',sHq='Sede in Grecia',cta='Trova un partner',mapL='Mappa dei paesi di esportazione DroneSpray',hq='Larissa',
 listEye='Dove siamo',listH='I nostri paesi',listP='Scegliete il vostro paese. Vi risponderemo e vi indirizzeremo al partner più vicino.',avail='Rete attiva',find='Trova un partner',
 c=dict(es='Spagna',it='Italia',lv='Lettonia',gb='Regno Unito',de='Germania',fr='Francia',hr='Croazia',ie='Irlanda'),
 howH='Come funziona',steps=[['Contatto','Inviateci un messaggio tramite il modulo o WhatsApp, indicando il vostro paese.'],['Indirizzamento','Vi mettiamo in contatto con il partner della vostra zona.'],['Assistenza','Consegna, formazione e supporto vicino a voi.']],
 ctaH='Il vostro paese non è nell’elenco?',ctaP='La rete sta crescendo. Diventate il primo partner DroneSpray nel vostro paese.')}
MSG={'el':'Γεια σας, θα ήθελα να επικοινωνήσω με τον συνεργάτη της DroneSpray στη χώρα: ','en':'Hello, I would like to contact the DroneSpray partner in: ','es':'Hola, me gustaría contactar con el distribuidor de DroneSpray en: ','it':'Salve, vorrei contattare il partner DroneSpray in: '}
for lang,anchor in [('el',"accNav:'Αξεσουάρ',"),('en',"accNav:'Accessories',"),('es',"accNav:'Accesorios',"),('it',"accNav:'Accessori',")]:
    j=json.dumps(N[lang],ensure_ascii=False)[:-1]+',msg:c=>'+json.dumps(MSG[lang],ensure_ascii=False)+'+c+"."}'
    r(anchor,"nw:"+j+","+anchor)
r(".acc-home{border-top:1px solid var(--line)}",""".acc-home{border-top:1px solid var(--line)}
.nw-hero{background:var(--ink);color:#e8e9e4;overflow:hidden}
.nw-hero .wrap{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:40px;align-items:center;padding-block:56px}
.nw-copy{display:flex;flex-direction:column;gap:16px;min-width:0}
.nw-hero .eyebrow{color:var(--yellow)}
.nw-hero h1{font-size:clamp(2.1rem,4.2vw,3.4rem);line-height:1.08;color:#fff}
.nw-hero p{color:#b9bbb3;font-size:1.1rem;max-width:32em}
.nw-stats{display:flex;gap:40px;margin-block:6px 10px}
.nw-stats div{display:flex;flex-direction:column;gap:4px;border-left:3px solid var(--yellow);padding-left:14px}
.nw-stats b{font-family:var(--model);font-size:2.8rem;line-height:1;color:#fff}
.nw-stats span{font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;color:#8d9088}
.nw-hero .btn.ghost{color:#fff;border-color:rgba(255,255,255,.4)}
.nw-hero .btn.ghost:hover{background:#fff;color:var(--ink);border-color:#fff}
.nw-map{width:100%;height:auto;display:block}
.nw-grid circle{fill:rgba(255,255,255,.07)}
.nw-arc{fill:none;stroke:var(--yellow);stroke-width:1.4;stroke-opacity:.75;stroke-dasharray:600;stroke-dashoffset:0;animation:nwDraw 1.6s ease both}
@keyframes nwDraw{from{stroke-dashoffset:600}to{stroke-dashoffset:0}}
.nw-pt circle{fill:#fff}.nw-pt .halo,.nw-hq .halo{fill:none;stroke:var(--yellow);stroke-opacity:.5;stroke-width:1.2}
.nw-pt text,.nw-hq text{fill:#e8e9e4;font-family:var(--display);font-weight:600;font-size:12px;letter-spacing:.06em}
.nw-hq circle{fill:var(--yellow)}.nw-hq text{fill:var(--yellow);font-size:13px}
@media (prefers-reduced-motion:reduce){.nw-arc{animation:none}}
.nw-grid-list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.nw-c{display:flex;flex-direction:column;gap:6px;padding:22px 20px;border:1px solid var(--line);background:var(--sheet);text-decoration:none;color:var(--ink);position:relative;overflow:hidden;transition:border-color .15s,transform .15s}
.nw-c::before{content:"";position:absolute;left:0;top:0;height:3px;width:0;background:var(--yellow);transition:width .25s}
.nw-c:hover{border-color:var(--ink);transform:translateY(-2px)}.nw-c:hover::before{width:100%}
.nw-code{font-family:var(--model);font-weight:700;font-size:2.4rem;line-height:1}
.nw-name{font-weight:700;font-size:1.05rem}
.nw-st{display:flex;align-items:center;gap:8px;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.nw-st::before{content:"";width:8px;height:8px;border-radius:50%;background:#2c8a4b}
.nw-go{margin-top:10px;font-family:var(--display);font-weight:600;font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ochre)}
.nw-steps{grid-template-columns:repeat(3,minmax(0,1fr))}
.nw-cta{background:var(--yellow);color:var(--on-yellow)}
.nw-cta .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px 32px;padding-block:40px}
.nw-cta h2{font-size:clamp(1.6rem,3vw,2.3rem)}.nw-cta p{margin-top:6px;max-width:36em}
.nw-cta .btn{background:var(--on-yellow);border-color:var(--on-yellow);color:#fff}.nw-cta .btn.ghost{background:transparent;color:var(--on-yellow)}
@media (max-width:900px){.nw-hero .wrap{grid-template-columns:minmax(0,1fr);padding-block:40px}.nw-grid-list{grid-template-columns:repeat(2,minmax(0,1fr))}.nw-steps{grid-template-columns:minmax(0,1fr)}}
@media (max-width:420px){.nw-grid-list{gap:10px}.nw-c{padding:16px 14px}.nw-code{font-size:2rem}}""")
open(p,'w',encoding='utf8').write(s)
