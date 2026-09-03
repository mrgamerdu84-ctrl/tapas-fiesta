from pathlib import Path
import runpy

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

meta = '<meta name="copyright" content="© 2026 tikowikoFamily — Tous droits réservés">'
if meta not in s:
    s = s.replace('</head>', '  ' + meta + '\n</head>', 1)

# The visible copyright is now rendered by scripts/add_privacy.py at the bottom
# of the opening screen, next to the legal-page entry point. Keeping only the
# metadata here avoids duplicate copyright blocks elsewhere in the app.
p.write_text(s, encoding='utf-8')

# Final gameplay feature stage: replace the old physical/mime challenge with
# the Pièce Mexico duel. It runs here so the following privacy step and the
# Node JavaScript validation both see the exact HTML that will ship in Android.
runpy.run_path('scripts/patch_coin_mexico_v71.py', run_name='__main__')

final_html = p.read_text(encoding='utf-8')
required = (
    'TF_MEXICO_COIN_V71',
    'function tfAnimateCoin(',
    'function wireMexicoCoinDuel(',
    'player.hand[seg.key]++;',
    'function runAiTurn()',
)
missing = [marker for marker in required if marker not in final_html]
if missing:
    raise SystemExit('ERROR: Pièce Mexico/stable gameplay validation failed: ' + ', '.join(missing))
if 'Mime un piment' in final_html:
    raise SystemExit('ERROR: old physical mime challenge still present')

print('Copyright metadata + Pièce Mexico challenge added and validated')
