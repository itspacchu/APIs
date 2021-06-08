import binascii
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

def find_dominant_color(imageurl: str, local=False):
    try:
        NUM_CLUSTERS = 10
        im = Image.open(imageurl)
        im = im.resize((25, 25))
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        vecs, dist = scipy.cluster.vq.vq(ar, codes)
        counts, bins = scipy.histogram(vecs, len(codes))
        index_max = scipy.argmax(counts)
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c)
                                  for c in peak)).decode('ascii')
        try:
            return hex(int(colour, 16))[:8],"No errors"
            #return colour
        except:
            return "0xffffff","Unable to parse Hex Value"
    except IndexError:
        return "0xffffff","Something Happened in Processing Image"
