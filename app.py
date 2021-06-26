from utils import find_dominant_color
import flask,os
from PIL import Image
from utils import find_dominant_color
from urllib.parse import unquote
from random import choice

app = flask.Flask(__name__)

@app.route('/')
def index():
    html = """
    <html><head><style>body { color: black;}
    </style></head><body><h1 id="pacchu-s-apis">Pacchu&#39;s APIs</h1>
    <p>Some Random APIs I&#39;m working on</p>
    <h2 id="dominant-color-dominant-colour-">Dominant Color ( <code>/dominant-color</code> )</h2>
    <blockquote>
    <p> method <strong>&#39;POST&#39;</strong></p>
    <p> key  = &#39;image&#39;</p>
    <p>Image shouldn&#39;t exceed 50x50 px</p>
    </blockquote>
    <h2 id="video-ogp-vidembed-url-encoded-url-mp4-">Video OGP (<code>/vidembed/[url-encoded-url.mp4]</code>)</h2>
    </body></html>
    """
    return html


@app.route(r'/login')
def login_doesnt_exist():
    return choice(["wut u lookin for mate", "hmm there should be something important here right?", "something seems missing...!! weird"])

@app.route(r'/vidembed')
def test_meta_tag():
    try:
        vid_url = unquote(flask.request.args.get('vsrc'))
        try:
            embed_title = unquote(flask.request.args.get('title'))
        except:
            embed_title = ""
        try:
            embed_desc = unquote(flask.request.args.get('desc'))
        except:
            embed_desc = ""
        return f"""
       <!DOCTYPE html>
       <html>
       <meta property="og:type" content="video">
       <meta property="og:video" content="{vid_url}" />
       <meta property="og:video:width" content="640" />
       <meta property="og:video:height" content="426" />
       <meta property="og:video:type" content="application/mp4" />
       <meta property="og:video" content="{vid_url}" />
       <meta property="og:video:type" content="video/mp4" />
       <meta property="og:video" content="{vid_url}" />
       <meta property="og:video:type" content="text/html" />
       <meta property="og:title" content="{embed_title}">
       <meta property="og:description"  content="{embed_desc}"/>
       <body>
       <video width="100%" src="{vid_url}" controls>
       </video>
        """
    except:
        return """
        Not a valid parameter <br> Did you url-encode?  <a href="https://meyerweb.com/eric/tools/dencoder/"> URL ENCODER </a>
        """

@app.route('/dominant_color', methods = ['POST'])
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['image']
        f.save(f.filename)
        img = Image.open(f.filename)
        try:
            if(img.size[0] > 50 or img.size[1] > 50):
                img.close()
                os.remove(f.filename)
                return flask.jsonify({
                    'hexval':'0x000000',
                    'status': 'you sent a large image so i aint processing it'
                })
            else: 
                returnable = find_dominant_color(f.filename,local=True)
                img.close()
                os.remove(f.filename)
                return flask.jsonify({
                    'hexval': str(returnable[0]),
                    'status': str(returnable[1])
                })
        except IndexError:
            return flask.jsonify({
                        'hexval':'0x000000',
                        'status':'BAD REQUEST'})
            
        

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0',port=80,debug=False)
