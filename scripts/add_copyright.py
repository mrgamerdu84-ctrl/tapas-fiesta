from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

meta = '<meta name="copyright" content="© 2026 tikowikoFamily — Tous droits réservés">'
if meta not in s:
    s = s.replace('</head>', '  ' + meta + '\n</head>', 1)

# The visible copyright is now rendered by scripts/add_privacy.py at the bottom
# of the opening screen, next to the legal-page entry point. Keeping only the
# metadata here avoids duplicate copyright blocks elsewhere in the app.
p.write_text(s, encoding='utf-8')
print('Copyright metadata added; visible notice handled by legal page')
