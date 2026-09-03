from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

meta = '<meta name="privacy-policy-contact" content="mrgamerdu84@gmail.com">'
if meta not in s:
    s = s.replace('</head>', '  ' + meta + '\n</head>', 1)

style = r'''
<style id="tf-privacy-style">
#tfPrivacyOpen{
  margin-top:8px;padding:7px 12px;border:1px solid rgba(122,93,73,.30);border-radius:999px;
  background:rgba(255,250,239,.82);color:#006E65;font:700 .74rem inherit;cursor:pointer;
}
#tfPrivacyOverlay{
  position:fixed;inset:0;z-index:2147483000;display:none;align-items:flex-end;justify-content:center;
  padding:18px;background:rgba(36,23,16,.55);backdrop-filter:blur(5px);
}
#tfPrivacyOverlay.open{display:flex;}
.tf-privacy-card{
  width:min(100%,520px);max-height:82vh;overflow:auto;padding:22px 20px 24px;
  background:linear-gradient(160deg,#FFFDF8,#FFF2D9);color:#382318;
  border:2px solid #D7A84B;border-radius:24px 24px 18px 18px;
  box-shadow:0 20px 50px rgba(31,18,12,.35);position:relative;
}
.tf-privacy-card h2{margin:0 42px 14px 0;font-family:Georgia,'Times New Roman',serif;color:#006E65;font-size:1.55rem;}
.tf-privacy-card h3{margin:18px 0 7px;color:#9E2C1F;font-size:1rem;}
.tf-privacy-card p,.tf-privacy-card li{font-size:.88rem;line-height:1.5;}
.tf-privacy-card ul{padding-left:1.15rem;}
.tf-privacy-card a{color:#006E65;font-weight:800;}
#tfPrivacyClose{
  position:absolute;right:14px;top:13px;width:36px;height:36px;border-radius:50%;border:1px solid #D7A84B;
  background:#FFF8E8;color:#9E2C1F;font-size:1.25rem;font-weight:900;cursor:pointer;
}
.tf-privacy-note{margin-top:18px;padding-top:12px;border-top:1px solid rgba(100,64,35,.18);font-size:.75rem!important;color:#786253;}
</style>
'''
if 'id="tf-privacy-style"' not in s:
    s = s.replace('</head>', style + '\n</head>', 1)

if 'id="tfPrivacyOpen"' not in s:
    pattern = r'(<div id="tfCopyright"[^>]*>.*?)(</div>)'
    repl = r'''\1<br><button id="tfPrivacyOpen" type="button">Confidentialité & contact</button>\2'''
    s, count = re.subn(pattern, repl, s, count=1, flags=re.S)
    if count != 1:
        raise SystemExit('ERROR: copyright footer not found for privacy link')

modal = r'''
<div id="tfPrivacyOverlay" role="dialog" aria-modal="true" aria-labelledby="tfPrivacyTitle">
  <div class="tf-privacy-card">
    <button id="tfPrivacyClose" type="button" aria-label="Fermer">×</button>
    <h2 id="tfPrivacyTitle">Politique de confidentialité</h2>
    <p>Tapas Fiesta respecte la vie privée de ses utilisateurs.</p>

    <h3>Données personnelles</h3>
    <ul>
      <li>Aucun compte utilisateur n’est demandé dans cette version.</li>
      <li>Tapas Fiesta ne transmet pas de données personnelles à un serveur.</li>
      <li>Les informations nécessaires au déroulement d’une partie sont traitées localement dans l’application.</li>
      <li>Aucune donnée personnelle n’est vendue à des tiers.</li>
      <li>Aucune publicité ni outil de suivi analytique n’est intégré par Tapas Fiesta dans cette version.</li>
    </ul>
    <p>Si une future version ajoute une fonctionnalité nécessitant des données personnelles, cette politique devra être mise à jour et les utilisateurs devront en être informés.</p>

    <h3>Contact</h3>
    <p>Pour toute question concernant la confidentialité, les données personnelles ou l’application :<br>
      <a href="mailto:mrgamerdu84@gmail.com">mrgamerdu84@gmail.com</a>
    </p>

    <p class="tf-privacy-note">Dernière mise à jour : 3 septembre 2026.<br>© 2026 tikowikoFamily — Tous droits réservés.</p>
  </div>
</div>
<script id="tf-privacy-script">
(function(){
  var openBtn=document.getElementById('tfPrivacyOpen');
  var overlay=document.getElementById('tfPrivacyOverlay');
  var closeBtn=document.getElementById('tfPrivacyClose');
  if(!openBtn || !overlay || !closeBtn) return;
  function openPrivacy(){ overlay.classList.add('open'); document.body.style.overflow='hidden'; }
  function closePrivacy(){ overlay.classList.remove('open'); document.body.style.overflow=''; }
  openBtn.addEventListener('click',openPrivacy);
  closeBtn.addEventListener('click',closePrivacy);
  overlay.addEventListener('click',function(e){ if(e.target===overlay) closePrivacy(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closePrivacy(); });
})();
</script>
'''
if 'id="tfPrivacyOverlay"' not in s:
    s = s.replace('</body>', modal + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Privacy policy and contact added')
