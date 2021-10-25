import pytube
import moviepy
import shutil
import threading
from random import sample
from mutagen import mp3,id3
from pytube.cli import on_progress
from moviepy.editor import AudioFileClip, os, sys
from Assets.Extensiones import DescargarMiniatura, ConvertirSegundos

RESPERMITIDAS=['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p']

# ------------------------------ Nota: Terminado ----------------------------- #

Error=0
ErrorLista=[]

# ---------------------------- Funciones Generales --------------------------- #
def MoverArchivo(NombreArchivo:str):
        try:
            if os.path.isfile(sys.argv[3])==False and os.path.exists(sys.argv[3]): shutil.move(NombreArchivo, sys.argv[3])
            else: raise IndexError
        except IndexError:
            try:
                if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): shutil.move(NombreArchivo, sys.argv[4])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.isfile(sys.argv[5])==False and os.path.exists(sys.argv[5]): shutil.move(NombreArchivo, sys.argv[5])
                    else: raise IndexError
                except IndexError:
                    try:
                        if os.path.isfile(sys.argv[6])==False and os.path.exists(sys.argv[6]): shutil.move(NombreArchivo, sys.argv[6])
                        else: raise IndexError
                    except IndexError:
                        try:
                            if os.path.isfile(sys.argv[7])==False and os.path.exists(sys.argv[7]): shutil.move(NombreArchivo, sys.argv[7])
                            else: raise IndexError
                        except IndexError:
                            try:
                                if os.path.isfile(sys.argv[8])==False and os.path.exists(sys.argv[8]): shutil.move(NombreArchivo, sys.argv[8])
                                else: raise IndexError
                            except IndexError:
                                try:
                                    if os.path.isfile(sys.argv[9])==False and os.path.exists(sys.argv[9]): shutil.move(NombreArchivo, sys.argv[9])
                                    else: raise IndexError
                                except IndexError: pass

def DescargarUbicacion(VideoADescargar:str):
    try:
        if os.path.isfile(sys.argv[3])==False and os.path.exists(sys.argv[3]): VideoADescargar.download(sys.argv[3]) 
        else: raise IndexError
    except IndexError:
        try:
            if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): VideoADescargar.download(sys.argv[4])
            else: raise IndexError
        except IndexError:
            try:
                if os.path.isfile(sys.argv[5])==False and os.path.exists(sys.argv[5]): VideoADescargar.download(sys.argv[5])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.isfile(sys.argv[6])==False and os.path.exists(sys.argv[6]): VideoADescargar.download(sys.argv[6]) 
                    else: raise IndexError
                except IndexError:
                    try:
                        if os.path.isfile(sys.argv[7])==False and os.path.exists(sys.argv[7]): VideoADescargar.download(sys.argv[7])
                        else: raise IndexError
                    except IndexError:
                        try:
                            if os.path.isfile(sys.argv[8])==False and os.path.exists(sys.argv[8]): VideoADescargar.download(sys.argv[8])
                            else: raise IndexError
                        except IndexError:
                            try:
                                if os.path.isfile(sys.argv[9])==False and os.path.exists(sys.argv[9]): VideoADescargar.download(sys.argv[9])
                                else: raise IndexError
                            except IndexError: VideoADescargar.download()

