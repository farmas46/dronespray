import json
p='/home/claude/dronespray/index.html';s=open(p,encoding='utf8').read()
def r(a,b):
    global s
    assert s.count(a)==1,a[:70];s=s.replace(a,b)
D={
'el':dict(nav='Γίνε dealer',eye='DroneSpray | Pre-Mixing Systems',h='Θέλετε να γίνετε dealer της DroneSpray;',p='Αναζητούμε συνεργάτες σε Ελλάδα και εξωτερικό, για να φέρουν τα συστήματα ανάδευσης DroneSpray στους επαγγελματίες ψεκασμού με drone.',cta='Κάντε αίτηση',
 whyH='Γιατί DroneSpray',why=[['Πλήρης σειρά','Έξι μοντέλα από 110 έως 600 λίτρα και αξεσουάρ, για κάθε μέγεθος drone και κάθε πελάτη.'],['Υποστήριξη πωλήσεων','Φωτογραφίες, τεχνικά φυλλάδια και υλικό προώθησης για το κατάστημα και τα κανάλια σας.'],['Τεχνική κατάρτιση','Σας δείχνουμε τη λειτουργία και τη συντήρηση, για να εξυπηρετείτε τους πελάτες σας με σιγουριά.'],['Άμεση επικοινωνία','Μιλάτε απευθείας με την FARMA Κυράτσας, χωρίς ενδιάμεσους.']],
 whoH='Ποιους αναζητούμε',whoP='Επιχειρήσεις που ήδη εξυπηρετούν αγρότες ή επαγγελματίες ψεκασμού.',who=['Καταστήματα γεωργικών μηχανημάτων','Εταιρείες πώλησης γεωργικών drone','Παρόχους υπηρεσιών ψεκασμού με drone','Διανομείς γεωργικών εφοδίων'],
 stepsH='Πώς ξεκινάμε',steps=[['Αίτηση','Συμπληρώνετε τη φόρμα με τα στοιχεία της επιχείρησής σας.'],['Γνωριμία','Σας καλούμε για να συζητήσουμε την περιοχή και τις ανάγκες σας.'],['Συμφωνία','Ορίζουμε μαζί τους όρους της συνεργασίας.'],['Ξεκίνημα','Λαμβάνετε υλικό, κατάρτιση και τα πρώτα μηχανήματα.']],
 formH='Αίτηση συνεργασίας',formP='Πείτε μας λίγα λόγια για την επιχείρησή σας και θα επικοινωνήσουμε μαζί σας.',region='Περιοχή / Πόλη',biz='Τύπος επιχείρησης',other='Άλλο',web='Ιστοσελίδα (προαιρετικά)',direct='Προτιμάτε να μιλήσουμε;'),
'en':dict(nav='Become a dealer',eye='DroneSpray | Pre-Mixing Systems',h='Want to become a DroneSpray dealer?',p='We are looking for partners in Greece and abroad to bring DroneSpray mixing systems to professional drone spraying operators.',cta='Apply now',
 whyH='Why DroneSpray',why=[['Complete range','Six models from 110 to 600 litres plus accessories, for every drone size and every customer.'],['Sales support','Photos, technical sheets and promotional material for your store and your channels.'],['Technical training','We show you operation and maintenance, so you can serve your customers with confidence.'],['Direct contact','You work directly with FARMA Kyratsas, with no intermediaries.']],
 whoH='Who we are looking for',whoP='Businesses that already serve farmers or spraying professionals.',who=['Agricultural machinery dealers','Agricultural drone resellers','Drone spraying service providers','Farm supply distributors'],
 stepsH='How it works',steps=[['Apply','Fill in the form with your company details.'],['Introduction','We call you to talk about your area and your needs.'],['Agreement','We set the partnership terms together.'],['Launch','You receive material, training and your first machines.']],
 formH='Dealer application',formP='Tell us a little about your business and we will get back to you.',region='Region / City',biz='Type of business',other='Other',web='Website (optional)',direct='Prefer to talk?'),
'es':dict(nav='Ser distribuidor',eye='DroneSpray | Pre-Mixing Systems',h='¿Quiere ser distribuidor de DroneSpray?',p='Buscamos socios en Grecia y en el extranjero para llevar los sistemas de mezcla DroneSpray a los profesionales de la pulverización con drones.',cta='Solicitar',
 whyH='Por qué DroneSpray',why=[['Gama completa','Seis modelos de 110 a 600 litros y accesorios, para cada tamaño de dron y cada cliente.'],['Apoyo comercial','Fotos, fichas técnicas y material promocional para su tienda y sus canales.'],['Formación técnica','Le enseñamos el funcionamiento y el mantenimiento para que atienda a sus clientes con seguridad.'],['Contacto directo','Trabaja directamente con FARMA Kyratsas, sin intermediarios.']],
 whoH='A quién buscamos',whoP='Empresas que ya atienden a agricultores o a profesionales de la pulverización.',who=['Concesionarios de maquinaria agrícola','Distribuidores de drones agrícolas','Empresas de pulverización con drones','Distribuidores de suministros agrícolas'],
 stepsH='Cómo empezamos',steps=[['Solicitud','Rellene el formulario con los datos de su empresa.'],['Presentación','Le llamamos para hablar de su zona y sus necesidades.'],['Acuerdo','Definimos juntos las condiciones de colaboración.'],['Inicio','Recibe material, formación y sus primeras máquinas.']],
 formH='Solicitud de distribuidor',formP='Cuéntenos un poco sobre su empresa y nos pondremos en contacto con usted.',region='Región / Ciudad',biz='Tipo de empresa',other='Otro',web='Sitio web (opcional)',direct='¿Prefiere hablar?'),
'it':dict(nav='Diventa rivenditore',eye='DroneSpray | Pre-Mixing Systems',h='Volete diventare rivenditori DroneSpray?',p='Cerchiamo partner in Grecia e all’estero per portare i sistemi di miscelazione DroneSpray agli operatori professionali di irrorazione con droni.',cta='Candidatevi',
 whyH='Perché DroneSpray',why=[['Gamma completa','Sei modelli da 110 a 600 litri e accessori, per ogni dimensione di drone e ogni cliente.'],['Supporto commerciale','Foto, schede tecniche e materiale promozionale per il vostro negozio e i vostri canali.'],['Formazione tecnica','Vi mostriamo funzionamento e manutenzione, per servire i clienti con sicurezza.'],['Contatto diretto','Lavorate direttamente con FARMA Kyratsas, senza intermediari.']],
 whoH='Chi cerchiamo',whoP='Aziende che già servono agricoltori o professionisti dell’irrorazione.',who=['Rivenditori di macchine agricole','Rivenditori di droni agricoli','Servizi di irrorazione con droni','Distributori di forniture agricole'],
 stepsH='Come iniziamo',steps=[['Candidatura','Compilate il modulo con i dati della vostra azienda.'],['Conoscenza','Vi chiamiamo per parlare della vostra zona e delle vostre esigenze.'],['Accordo','Definiamo insieme le condizioni di collaborazione.'],['Avvio','Ricevete materiale, formazione e le prime macchine.']],
 formH='Candidatura rivenditore',formP='Raccontateci qualcosa della vostra azienda e vi ricontatteremo.',region='Regione / Città',biz='Tipo di attività',other='Altro',web='Sito web (facoltativo)',direct='Preferite parlarne?')}
