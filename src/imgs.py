import sys
from PIL import Image
src='catalog/'  # папка с исходным PDF (в репозиторий не входит)
out='docs/img/'
lines=[l.split() for l in open(src+'map.txt')]
for pdfpage,num in lines:
    p=int(pdfpage)-3
    im=Image.open(f'{src}raw/pg-{int(num):03d}.png').convert('RGB')
    W,H=im.size
    im.resize((1600,int(1600*H/W)),Image.LANCZOS).save(f'{out}pages/{p:02d}.webp',quality=80,method=5)
    c=im.crop((int(W*.25),int(H*.13),int(W*.99),int(H*.84)))
    c.resize((1000,int(1000*c.size[1]/c.size[0])),Image.LANCZOS).save(f'{out}products/{p:02d}.webp',quality=80,method=5)
# logos
im=Image.open(src+'raw/p1-000.png').convert('L')
for name,box in [('mc',(1200,1460,1780,1770)),('mm',(2060,1440,2400,1810))]:
    c=im.crop(box)
    # alpha from brightness above background
    bg=min(c.getdata()) if False else 52
    a=c.point(lambda v: max(0,min(255,int((v-bg)*255/(255-bg)*1.15))))
    bb=a.getbbox(); a=a.crop(bb)
    for col,suf in [((255,255,255),'light'),((51,44,43),'dark')]:
        o=Image.new('RGBA',a.size,col+(0,)); o.putalpha(a); o.save(f'{out}brand/{name}-{suf}.png')
    print(name,bb,a.size)
