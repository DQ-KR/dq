import sys, glob
from playwright.sync_api import sync_playwright
exe=glob.glob('/opt/pw-browsers/chromium-1194/*/chrome')[0]
FOOT='<div style="width:100%;font-size:8px;text-align:center;color:#666;font-family:NanumGothic,sans-serif"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=exe,args=['--no-sandbox'])
    for name in sys.argv[1:]:
        pg=b.new_page(); pg.goto(f'file:///home/user/dq/output/{name}.html'); pg.wait_for_load_state('networkidle')
        pg.evaluate("Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r})))")
        pg.pdf(path=f'/home/user/dq/output/{name}.pdf',format='A4',print_background=True,display_header_footer=True,
               header_template='<div></div>',footer_template=FOOT,margin=dict(top='12mm',bottom='15mm',left='11mm',right='11mm'),prefer_css_page_size=False)
        print(name,'pdf done')
    b.close()
