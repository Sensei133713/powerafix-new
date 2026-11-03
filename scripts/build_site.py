"""Build both language versions from shared prices and localized content.
Run with Python 3; no third-party packages required.
"""
from pathlib import Path
from seo_content import SEO
import html
import json
import posixpath
import hashlib

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://powerafix.com/'
WA = 'https://wa.me/46720256828'
PHONE = '+46 72 025 68 28'
EMAIL = 'info@powerafix.com'
PRICES = {'car': 590, 'van': 690, 'sprinter': 790, 'polish': 3500, 'interior': 600}
ROUTES = {'home':'index.html','prices':'hinnoittelu.html','gallery':'galleria.html','about':'meista.html','contact':'yhteystiedot.html','interior':'palvelut/sisapuhdistus.html','exterior':'palvelut/ulkopuhdistus.html','ceramic':'palvelut/keraamiset-pinnoitteet.html','special':'palvelut/erikoispalvelut.html'}
SERVICE_KEYS = ['interior','exterior','ceramic','special']
PHOTOS = dict(zip(SERVICE_KEYS,['sisa.jpg','ulko.jpg','pinnoitus.jpg','erikois.jpg']))

TEXT = {
 'sv': {
  'nav':['Hem','Priser','Galleri','Om oss','Kontakt'], 'services':'Tjänster', 'menu':'Meny', 'mainnav':'Huvudmeny', 'language':'Språk', 'skip':'Hoppa till innehållet', 'brand':'BILVÅRD · HAPARANDA', 'city':'Haparanda', 'book':'Boka tid', 'contact':'Kontakta oss', 'ask':'Begär offert', 'from':'Från', 'onrequest':'Pris på förfrågan', 'price':'Pris', 'prices':'Priser', 'allservices':'Alla tjänster', 'more':'Läs mer', 'seeprices':'Se priser', 'craft':'Noggrant arbete. Ett välvårdat resultat.', 'currency':'Alla priser anges i svenska kronor (SEK).', 'price_note':'Kontakta oss för pris på övriga behandlingar. Vid polering bedömer vi lackens skick och bekräftar priset innan arbetet påbörjas.',
  'home_title':'Bilvård i Haparanda.<br><span class="gradient-text">Glans som syns.</span>', 'home_intro':'Handtvätt, invändig rekond, polering och keramiska lackskydd på Norrmalmsvägen 18 i Haparanda. Boka bilvård efter din bils behov.', 'explore':'Upptäck våra tjänster', 'services_title':'Vad kan vi hjälpa dig med?', 'services_intro':'Från en ren kupé till en välvårdad lack. Välj den behandling som passar din bil.',
  'titles':{'home':'Bilvård i Haparanda','prices':'Priser','gallery':'Galleri','about':'Om oss','contact':'Kontakt','interior':'Invändig rekond','exterior':'Utvändig tvätt','ceramic':'Keramiska lackskydd','special':'Polering & specialbehandlingar'},
  'intros':{'prices':'Tydliga priser för din bilvård. Vi hjälper dig att välja rätt behandling.','gallery':'Se bilder från vårt bildgalleri – före och efter.','about':'Omsorgsfullt hantverk och ett intresse för välvårdade bilar.','contact':'Hör av dig så hittar vi en behandling och en tid som passar.'},
  'service':{
   'interior':{'tag':'En fräsch kupé. Ett omsorgsfullt resultat.','intro':'Invändig rengöring med hänsyn till bilens ytor och material.','heading':'Ge kupén lite extra omsorg','body':'Damm, smuts och vardagens spår påverkar känslan i bilen. Med invändig rekond får kupén den omsorg den behöver.','list':['Rengöring med hänsyn till material och skick','Fokus på en ren och välvårdad kupé','Berätta gärna om fläckar eller särskilda önskemål'],'note':'Vi går igenom behandlingens innehåll vid bokningen. Specialbehandlingar offereras separat.','label':'Invändig rekond','pricekey':'interior'},
   'exterior':{'tag':'Ren lack. En välvårdad helhet.','intro':'Skonsam utvändig handtvätt för personbilar, SUV:ar och skåpbilar.','heading':'Utvändig tvätt för din bil','body':'En noggrann handtvätt tar hand om smutsen på utsidan och lyfter bilens helhetsintryck. Välj pris efter biltyp.','list':['Personbil: 590 kr','SUV / skåpbil: 690 kr','Mercedes-Benz Sprinter: 790 kr','Husbil: pris efter bedömning','Invändig rekond bokas separat'],'note':'Priserna gäller utvändig tvätt. Kontakta oss om du önskar ytterligare behandlingar.'},
   'ceramic':{'tag':'Skydd för lacken. Djup i glansen.','intro':'Keramiskt lackskydd för en lättskött och välvårdad lack.','heading':'Ett lackskydd anpassat till bilen','body':'Ett keramiskt lackskydd appliceras på en noggrant förberedd yta. Behandlingens omfattning beror på lackens skick och vilket skydd du vill ha.','list':['Vi bedömer lackens skick','Förberedelse och eventuell polering planeras tillsammans','Vi hjälper dig att välja lämplig behandling'],'note':'Pris, behandling och tidsåtgång bekräftas efter bedömning.','label':'Keramiskt lackskydd'},
   'special':{'tag':'Omsorg ända ner i detaljerna.','intro':'Maskinpolering och specialbehandlingar efter bilens behov.','heading':'Lyft fram lackens glans','body':'Maskinpolering kan förbättra lackens glans och minska synliga tvättrepor. Vi bedömer ytan och väljer en lämplig behandling.','list':['Maskinpolering från 3 500 kr','Omfattningen anpassas efter lackens skick','Övriga specialbehandlingar: pris på förfrågan'],'note':'Det slutliga priset för polering bekräftas efter bedömning av bilen.','label':'Maskinpolering','pricekey':'polish'}
  },
  'price_labels':['Utvändig tvätt · personbil','Utvändig tvätt · SUV / skåpbil','Invändig rekond','Maskinpolering','Keramiskt lackskydd','Övriga specialbehandlingar','Utvändig tvätt · Mercedes-Benz Sprinter','Utvändig tvätt · husbil'],
  'why':'Omsorg om varje detalj', 'why_intro':'En välvårdad bil börjar med rätt behandling och en tydlig dialog.', 'values':[('Noggrant arbete','Vi utgår från bilens skick och tar hänsyn till ytor och material.'),('Tydlig dialog','Vi går igenom dina önskemål och kommer överens om arbetets omfattning.'),('En genomtänkt helhet','Från kupén till lacken – vi hjälper dig att välja rätt vård för bilen.')],
  'process_label':'SÅ GÅR DET TILL', 'process_title':'Ett bra resultat börjar med ett samtal.', 'steps':[('Berätta om din bil','Kontakta oss via WhatsApp, telefon eller e-post. Berätta vilken bil du har och vad du vill ha hjälp med.'),('Vi kommer överens','Vi går igenom bilens skick, behandlingens innehåll och priset innan arbetet börjar.'),('Hämta din bil','Hämta bilen vid avtalad tid. Fråga gärna om hur du bäst tar hand om ytorna efteråt.')],
  'cta_title':'Redo att ge din bil lite extra omsorg?', 'cta_text':'Hör av dig så hjälper vi dig att välja rätt behandling.', 'footer_text':'Noggrann bilvård i Haparanda.<br>Tvättad för hand. Omsorgsfullt behandlad.', 'address':'Adress', 'phone':'Telefon', 'email':'E-post', 'country':'Sverige', 'booking':'Tidsbokning', 'booking_text':'Kontakta oss för lediga tider.',
  'about_title':'Din bil förtjänar omsorg.', 'about_paras':['PoweraFix finns på Norrmalmsvägen 18 i Haparanda. Vi erbjuder utvändig tvätt, invändig rekond, polering och keramiska lackskydd.','För oss handlar bilvård om detaljerna: en ren kupé, en välvårdad lack och ett omsorgsfullt avslut.','Berätta om din bil och vad du vill uppnå. Vi hjälper dig att välja en passande behandling och kommer överens om arbetets omfattning innan vi börjar.'],
  'before':'Före', 'after':'Efter', 'car':'Bil', 'findus':'Hitta hit', 'openmap':'Öppna karta', 'message_title':'Skriv till oss', 'message_intro':'Fyll i uppgifterna och öppna ett färdigt meddelande i ditt e-postprogram. Skicka sedan meddelandet därifrån.', 'fields':['Förnamn','Efternamn','E-post','Telefon','Tjänst','Bilmärke och modell','Meddelande'], 'select':'Välj tjänst', 'other':'Övrigt / hjälp att välja', 'model_placeholder':'t.ex. Volvo V60 2020', 'message_placeholder':'Berätta vad du vill ha hjälp med…', 'send':'Öppna e-postmeddelande', 'direct_email':'Du kan också skriva direkt till',
  'faq_title':'Vanliga frågor', 'faqs':[('Hur bokar jag en tid?','Kontakta oss via WhatsApp, telefon eller e-post. Vi kommer överens om en tid och en behandling som passar din bil.'),('Vad ingår i tvättpriset?','Utvändig tvätt kostar 590 kr för personbil, 690 kr för SUV eller skåpbil och 790 kr för Mercedes-Benz Sprinter. Husbilar prissätts efter bedömning. Invändig rekond kostar 600 kr och bokas separat.'),('Vad kostar polering?','Maskinpolering kostar från 3 500 kr. Vi bedömer lackens skick och bekräftar det slutliga priset innan arbetet börjar.'),('Vad kostar keramiska lackskydd och andra behandlingar?','Pris lämnas på förfrågan. Berätta om din bil och önskad behandling så hjälper vi dig vidare.')]
 },
 'fi': {
  'nav':['Etusivu','Hinnat','Galleria','Meistä','Yhteystiedot'], 'services':'Palvelut', 'menu':'Valikko', 'mainnav':'Päävalikko', 'language':'Kieli', 'skip':'Siirry sisältöön', 'brand':'AUTONHOITO · HAAPARANTA', 'city':'Haaparanta', 'book':'Varaa aika', 'contact':'Ota yhteyttä', 'ask':'Pyydä tarjous', 'from':'Alkaen', 'onrequest':'Hinta kysyttäessä', 'price':'Hinta', 'prices':'Hinnat', 'allservices':'Kaikki palvelut', 'more':'Lue lisää', 'seeprices':'Katso hinnat', 'craft':'Huolellinen työ. Viimeistelty lopputulos.', 'currency':'Kaikki hinnat ovat Ruotsin kruunuina (SEK).', 'price_note':'Muiden käsittelyjen hinnat saat kysymällä. Myllytyksen lopullinen hinta vahvistetaan maalipinnan kunnon arvioinnin jälkeen ennen työn aloittamista.',
  'home_title':'Autonhoitoa Haaparannalla.<br><span class="gradient-text">Näkyvää kiiltoa.</span>', 'home_intro':'Käsinpesu, sisäfix, myllytys ja keraamiset pinnoitteet Haaparannalla, Norrmalmsvägen 18. Varaa autosi tarpeisiin sopiva käsittely.', 'explore':'Tutustu palveluihin', 'services_title':'Mitä voimme tehdä autollesi?', 'services_intro':'Puhtaista sisätiloista huoliteltuun maalipintaan. Valitse autollesi sopiva käsittely.',
  'titles':{'home':'Autonhoitoa Haaparannalla','prices':'Hinnat','gallery':'Galleria','about':'Meistä','contact':'Yhteystiedot','interior':'Sisäfix','exterior':'Ulkopesu','ceramic':'Keraamiset pinnoitteet','special':'Myllytys ja erikoispalvelut'},
  'intros':{'prices':'Selkeät hinnat autonhoitoon. Autamme valitsemaan sopivan käsittelyn.','gallery':'Tutustu kuvagallerian ennen- ja jälkeen-kuviin.','about':'Huolellista käsityötä ja kiinnostusta hyvin hoidettuihin autoihin.','contact':'Ota yhteyttä, niin sovitaan autollesi sopiva palvelu ja aika.'},
  'service':{
   'interior':{'tag':'Raikkaat sisätilat. Huolellinen lopputulos.','intro':'Sisäpuhdistus auton pinnat ja materiaalit huomioiden.','heading':'Anna sisätiloille huolenpitoa','body':'Pöly, lika ja arjen jäljet vaikuttavat auton viihtyisyyteen. Sisäfix tuo sisätiloihin niiden kaipaamaa huolenpitoa.','list':['Puhdistus materiaalien ja kunnon mukaan','Tavoitteena puhdas ja huoliteltu matkustamo','Kerro tahroista tai erityistoiveista varauksen yhteydessä'],'note':'Käymme palvelun sisällön läpi ajanvarauksen yhteydessä. Erikoiskäsittelyt hinnoitellaan erikseen.','label':'Sisäfix','pricekey':'interior'},
   'exterior':{'tag':'Puhdas pinta. Huoliteltu kokonaisuus.','intro':'Hellävarainen ulkopesu käsin henkilöautoille, SUV-autoille ja pakettiautoille.','heading':'Ulkopesu autosi mukaan','body':'Huolellinen käsinpesu poistaa ulkopintojen likaa ja kohentaa auton yleisilmettä. Valitse hinta ajoneuvotyypin mukaan.','list':['Henkilöauto: 590 kr','SUV / pakettiauto: 690 kr','Mercedes-Benz Sprinter: 790 kr','Matkailuauto: hinta tapauskohtaisesti','Sisäfix varataan erikseen'],'note':'Hinnat koskevat ulkopesua. Kysy lisää, jos toivot muita käsittelyjä.'},
   'ceramic':{'tag':'Suojaa pinnalle. Syvyyttä kiiltoon.','intro':'Keraaminen pinnoite helpottaa maalipinnan hoitoa ja ylläpitoa.','heading':'Autollesi sopiva pinnoitus','body':'Keraaminen pinnoite levitetään huolellisesti valmistellulle pinnalle. Käsittelyn laajuus riippuu maalipinnan kunnosta ja toivomastasi suojasta.','list':['Arvioimme maalipinnan kunnon','Suunnittelemme pohjatyöt ja mahdollisen kiillotuksen yhdessä','Autamme sopivan käsittelyn valinnassa'],'note':'Hinta, käsittely ja työn kesto vahvistetaan arvion perusteella.','label':'Keraaminen pinnoite'},
   'special':{'tag':'Viimeistelyä yksityiskohtia myöten.','intro':'Myllytys ja erikoiskäsittelyt autosi tarpeiden mukaan.','heading':'Tuo maalipinnan kiilto esiin','body':'Myllytys eli koneellinen kiillotus voi parantaa maalipinnan kiiltoa ja vähentää näkyviä pesunaarmuja. Arvioimme pinnan ja valitsemme sopivan käsittelyn.','list':['Myllytys alkaen 3 500 kr','Työn laajuus maalipinnan kunnon mukaan','Muut erikoiskäsittelyt: hinta kysyttäessä'],'note':'Myllytyksen lopullinen hinta vahvistetaan auton kunnon arvioinnin jälkeen.','label':'Myllytys','pricekey':'polish'}
  },
  'price_labels':['Ulkopesu · henkilöauto','Ulkopesu · SUV / pakettiauto','Sisäfix','Myllytys','Keraaminen pinnoite','Muut erikoiskäsittelyt','Ulkopesu · Mercedes-Benz Sprinter','Ulkopesu · matkailuauto'],
  'why':'Huolenpitoa jokaiseen yksityiskohtaan', 'why_intro':'Hyvin hoidettu auto alkaa sopivasta käsittelystä ja selkeästä keskustelusta.', 'values':[('Huolellinen työ','Lähdemme auton kunnosta ja huomioimme pinnat ja materiaalit.'),('Selkeä keskustelu','Käymme toiveesi läpi ja sovimme työn sisällöstä yhdessä.'),('Harkittu kokonaisuus','Sisätiloista maalipintaan – autamme valitsemaan autollesi sopivan hoidon.')],
  'process_label':'NÄIN PALVELU ETENEE', 'process_title':'Hyvä lopputulos alkaa keskustelusta.', 'steps':[('Kerro autostasi','Ota yhteyttä WhatsAppissa, puhelimitse tai sähköpostilla. Kerro auton malli ja millaista hoitoa toivot.'),('Sovitaan työstä','Käydään läpi auton kunto, palvelun sisältö ja hinta ennen työn aloittamista.'),('Nouda autosi','Noudat autosi sovittuna ajankohtana. Kysy samalla vinkit pintojen hoitoon ja ylläpitoon.')],
  'cta_title':'Valmis antamaan autollesi huolenpitoa?', 'cta_text':'Ota yhteyttä, niin autamme valitsemaan sopivan käsittelyn.', 'footer_text':'Huolellista autonhoitoa Haaparannalla.<br>Käsin pesty. Huolella viimeistelty.', 'address':'Osoite', 'phone':'Puhelin', 'email':'Sähköposti', 'country':'Ruotsi', 'booking':'Ajanvaraus', 'booking_text':'Kysy vapaita aikoja ottamalla yhteyttä.',
  'about_title':'Autosi ansaitsee huolellista hoitoa.', 'about_paras':['PoweraFix palvelee Haaparannalla osoitteessa Norrmalmsvägen 18. Tarjoamme ulkopesua, sisäfixiä, myllytystä ja keraamisia pinnoitteita.','Meille autonhoito on yksityiskohtiin keskittymistä: siistit sisätilat, puhdas maalipinta ja huolellinen viimeistely muodostavat kokonaisuuden.','Kerro autostasi ja toiveistasi. Autamme valitsemaan sopivan käsittelyn ja sovimme työn sisällöstä ennen aloittamista.'],
  'before':'Ennen', 'after':'Jälkeen', 'car':'Auto', 'findus':'Täältä löydät meidät', 'openmap':'Avaa kartta', 'message_title':'Kirjoita meille', 'message_intro':'Täytä tiedot ja avaa valmis viesti sähköpostiohjelmassasi. Lähetä viesti sieltä meille.', 'fields':['Etunimi','Sukunimi','Sähköposti','Puhelin','Palvelu','Auton merkki ja malli','Viesti'], 'select':'Valitse palvelu', 'other':'Muu / apua valintaan', 'model_placeholder':'esim. Volvo V60 2020', 'message_placeholder':'Kerro, millaista hoitoa toivot…', 'send':'Avaa sähköpostiviesti', 'direct_email':'Voit myös kirjoittaa suoraan osoitteeseen',
  'faq_title':'Usein kysytyt kysymykset', 'faqs':[('Miten varaan ajan?','Ota yhteyttä WhatsAppissa, puhelimitse tai sähköpostilla. Sovitaan autollesi sopiva käsittely ja ajankohta.'),('Mitä pesun hintaan sisältyy?','Ulkopesu maksaa henkilöautolle 590 kr, SUV- tai pakettiautolle 690 kr ja Mercedes-Benz Sprinterille 790 kr. Matkailuautot hinnoitellaan tapauskohtaisesti. Sisäfix maksaa 600 kr ja varataan erikseen.'),('Mitä myllytys maksaa?','Myllytys maksaa alkaen 3 500 kr. Arvioimme maalipinnan kunnon ja vahvistamme lopullisen hinnan ennen työn aloittamista.'),('Mitä pinnoitteet ja muut käsittelyt maksavat?','Hinta selviää kysymällä. Kerro autostasi ja toivomastasi käsittelystä, niin autamme eteenpäin.')]
 }
}

