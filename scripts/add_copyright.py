from pathlib import Path
import runpy

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

meta = '<meta name="copyright" content="© 2026 tikowikoFamily — Tous droits réservés">'
if meta not in s:
    s = s.replace('</head>', '  ' + meta + '\n</head>', 1)
p.write_text(s, encoding='utf-8')

# Gameplay stages kept in a fixed order: stable V7 -> Pièce Mexico -> Fiesta Games V8.
runpy.run_path('scripts/patch_coin_mexico_v71.py', run_name='__main__')
runpy.run_path('scripts/patch_fiesta_games_v8.py', run_name='__main__')

final_html = p.read_text(encoding='utf-8')
required = (
    'TF_MEXICO_COIN_V71',
    'function tfAnimateCoin(',
    'function tfRunWheelCoin(',
    'function tfRunMemory(',
    'function tfSpeak(',
    'Mémoire Mexico',
    'Panier Surprise',
    'Échange Fiesta',
    'Maximum 7 essais',
    'if(seg.type==="ingredient"||seg.type==="mystere")',
    'function runAiTurn()',
    'setTimeout(runAiTurn, 800)',
)
missing = [marker for marker in required if marker not in final_html]
if missing:
    raise SystemExit('ERROR: V8/stable gameplay validation failed: ' + ', '.join(missing))
if 'Mime un piment' in final_html:
    raise SystemExit('ERROR: old physical mime challenge still present')

# The new wheel must contain exactly the four Fiesta Game special types.
for special in ('type:"coin"', 'type:"memory"', 'type:"bonus"', 'type:"exchange"'):
    if special not in final_html:
        raise SystemExit('ERROR: missing V8 wheel special: ' + special)

print('Copyright + Pièce Mexico + V8 Fiesta Games added and validated')
