from pathlib import Path
import runpy

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

meta = '<meta name="copyright" content="© 2026 tikowikoFamily — Tous droits réservés">'
if meta not in s:
    s = s.replace('</head>', '  ' + meta + '\n</head>', 1)
p.write_text(s, encoding='utf-8')

# Gameplay stages: stable V7 -> Pièce Mexico -> Fiesta Games V8 -> V8.1 -> V8.2 -> V9 -> V9.1 -> V10 Mobile.
runpy.run_path('scripts/patch_coin_mexico_v71.py', run_name='__main__')
runpy.run_path('scripts/patch_fiesta_games_v8.py', run_name='__main__')
runpy.run_path('scripts/fix_v81_memory_wheel_ai.py', run_name='__main__')
runpy.run_path('scripts/fix_v82_visibility.py', run_name='__main__')
runpy.run_path('scripts/patch_gameplay_v9.py', run_name='__main__')
runpy.run_path('scripts/patch_memory_voice_v91.py', run_name='__main__')
runpy.run_path('scripts/patch_mobile_v10.py', run_name='__main__')
runpy.run_path('scripts/patch_developer_splash_v10.py', run_name='__main__')

final_html = p.read_text(encoding='utf-8')
required = (
    'TF_MEXICO_COIN_V71',
    'function tfAnimateCoin(',
    'function tfRunWheelCoin(',
    'function tfRunMemory(',
    'function tfSpeak(',
    'Mémoire Duel',
    'Panier Surprise',
    'Échange Fiesta',
    'function runAiTurn()',
    'setTimeout(runAiTurn, 800)',
    'tf-v81-fixes',
    'tf-v82-visibility',
    'aria-label="Légende de la roue"',
    'tfAiWheelCoin',
    'tf-ai-showcase',
    'type:"bomb"',
    'type:"lightning"',
    'type:"mask"',
    'function tfAwardCompleteRecipe(',
    'function tfLoseCompleteRecipe(',
    'function tfRunLightning(',
    'function tfRunExchange(',
    'Premier à 3 paires',
    'tf-turbo-brake',
    'TF_V91_MEMORY_VOICE',
    'Égalité 2–2',
    'Nouvelle manche automatique',
    'st.roundStarter',
    'possède trois recettes et remporte la Tapas Fiesta',
    'type:"dicegame"',
    'function tfRunDiceTapas(',
    'Dé Tapas — Duel',
    'tf-die3d',
    'id="tfModeMobile"',
    'id="tfModeBoard"',
    'dicegame:"🎲 Dé Tapas !"',
    'TF_TIKOWIKO_FAMILY_SPLASH',
    'tikowiko-family-splash.webp',
    'id="tfGameSplash"',
    'hideDeveloperSplash',
)
missing = [marker for marker in required if marker not in final_html]
if missing:
    raise SystemExit('ERROR: V10/stable gameplay/splash validation failed: ' + ', '.join(missing))
if 'Mime un piment' in final_html:
    raise SystemExit('ERROR: old physical mime challenge still present')
if 'var tfShortLabels=' in final_html:
    raise SystemExit('ERROR: old text labels are still drawn inside the wheel')

for special in ('type:"coin"', 'type:"memory"', 'type:"bonus"', 'type:"exchange"', 'type:"bomb"', 'type:"lightning"', 'type:"mask"', 'type:"dicegame"'):
    if special not in final_html:
        raise SystemExit('ERROR: missing V10 wheel special: ' + special)

print('Copyright + V10 Mobile gameplay + tikoWikoFamily developer splash added and validated')
