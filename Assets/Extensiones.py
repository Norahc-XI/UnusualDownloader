from requests import get

# ------------------------------ Nota: Terminado ----------------------------- #

def ConvertirSegundos(SegundosOriginal:int) -> int:
    "Funcion encargada de convertir los segundos a minutos, de manera que sea mas facil a la vista y lectura, Lo hace diviendo los segundos por 60, y tomando el cociente como minutos y el resto como los segundos."
    Minutos, Segundos = divmod(SegundosOriginal, 60)
    BaseDecimal=[0,1,2,3,4,5,6,7,8,9]
    if Segundos in BaseDecimal:
        Segundos=str(0)+str(Segundos)
    return f"[!] Duración: {Minutos}:{Segundos}"

def DescargarMiniatura(Url:str, Name:str="mini.jpg"):
    "Descargar la miniatura del video para colocarlo como caratula del audio."
    Peticion=get(Url)
    Archivo=open(Name, "wb")
    Archivo.write(Peticion.content)
    Archivo.close()

def MostrarInfo(yt:str, Miniatura:bool) -> str:
    "Mostrar la informacion del video a descargar"
    print("[!] Titulo: "+yt.title)
    print(ConvertirSegundos(yt.length))
    if Miniatura: print("[!] Miniatura: "+yt.thumbnail_url)