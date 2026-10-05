from playwright.sync_api import sync_playwright
import glob
exe=glob.glob('/opt/pw-browsers/chromium-1194/*/chrome')[0]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=exe,args=['--no-sandbox'])
    pg=b.new_page(); pg.goto('file:///home/user/dq/derm_notes/derm_notes.html'); pg.wait_for_timeout(500)
    pg.pdf(path='derm_notes.pdf',format='A4',print_background=True,margin=dict(top='9mm',bottom='9mm',left='9mm',right='9mm'))
    b.close()
