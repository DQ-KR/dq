import pymupdf, io
from PIL import Image
W='/tmp/claude-0/-home-user-dq/11c67a3c-075f-5213-9dc2-1b7a08590888/scratchpad/w/'
OUT='/home/user/dq/output/assets/족보/'
d=pymupdf.open(W+'E.pdf')
# 원본 이미지 객체 (2025 시험지 73번, 79번 사진)
for pg,name in [(9,'2025_exam_q73_photo'),(10,'2025_exam_q79_photo')]:
    page=d[pg-1]; inf=[i for i in page.get_image_info(xrefs=True) if i['xref']][0]
    ex=d.extract_image(inf['xref']); im=Image.open(io.BytesIO(ex['image'])).convert('RGB')
    im.save(OUT+name+'.png',optimize=True); print(name,im.size,ex['ext'])
# 문제 영역 crop (300DPI): 문제 번호~다음 문제 번호 직전
def crop(pg,start,end,name,col):
    page=d[pg-1]; w=page.rect.width; h=page.rect.height
    x0,x1=(0,w/2) if col==0 else (w/2,w)
    s=[r for r in page.search_for(start) if x0<=r.x0<x1][0]
    e=[r for r in page.search_for(end) if x0<=r.x0<x1]
    y1=e[0].y0-2 if e else h-40
    clip=pymupdf.Rect(x0+10,s.y0-3,x1-5,y1)
    pm=page.get_pixmap(dpi=300,clip=clip); pm.save(OUT+name+'.png'); print(name,pm.width,pm.height)
crop(9,'73.','74.','2025_exam_q73_question',1)
crop(10,'79.','80.','2025_exam_q79_question',1)
