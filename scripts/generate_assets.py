from pathlib import Path
import sys
sys.path.insert(0,"/private/tmp/nn-qrcode")
import qrcode
from PIL import Image,ImageDraw,ImageFont,ImageFilter

ROOT=Path(__file__).resolve().parents[1]; A=ROOT/"assets"; URL="https://biocool.github.io/nikki-nitro-pegah-card/"
GOLD="#FFC437"; INK="#343638"; WHITE="#FFFFFF"
def font(size,bold=False):
  for p in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else ["/System/Library/Fonts/Supplemental/Arial.ttf"]):
    if Path(p).exists(): return ImageFont.truetype(p,size)
  return ImageFont.load_default()
def center(d,y,text,f,fill):
  b=d.textbbox((0,0),text,font=f); d.text(((1080-(b[2]-b[0]))/2,y),text,font=f,fill=fill)

qr=qrcode.QRCode(version=None,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=16,border=4);qr.add_data(URL);qr.make(fit=True);qr.make_image(fill_color=INK,back_color=WHITE).convert("RGB").save(A/"card-qr.png")

for size,name in [(180,"icon-180.png"),(192,"icon-192.png"),(512,"icon-512.png")]:
  im=Image.new("RGB",(size,size),INK);d=ImageDraw.Draw(im);pad=int(size*.08);d.rounded_rectangle((pad,pad,size-pad,size-pad),radius=int(size*.18),fill=GOLD);d.text((size*.19,size*.25),"NN",font=font(int(size*.34),True),fill=INK);d.text((size*.38,size*.59),"COFFEE",font=font(int(size*.09),True),fill=INK);im.save(A/name)

W,H=1080,1920;im=Image.new("RGB",(W,H),INK);d=ImageDraw.Draw(im)
for y in range(H):
  t=y/(H-1);v=int(52-15*t);d.line((0,y,W,y),fill=(v,v+1,v+2))
d.line((75,75,1005,75),fill=GOLD,width=8);d.line((1005,75,1005,1845),fill=GOLD,width=8)
d.text((95,145),"NIKKI",font=font(115,True),fill=GOLD);d.text((430,145),"NITRO",font=font(115,True),fill=WHITE);d.text((665,270),"Coffee",font=font(55,True),fill=GOLD)
portrait=Image.open(A/"pegah-karimi-cutout.png").convert("RGBA");portrait.thumbnail((720,760),Image.Resampling.LANCZOS);im.paste(portrait,((W-portrait.width)//2,370),portrait)
d.rounded_rectangle((100,1040,980,1220),radius=35,fill="#292B2D",outline=GOLD,width=4);center(d,1065,"DR. PEGAH KARIMI",font(64,True),WHITE);center(d,1140,"MANAGING DIRECTOR",font(31,True),GOLD)
d.rounded_rectangle((155,1265,925,1760),radius=48,fill=WHITE,outline=GOLD,width=10);q=Image.open(A/"card-qr.png").resize((650,650),Image.Resampling.NEAREST);im.paste(q,(215,1190))
center(d,1780,"SCAN TO CONNECT",font(36,True),GOLD);center(d,1830,"NIKKINITROCOFFEE.COM",font(27,True),WHITE)
im.save(A/"phone-card.png",optimize=True)