def DescargaHilos(Ubicacion:int, MaxHilos:int, Miniatura:bool, SoloAudio:bool, Resolucion:str="360p"):
    global Error
    global ErrorLista

    def EjecutarHilo(Video:pytube.YouTube, Mini:bool, Audio:bool, Res:str):
        global Error
        global ErrorLista

        try:
            print("┌──[!] Titulo: "+Video.title)
            if Mini: print("├──[!] Miniatura: "+Video.thumbnail_url)
            print("├──", end=ConvertirSegundos(Video.length)+"\n")
            print("\n")
            Saltar=False
        except pytube.exceptions.VideoUnavailable:
            Saltar=True
            Error+=1
            ErrorLista.append(Video.watch_url)

        if not Saltar:
            if Audio:
                if not os.path.isdir("temp"): os.makedirs("temp")
                abc="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
                TempImg="".join(sample(abc, 6))
                TempAudio="".join(sample(abc, 6))
                TempNameImg="temp\\"+TempImg+".jpg"
                TempNameAudio="temp\\"+TempAudio+".mp4"
                Video.streams.filter(only_audio=True, abr="128kbps").first().download(filename=TempNameAudio)
                DescargarMiniatura(Video.thumbnail_url, TempNameImg)
                ArchivoAudio=AudioFileClip(TempNameAudio)
                LetrasNombre=[]
                ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
                for Letra in Video.title:
                    if Letra not in ParametrosNoValidos:
                        LetrasNombre.append(str(Letra))
                NombreArchivo="".join(LetrasNombre)+".mp3"
                ArchivoAudio.write_audiofile(NombreArchivo)
                AudioConMiniatura=mp3.MP3(NombreArchivo)
                AudioConMiniatura.tags.add(id3.APIC(data=open(TempNameImg,'rb').read()))
                AudioConMiniatura.save()
                os.remove(TempNameAudio)
                os.remove(TempNameImg)
                MoverArchivo(NombreArchivo)
            else:
                try:
                    Progresivo=Video.streams.filter(res=Res, file_extension="mp4").first()
                    if not Progresivo.is_progressive:
                        if not os.path.isdir("temp"): os.makedirs("temp")
                        abc="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
                        TempVideo="".join(sample(abc, 6))
                        TempAudio="".join(sample(abc, 6))
                        TempNameVideo="temp\\"+TempVideo+".mp4"
                        TempNameAudio="temp\\"+TempAudio+".mp4"
                        Video.streams.filter(res=Res, file_extension="mp4").first().download(filename=TempNameVideo)
                        Video.streams.filter(only_audio=True, abr="128kbps").first().download(filename=TempNameAudio)
                        LetrasNombres=[]
                        ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|', '\\']
                        for Letra in Video.title:
                            if Letra not in ParametrosNoValidos:
                                LetrasNombres.append(str(Letra))
                            else: pass
                        NombreArchivo="".join(LetrasNombres)+".mp4"
                        try:
                            moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio(TempNameVideo, TempNameAudio, NombreArchivo)
                            os.remove(TempNameVideo)
                            os.remove(TempNameAudio)
                        except OSError:
                            print("[*] Ha ocurrido un Error al unir el audio al video.")
                            exit()
                        MoverArchivo(NombreArchivo)
                    else: 
                        VideoADescargar=Video.streams.filter(res=Res, file_extension="mp4", progressive=True).first()
                        DescargarUbicacion(VideoADescargar)
                except AttributeError:
                    VideoADescargar=Video.streams.get_highest_resolution()
                    DescargarUbicacion(VideoADescargar)
            print("\n└──[+] Completado...")
    try:
        yt=pytube.Playlist(sys.argv[Ubicacion])
    except pytube.exceptions.RegexMatchError:
        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Url No Valida!")
        else: print("[*] Url No Valida!")
        exit()

    Videos=[]
    try: 
        for v in yt.videos: Videos.append(v)
    except KeyError:
        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Lista de Reproduccion no valida!")
        else: print("[*] Lista de Reproduccion no valida!")
        exit()
    Total=yt.length
    Contador=0
    ContenedorHilos=[]
    while len(Videos)!=0:
        if len(Videos)<=MaxHilos: MaxHilos=len(Videos)
        Contador+=MaxHilos
        print(f"|-------- [!] Playlist:{yt.title} [ {Contador} / {Total} ] --------|\n")
        for _ in range(MaxHilos):
            try:
                hilo=threading.Thread(target=EjecutarHilo, args=(Videos[0], Miniatura, SoloAudio, Resolucion), daemon=True)
                hilo.start()
                ContenedorHilos.append(hilo)
            except pytube.exceptions.RegexMatchError:
                if os.path.isfile("debug.on"): print("DEBUG-5: [*] No se ha podido descargar: "+Videos[0])
                else: print("[*] No se ha podido descargar: "+Videos[0])
                Error+=1
                ErrorLista.append(Videos[0])
            Videos.pop(0)
        for h in ContenedorHilos: h.join()
        os.system("cls")
    if Error==0: print("\n[+] Todos Los videos Descargados :D.")
    else: 
        print(f"\n[+] No se han podido descargar {Error} videos: ")
        for i in ErrorLista: print(i)
    if os.path.isdir("temp"): os.removedirs("temp")
    exit()

def DescargarAudio(Video:pytube.YouTube):
    Video.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio.mp4")
    DescargarMiniatura(Video.thumbnail_url)
    ArchivoAudio=AudioFileClip("audio.mp4")
    LetrasNombre=[]
    ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
    for Letra in Video.title:
        if Letra not in ParametrosNoValidos:
            LetrasNombre.append(str(Letra))
    NombreArchivo="".join(LetrasNombre)+".mp3"
    print("├──\n")
    ArchivoAudio.write_audiofile(NombreArchivo)
    AudioConMiniatura=mp3.MP3(NombreArchivo)
    AudioConMiniatura.tags.add(id3.APIC(data=open("mini.png",'rb').read()))
    AudioConMiniatura.save()
    os.remove("audio.mp4")
    os.remove("mini.png")
    return NombreArchivo

