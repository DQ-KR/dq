"""강의록 PDF의 원본 이미지 객체를 그대로 추출하고, 필요한 영역만 무손실(PNG)로 crop한다.
- 원본 해상도 유지(업스케일/다운샘플 없음). crop 불필요 + JPEG 원본이면 원본 바이트를 그대로 저장."""
import pymupdf, io, json, os, sys
from PIL import Image, ImageChops
sys.path.insert(0, os.path.dirname(__file__))
from crops import CROPS
W='/tmp/claude-0/-home-user-dq/11c67a3c-075f-5213-9dc2-1b7a08590888/scratchpad/w/'
OUT='/home/user/dq/output/assets/강의록/'
# image key -> (ascii filename stem, 설명)
NAMES={
'L1_p02_1':'tumor_classification','L1_p03_1':'ak_to_scc_uv','L1_p05_1':'ak_histology','L1_p08_1':'mammary_paget',
'L1_p10_1':'empd_vulva','L1_p11_1':'empd_histology','L1_p16_2':'melanoma_who_table','L1_p17_1':'melanoma_subtypes',
'L1_p21_1':'ectopic_mongolian_spot','L1_p23_1':'halo_nevus','L1_p25_1':'giant_congenital_nevus',
'L2_p03_1':'em_spectrum_table','L2_p08_1':'infrared_spectrum','L2_p10_1':'uv_detrimental_effects','L2_p13_1':'wrinkle',
'L2_p14_1':'photoaging_mechanism','L2_p17_1':'phototherapy_spectrum','L2_p21_1':'melanocyte_structure',
'L2_p24_1':'vitiligo_nonsegmental_acrofacial','L2_p25_1':'vitiligo_segmental','L2_p29_1':'vitiligo_lesions',
'L2_p30_1':'vitiligo_repigmentation',
'L3_p04_1':'psoriasis_types','L3_p08_1':'psoriasis_histology','L3_p11_1':'psoriasis_clinical','L3_p13_1':'psoriasis_plaque_a',
'L3_p14_1':'psoriasis_plaque_b','L3_p15_1':'psoriasis_plaque_c','L3_p16_1':'psoriasis_koebner','L3_p17_1':'psoriasis_nail',
'L3_p25_1':'pityriasis_rosea','L3_p28_1':'prp_a','L3_p29_1':'prp_palmoplantar','L3_p30_1':'prp_normal_islands',
'L3_p33_1':'parapsoriasis_small_plaque','L3_p34_1':'parapsoriasis_large_plaque','L3_p36_1':'pityriasis_lichenoides_chronica',
'L3_p39_1':'lichen_planus_skin','L3_p40_1':'lichen_planus_oral','L3_p41_1':'lichen_planus_nail'}
manifest=[]
docs={n:pymupdf.open(W+n+'.pdf') for n in ['L1','L2','L3']}
for key,(l,t,r,b) in CROPS.items():
    n,pg,k=key[:2],int(key[4:6]),int(key.split('_')[-1])
    d=docs[n]; page=d[pg-1]
    infos=[i for i in sorted(page.get_image_info(xrefs=True),key=lambda i:(round(i['bbox'][1]/50),i['bbox'][0])) if i['xref'] and not(i['width']<=110 and i['height']<=110)]
    inf=infos[k-1]; xref=inf['xref']; ex=d.extract_image(xref)
    raw=ex['image']; ext=ex['ext']
    im=Image.open(io.BytesIO(raw)); 
    if ex.get('smask'):
        m=Image.open(io.BytesIO(d.extract_image(ex['smask'])['image'])).convert('L')
        bg=Image.new('RGB',im.size,'white'); bg.paste(im.convert('RGB'),mask=m); im=bg
    im=im.convert('RGB'); Wd,Ht=im.size
    box=(int(l*Wd),int(t*Ht),int(r*Wd),int(b*Ht)); c=im.crop(box)
    bb=ImageChops.difference(c,Image.new('RGB',c.size,'white')).point(lambda p:255 if p>18 else 0).getbbox()
    if bb: box=(box[0]+bb[0],box[1]+bb[1],box[0]+bb[2],box[1]+bb[3]); c=im.crop(box)
    full = box[0]<=3 and box[1]<=3 and box[2]>=Wd-3 and box[3]>=Ht-3
    stem=f'{NAMES[key]}_{key[:2].lower()}p{pg:02d}'
    if full and ext in('jpeg','jpg') and not ex.get('smask'):
        fn=stem+'.jpg'; open(OUT+fn,'wb').write(raw); method='원본 JPEG 바이트 그대로'
    else:
        fn=stem+'.png'; c.save(OUT+fn,optimize=True); method='원본 이미지 객체에서 무손실 crop(PNG)' if not full else '원본 이미지 객체 무손실 저장(PNG)'
    # 검증: 열림/크기
    chk=Image.open(OUT+fn); chk.load()
    manifest.append(dict(image_id=stem,src_pdf=n,page=pg,crop_box_px=list(box),method=method,orig_px=[Wd,Ht],orig_fmt=ext,final=fn,final_px=list(chk.size),bytes=os.path.getsize(OUT+fn)))
json.dump(manifest,open('/home/user/dq/tools/image_manifest.json','w'),ensure_ascii=False,indent=1)
print(len(manifest)); print(sum(m['bytes'] for m in manifest)/1e6,'MB')
for m in manifest: print(m['final'],m['orig_px'],m['final_px'],m['orig_fmt'])
