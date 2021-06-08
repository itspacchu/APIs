from utils import find_dominant_color
import flask,os,time
from flask.json import jsonify
app = flask.Flask(__name__)
from PIL import Image
from utils import find_dominant_color


@app.route('/')
def default_page():
    html = """
    <html><head><style>body { color: black;}
    </style></head><body><h1 id="pacchu-s-apis">Pacchu&#39;s APIs</h1>
    <p>Some Random APIs I&#39;m working on</p>
    <h2 id="dominant-color-dominant-colour-">Dominant Color ( <code>/dominant-colour</code> )</h2>
    <blockquote>
    <p> method <strong>&#39;POST&#39;</strong></p>
    <p> key  = &#39;image&#39;</p>
    <p>Image shouldn&#39;t exceed 50x50 px</p>
    </blockquote>
    </body></html>
    """
    return html


@app.route('/dominant_color', methods = ['POST'])
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['image']
        img = Image.open(f)
        try:
            if(img.size[0] > 50 or img.size[1] > 50):
                return flask.jsonify({
                    'hexval':'0x000000',
                    'status': 'you sent a large image so i aint processing it'
                })
            else:
                returnable = find_dominant_color(f.filename,local=True)
                return flask.jsonify({
                    'hexval': str(returnable[0]),
                    'status': str(returnable[1])
                })
        except:
            return flask.jsonify({
                        'hexval':'0x000000',
                        'status':'BAD REQUEST'
                    })
        

        
if __name__ == '__main__':
      app.run()
