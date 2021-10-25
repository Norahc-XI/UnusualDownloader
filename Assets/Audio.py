import pytube
import threading
from time import sleep
from shutil import move
from random import sample
from mutagen import mp3,id3
from pytube.cli import on_progress
from moviepy.editor import AudioFileClip, os, sys
from Assets.Extensiones import DescargarMiniatura, MostrarInfo

# ------------------------------ Nota: Terminado ----------------------------- #

Error=0
ErrorLista=[]

def DescargarAudio(Url:str, Miniatura:bool):
    "Descargar y colocar en formato .mp3 el audio de la url"
    global Error
    global ErrorLista

    try: yt=pytube.YouTube(Url, on_progress_callback=on_progress); Skip=False
    except pytube.exceptions.RegexMatchError:
        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Url No Valida!")
        else: print("[*] Url No Valida!")
        Error+=1
        ErrorLista.append(Url)
        sleep(2)
        Skip=True
    if not Skip:
        MostrarInfo(yt, Miniatura)
        print("\n[|] Descargando...")
        yt.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio.mp4")
        print("###\n")
        AudioCambioFormato=AudioFileClip("audio.mp4")
        LetrasNombres=[]
        ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
        for Letra in yt.title:
            if Letra not in ParametrosNoValidos:
                LetrasNombres.append(str(Letra))
        NombreArchivo="".join(LetrasNombres)+".mp3"
        AudioCambioFormato.write_audiofile(NombreArchivo)
        DescargarMiniatura(yt.thumbnail_url, NombreArchivo[:-4]+".jpg")
        AudioConMiniatura=mp3.MP3(NombreArchivo)
        AudioConMiniatura.tags.add(id3.APIC(data=open(NombreArchivo[:-4]+".jpg",'rb').read()))
        AudioConMiniatura.save()
        os.remove("audio.mp4")
        if not Miniatura:
            os.remove(NombreArchivo[:-4]+".jpg")
        print("\n[+] Completado...")
        try:
            if os.path.exists(sys.argv[5]) and os.path.isfile(sys.argv[5])==False: move(NombreArchivo, sys.argv[5])
            else: raise IndexError
        except IndexError:
            try:
                if os.path.exists(sys.argv[4]) and os.path.isfile(sys.argv[4])==False: move(NombreArchivo, sys.argv[4])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.exists(sys.argv[3]) and os.path.isfile(sys.argv[3])==False: move(NombreArchivo, sys.argv[3])
                    else: raise IndexError
                except IndexError: 
                    if os.os.path.isfile("debug.on"): print("DEBUG-?: [!] Archivo No Movido.")
        if Miniatura:
            try:
                if os.path.exists(sys.argv[5]) and os.path.isfile(sys.argv[5])==False: move(NombreArchivo[:-4]+".jpg", sys.argv[5])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.exists(sys.argv[4]) and os.path.isfile(sys.argv[4])==False: move(NombreArchivo[:-4]+".jpg", sys.argv[4])
                    else: raise IndexError
                except IndexError:
                    try:
                        if os.path.exists(sys.argv[3]) and os.path.isfile(sys.argv[3])==False: move(NombreArchivo[:-4]+".jpg", sys.argv[3])
                        else: raise IndexError
                    except IndexError: 
                        if os.path.isfile("debug.on"): print("DEBUG-?: [!] Miniatura No Movida.")
    
