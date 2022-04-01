from PIL import ImageFilter,ImageEnhance,ImageDraw,ImageFont,Image
from io import StringIO,BytesIO 
from flask import Flask , send_file , request , current_app 
from urllib.parse import unquote

app = Flask(__name__)

def get_dominant_color(pil_img, palette_size=16):
    #https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
    img = pil_img.copy()
    img.thumbnail((100, 100))
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]
    return tuple(dominant_color)

def add_corners(im, rad):
    #https://stackoverflow.com/questions/11287402/how-to-round-corner-a-logo-without-white-backgroundtransparent-on-it-using-pi
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def generateBanner(icon="./logos/github.png",color=None,text="@itspacchu",BUFF=16,effect=None):
    showIcon = Image.open(icon).resize((64,64))
    textColor = (255,255,255)
    if(color == None):
        color = get_dominant_color(showIcon,3)
        if(color[0] > 255/2 and color[1] > 255/2 and color[2] > 255/2):
            textColor = (10,10,10)
    img_new = Image.new("RGB", (64 + BUFF + len(text.strip().replace("%2",""))*17 ,64) + BUFF, color=color)
    img_new.paste(showIcon, (8,0), mask=showIcon)
    draw = ImageDraw.Draw(img_new)
    font = ImageFont.truetype("./fonts/FiraSans-Medium.ttf", 32)
    draw.text((showIcon.size[0] + BUFF, 12), text=text, font=font,fill=textColor)
    if(effect):
        if("grayscale" in effect):
            img_new = img_new.convert('L')
        if("edge" in effect):
            img_new = img_new.filter(ImageFilter.FIND_EDGES)
        if("contour" in effect):
            img_new = img_new.filter(ImageFilter.CONTOUR)
        if("emboss" in effect):
            img_new = img_new.filter(ImageFilter.EMBOSS)
        if("smooth" in effect):
            img_new = img_new.filter(ImageFilter.SMOOTH)
        final = add_corners(img_new, 20)
        return final

def serveBanner(genImage):
    img_io = BytesIO()
    genImage.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route("/generate/badge/",methods=['GET'])
def banner():
    try:
        page = request.args.get('text', default = "pacchu#4112", type = str)
        icon = "./logos/" + unquote(request.args.get('icon', default = "no", type = str)) + ".png"
        effect = unquote(request.args.get('effect', default = "none", type = str))
        buff = unquote(request.args.get('buff', default = 16, type = int))
        return serveBanner(generateBanner(icon=icon,text=page,effect=effect,BUFF=buff))
    except IndexError:
        return serveBanner(generateBanner(icon="./logos/err.png",text="its somewhere?"))

@app.route("/")
def index():
    return send_file("./templates/index.html")

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000) #nginx proxy


