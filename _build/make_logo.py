# -*- coding: utf-8 -*-
"""Deriva el logotipo en cobre (fondo transparente) a partir del archivo original del cliente."""
from PIL import Image
import numpy as np, colorsys, os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
src=Image.open(os.path.join(ROOT,'Logotipo bronce sobre fondo negro-2.png')).convert('RGB')
a=np.asarray(src).astype(float)
lum=a.max(axis=2)
alpha=np.clip((lum-14)/(150-14),0,1)**0.8
rgb=np.where(alpha[...,None]>0.02, np.clip(a/np.maximum(alpha[...,None],0.25),0,255),0)/255
flat=rgb.reshape(-1,3)
hsv=np.array([colorsys.rgb_to_hsv(*p) for p in flat[::1]]) if False else None
# vectorizado
mx=rgb.max(2); mn=rgb.min(2); d=mx-mn
r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
dd=np.where(d==0,1,d)
h=np.where(mx==r,((g-b)/dd)%6,np.where(mx==g,(b-r)/dd+2,(r-g)/dd+4))*60
h=np.where(d==0,0,h)
s=np.where(mx==0,0,d/np.where(mx==0,1,mx)); v=mx
h2=(h-14)%360; s2=np.clip(s*0.80,0,1); v2=np.clip(v*1.18,0,1)
def hsv2rgb(h,s,v):
    c=v*s; x=c*(1-abs((h/60)%2-1)); m=v-c; z=np.zeros_like(h); out=np.zeros(h.shape+(3,))
    for i,(rr,gg,bb) in enumerate([(c,x,z),(x,c,z),(z,c,x),(z,x,c),(x,z,c),(c,z,x)]):
        sel=(h>=i*60)&(h<(i+1)*60); out[sel]=np.stack([rr,gg,bb],-1)[sel]
    return out+m[...,None]
o=hsv2rgb(h2,s2,v2)
im=Image.fromarray((np.dstack([o,alpha])*255).astype('uint8'),'RGBA')
bbox=im.getchannel('A').point(lambda x:255 if x>20 else 0).getbbox(); im=im.crop(bbox)
side=max(im.size); sq=Image.new('RGBA',(side,side),(0,0,0,0)); sq.paste(im,((side-im.width)//2,(side-im.height)//2))
out=os.path.join(ROOT,'assets/img/logo')
sq.resize((1000,1000),Image.LANCZOS).save(out+'/logo-transparent.png',optimize=True)
sq.resize((512,512),Image.LANCZOS).save(out+'/logo-512.png',optimize=True)
sq.resize((256,256),Image.LANCZOS).save(out+'/logo-mark.png',optimize=True)
fav=Image.new('RGB',(256,256),(14,14,15)); l=sq.resize((256,256),Image.LANCZOS); fav.paste(l,(0,0),l); fav.save(out+'/favicon.png')
