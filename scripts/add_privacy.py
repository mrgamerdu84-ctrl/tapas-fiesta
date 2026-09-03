from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

meta = '<meta name="privacy-policy-contact" content="mrgamerdu84@gmail.com">'
if meta not in s:
    s = s.replace('</head>', '  ' + meta + '\n</head>', 1)

style = r'''
<style id="tf-privacy-style">
#tfHomeLegal{
  margin:22px 4px 8px;padding:13px 12px 12px;text-align:center;
  color:#725848;font-size:.72rem;line-height:1.45;
}
#tfHomeLegal strong{color:#5C382B;}
#tfPrivacyOpen{
  display:inline-flex;align-items:center;justify-content:center;gap:6px;
  margin:0 0 8px;padding:9px 14px;border:1px solid rgba(0,110,101,.30);border-radius:999px;
  background:rgba(255,250,239,.92);color:#006E65;font:800 .76rem inherit;cursor:pointer;
  box-shadow:0 3px 8px rgba(75,45,25,.08);
}
#tfPrivacyPage{
  position:fixed;inset:0;z-index:2147483000;display:none;overflow:auto;
  background:#F8E8C9;
  background-image:linear-gradient(180deg,#FFF2D8 0%,#F8E8C9 100%);
}
#tfPrivacyPage.open{display:block;}
.tf-legal-header{
  position:sticky;top:0;z-index:4;display:flex;align-items:center;gap:12px;
  min-height:76px;padding:14px 16px;background:linear-gradient(120deg,#045B55,#00776C 56%,#075F58);
  border-bottom:6px solid #E3A72D;box-shadow:0 5px 16px rgba(22,63,54,.20);
}
#tfPrivacyClose{
  flex:0 0 auto;width:42px;height:42px;border-radius:50%;border:2px solid #E5C161;
  background:#FFF5D8;color:#6D3526;font-size:1.4rem;font-weight:900;cursor:pointer;
}
.tf-legal-header h2{
  margin:0;color:#FFF4D7;font-family:Georgia,'Times New Roman',serif;font-size:1.35rem;line-height:1.12;
  text-shadow:0 2px 0 rgba(80,36,24,.35);
}
.tf-legal-header p{margin:3px 0 0;color:#F2CE65;font-size:.7rem;font-weight:900;letter-spacing:.10em;text-transform:uppercase;}
.tf-legal-main{width:min(100% - 28px,560px);margin:20px auto 110px;}
.tf-legal-card{
  margin:0 0 14px;padding:18px 17px;background:linear-gradient(160deg,#FFFDF8,#FFF3DD);
  border:1px solid rgba(137,85,42,.22);border-radius:20px;box-shadow:0 8px 18px rgba(83,48,25,.10);
}
.tf-legal-card h3{margin:0 0 9px;color:#9E2C1F;font-family:Georgia,'Times New Roman',serif;font-size:1.08rem;}
.tf-legal-card p,.tf-legal-card li{font-size:.87rem;line-height:1.55;color:#4F392D;}
.tf-legal-card ul{margin:8px 0 0;padding-left:1.1rem;}
.tf-legal-card a{color:#006E65;font-weight:900;word-break:break-word;}
.tf-legal-icon{font-size:1.4rem;margin-right:6px;vertical-align:-2px;}
.tf-legal-final{text-align:center;color:#725848;font-size:.75rem;line-height:1.5;padding:8px 10px;}
.tf-legal-final strong{color:#5C382B;}
</style>
'''
if 'id="tf-privacy-style"' not in s:
    s = s.replace('</head>', style + '\n</head>', 1)

home_legal = r'''
    <div id="tfHomeLegal" aria-label="Informations légales">
      <button id="tfPrivacyOpen" type="button">🔒 Confidentialité • Contact • Droits</button><br>
      <strong>© 2026 tikowikoFamily</strong> — Tous droits réservés.
    </div>
'''
if 'id="tfHomeLegal"' not in s:
    marker = '    <div class="goal-box">🏆 <strong>But du jeu :</strong> être le premier cuistot à valider 3 Recettes Tapas complètes.</div>\n  </section>'
    if marker in s:
        s = s.replace(marker, marker.replace('\n  </section>', '\n' + home_legal + '  </section>'), 1)
    else:
        # Robust fallback: append inside the opening Accueil section.
        m = re.search(r'(<section class="view active" id="view-accueil">)(.*?)(</section>)', s, flags=re.S)
        if not m:
            raise SystemExit('ERROR: accueil section not found')
        replacement = m.group(1) + m.group(2) + home_legal + m.group(3)
        s = s[:m.start()] + replacement + s[m.end():]