def DescargarAndComponer(Video:pytube.YouTube, Resolucion:str):
    Video.streams.filter(res=Resolucion, file_extension="mp4").first().download(filename="video.mp4")
    Video.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio.mp4")
    LetrasNombres=[]
    ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|', '\\']
    for Letra in Video.title:
        if Letra not in ParametrosNoValidos:
            LetrasNombres.append(str(Letra))
        else: pass
    NombreArchivo="".join(LetrasNombres)+".mp4"
    try:
        print("├──\n")
        moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio("video.mp4", "audio.mp4", NombreArchivo)
        os.remove("video.mp4")
        os.remove("audio.mp4")
    except:
        print("[*] No se ha podido descargar el video, pero los archivos sin juntar se guardaran en el directorio de ejecucion, por si desea manualmente componerlos, el error se debe al titulo del video.")
        exit()
    return NombreArchivo
    
def DescargadorPrincipal(Video:pytube.YouTube, OnlyAudio:bool=False, Resolucion:str="360p"):
    "Funcion encargada de descargar los multiples videos de la lista de reproduccion, segun los parametros establecidos por el usuario."
    Video.register_on_progress_callback(on_progress)
    try:
        Stream=Video.streams.filter(res=Resolucion, file_extension="mp4").first()
        if OnlyAudio:
            NombreArchivo=DescargarAudio(Video)
            MoverArchivo(NombreArchivo)
        elif not Stream.is_progressive:
            NombreArchivo=DescargarAndComponer(Video, Resolucion)
            MoverArchivo(NombreArchivo)
        else:
            VideoADescargar=Video.streams.filter(res=Resolucion, file_extension="mp4", progressive=True).first()
            DescargarUbicacion(VideoADescargar)
            print("├###")
    except AttributeError:
        VideoADescargar=Video.streams.get_highest_resolution()
        DescargarUbicacion(VideoADescargar)