def DescargarHilos(Ubicacion:int, MaxHilos:int, Miniatura:bool):
    "Descargar multiples audios simultaneamente"
    def CodigoHilo(Link:str):
        "Codigo ha ejecutar del hilo"
        global Error
        global ErrorLista
        try: yt=pytube.YouTube(Link)
        except pytube.exceptions.RegexMatchError: 
            if os.path.isfile("debug.on"): print("DEBUG-?: [*] No se ha podido descargar: "+LinksVideos[0])
            else: print("[*] No se ha podido descargar: "+LinksVideos[0])
            Error+=1
            ErrorLista.append(LinksVideos[0])
            exit()
        MostrarInfo(yt, Miniatura)
        print("\n")
        ID="".join(sample("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789", 6))+".mp4"
        yt.streams.filter(only_audio=True, abr="128kbps").first().download(filename=ID)
        # Filtrar nombre
        LetrasNombres=[]
        ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
        for Letra in yt.title:
            if Letra not in ParametrosNoValidos:
                LetrasNombres.append(str(Letra))
        NombreArchivo="".join(LetrasNombres)+".mp3"
        # Cambiar formato y colocar portada
        AudioCambioFormato=AudioFileClip(ID)
        AudioCambioFormato.write_audiofile(NombreArchivo)
        DescargarMiniatura(yt.thumbnail_url, NombreArchivo[:-4]+".jpg")
        AudioConMiniatura=mp3.MP3(NombreArchivo)
        AudioConMiniatura.tags.add(id3.APIC(data=open(NombreArchivo[:-4]+".jpg",'rb').read()))
        AudioConMiniatura.save()
        os.remove(ID)
        if not Miniatura: os.remove(NombreArchivo[:-4]+".jpg")
        try:
            if os.path.exists(sys.argv[6]) and os.path.isfile(sys.argv[6])==False: move(NombreArchivo, sys.argv[6])
            else: raise IndexError
        except IndexError:
            try:
                if os.path.exists(sys.argv[5]) and os.path.isfile(sys.argv[5])==False: move(NombreArchivo, sys.argv[5])
                else: raise IndexError
            except IndexError:
                if os.os.path.isfile("debug.on"): print("DEBUG-?: [!] Archivo No Movido.")
        if Miniatura:
            try:
                if os.path.exists(sys.argv[6]) and os.path.isfile(sys.argv[6])==False: move(NombreArchivo[:-4]+".jpg", sys.argv[6])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.exists(sys.argv[5]) and os.path.isfile(sys.argv[5])==False: move(NombreArchivo[:-4]+".jpg", sys.argv[5])
                    else: raise IndexError
                except IndexError:
                    if os.path.isfile("debug.on"): print("DEBUG-?: [!] Miniatura No Movida.")

    Archivo=open(sys.argv[Ubicacion], "r")
    if os.path.getsize(sys.argv[Ubicacion])!=0:
        LinksVideos=[]
        for Link in Archivo: LinksVideos.append(Link.replace("\n", ""))
        Contador=0
        Total=len(LinksVideos)
        ContenedorHilos=[]
        while len(LinksVideos)!=0:
            if len(LinksVideos)<=MaxHilos: MaxHilos=len(LinksVideos)
            Contador+=MaxHilos
            print(f"\n|--------------- Descargando [ {Contador} / {Total} ] ---------------|")
            for _ in range(MaxHilos):
                hilo=threading.Thread(target=CodigoHilo, args=[LinksVideos[0]], daemon=True)
                hilo.start()
                ContenedorHilos.append(hilo)
                LinksVideos.pop(0)
            for h in ContenedorHilos:
                h.join()
            os.system("cls")
            ContenedorHilos.clear()
        if Error!=0:
            print(f"[/] No se han podido descargar {Error} Audios: ")
            for E in ErrorLista: print(E)
        else:  print("[+] Se han completado todas las descargas...")
    exit()

def DescargarTxt(Ubicacion:int, Miniatura:bool):
    "Descargar los audios de los links provenientes de un archivo .txt"
    Archivo=open(sys.argv[Ubicacion], "r")
    if os.path.getsize(sys.argv[Ubicacion])!=0:
        Contador=1
        Total=len(Archivo.readlines())
        Archivo.seek(0)
        for Url in Archivo:
            print(f"|-------- Descargando [ {Contador} / {Total} ] --------|\n")
            DescargarAudio(Url, Miniatura)
            Contador+=1
            os.system("cls")
    else:
        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Archivo Vacio!")
        else: print("[*] Archivo Vacio!")
    Archivo.close()
    if Error==0: print("[+] Completado...")
    else: 
        print(f"[/] No se han podido descargar {Error} Audios: ")
        for i in ErrorLista:
            print(i)
    exit()

def AudioOpciones(Rango:int):
    "Verificar paremetros y llamar a las demas funciones correspodientes"
    os.system("title UnusualDonwloader - Descargando Audios")
    if Rango>7:  #En caso que el limite de paremetros sea superado
        print("[*] Demasiados valores!")
        exit()

    elif Rango>=4 and Rango<=7:
        if sys.argv[2]=="-i" or sys.argv[2]=="-image":
            if sys.argv[3]=="-t" or sys.argv[3]=="-times":
                try:
                    if int(sys.argv[4])>5: MaxHilos=5
                    elif int(sys.argv[4])>=2: MaxHilos=int(sys.argv[4])
                    elif int(sys.argv[4])==1: DescargarTxt(5, True)
                except ValueError:
                    if os.path.isfile("debug.on"): print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                    else: print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                    exit()
                try: DescargarHilos(5, MaxHilos, True)
                except OSError: pass
            else: 
                try: DescargarTxt(3, True)
                except OSError: DescargarAudio(sys.argv[3], True); exit()
                
        else:
            if sys.argv[2]=="-t" or sys.argv[2]=="-times":
                try:
                    if int(sys.argv[3])>5: MaxHilos=5
                    elif int(sys.argv[3])>=2: MaxHilos=int(sys.argv[3])
                    elif int(sys.argv[3])==1: DescargarTxt(4, False)
                except ValueError:
                    if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe colocar un numero valido de Descargas Simultaneas!")
                    else: print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                    exit()
                try: DescargarHilos(4, MaxHilos, False)
                except OSError:
                    if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe colocar un archivo txt para descargas por hilos!")
                    else: print("[*] Debe colocar un archivo txt para descargas por hilos!")
                    exit()
    
    if Rango>=1 and Rango<=4:
        try:
            Archivo=open(sys.argv[2], "r")
            if os.path.getsize(sys.argv[2])!=0:
                Contador=1
                Total=len(Archivo.readlines())
                Archivo.seek(0)
                for Url in Archivo:
                    print(f"|-------- Descargando [ {Contador} / {Total} ] --------|\n")
                    DescargarAudio(Url, False)
                    Contador+=1
                    os.system("cls")
            Archivo.close()
            if Error==0: print("[+] Completado...")
            else: 
                print(f"[/] No se han podido descargar {Error} Audios: ")
                for i in ErrorLista:
                    print(i)
        except OSError:
            DescargarAudio(sys.argv[2], False)
    else: print("[*] Parametros invalidos!")