page = r'''
<div id="tfPrivacyPage" role="dialog" aria-modal="true" aria-labelledby="tfPrivacyTitle">
  <header class="tf-legal-header">
    <button id="tfPrivacyClose" type="button" aria-label="Retour">←</button>
    <div>
      <h2 id="tfPrivacyTitle">Confidentialité & Contact</h2>
      <p>Droits et informations légales</p>
    </div>
  </header>

  <main class="tf-legal-main">
    <section class="tf-legal-card">
      <h3><span class="tf-legal-icon">🔒</span>Politique de confidentialité</h3>
      <p>Tapas Fiesta respecte la vie privée de ses utilisateurs.</p>
      <ul>
        <li>Aucun compte utilisateur n’est demandé dans cette version.</li>
        <li>Tapas Fiesta ne transmet pas de données personnelles à un serveur.</li>
        <li>Les informations nécessaires au déroulement d’une partie sont traitées localement dans l’application.</li>
        <li>Aucune donnée personnelle n’est vendue à des tiers.</li>
        <li>Aucune publicité ni outil de suivi analytique n’est intégré par Tapas Fiesta dans cette version.</li>
      </ul>
      <p>Si une future version ajoute une fonctionnalité nécessitant des données personnelles, cette page devra être mise à jour et les utilisateurs devront en être informés clairement.</p>
    </section>

    <section class="tf-legal-card">
      <h3><span class="tf-legal-icon">✉️</span>Contact</h3>
      <p>Pour toute question concernant l’application, la confidentialité ou les données personnelles :</p>
      <p><a href="mailto:mrgamerdu84@gmail.com">mrgamerdu84@gmail.com</a></p>
    </section>

    <section class="tf-legal-card">
      <h3><span class="tf-legal-icon">⚖️</span>Vos droits</h3>
      <p>Dans la version actuelle, l’application n’exige pas de compte et indique ne pas transmettre de données personnelles à un serveur.</p>
      <p>Si des données personnelles sont traitées dans une future version, vous pourrez contacter l’adresse ci-dessus pour toute demande concernant vos droits applicables, notamment l’accès, la rectification ou la suppression de vos données.</p>
    </section>

    <section class="tf-legal-card">
      <h3><span class="tf-legal-icon">©️</span>Droits d’auteur</h3>
      <p><strong>© 2026 tikowikoFamily — Tous droits réservés.</strong></p>
      <p>Les éléments originaux de Tapas Fiesta sont protégés par le droit d’auteur. Cette mention ne remplace pas les droits éventuels de tiers sur leurs propres contenus.</p>
    </section>

    <div class="tf-legal-final">
      Dernière mise à jour : 3 septembre 2026.<br>
      <strong>Contact : mrgamerdu84@gmail.com</strong>
    </div>
  </main>
</div>
<script id="tf-privacy-script">
(function(){
  var openBtn=document.getElementById('tfPrivacyOpen');
  var page=document.getElementById('tfPrivacyPage');
  var closeBtn=document.getElementById('tfPrivacyClose');
  if(!openBtn || !page || !closeBtn) return;
  function openPrivacy(){ page.classList.add('open'); page.scrollTop=0; document.body.style.overflow='hidden'; }
  function closePrivacy(){ page.classList.remove('open'); document.body.style.overflow=''; }
  openBtn.addEventListener('click',openPrivacy);
  closeBtn.addEventListener('click',closePrivacy);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape' && page.classList.contains('open')) closePrivacy(); });
})();
</script>
'''
if 'id="tfPrivacyPage"' not in s:
    s = s.replace('</body>', page + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Dedicated privacy/contact/rights page added')