def ListaOpciones(Rango:int):
    os.system("title UnusualDonwloader - Descargando Lista de Reproduccin")
    "Funcion principal encargada de procesar los parametros establecidos por el usuario, y ejecutar lo que el ordene."
    if Rango>10:
        # ---------- Si el rango es mayor al permitidor se sale el programa ---------- #
        print("[*] Demasiados Valores!!")
        exit()

    elif Rango<=10:
        if sys.argv[2]=="-r" or sys.argv[2]=="-resolution":
            try:
                for Res in RESPERMITIDAS:
                    if sys.argv[3]==Res: ResAsignada=sys.argv[3]; break
                    else: ResAsignada=None
                if ResAsignada in RESPERMITIDAS: pass
                else: 
                    if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe establecer una resolucion valida")
                    else: print("[*] Debe establecer una resolucion valida")
                    exit()

            except IndexError:
                if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe establecer una resolucion")
                else: print("[*] Debe establecer una resolucion")
                exit()

            if sys.argv[4]=="-i" or sys.argv[4]=="-image":
                if sys.argv[5]=="-t" or sys.argv[5]=="-times":
                    try:
                        if int(sys.argv[6])>5: MaxHilos=5
                        elif int(sys.argv[6])>=1: MaxHilos=int(sys.argv[6])
                    except ValueError:
                        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe colocar un numero valido de Descargas Simultaneas!")
                        else: print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                        exit()
                    
                    if sys.argv[7]=="-o" or sys.argv[7]=="-only_audio":
                        if ResAsignada==None:
                            try: DescargaHilos(8, MaxHilos, True, True)
                            except OSError:
                                yt=pytube.Playlist(sys.argv[8])
                                SoloAudio=True
                        else:
                            if os.path.isfile("debug.on"): print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!")
                            else: print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!")
                            exit()
                    else:
                        try: DescargaHilos(7, MaxHilos, True, False, ResAsignada)
                        except OSError:
                            yt=pytube.Playlist(sys.argv[7])
                            SoloAudio=False
                else:
                    if sys.argv[5]=="-o" or sys.argv[5]=="-only_audio":
                        if ResAsignada==None:
                            yt=pytube.Playlist(sys.argv[6])
                            SoloAudio=True
                        else:
                            if os.path.isfile("debug.on"): print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!")
                            else: print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!")
                            exit()
                    else:
                        yt=pytube.Playlist(sys.argv[5])
                        SoloAudio=False
                Miniatura=True
            elif sys.argv[4]=="-t" or sys.argv[4]=="-times":
                    try:
                        if int(sys.argv[5])>5: MaxHilos=5
                        elif int(sys.argv[5])>=1: MaxHilos=int(sys.argv[5])
                    except ValueError:
                        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe colocar un numero valido de Descargas Simultaneas!")
                        else: print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                        exit()
                    if sys.argv[6]=="-o" or sys.argv[6]=="-only_audio":
                        if ResAsignada==None:
                            try: DescargaHilos(7, MaxHilos, False, True)
                            except OSError:
                                yt=pytube.Playlist(sys.argv[8])
                                SoloAudio=True
                        else:
                            if os.path.isfile("debug.on"): print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!")
                            else: print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!")
                            exit()
                    else:
                        try: DescargaHilos(6, MaxHilos, False, False, ResAsignada)
                        except OSError:
                            yt=pytube.Playlist(sys.argv[6])
                            SoloAudio=False
                    Miniatura=False
            else:
                if sys.argv[4]=="-o" or sys.argv[4]=="-only_audio":
                        yt=pytube.Playlist(sys.argv[5])
                        SoloAudio=True
                else:
                    yt=pytube.Playlist(sys.argv[4])
                    SoloAudio=False
                Miniatura=False

        else:
            try:
                if sys.argv[2]=="-i" or sys.argv[2]=="-image":
                    if sys.argv[3]=="-t" or sys.argv[3]=="-times":
                        try:
                            if int(sys.argv[4])>5: MaxHilos=5
                            elif int(sys.argv[4])>=1: MaxHilos=int(sys.argv[4])
                        except ValueError:
                            if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe colocar un numero valido de Descargas Simultaneas!")
                            else: print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                            exit()
                        if sys.argv[5]=="-o" or sys.argv[5]=="-only_audio":
                            try: DescargaHilos()
                            except OSError:
                                yt=pytube.Playlist(sys.argv[6])
                                SoloAudio=True
                        else:
                            try: DescargaHilos()
                            except OSError:
                                yt=pytube.Playlist(sys.argv[5])
                                SoloAudio=False
                    else:
                        if sys.argv[3]=="-o" or sys.argv[3]=="-only_audio":
                            yt=pytube.Playlist(sys.argv[4])
                            SoloAudio=True
                        else:
                            yt=pytube.Playlist(sys.argv[3])
                            SoloAudio=False
                    Miniatura=True
                elif sys.argv[2]=="-t" or sys.argv[2]=="-times":
                    try:
                        if int(sys.argv[3])>5: MaxHilos=5
                        elif int(sys.argv[3])>=1: MaxHilos=int(sys.argv[3])
                    except ValueError:
                        if os.path.isfile("debug.on"): print("DEBUG-?: [*] Debe colocar un numero valido de Descargas Simultaneas!")
                        else: print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                        exit()
                    if sys.argv[4]=="-o" or sys.argv[4]=="-only_audio":
                        try: DescargaHilos(5, MaxHilos, False, True)
                        except OSError:
                            yt=pytube.Playlist(sys.argv[4])
                            SoloAudio=True
                    else:
                        try: DescargaHilos(4, MaxHilos, False, False)
                        except OSError:
                            yt=pytube.Playlist(sys.argv[3])
                            SoloAudio=False
                    Miniatura=False
                else:
                    if sys.argv[2]=="-o" or sys.argv[2]=="-only_audio":
                        yt=pytube.Playlist(sys.argv[3])
                        SoloAudio=True
                    else:
                        yt=pytube.Playlist(sys.argv[2])
                        SoloAudio=False
                    Miniatura=False
            except pytube.exceptions.RegexMatchError:
                if os.path.isfile("debug.on"): print("DEBUG-?: [*] Url No Valida!")
                else: print("[*] Url No Valida!")
                exit()

        # ---------------------------- Descargar Playlist ---------------------------- #
        Total=yt.length
        Contador=1
        for Video in yt.videos:
            print(f"[!] Playlist:{yt.title} --- [ {Contador} / {Total} ]")
            print("├──[!] Titulo: "+Video.title)
            if Miniatura:
                print("├──[!] Miniatura: "+Video.thumbnail_url)
            print("├──", end=ConvertirSegundos(Video.length)+"\n")
            if SoloAudio: DescargadorPrincipal(Video, OnlyAudio=True)
            else: 
                try: ResAsignada; DescargadorPrincipal(Video, Resolucion=ResAsignada)
                except UnboundLocalError: DescargadorPrincipal(Video)
            print("\n└──[+] Completado...")
            os.system("cls")
            Contador+=1
        print("\n[+] Todos Los videos Descargados :D")