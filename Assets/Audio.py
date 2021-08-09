import pytube
import threading
from os import path
from time import sleep
from shutil import move
from random import sample
from mutagen import mp3,id3
from pytube.cli import on_progress
from moviepy.editor import AudioFileClip, os, sys
from Assets.Extensiones import ConvertirSegundos, DescargarMiniatura

Errores=0
LinkError=[]

def DescargarPorHilos(Archivo, HilosMaximos):
    def Descargar(LinkVideo):
        global Errores
        global LinkError
        Valores="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"
        ID="".join(sample(Valores, 6))
        try: yt=pytube.YouTube(LinkVideo)
        except pytube.exceptions.RegexMatchError:
            if os.path.isfile("debug.on"): print(f"DEBUG-?: Error al descargar: {LinkVideo[:-1]} [*] Url no valida!!!")
            else: print(f"Error al descargar: {LinkVideo[-1]} [*] Url no valida!!!")
            Errores+=1
            LinkError.append(LinkVideo)
            exit()
        print("[!] Titulo: "+yt.title)
        ConvertirSegundos(yt.length)
        AudioDescargado=yt.streams.filter(only_audio=True, abr="128kbps").first()
        Nombre=ID+".mp4"
        AudioDescargado.download(filename=Nombre)
        DescargarMiniatura(yt.thumbnail_url, Name=Nombre[:-4]+".png")
        AudioCambioFormato=AudioFileClip(Nombre)
        LetrasNombres=[]
        ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
        for Letra in yt.title:
            if Letra not in ParametrosNoValidos:
                LetrasNombres.append(str(Letra))
        NombreArchivo="".join(LetrasNombres)+".mp3"
        print("###\n")
        AudioCambioFormato.write_audiofile(NombreArchivo)
        AudioConMiniatura=mp3.MP3(NombreArchivo)
        AudioConMiniatura.tags.add(id3.APIC(data=open(Nombre[:-4]+".png",'rb').read()))
        AudioConMiniatura.save()
        os.remove(Nombre[:-4]+".png")
        os.remove(Nombre)
        try:
            if path.exists(sys.argv[5]) and path.isfile(sys.argv[5])==False: move(NombreArchivo, sys.argv[5])
            else: raise TypeError
        except (TypeError, IndexError):
            if os.path.isfile("debug.on"): print("DEBUG-?: [!] Archivo No Movido.")

    LinksVideos=[]
    for x in Archivo:
        LinksVideos.append(x)

    N=HilosMaximos
    Total=len(LinksVideos)

    Hilos=0
    Descargados=len(LinksVideos)
    
    Iterador=len(LinksVideos)-1

    while True:
        if N>=Total: N=Total
        print(f"\n|--------------- Descargando [ {N} / {Total} ] ---------------|")

        if len(LinksVideos)>=HilosMaximos: Hilos=HilosMaximos
        else: Hilos=len(LinksVideos)

        for X in range(Hilos):
            hilo=threading.Thread(target=Descargar, args=[LinksVideos[Iterador]])
            hilo.start()
            N+=1
            LinksVideos.remove(LinksVideos[Iterador])
            Iterador-=1
            Descargados-=1
            sleep(1)
            print("\n")
    
        hilo.join()
            
        if Descargados==0: break
        os.system("cls")
    
    if Errores!=0:
        print("[*] No se han podiddo descargar: ")
        for i in LinkError:
            print("---"+i.replace("\n", " "))
    else:
        print("[+] Todos los audios descargados :D")


