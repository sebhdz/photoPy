from PIL import Image
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO

ctk.set_appearance_mode("dark")

dataFrameim = []
imSize = (250,250)

backgroundColor = '#0B0B0D'
secondaryBackground = '#1B1B1B'
borderColor = '#383838'

ESTILO_BOTON = {
    "corner_radius":0,
    "font":("JetBrains Mono", 12),
    "height": 40,
}

# ELEGIR IMAGEN
def seleccionarImagen():
    global dataFrameim
    global imSize

    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imagenes", "*.jpg *.jpeg *.png")]
    )
    im = Image.open(ruta)
    im = im.resize(imSize)

    dataFrameim = list(im.getdata())

    foto = CTkImage(light_image=im, size=(250, 250))

    imgOriginal.configure(text="", image=foto)
    imgOriginal.image = foto
    crearBotones()
    crearHistogramas()

def crearHistogramas():
    global dataFrameim

    pixelesRojos = []
    pixelesVerdes = []
    pixelesAzules = []
    piexelesLuz = []

    for pixel in dataFrameim:
        r, g, b = pixel
        pixelesRojos.append(r)
        pixelesVerdes.append(g)
        pixelesAzules.append(b)
        piexelesLuz.append(((r * 0.299) + (g * 0.587) + (b * 0.114)))
    
    # Crear histograma de escala de grises
    fig, ax = plt.subplots(figsize=(3, 2), facecolor='black')
    ax.set_facecolor('black')
    ax.hist(piexelesLuz, bins=50, range=(0, 255), color='gray', alpha=0.8)
    ax.set_title('Escala de Grises', color='white', fontsize=10)
    ax.tick_params(colors='white', labelsize=8)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='PNG', facecolor='black', bbox_inches='tight', dpi=80)
    buffer.seek(0)
    hist_image = Image.open(buffer)
    ctk_image = CTkImage(light_image=hist_image, size=(299, 150))
    lblHGY.configure(image=ctk_image, text="")
    lblHGY.image = ctk_image
    plt.close(fig)
    buffer.close()
    
    # Crear histograma rojo
    fig, ax = plt.subplots(figsize=(3, 2), facecolor='black')
    ax.set_facecolor('black')
    ax.hist(pixelesRojos, bins=50, range=(0, 255), color='red', alpha=0.8)
    ax.set_title('Canal Rojo', color='white', fontsize=10)
    ax.tick_params(colors='white', labelsize=8)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='PNG', facecolor='black', bbox_inches='tight', dpi=80)
    buffer.seek(0)
    hist_image = Image.open(buffer)
    ctk_image = CTkImage(light_image=hist_image, size=(299, 150))
    lblHR.configure(image=ctk_image, text="")
    lblHR.image = ctk_image
    plt.close(fig)
    buffer.close()
    
    # Crear histograma verde
    fig, ax = plt.subplots(figsize=(3, 2), facecolor='black')
    ax.set_facecolor('black')
    ax.hist(pixelesVerdes, bins=50, range=(0, 255), color='green', alpha=0.8)
    ax.set_title('Canal Verde', color='white', fontsize=10)
    ax.tick_params(colors='white', labelsize=8)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='PNG', facecolor='black', bbox_inches='tight', dpi=80)
    buffer.seek(0)
    hist_image = Image.open(buffer)
    ctk_image = CTkImage(light_image=hist_image, size=(299, 150))
    lblHGR.configure(image=ctk_image, text="")
    lblHGR.image = ctk_image
    plt.close(fig)
    buffer.close()
    
    # Crear histograma azul
    fig, ax = plt.subplots(figsize=(3, 2), facecolor='black')
    ax.set_facecolor('black')
    ax.hist(pixelesAzules, bins=50, range=(0, 255), color='blue', alpha=0.8)
    ax.set_title('Canal Azul', color='white', fontsize=10)
    ax.tick_params(colors='white', labelsize=8)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='PNG', facecolor='black', bbox_inches='tight', dpi=80)
    buffer.seek(0)
    hist_image = Image.open(buffer)
    ctk_image = CTkImage(light_image=hist_image, size=(299, 150))
    lblHB.configure(image=ctk_image, text="")
    lblHB.image = ctk_image
    plt.close(fig)
    buffer.close()
    


# NEGATIVO
def convertirNegativo():
    global dataFrameim
    
    imagenNegativa = []
    for pixel in dataFrameim:
        pixelNegativo = []
        for color in pixel:
            pixelNegativo.append(255 - color)
        imagenNegativa.append(tuple(pixelNegativo))

    mostrarImagen(imagenNegativa)


# COLOR RGB
def convertirColor(color):
    global dataFrameim

    imagenColor = []

    colores = ['rojo', 'verde', 'azul']
    index = colores.index(color)

    for pixel in dataFrameim:
        pixelNuevo=[0, 0, 0]
        pixelNuevo[index] = pixel[index]
        imagenColor.append(tuple(pixelNuevo))
    
    mostrarImagen(imagenColor)


