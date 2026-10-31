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
# Use a tighter head-and-upper-body crop for the saved phone card.
portrait_source=Image.open(A/"pegah-karimi-cutout.png").convert("RGBA")
portrait=portrait_source.crop((105,0,955,1040))
portrait.thumbnail((690,760),Image.Resampling.LANCZOS)
im.paste(portrait,((W-portrait.width)//2+70,285),portrait)

# Simple coffee cue, kept away from the face and the QR quiet zone.
cup_x,cup_y=92,665
d.ellipse((cup_x-28,cup_y-35,cup_x+190,cup_y+183),fill="#2D2F31",outline=GOLD,width=5)
d.rounded_rectangle((cup_x+12,cup_y+22,cup_x+128,cup_y+120),radius=15,fill=GOLD)
d.ellipse((cup_x+110,cup_y+45,cup_x+170,cup_y+105),outline=GOLD,width=18)
d.line((cup_x+15,cup_y+139,cup_x+150,cup_y+139),fill=GOLD,width=8)
for sx in (cup_x+35,cup_x+73,cup_x+109):
  d.arc((sx,cup_y-22,sx+34,cup_y+37),190,345,fill=GOLD,width=7)
d.text((88,865),"NITRO COFFEE",font=font(28,True),fill=GOLD)
d.text((88,900),"FOR EVERY EVENT",font=font(22,True),fill=WHITE)
d.rounded_rectangle((100,1020,980,1195),radius=35,fill="#292B2D",outline=GOLD,width=4)
center(d,1044,"DR. PEGAH KARIMI",font(64,True),WHITE)
center(d,1120,"MANAGING DIRECTOR",font(31,True),GOLD)

# Keep the QR and all captions fully inside the 1080 x 1920 phone canvas.
# The previous version let the code overlap the captions at the bottom.
d.rounded_rectangle((178,1240,902,1782),radius=48,fill=WHITE,outline=GOLD,width=10)
q=Image.open(A/"card-qr.png").resize((500,500),Image.Resampling.NEAREST)
im.paste(q,(290,1261))
center(d,1810,"SCAN TO CONNECT",font(36,True),GOLD)
center(d,1860,"NIKKINITROCOFFEE.COM",font(27,True),WHITE)
im.save(A/"phone-card.png",optimize=True)
