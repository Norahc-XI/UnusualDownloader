import pytube
import moviepy
import shutil
import requests
from os import path
from mutagen import mp3,id3
from pytube.cli import on_progress
from moviepy.editor import AudioFileClip, os, sys

def DescargarMiniatura(Url):
    """Doc: Descargar la miniatura del video para colocarlo como caratula del audio."""
    Peticion=requests.get(Url)
    Archivo=open("mini.png", "wb")
    Archivo.write(Peticion.content)
    Archivo.close()

def ConvertirSegundos(SegundosOriginal):
    """Doc: Funcion encargada de convertir los segundos a minutos, de manera que sea mas facil a la vista y lectura, Lo hace diviendo los segundos por 60, y tomando el cociente como minutos y el resto como los segundos."""
    Minutos, Segundos=divmod(SegundosOriginal, 60)
    BaseDecimal=[0,1,2,3,4,5,6,7,8,9]
    if Segundos in BaseDecimal:
        Segundos=str(0)+str(Segundos)
    print("├──[!] Duración: {}:{}".format(Minutos, Segundos))

def Descargar(Video, Only_audio=False, Resolucion=None):
    """Doc: Funcion encargada de descargar los multiples videos de la lista de reproduccion, segun los parametros establecidos por el usuario."""
    Video.register_on_progress_callback(on_progress)
    Stream=Video.streams.filter(res=Resolucion, file_extension="mp4").first()
    try:
        if Only_audio:
            Video.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio")
            DescargarMiniatura(Video.thumbnail_url)
            ArchivoAudio=AudioFileClip("audio.mp4")
            LetrasNombre=[]
            ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
            for Letra in Video.title:
                if Letra not in ParametrosNoValidos:
                    LetrasNombre.append(str(Letra))
            NombreArchivo="".join(LetrasNombre)+".mp3"
            print("###\n")
            ArchivoAudio.write_audiofile(NombreArchivo)
            AudioConMiniatura=mp3.MP3(NombreArchivo)
            AudioConMiniatura.tags.add(id3.APIC(data=open("mini.png",'rb').read()))
            AudioConMiniatura.save()
            os.remove("audio.mp4")
            os.remove("mini.png")
            try:
                if path.exists(sys.argv[4]):
                    if path.isfile(sys.argv[4])==False:
                        shutil.move(NombreArchivo, sys.argv[4])
                    else:
                        raise TypeError
                else:
                    raise TypeError
            except (TypeError, IndexError):
                try:
                    if path.exists(sys.argv[5]):
                        if path.isfile(sys.argv[5])==False:
                            shutil.move(NombreArchivo, sys.argv[5])
                        else:
                            raise TypeError
                    else:
                        raise TypeError
                except (TypeError, IndexError):
                    pass
        elif Stream.is_progressive==False:
            Video.streams.filter(res=Resolucion, file_extension="mp4").first().download(filename="video")
            Video.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio")
            LetrasNombres=[]
            ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
            for Letra in Video.title:
                if Letra not in ParametrosNoValidos:
                    LetrasNombres.append(str(Letra))
                else:
                    pass
            NombreArchivo="".join(LetrasNombres)+".mp4"
            try:
                print("###\n")
                moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio("video.mp4", "audio.mp4", NombreArchivo)
                os.remove("video.mp4")
                os.remove("audio.mp4")
            except:
                print("[*] No se ha podido descargar el video, pero los archivos sin juntar se guardaran en el directorio de ejecucion, por si desea manualmente componerlos, el error se debe al titulo del video.")
                exit()
            try:
                if path.exists(sys.argv[4]):
                    if path.isfile(sys.argv[4])==False:
                        shutil.move(NombreArchivo, sys.argv[4])
                    else:
                        raise TypeError
                else:
                    raise TypeError
            except (TypeError, IndexError):
                try:
                    if path.exists(sys.argv[5]):
                        if path.isfile(sys.argv[5])==False:
                            shutil.move(NombreArchivo, sys.argv[5])
                        else:
                            raise TypeError
                    else:
                        raise TypeError
                except (TypeError, IndexError):
                    try:
                        if path.exists(sys.argv[6]):
                            if path.isfile(sys.argv[6])==False:
                                shutil.move(NombreArchivo, sys.argv[6])
                            else:
                                raise TypeError
                        else:
                            raise TypeError
                    except (TypeError, IndexError):
                        pass
        else:
            VideoADescargar=Video.streams.filter(res=Resolucion, file_extension="mp4", progressive=True).first()
            try:
                try:
                    if path.exists(sys.argv[3]):
                        if path.isfile(sys.argv[3])==False:
                            VideoADescargar.download(sys.argv[3])
                        else:
                            raise TypeError
                    else:
                        raise TypeError 
                except (TypeError, IndexError):
                    try:
                        if path.exists(sys.argv[4]):
                            if path.isfile(sys.argv[4])==False:
                                    VideoADescargar.download(sys.argv[4])
                            else:
                                raise TypeError
                        else:
                            raise TypeError
                    except: 
                        if path.exists(sys.argv[5]):
                            if path.isfile(sys.argv[5])==False:
                                VideoADescargar.download(sys.argv[5])
                        else:
                            raise TypeError
            except (TypeError, IndexError):
                VideoADescargar.download()
            print("├###")
    except AttributeError:
        VideoADescargar=Video.streams.get_highest_resolution()
        try:
            try:
                if path.exists(sys.argv[3]):
                    if path.isfile(sys.argv[3])==False:
                        VideoADescargar.download(sys.argv[3])
                    else:
                        raise TypeError
                else:
                    raise TypeError 
            except (TypeError, IndexError):
                try:
                    if path.exists(sys.argv[4]):
                        if path.isfile(sys.argv[4])==False:
                                VideoADescargar.download(sys.argv[4])
                        else:
                            raise TypeError
                    else:
                        raise TypeError
                except: 
                    if path.exists(sys.argv[5]):
                        if path.isfile(sys.argv[5])==False:
                            VideoADescargar.download(sys.argv[5])
                    else:
                        raise TypeError
        except (TypeError, IndexError):
            VideoADescargar.download()
        print("├###")
    print("└──[+] Descargado :D\n")

