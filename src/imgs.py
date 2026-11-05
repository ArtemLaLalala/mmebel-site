import sys
from PIL import Image
import numpy as np
def process(path):
    im=Image.open(path).convert('RGB'); W,H=im.size
    arr=np.asarray(im).copy()
    y0,y1=int(H*.13),int(H*.78)
    g=arr[y0:y1].mean(axis=2)
    dark=(g<235).mean(axis=0)
    L=int(W*.25)
    start=L
    for x in range(L,int(W*.42)):
        if dark[x:x+15].min()>0.18: start=x;break
    for x in range(L,start-2):
        if dark[x]<0.25: arr[y0:y1,x]=255
    im=Image.fromarray(arr)
    return im.crop((L,int(H*.13),int(W*.99),int(H*.84))), start/W
if __name__=='__main__':
    out=sys.argv[1]
    for l in open('src/catalog/map.txt'):
        pg,num=l.split(); p=int(pg)-3
        if p==20: continue
        c,s=process(f'src/catalog/raw/pg-{int(num):03d}.png')
        c.resize((1000,int(1000*c.size[1]/c.size[0])),Image.LANCZOS).save(f'{out}/{p:02d}.webp',quality=82,method=5)