def e(s): return html.escape(str(s), quote=True)
def page_path(lang,key): return ('fi/' if lang=='fi' else '')+ROUTES[key]
def relative(current,target):
    path=posixpath.relpath(target,posixpath.dirname(current) or '.')
    return path.removesuffix('index.html') or './' if target.endswith('index.html') else path
def canonical(lang,key): return BASE+page_path(lang,key).removesuffix('index.html')
def amount(key,t):
    if not key: return t['onrequest']
    value=f'{PRICES[key]:,}'.replace(',','\u00a0')+' kr'
    return t['from']+' '+value if key=='polish' else value

def build(lang,key):
    t=TEXT[lang]; current=page_path(lang,key)
    url=lambda name:relative(current,page_path(lang,name))
    def asset(name):
        path=relative(current,'assets/'+name)
        if name.endswith(('.css','.js')):
            path+='?v='+hashlib.sha256((ROOT/'assets'/name).read_bytes()).hexdigest()[:10]
        return path
    title=t['titles'][key]
    def button(text,href,kind='primary'):
        external=' target="_blank" rel="noopener"' if href.startswith('https:') else ''
        return f'<a class="btn btn-{kind}" href="{e(href)}"{external}>{e(text)} ↗</a>'
    def heading():
        return f'<section class="page-heading"><div class="container"><span class="eyebrow">POWERAFIX / {e(t["city"].upper())}</span><h1>{e(title)}</h1><p>{e(t["intros"][key])}</p></div></section>'
    def cards(items, label=None, title=None, intro=None):
        header=f'<div class="section-header"><span class="eyebrow">{e(label or "POWERAFIX")}</span><h2 class="section-title">{e(title or t["why"])}</h2>'+ (f'<p class="section-subtitle">{e(intro)}</p>' if intro else '')+'</div>'
        content=''.join(f'<article class="feature-card"><span class="process-number">{n:02}</span><h3 class="feature-title">{e(a)}</h3><p class="feature-description">{e(b)}</p></article>' for n,(a,b) in enumerate(items,1))
        return f'<section class="section bg-darker"><div class="container">{header}<div class="grid grid-cols-1 md:grid-cols-3 gap-6">{content}</div></div></section>'
    def process(): return cards(t['steps'],t['process_label'],t['process_title'])
    def cta(): return f'<section class="section brand-cta"><div class="container text-center"><h2 class="section-title">{e(t["cta_title"])}</h2><p class="section-subtitle mb-8">{e(t["cta_text"])}</p>{button(t["book"]+" · WhatsApp",WA)} {button(t["contact"],url("contact"),"outline")}</div></section>'
    def social_links(large=False):
        facebook='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.51 1.5-3.9 3.78-3.9 1.09 0 2.23.2 2.23.2v2.46H15.2c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12Z"/></svg>'
        instagram='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
        links=''.join(f'<a class="social-link social-{name.lower()}" href="{href}" target="_blank" rel="noopener" aria-label="PoweraFix · {name}">{icon}<span>{name}</span><span aria-hidden="true">↗</span></a>' for name,href,icon in [('Facebook','https://www.facebook.com/p/Powerafix-61571460449785/',facebook),('Instagram','https://www.instagram.com/powerafix1/',instagram)])
        heading=('Följ oss på sociala medier' if lang=='sv' else 'Seuraa meitä somessa')
        return (f'<section class="contact-social"><h2>{heading}</h2><div class="social-links social-links-large">{links}</div></section>' if large else f'<div class="social-links">{links}</div>')
    def wash_includes():
        heading='Alla utvändiga tvättar inkluderar' if lang=='sv' else 'Kaikki ulkopesut sisältävät'
        steps=['Förtvätt','Borttagning av tjära, flygrost och salt','Handtvätt','Wet Coat – snabbförsegling','Torkning'] if lang=='sv' else ['Esipesu','Pien, raudan ja suolan poisto','Käsinpesu','Wet Coat eli pikapinnoite','Kuivaus']
        items=''.join(f'<li><span aria-hidden="true">✓</span>{e(step)}</li>' for step in steps)
        return f'<aside class="service-note wash-includes"><h3>{e(heading)}</h3><ul class="care-list">{items}</ul></aside>'
    def price_cards(keys):
        pricekeys=['car','van','interior','polish',None,None,'sprinter',None]
        pages=['exterior','exterior','interior','special','ceramic','special','exterior','exterior']
        result=''
        for i in keys:
            p=pricekeys[i]; val=amount(p,t)
            if i==7: val='Pris efter bedömning' if lang=='sv' else 'Hinta tapauskohtaisesti'
            result+=f'<article class="price-tile"><span class="eyebrow">{e(t["prices"])}</span><h3>{e(t["price_labels"][i])}</h3><p class="price-value'+(' price-on-request' if p is None else '')+f'">{e(val)}</p>{button(t["book"] if p else t["ask"],WA,"primary" if p else "outline")}<a class="price-detail" href="{e(url(pages[i]))}">{e(t["more"])} →</a></article>'
        return f'<div class="price-tiles">{result}</div>'
    def price_section(indices):
        section_title=('Våra behandlingar' if lang=='sv' else 'Palveluhinnasto') if key=='prices' else t['titles'][key]
        return f'<section class="section"><div class="container"><div class="section-header"><span class="eyebrow">{e(t["prices"])}</span><h2 class="section-title">{e(section_title)}</h2><p class="section-subtitle">{e(t["currency"])}</p></div>{price_cards(indices)}{wash_includes() if key in ("prices","exterior") else ""}<p class="price-note">{e(t["price_note"])}</p></div></section>'

    if key=='home':
        hero=f'<section class="hero"><div class="hero-bg"><img src="{asset("images/axhzu.jpg")}" alt="" aria-hidden="true" fetchpriority="high"></div><div class="hero-overlay"></div><div class="hero-content"><div class="hero-badge"><span class="hero-badge-dot"></span>POWERAFIX · {e(t["city"].upper())}</div><h1 class="hero-title">{t["home_title"]}</h1><p class="hero-subtitle">{e(t["home_intro"])}</p><div class="hero-buttons">{button(t["book"],WA)}{button(t["explore"],"#palvelut","outline")}</div></div></section>'
        tiles=''.join(f'<a class="service-card" href="{url(k)}"><div class="service-card-image"><img src="{asset("images/"+PHOTOS[k])}" alt="{e(t["titles"][k])}" loading="lazy"><div class="service-card-content"><h3 class="service-card-title">{e(t["titles"][k])}</h3><p class="service-card-description">{e(t["service"][k]["intro"])}</p><span class="service-card-link">{e(t["more"])} →</span></div></div></a>' for k in SERVICE_KEYS)
        body=hero+f'<section class="section" id="palvelut"><div class="container"><div class="section-header"><span class="eyebrow">{e(t["services"])}</span><h2 class="section-title">{e(t["services_title"])}</h2><p class="section-subtitle">{e(t["services_intro"])}</p></div><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">{tiles}</div></div></section>'
        body+=f'<section class="section"><div class="container"><div class="section-header"><span class="eyebrow">{e(t["prices"])}</span><h2 class="section-title">{e(t["seeprices"])}</h2><p class="section-subtitle">{e(t["currency"])}</p></div>{price_cards([0,1,6,7,2,3])}{wash_includes()}<p class="price-note"><a href="{url("prices")}">{e(t["seeprices"])} →</a></p></div></section>'+process()+cta()
    elif key in SERVICE_KEYS:
        s=t['service'][key]
        body=f'<section class="detail-hero"><div class="container detail-hero-layout"><div><a class="breadcrumb" href="{url("home")}#palvelut">← {e(t["allservices"])}</a><span class="eyebrow">POWERAFIX / {e(t["services"].upper())}</span><h1>{e(title)} {'i Haparanda' if lang=='sv' else 'Haaparannalla'}</h1><p class="detail-lead">{e(s["tag"])}</p><p>{e(s["intro"])}</p><div class="detail-actions">{button(t["book"],WA)}{button(t["seeprices"],"#priser","outline")}</div></div><figure><img src="{asset("images/"+PHOTOS[key])}" alt="{e(title)}" fetchpriority="high"><figcaption>{e(t["craft"])}</figcaption></figure></div></section>'
        li=''.join(f'<li><span aria-hidden="true">✓</span>{e(line)}</li>' for line in s['list'])
        body+=f'<section class="section"><div class="container service-description-grid"><div><span class="eyebrow">{e(t["services"])}</span><h2 class="section-title">{e(s["heading"])}</h2><p class="section-subtitle">{e(s["body"])}</p><ul class="care-list">{li}</ul></div><aside class="service-note"><span class="eyebrow">POWERAFIX</span><h3>{e(t["contact"])}</h3><p>{e(s["note"])}</p>{button(t["contact"],url("contact"),"outline")}</aside></div></section>'
        indices={'interior':[2],'exterior':[0,1,6,7],'ceramic':[4],'special':[3,5]}[key]
        body+='<div id="priser">'+price_section(indices)+'</div>'
        if key=='special':
            extras=(['Lackskyddsfilm (PPF)','Fälgskydd','Glasbehandling','Strålkastarrenovering','Motortvätt','Lädervård','Luktbehandling'] if lang=='sv' else ['Maalinsuojakalvo (PPF)','Vanteiden pinnoitus','Lasinpinnoite','Ajovaloumpioiden kunnostus','Moottoritilan puhdistus','Nahanhoito','Hajunpoisto'])
            extra_cards=''.join(f'<article class="special-service-card"><span class="eyebrow">{n:02}</span><h3 class="special-service-title">{e(name)}</h3><p class="special-service-price">{e(t["onrequest"])}</p></article>' for n,name in enumerate(extras,1))
            body+=f'<section class="section bg-darker"><div class="container"><div class="section-header"><h2 class="section-title">{e(t["price_labels"][5])}</h2><p class="section-subtitle">{e(t["cta_text"])}</p></div><div class="special-services-grid">{extra_cards}</div></div></section>'
        body+=cta()
    elif key=='prices': body=heading()+price_section([0,1,6,7,2,3,4,5])+cta()
    elif key=='about':
        paras=''.join(f'<p>{e(p)}</p>' for p in t['about_paras'])
        body=heading()+f'<section class="section"><div class="container about-content"><div class="about-text"><span class="eyebrow">POWERAFIX</span><h2 class="section-title">{e(t["about_title"])}</h2>{paras}{button(t["contact"],url("contact"),"outline")}</div><div class="about-image"><img src="{asset("images/powerafix-character.png")}" alt="PoweraFix" loading="lazy"></div></div></section>'+cards(t['values'],title=t['why'],intro=t['why_intro'])+process()+cta()
    elif key=='gallery':
        photos=''.join(f'<figure class="portfolio-card"><img src="{asset(f"images/auto{i}-{state}.jpeg")}" alt="{e(t["car"])} {i}, {e(t[label].lower())}" loading="lazy"><figcaption><span>{e(t["car"])} {i:02}</span><strong>{e(t[label])}</strong></figcaption></figure>' for i in range(1,4) for state,label in [('ennen','before'),('jalkeen','after')])
        body=heading()+f'<section class="section"><div class="container"><div class="portfolio-grid">{photos}</div></div></section>'+cta()
    else:
        contact_cards=[(t['address'],f'Norrmalmsvägen 18<br>95334 Haparanda, {e(t["country"])}'),(t['phone'],f'<a href="tel:+46720256828">{PHONE}</a><br><a href="{WA}" target="_blank" rel="noopener">WhatsApp (SE): {PHONE}</a><br><a href="https://wa.me/358465549098" target="_blank" rel="noopener">WhatsApp (FI): +358 46 554 9098</a>'),(t['email'],f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),(t['booking'],e(t['booking_text']))]
        contact_cards += [('Org. Nr', '559300-2610'), ('Faktureringsadress' if lang=='sv' else 'Laskutusosoite', f'<a href="mailto:{EMAIL}">{EMAIL}</a>')]
        infos=''.join(f'<article class="contact-info-card"><h2>{e(a)}</h2><p>{b}</p></article>' for a,b in contact_cards)
        fields=''
        for idx,(name,typ) in enumerate([('firstName','text'),('lastName','text'),('email','email'),('phone','tel')]):
            required=' required' if idx<3 else ''
            auto=['given-name','family-name','email','tel'][idx]
            fields+=f'<div class="form-group"><label class="form-label" for="{name}">{e(t["fields"][idx])}'+(' *' if idx<3 else '')+f'</label><input class="form-input" id="{name}" name="{name}" type="{typ}" autocomplete="{auto}"{required}></div>'
        opts=''.join(f'<option value="{e(t["titles"][k])}">{e(t["titles"][k])}</option>' for k in SERVICE_KEYS)
        form=f'<form id="contactForm" class="contact-form"><div class="form-row">{fields[:fields.index(chr(60)+"div class=\"form-group\"><label class=\"form-label\" for=\"email\"")]}</div>{fields[fields.index(chr(60)+"div class=\"form-group\"><label class=\"form-label\" for=\"email\""):]}<div class="form-group"><label class="form-label" for="service">{e(t["fields"][4])}</label><select class="form-input" id="service" name="service"><option value="">{e(t["select"])}</option>{opts}<option>{e(t["other"])}</option></select></div><div class="form-group"><label class="form-label" for="carModel">{e(t["fields"][5])}</label><input id="carModel" name="carModel" class="form-input" placeholder="{e(t["model_placeholder"])}"></div><div class="form-group"><label class="form-label" for="message">{e(t["fields"][6])} *</label><textarea id="message" name="message" class="form-textarea" rows="5" placeholder="{e(t["message_placeholder"])}" required></textarea></div><button type="submit" class="btn btn-primary">{e(t["send"])} ↗</button><p id="formStatus" role="status" aria-live="polite"></p></form>'
        location=f'<div class="location-panel"><span class="eyebrow">POWERAFIX / {e(t["city"].upper())}</span><h3>{e(t["findus"])}</h3><p>Norrmalmsvägen 18<br>95334 Haparanda, {e(t["country"])}</p>{button(t["openmap"],"https://www.google.com/maps/search/?api=1&query=Norrmalmsv%C3%A4gen+18+95334+Haparanda","outline")}</div>'
        wash_answer='Alla utvändiga tvättar inkluderar förtvätt, borttagning av tjära, flygrost och salt, handtvätt, Wet Coat (snabbförsegling) samt torkning.' if lang=='sv' else 'Kaikki ulkopesut sisältävät esipesun, pien, raudan ja suolan poiston, käsinpesun, Wet Coat -pikapinnoitteen sekä kuivauksen.'
        faq_items=[(q,a+' '+wash_answer if i==1 else a) for i,(q,a) in enumerate(t['faqs'])]
        faqs=''.join(f'<details class="faq-native"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in faq_items)
        body=heading()+f'<section class="section"><div class="container"><div class="contact-info-grid">{infos}</div>{social_links(True)}</div></section><section class="section"><div class="container contact-content"><div class="contact-form-section"><h2 class="section-title">{e(t["message_title"])}</h2><p class="mb-8">{e(t["message_intro"])}</p>{form}<p class="direct-email">{e(t["direct_email"])} <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div><div>{location}</div></div></section><section class="section"><div class="container"><div class="section-header"><h2 class="section-title">{e(t["faq_title"])}</h2></div><div class="faq-container">{faqs}</div></div></section>'+cta()

    # Every language link points to the equivalent page; navigation stays in that language.
    nav=''
    for n,k in enumerate(['home','prices','gallery','about','contact']):
        active=' aria-current="page"' if k==key else ''
        nav+=f'<a href="{url(k)}"{active}>{e(t["nav"][n])}</a>'
        if n==0:
            links=''.join(f'<a href="{url(s)}"'+(' aria-current="page"' if s==key else '')+f'>{e(t["titles"][s])}</a>' for s in SERVICE_KEYS)
            nav+=f'<details class="site-dropdown"><summary>{e(t["services"])}</summary><div>{links}</div></details>'
    langs=''.join(f'<a href="{relative(current,page_path(l,key))}" lang="{l}" hreflang="{l}"'+(' aria-current="true"' if l==lang else '')+f'>{label}</a>' for l,label in [('sv','Svenska'),('fi','Suomi')])
    language=f'<div class="language-switch" role="group" aria-label="{e(t["language"])}">{langs}</div>'
    header=f'<a class="skip-link" href="#main">{e(t["skip"])}</a><header class="site-header"><div class="site-nav container"><a class="site-brand" href="{url("home")}" aria-label="PoweraFix — {e(t["nav"][0])}"><img src="{asset("images/powerafix-logo.png")}" alt="PoweraFix"><span>POWERAFIX<small>{e(t["brand"])}</small></span></a><button class="site-menu-toggle" aria-expanded="false" aria-controls="site-menu">{e(t["menu"])} <span aria-hidden="true">☰</span></button><nav class="site-menu" id="site-menu" aria-label="{e(t["mainnav"])}">{nav}{language}{button(t["book"],WA)}</nav></div></header>'
    footer_links=''.join(f'<a href="{url(s)}">{e(t["titles"][s])}</a>' for s in SERVICE_KEYS)
    footer=f'<footer class="site-footer"><div class="container footer-layout"><div><a class="footer-wordmark" href="{url("home")}">POWERAFIX<span>.</span></a><p>{t["footer_text"]}</p></div><div><h2>{e(t["services"])}</h2>{footer_links}</div><div><h2>{e(t["contact"])}</h2><a href="tel:+46720256828">{PHONE}</a><a href="{WA}" target="_blank" rel="noopener">WhatsApp (SE): {PHONE}</a><a href="https://wa.me/358465549098" target="_blank" rel="noopener">WhatsApp (FI): +358 46 554 9098</a><a href="mailto:{EMAIL}">{EMAIL}</a><p>Norrmalmsvägen 18<br>95334 Haparanda, {e(t["country"])}</p></div></div><div class="container footer-base"><span>© PoweraFix</span>{language}{social_links()}</div></footer><a class="contact-float" href="{WA}" target="_blank" rel="noopener" aria-label="{e(t["contact"])} · WhatsApp">WhatsApp ↗</a>'
    seo_title,desc=SEO[lang][key]
    schema={'@context':'https://schema.org','@type':'AutoWash','name':'PoweraFix','url':canonical(lang,'home'),'telephone':'+46720256828','email':EMAIL,'address':{'@type':'PostalAddress','streetAddress':'Norrmalmsvägen 18','postalCode':'95334','addressLocality':'Haparanda','addressCountry':'SE'},'currenciesAccepted':'SEK','identifier':{'@type':'PropertyValue','propertyID':'Org. Nr','value':'559300-2610'}}
    schema.update({'@id':BASE+'#business','url':BASE,'image':BASE+'assets/images/powerafix-banner.jpg','logo':BASE+'assets/images/powerafix-logo.png','sameAs':['https://www.facebook.com/p/Powerafix-61571460449785/','https://www.instagram.com/powerafix1/']})
    graph=[schema,{'@type':'WebSite','@id':BASE+'#website','url':BASE,'name':'PoweraFix','inLanguage':['sv','fi'],'publisher':{'@id':BASE+'#business'}}, {'@type':'WebPage','@id':canonical(lang,key)+'#webpage','url':canonical(lang,key),'name':seo_title+' | PoweraFix','description':desc,'inLanguage':lang,'isPartOf':{'@id':BASE+'#website'},'about':{'@id':BASE+'#business'}}]
    if key in SERVICE_KEYS:
        graph.append({'@type':'Service','@id':canonical(lang,key)+'#service','name':title,'serviceType':title,'provider':{'@id':BASE+'#business'},'areaServed':{'@type':'City','name':'Haparanda'},'url':canonical(lang,key),'description':t['service'][key]['intro']})
    if key!='home':
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':t['nav'][0],'item':canonical(lang,'home')},{'@type':'ListItem','position':2,'name':title,'item':canonical(lang,key)}]})
        body=f'<nav class="container seo-breadcrumb" aria-label="Breadcrumb"><a href="{url("home")}">{e(t["nav"][0])}</a><span aria-hidden="true"> / </span><span>{e(title)}</span></nav>'+body
    schema={'@context':'https://schema.org','@graph':graph}
    hreflang=''.join(f'<link rel="alternate" hreflang="{l}" href="{canonical(l,key)}">' for l in ['sv','fi'])+f'<link rel="alternate" hreflang="x-default" href="{canonical("sv",key)}">'
    result=f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(seo_title)} | PoweraFix</title><meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="PoweraFix">
<meta property="og:title" content="{e(seo_title)} | PoweraFix"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical(lang,key)}"><meta property="og:locale" content="{'sv_SE' if lang=='sv' else 'fi_FI'}">
<meta property="og:image" content="{BASE}assets/images/powerafix-banner.jpg"><meta property="og:image:alt" content="PoweraFix — {e(t['brand'])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical(lang,key)}">{hreflang}
<link rel="icon" type="image/png" href="{asset('images/powerafix-logo.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('css/style.css')}"><link rel="stylesheet" href="{asset('css/refinement.css')}">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
</head><body>
{header}
<main id="main">{body}</main>
{footer}
<script src="{asset('js/main.js')}" defer></script>
</body></html>
'''
    dest=ROOT/current;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(result,encoding='utf-8')

if __name__=='__main__':
    for language in TEXT:
        for page in ROUTES: build(language,page)
    urls = [canonical(language, page) for language in TEXT for page in ROUTES]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += '\n'.join('<url><loc>' + e(url) + '</loc></url>' for url in urls)
    (ROOT/'sitemap.xml').write_text(sitemap+'\n</urlset>\n', encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'sitemap.xml\n', encoding='utf-8')
    print('Built 18 pages: Swedish default and Finnish, using shared SEK prices.')
