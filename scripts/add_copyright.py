from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

meta = '<meta name="copyright" content="© 2026 tikowikoFamily — Tous droits réservés">'
if meta not in s:
    s = s.replace('</head>', '  ' + meta + '\n</head>', 1)

style = '''\n<style id="tf-copyright-style">\n#tfCopyright{max-width:520px;margin:28px auto 92px;padding:10px 16px;text-align:center;font-size:.72rem;line-height:1.35;color:#7a5d49;opacity:.88;}\n#tfCopyright strong{color:#6a4030;}\n</style>\n'''
if 'id="tf-copyright-style"' not in s:
    s = s.replace('</head>', style + '</head>', 1)

footer = '''\n<div id="tfCopyright" aria-label="Copyright">\n  <strong>© 2026 tikowikoFamily</strong> — Tous droits réservés.<br>\n  Tapas Fiesta! et ses éléments originaux sont protégés par le droit d’auteur.\n</div>\n'''
if 'id="tfCopyright"' not in s:
    s = s.replace('</body>', footer + '</body>', 1)

p.write_text(s, encoding='utf-8')
print('Copyright notice added')