def DescargarVariosAudios(Url, Num, Total):
    """Doc: Funcion encargada de descargar multiples audios de un archivo txt"""
    print("|-------- Descargando [ "+str(Num)+" / "+str(Total)+" ] --------|")
    try: yt=pytube.YouTube(Url, on_progress_callback=on_progress)
    except pytube.exceptions.RegexMatchError:
        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Url No Valida!!!")
        else: print("[*] Url no valida!!!")
        exit()
    try:
        print("[!] Titulo: "+yt.title)
        ConvertirSegundos(yt.length)
    except KeyError:
        print("[*] Url No Valida!!!")
        exit()
    print("\n[|} Descargando :)...")
    yt.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio.mp4")
    DescargarMiniatura(yt.thumbnail_url)
    AudioDescargado=AudioFileClip("audio.mp4")
    LetrasNombres=[]
    ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
    for Letra in yt.title:
        if Letra not in ParametrosNoValidos:
            LetrasNombres.append(str(Letra))
    NombreArchivo="".join(LetrasNombres)+".mp3"
    print("###\n")
    AudioDescargado.write_audiofile(NombreArchivo)
    AudioDescargado.close()
    AudioConMiniatura=mp3.MP3(NombreArchivo)
    AudioConMiniatura.tags.add(id3.APIC(data=open("mini.png",'rb').read()))
    AudioConMiniatura.save()
    os.remove("audio.mp4")
    os.remove("mini.png")
    # --------------- Mover el archivo a la dirrecion especificada --------------- #
    try:
        if path.exists(sys.argv[3]) and path.isfile(sys.argv[3])==False: move(NombreArchivo, sys.argv[3])
        else: raise TypeError
    except (TypeError, IndexError):
        pass
    if Num==Total:
        os.system("cls")
        print("[---Todos Los Audios Descargados---]")
    else:
        os.system("cls")

def AudioOpciones():
    "Doc: Funcion principal encargada de anazilar la opciones establecidas por el usuario y llamar a las demas funciones."
    try:
        Archivo=open(sys.argv[4], "r")
        if path.getsize(sys.argv[4])!=0:
            HilosMaximos=int(sys.argv[3])
            if HilosMaximos>=5:
                if os.path.isfile("debug.on"): print("[*] Numero de hilos invalido!!")
                else: print("[*] Numero de hilos invalido!!")
            else: 
                DescargarPorHilos(Archivo, HilosMaximos)
        else:
            if os.path.isfile("debug.on"): print("DEBUG-?: [*] Archivo Vacio!!!")
            else: print("[*] Archivo Vacio!!!")
        Archivo.close()     
        exit()

    except (IndexError, OSError):
        try:
            Archivo=open(sys.argv[2], "r")
            if path.getsize(sys.argv[2])!=0:
                N=1
                Total=len(Archivo.readlines())
                Archivo.seek(0)
                for Url in Archivo:
                    DescargarVariosAudios(Url, Num=N, Total=Total)
                    N+=1
            else:
                if os.path.isfile("debug.on"): print("DEBUG-?: [*] Archivo Vacio!!!")
                else: print("[*] Archivo Vacio!!!")
            Archivo.close()     
            exit()
        except (IndexError, OSError): yt=pytube.YouTube(sys.argv[2], on_progress_callback=on_progress)



    except UnicodeDecodeError:
        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Archivo No Valido")
        else: print("[*] Archivo No Valido")
        exit()
    except pytube.exceptions.RegexMatchError:
        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Url No Valida!!!")
        else: print("[*] Url No Valida!!!")
        exit()

    # ------------------------- Descargar un solo Archivo ------------------------ #
    try:
        print("\n[------------------------------ UnusualDownloader ------------------------------]")
        print("[!] Titulo: "+yt.title)
    except KeyError:
        print("[*] Url No Valida!!!")
        exit()
    ConvertirSegundos(yt.length)
    AudioDescargado=yt.streams.filter(only_audio=True, abr="128kbps").first()
    print("\n[|] Descargando :)...")
    AudioDescargado.download(filename="audio.mp4")
    DescargarMiniatura(yt.thumbnail_url)
    AudioCambioFormato=AudioFileClip("audio.mp4")
    LetrasNombres=[]
    ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
    for Letra in yt.title:
        if Letra not in ParametrosNoValidos:
            LetrasNombres.append(str(Letra))
    NombreArchivo="".join(LetrasNombres)+".mp3"
    print("###\n")
    AudioCambioFormato.write_audiofile(NombreArchivo)
    AudioConMiniatura=mp3.MP3(NombreArchivo)
    AudioConMiniatura.tags.add(id3.APIC(data=open("mini.png",'rb').read()))
    AudioConMiniatura.save()
    os.remove("mini.png")
    os.remove("audio.mp4")
    print("\n[+] Descargado :D.")
    try:
        if path.exists(sys.argv[3]) and path.isfile(sys.argv[3])==False: move(NombreArchivo, sys.argv[3])
        else: raise TypeError
    except (TypeError, IndexError):
        if os.path.isfile("debug.on"): print("DEBUG-?: [!] Archivo No Movido.")
    exit()