for lang,anchor in [('el',"accNav:'Αξεσουάρ',"),('en',"accNav:'Accessories',"),('es',"accNav:'Accesorios',"),('it',"accNav:'Accessori',")]:
    r(anchor,"dl:"+json.dumps(D[lang],ensure_ascii=False)+","+anchor)
r("function accCards(list){",r"""function dealers(){const t=T[lang],d=t.dl,v=k=>esc(form[k]||'');
  const f=(id,label,type,req)=>`<div class="field"><label for="${id}">${label}${req?' *':''}</label><input id="${id}" name="${id}" type="${type}" value="${v(id)}" ${req?'required':''}></div>`;
  return `<section class="dl-hero"><div class="wrap"><div><span class="eyebrow">${d.eye}</span><h1>${d.h}</h1><p>${d.p}</p><a class="btn" href="#dealers" data-jump="dl-form">${d.cta} →</a></div><div class="dl-stack" aria-hidden="true"><img class="a" src="img/ds420.webp" alt=""><img class="b" src="img/ds600.webp" alt=""><img class="c" src="img/ds110.webp" alt=""></div></div></section>
<section class="band white"><div class="wrap"><div class="head"><h2>${d.whyH}</h2></div><div class="dl-why">${d.why.map(w=>`<div class="dl-card"><h3>${w[0]}</h3><p>${w[1]}</p></div>`).join('')}</div></div></section>
<section class="band"><div class="wrap dl-who"><div class="head"><h2>${d.whoH}</h2><p>${d.whoP}</p></div><ul class="chips">${d.who.map(w=>`<li>${w}</li>`).join('')}</ul></div></section>
<section class="band white"><div class="wrap"><div class="head"><h2>${d.stepsH}</h2></div><ol class="dl-steps">${d.steps.map((s,n)=>`<li><span class="num">0${n+1}</span><h3>${s[0]}</h3><p>${s[1]}</p></li>`).join('')}</ol></div></section>
<section class="band" id="dl-form"><div class="wrap"><div class="head"><h2>${d.formH}</h2><p>${d.formP}</p></div><div class="contact"><form id="form" novalidate>${f('name',t.fName,'text',true)}${f('company',t.fCompany,'text')}${f('region',d.region,'text')}${f('country',t.fCountry,'text')}${f('phone',t.fPhone,'tel')}${f('email','Email','email')}<div class="field"><label for="biz">${d.biz}</label><select id="biz" name="biz">${[...d.who,d.other].map(o=>`<option ${form.biz===o?'selected':''}>${o}</option>`).join('')}</select></div>${f('web',d.web,'url')}<div class="field full"><label for="msg">${t.fMsg}</label><textarea id="msg" name="msg">${v('msg')}</textarea></div><p class="err" id="err" role="alert" hidden></p><button class="btn" type="submit">${t.send} →</button><p class="notice ${formState==='ok'?'ok':''}" id="note" role="status">${formState==='ok'?t.okNote:t.demoNote}</p></form><aside class="company"><h2>${d.direct}</h2><dl><dd class="co">${CO.name}</dd><dt>${t.fPhone}</dt><dd>${PH()}</dd><dt>Email</dt><dd>${EM()}</dd><dt>${t.hours}</dt><dd>${CO.hours[lang]}</dd></dl></aside></div></div></section>`}
function accCards(list){""")
r("'pm20','accessories','contact'].includes(h)?h:'home'}","'pm20','accessories','dealers','contact'].includes(h)?h:'home'}")
r("view==='accessories'?accessories():product(view)","view==='accessories'?accessories():view==='dealers'?dealers():product(view)")
r("+ln('contact',t.contact,view==='contact');","+ln('dealers',t.dl.nav,view==='dealers')+ln('contact',t.contact,view==='contact');")
r("  const db=e.target.closest('#dd-btn');","  const j=e.target.closest('[data-jump]');if(j){e.preventDefault();const el=$(j.dataset.jump);if(el)el.scrollIntoView({behavior:'smooth'});return}\n  const db=e.target.closest('#dd-btn');")
r(".acc-home{border-top:1px solid var(--line)}",""".acc-home{border-top:1px solid var(--line)}
.dl-hero{background:var(--yellow);color:var(--on-yellow);overflow:hidden}
.dl-hero .wrap{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:40px;align-items:center;padding-block:56px 0}
.dl-hero .wrap>div:first-child{padding-bottom:56px}
.dl-hero .eyebrow{color:var(--on-yellow)}
.dl-hero h1{font-size:clamp(2.1rem,4.4vw,3.6rem);line-height:1.08;margin-top:10px}
.dl-hero p{font-size:1.15rem;max-width:32em;margin-top:16px}
.dl-hero .btn{background:var(--on-yellow);border-color:var(--on-yellow);color:#fff;margin-top:26px}
.dl-hero .btn:hover{background:#34362a;border-color:#34362a}
.dl-stack{position:relative;height:400px;align-self:end}
.dl-stack img{position:absolute;bottom:0;height:auto;filter:drop-shadow(0 14px 14px rgba(28,31,27,.28))}
.dl-stack .a{left:0;width:40%;bottom:8px}
.dl-stack .b{left:22%;width:56%;z-index:2}
.dl-stack .c{right:0;width:36%;bottom:12px}
.dl-why{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px}
.dl-card{border-top:4px solid var(--yellow);padding-top:16px;display:flex;flex-direction:column;gap:8px;min-width:0}
.dl-card h3{font-size:1.25rem}
.dl-card p{color:var(--muted)}
.dl-who{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:40px;align-items:center}
.dl-who .head{margin-bottom:0}
.chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:12px}
.chips li{background:var(--sheet);border:1px solid var(--ink);padding:12px 18px;font-weight:600}
.dl-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px}
.dl-steps li{display:flex;flex-direction:column;gap:8px;min-width:0;border-left:1px solid var(--line);padding-left:18px}
.dl-steps .num{font-family:var(--model);font-weight:700;font-size:2.6rem;line-height:1;color:var(--ochre)}
.dl-steps h3{font-size:1.25rem}
.dl-steps p{color:var(--muted)}
@media (max-width:900px){.dl-hero .wrap{grid-template-columns:minmax(0,1fr);gap:0;padding-top:40px}.dl-hero .wrap>div:first-child{padding-bottom:28px}.dl-stack{height:300px}.dl-why,.dl-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.dl-who{grid-template-columns:minmax(0,1fr);gap:24px}}
@media (max-width:520px){.dl-stack{height:220px}.dl-why,.dl-steps{grid-template-columns:minmax(0,1fr)}}""")
open(p,'w',encoding='utf8').write(s)