def convertirBN():
    global dataFrameim
    global imSize

    imgBN = []
    for pixel in dataFrameim:
        r, g, b = pixel
        pixelBN = (r * 0.299) + (g * 0.587) + (b * 0.114)
        imgBN.append(pixelBN)
    
    plt.hist(imgBN, bins=256, range=(0,255), density=False)
    plt.show()

    nuevaImagen = Image.new("L", imSize)
    nuevaImagen.putdata(imgBN)
    foto = CTkImage(light_image=nuevaImagen, size=imSize)
    imgEditada.configure(image=foto, text="")
    imgEditada.image = foto
    
# MOSTRAR IMAGEN
def mostrarImagen(pixeles):

    global imSize
    nuevaImagen = Image.new("RGB", imSize)
    nuevaImagen.putdata(pixeles)
    foto = CTkImage(light_image=nuevaImagen, size=imSize)
    imgEditada.configure(image=foto, text="")
    imgEditada.image = foto


btnNegativo  = None
def crearBotones():
    global btnNegativo
    if btnNegativo:
        return
    btnNegativo = ctk.CTkButton(btnsFrame, text="Negativo", command=convertirNegativo, **ESTILO_BOTON)
    btnNegativo.pack(side="left", padx=10)

    btnRojo = ctk.CTkButton(btnsFrame, text="Rojo", command=lambda: convertirColor('rojo'), **ESTILO_BOTON)
    btnRojo.pack(side="left", padx=10)

    btnVerde = ctk.CTkButton(btnsFrame, text="Verde", command=lambda: convertirColor('verde'), **ESTILO_BOTON)
    btnVerde.pack(side="left", padx=10)

    btnAzul = ctk.CTkButton(btnsFrame, text="Azul", command=lambda: convertirColor('azul'), **ESTILO_BOTON)
    btnAzul.pack(side="left", padx=10)
    
    btnBN = ctk.CTkButton(btnsFrame, text="Escala de grises", command=convertirBN, **ESTILO_BOTON)
    btnBN.pack(side="left", padx=10)

app = ctk.CTk()
app.title("PhotoPy")
app.geometry("1400x700")
app.configure(fg_color=backgroundColor)

# HEADER
header = ctk.CTkFrame(app, height=100, fg_color=secondaryBackground,corner_radius=0, border_color=borderColor, border_width=1)
header.pack(side="top", fill="x", padx=10, pady=(10, 0))
header.pack_propagate(False)

btnSelectImage = ctk.CTkButton(header, text="Elegir imagen", command=seleccionarImagen, **ESTILO_BOTON)
btnSelectImage.pack(side="right", padx=(0, 30))


# Aside
infoAside = ctk.CTkFrame(app, width=300, fg_color=backgroundColor, corner_radius=0, border_color=borderColor, border_width=1)
infoAside.pack(side="left", fill="y", padx=(10, 0), pady=(0, 10))

infoAside.grid_rowconfigure(0, weight=1)
infoAside.grid_rowconfigure(1, weight=1)
infoAside.grid_rowconfigure(2, weight=1)
infoAside.grid_rowconfigure(3, weight=1)

lblHGY = ctk.CTkLabel(infoAside, text=" ", fg_color="transparent", width=299)
lblHGY.grid(column=0, row=0, sticky="nsew")

lblHR = ctk.CTkLabel(infoAside, text=" ", fg_color="transparent", width=299)
lblHR.grid(column=0, row=1, sticky="nsew")

lblHGR = ctk.CTkLabel(infoAside, text=" ", fg_color="transparent", width=299)
lblHGR.grid(column=0, row=2, sticky="nsew")

lblHB = ctk.CTkLabel(infoAside, text=" ", fg_color="transparent", width=300)
lblHB.grid(column=0, row=3, sticky="nsew")

# Main
main = ctk.CTkFrame(app, fg_color=backgroundColor, corner_radius=0, border_color=borderColor, border_width=1)
main.pack(expand=True, fill="both", padx=(0, 10), pady=(0, 10), ipady=0, ipadx=0)

main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=1)
main.grid_rowconfigure(0, weight=1)

imgOriginal = ctk.CTkLabel(main, fg_color=secondaryBackground,  width=250, height=250, text=" ")
imgOriginal.grid(column=0, row=0)

imgEditada = ctk.CTkLabel(main, fg_color=secondaryBackground, width=250, height=250, text=" ")
imgEditada.grid(column=1, row=0)

# Options
options = ctk.CTkFrame(main, fg_color=backgroundColor, corner_radius=0, border_color=borderColor, border_width=1, height=150)
options.grid(column=0, columnspan=2, row=1, sticky="nsew")
options.pack_propagate(False)

btnsFrame = ctk.CTkFrame(options, fg_color="transparent", height=80)
btnsFrame.pack(expand=True)


app.mainloop()
