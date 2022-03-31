from curses.textpad import rectangle
import pwd
import PIL as pil
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from io import StringIO,BytesIO 
from flask import Flask , send_file , request , current_app
from urllib.parse import unquote
app = Flask(__name__)

class LogoData:
    DISCORD = "./logos/discord.png"
    TWITCH = "./logos/twitch.png"
    GITHUB = "./logos/github.png"
    LINKEDIN = "./logos/linkedin.png"
    TWITTER = "./logos/twitter.png"
    INSTAGRAM = "./logos/instagram.png"
    YOUTUBE = "./logos/youtube.png"
    MINECRAFT = "./logos/minecraft.png"
    SPOTIFY = "./logos/spotify.png"
    STEAM = "./logos/steam.png"
    EPICGAMES = "./logos/epicgames.png"
    PORNHUB = "./logos/pornhub.png"
    RISEUP = "./logos/riseup.png"
    GMAIL = "./logos/gmail.png"
    KINDLE = "./logos/kindle.png"
    STACKOVERFLOW = "./logos/stackoverflow.png"
    LASTFM = "./logos/lastfm.png"
    ERROR = "./logos/err.png"
    NO = "./logos/no.png"


    def fetchFromString(string):
        if(string == "discord"):
            return LogoData.DISCORD
        elif(string == "twitch"):
            return LogoData.TWITCH
        elif(string == "github"):
            return LogoData.GITHUB
        elif(string == "linkedin"):
            return LogoData.LINKEDIN
        elif(string == "twitter"):
            return LogoData.TWITTER
        elif(string == "instagram"):
            return LogoData.INSTAGRAM
        elif(string == "youtube"):
            return LogoData.YOUTUBE
        elif(string == "minecraft"):
            return LogoData.MINECRAFT
        elif(string == "spotify"):
            return LogoData.SPOTIFY
        elif(string == "steam"):
            return LogoData.STEAM
        elif(string == "epicgames"):
            return LogoData.EPICGAMES
        elif(string == "pornhub"):
            return LogoData.PORNHUB
        elif(string == "riseup"):
            return LogoData.RISEUP
        elif(string == "gmail"):
            return LogoData.GMAIL
        elif(string == "kindle"):
            return LogoData.KINDLE
        elif(string == "lastfm"):
            return LogoData.LASTFM
        elif(string == "stackoverflow"):
            return LogoData.STACKOVERFLOW
        else:
            return LogoData.NO

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

def generateBanner(icon="./logos/github.png",color=None,text="@itspacchu",BUFF=16):
    showIcon = Image.open(icon).resize((64,64))
    textColor = (255,255,255)
    if(color == None):
        color = get_dominant_color(showIcon,3)
        if(color[0] > 255/2 and color[1] > 255/2 and color[2] > 255/2):
            textColor = (10,10,10)
    img_new = Image.new("RGB", (110 + len(text.strip().replace(" ",""))*17 ,64), color=color)
    img_new.paste(showIcon, (8,0), mask=showIcon)
    draw = ImageDraw.Draw(img_new)
    font = ImageFont.truetype("./fonts/FiraSans-Medium.ttf", 32)
    draw.text((showIcon.size[0] + BUFF, 12), text=text, font=font,fill=textColor)
    return add_corners(img_new, 20)

def serveBanner(genImage):
    img_io = BytesIO()
    genImage.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route("/generate/badge/",methods=['GET'])
def banner():
    try:
        page = request.args.get('text', default = "pacchu#4112", type = str)
        icon = LogoData.fetchFromString(unquote(request.args.get('icon', default = LogoData.DISCORD, type = str)))
        return serveBanner(generateBanner(icon=icon,text=page))
    except:
        return serveBanner(generateBanner(icon=LogoData.ERROR,text="its somewhere?"))

@app.route("/")
def index():
    return send_file("./templates/index.html")

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000) #nginx proxy


