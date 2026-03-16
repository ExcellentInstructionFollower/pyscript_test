import ctypes

#https://excellentinstructionfollower.github.io/pyscript_test/

import matplotlib.pyplot as plt
from PIL import Image
#import easygui
import numpy as np
#from math import sin, pi, floor
#from pathlib import Path
#import sys
from js import document, window, Uint8Array, File, console
import io
#import asyncio
from pyscript import web, when, display

import libraries.Lanczos as Lanczos

@when("click", "#buttonid")
def confirm_click(e) :
    display("Upload clicked")
    console.log("clicked on upload")

@when("click", "#submitid")
def get_and_compress(event) :

    console.log("attempting to compress image")

    file_list = event.target.files
    first_item = file_list.item(0)

    #Get the data from the files arrayBuffer as an array of unsigned bytes
    array_buf = Uint8Array.new(first_item.arrayBuffer())

    #BytesIO wants a bytes-like object, so convert to bytearray first
    bytes_list = bytearray(array_buf)
    my_bytes = io.BytesIO(bytes_list) 

    #myimg = Image.open(easygui.fileopenbox())
    #myimg = Image.open(Path(sys.argv[1]))
    myimg = Image.open(my_bytes)

    img_array = np.ascontiguousarray(np.array(myimg, dtype=np.int32))
    ptr_img = img_array.ctypes.data_as(ctypes.c_void_p)
    H, W = img_array.shape[:2]

    new_H = document.getElementById('new_height')
    new_W = document.getElementById('new_width')
    #new_H = int(sys.argv[2])
    #new_W = int(sys.argv[3])
    a = 6

    ptr_image_reduced = Lanczos.lanczos(ptr_img, H, W, new_H, new_W, a)

    result_array = np.ctypeslib.as_array(
        ctypes.cast(ptr_image_reduced, ctypes.POINTER(ctypes.c_int)),
        shape=(new_H, new_W, 3)
    )

    # Convertir en uint8 pour une image
    result_img = result_array.astype(np.uint8)

    my_stream = io.BytesIO()
    myimg.save(my_stream, format="PNG")

    #Create a JS File object with our data and the proper mime type
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], "new_image_file.png", {type: "image/png"})

    #Create new tag and insert into page
    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(image_file)
    document.getElementById("output").appendChild(new_image)

    console.log("image compressed")

    #im_base = myimg.resize((new_W, new_H), Image.LANCZOS)

    #fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    #axes[0].imshow(myimg)
    #axes[0].set_title(f"Original ({W}x{H})")
    #axes[0].axis("off")

    #axes[1].imshow(result_img)
    #axes[1].set_title(f"Lanczos maison ({new_W}x{new_H})")
    #axes[1].axis("off")

    #axes[2].imshow(im_base)
    #axes[2].set_title(f"Lanczos PIL ({new_W}x{new_H})")
    #axes[2].axis("off")

    #plt.tight_layout()
    #plt.show()






# Run image processing code above whenever file is uploaded    
#document.getElementById("submitid").addEventListener("click", get_and_compress)
display("Site loaded with pyscript")






    # ANCIEN ALGORITHME FAIT EN PYTHON

    # def lanczos_kernel(x, a=3):
    #     if abs(x) < a:
    #         return np.sinc(x) * np.sinc(x / a)
    #     return 0.0


    # def lanczos_resize(img, new_h, new_w, a=3):

    #     #Récupération de la hauteur, et largeur de l'image
    #     H, W = img.shape[:2]


    #     #Récupération des canaux de couleurs (si il existe sinon 1)
    #     if len(img.shape) == 3:
    #         channels = img.shape[2]
    #     else:
    #         channels = 1

    #     # image de sortie
    #     if channels == 1:
    #         output = np.zeros((new_h, new_w))
    #     else:
    #         output = np.zeros((new_h, new_w, channels))

    #     # facteurs d'échelle
    #     scale_x = W / new_w
    #     scale_y = H / new_h

    #     # boucle principale
    #     for y_new in range(new_h):
    #         for x_new in range(new_w):

    #             # position réelle dans l'image originale
    #             x_old = x_new * scale_x
    #             y_old = y_new * scale_y

    #             x_base = floor(x_old)
    #             y_base = floor(y_old)

    #             sum_val = np.zeros(channels) if channels > 1 else 0
    #             total_weight = 0

    #             # voisins autour
    #             for y in range(y_base - a + 1, y_base + a + 1):
    #                 for x in range(x_base - a + 1, x_base + a + 1):

    #                     # vérification bordures
    #                     if 0 <= x < W and 0 <= y < H:

    #                         dx = x_old - x
    #                         dy = y_old - y

    #                         weight = lanczos_kernel(dx, a) * lanczos_kernel(dy, a)

    #                         sum_val += img[y, x] * weight
    #                         total_weight += weight

    #             # normalisation
    #             if total_weight != 0:
    #                 output[y_new, x_new] = sum_val / total_weight

    #     return output.astype(np.uint8)

    # # Le dernier paramètre de lanczos_resize est la valeur de a. Plus cette dernière est faible, plus l'algorithme sera rapide et moins qualitative
    # new_H = 250
    # new_W = 250

    # img2 = lanczos_resize(img, new_H, new_W, 3)
    # plt.imshow(img2)
    # plt.show()

    # print("Compression termniée")
    # """ print("Dimensions de l'image : ",img.shape) # Dimensions x, y et nombre de couleurs
    # print("Pixel 500 sur 200 : ",img[200,500]) #pour afficher les composantes RVB du pixel aux coordonnées (200; 500)
    # print("Composante rouge de ce dernier pixel :",img[200,500][0])
    # print("Rouge : ",img[:,:,0]) """