def ListaOpciones(ResolucionesPermitidas):
    """Doc: Funcion principal encargada de procesar los parametros establecidos por el usuario, y ejecutar lo que el ordene."""
    if sys.argv[2]=="-resolution":
        try:
            for Resolucion in ResolucionesPermitidas:
                if sys.argv[3]==Resolucion:
                    ResolucionAsignada=Resolucion
                    ResolucionVerificar=True
                    break
                else:
                    ResolucionVerificar=False
        except IndexError:
            print("[*] Debe Establecer una Resolucion")
            exit()
        try:
            try:
                if sys.argv[4]=="-image":
                    if sys.argv[5]=="-only_audio":
                        if ResolucionVerificar=="False":
                            yt=pytube.Playlist(sys.argv[6])
                            SoloAudio=True
                        else:
                            print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!!!")
                            exit()
                    else:
                        yt=pytube.Playlist(sys.argv[5])
                        SoloAudio=False
                    Miniatura=True
                else:
                    if sys.argv[4]=="-only_audio":
                        if ResolucionVerificar=="False":
                            yt=pytube.Playlist(sys.argv[5])
                            SoloAudio=True
                        else:
                            print("[*] No Puede Colocar Resolucion a Descargas de Solo Audio!!!")
                            exit()
                    else:
                        yt=pytube.Playlist(sys.argv[4])
                        SoloAudio=False
                    Miniatura=False
            except IndexError:
                yt=pytube.Playlist(sys.argv[3])
                Miniatura=False
                SoloAudio=False
        except KeyError:
            print("[*] Url No Valida!!!")
        N=0
        for Null in yt.videos:
            N+=1
        Num=1
        for Video in yt.videos:
            print("\n[------------------------------ UnusualDownloader ------------------------------]\n")
            print("|[!] Playlist: "+yt.title)
            print("|[!] Videos: [ "+str(Num)+" / "+str(N)+" ]")
            print("├──[!] Titulo: "+Video.title)
            if Miniatura:
                print("├──[!] Miniatura: "+Video.thumbnail_url)
            ConvertirSegundos(Video.length)
            if SoloAudio:
                Descargar(Video, Only_audio=True)
            else:
                try:
                    Descargar(Video, Resolucion=ResolucionAsignada)
                except UnboundLocalError:
                    Descargar(Video)
            os.system("cls")
            Num+=1
        print("\n[+] Todos Los videos Descargados :D.")
            
    else:
        try:
            if sys.argv[2]=="-image":
                if sys.argv[3]=="-only_audio":
                    yt=pytube.Playlist(sys.argv[4])
                    SoloAudio=True
                else:
                    yt=pytube.Playlist(sys.argv[3])
                    SoloAudio=False
                Miniatura=True
            else:
                if sys.argv[2]=="-only_audio":
                    yt=pytube.Playlist(sys.argv[3])
                    SoloAudio=True
                else:
                    yt=pytube.Playlist(sys.argv[2])
                    SoloAudio=False
                Miniatura=False
        except (pytube.exceptions.RegexMatchError, KeyError):
            print("[*] Url No Valida!!!")
            exit()
        N=0
        for Null in yt.videos:
            N+=1
        Num=1
        for Video in yt.videos:
            print("\n[------------------------------ UnusualDownloader ------------------------------]\n")
            print("|[!] Playlist: "+yt.title)
            print("|[!] Videos: [ "+str(Num)+" / "+str(N)+" ]")
            print("├──[!] Titulo: "+Video.title)
            if Miniatura:
                print("├──[!] Miniatura: "+Video.thumbnail_url)
            ConvertirSegundos(Video.length)
            if SoloAudio:
                Descargar(Video, Only_audio=True)
            else:
                Descargar(Video, Resolucion="360p")
            os.system("cls")
            Num+=1
        print("\n[+] Todos Los videos Descargados :D.")