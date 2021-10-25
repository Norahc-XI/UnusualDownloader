import re
import pytube
import moviepy
import threading
import shutil
from time import sleep
from random import sample
from pytube.cli import on_progress
from moviepy.editor import os, sys
from Assets.Extensiones import MostrarInfo

RESPERMITIDAS=['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p']

# ------------------------------ Nota: Terminado ----------------------------- #

Error=0
ErrorLista=[]

def DescargaHilos(Url:str, Miniatura:bool=False, Resolucion:str="360p"):
    "Descargar videos desde archivo txt con hilos para multiples descargas al mismo tiempo"
    global Error
    global ErrorLista
    # ---------------- Comprueba que la url sea valida y si se va a usar la barra de progreso ---------------- #
    try:
        # --------------------------------- Prueba 1 --------------------------------- #
        yt=pytube.YouTube(Url)
        # --------------------------------- Prueba 2 --------------------------------- #
        Progresivo=yt.streams.filter(res=Resolucion, file_extension="mp4").first()
        if Progresivo.is_progressive: pass
        if os.path.isfile("debug.on"): print("DEBUG-PROGRESIVO: "); print(Progresivo)
        Saltar=False
    except pytube.exceptions.RegexMatchError: #Error 1
        if os.path.isfile("debug.on"): print("DEBUG-0: [*] Url No Valida!\n")
        else: print("[*] Url No Valida!\n")
        Error+=1
        ErrorLista.append(Url)
        Saltar=True
    except AttributeError: #Error 2
        if os.path.isfile("debug.on"): print("DEBUG-1: [*] Video no disponible en la resolucion selecionada!")
        else: print("[*] Video no disponible en la resolucion selecionada!")
        Error+=1
        ErrorLista.append(Url)
        Saltar=True
    except pytube.exceptions.VideoUnavailable: #Error 3
        if os.path.isfile("debug.on"): print("DEBUG-2: [*] El video especificado no esta disponible!")
        else: print("[*] El video especificado no esta disponible!")
        Error+=1
        ErrorLista.append(Url)
        Saltar=True
    if not Saltar:
        if not Progresivo.is_progressive:
            if not os.path.isdir("temp"):
                os.makedirs("temp")
            # --- Descargar el video individual y el audio aparte para juntarlos y dar un unico archivo --- #
            abc="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            TempVideo="".join(sample(abc, 6))
            TempAudio="".join(sample(abc, 6))
            TempNameVideo="temp\\"+TempVideo+".mp4"
            TempNameAudio="temp\\"+TempAudio+".mp4"
            try: MostrarInfo(yt, Miniatura)
            except pytube.exceptions.VideoUnavailable:
                if os.path.isfile("debug.on"): print("DEBUG-3: [*] El video especificado no esta disponible!")
                else: print("[*] El video especificado no esta disponible!")
                exit()
            print("\n")
            yt.streams.filter(res=Resolucion, file_extension="mp4").first().download(filename=TempNameVideo)
            yt.streams.filter(only_audio=True, abr="128kbps").first().download(filename=TempNameAudio)
            # -------------- Limpiar el titulo del video de caracteres raros -------------- #
            LetrasNombres=[]
            ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|', '\\']
            for Letra in yt.title:
                if Letra not in ParametrosNoValidos:
                    LetrasNombres.append(str(Letra))
                else: pass
            NombreArchivo="".join(LetrasNombres)+".mp4"
            # ----------------------------- Componer el video ---------------------------- #
            try:
                moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio(TempNameVideo, TempNameAudio, NombreArchivo)
                os.remove(TempNameVideo)
                os.remove(TempNameAudio)
            except:
                print("[*] No se ha podido descargar el video, pero los archivos sin juntar se guardaran en el directorio de ejecucion, por si deseamanualmente componerlos, error se debe al titulo del video.")
                exit()
            try:
                try:            
                    if os.path.isfile(sys.argv[7])==False and os.path.exists(sys.argv[7]): shutil.move(NombreArchivo, sys.argv[7])
                    else: raise IndexError
                except IndexError:
                    try:
                        if os.path.isfile(sys.argv[8])==False and os.path.exists(sys.argv[8]): shutil.move(NombreArchivo, sys.argv[8])
                        else: raise IndexError
                    except IndexError: pass
            except shutil.Error:
                os.remove(NombreArchivo)
        else:
            # -------------------- Descargar video si ya esta conjunto ------------------- #
            try: MostrarInfo(yt, Miniatura)
            except pytube.exceptions.VideoUnavailable:
                if os.path.isfile("debug.on"): print("DEBUG-4: [*] El video especificado no esta disponible!")
                else: print("[*] El video especificado no esta disponible")
                exit()
            print("\n")
            VideoADescargar=yt.streams.filter(res=Resolucion, file_extension="mp4", progressive=True).first()
            # --- Descargalo en la ubicacion dicha por el usuario o en la de ejecucion --- #
            try:
                if os.path.isfile(sys.argv[7])==False and os.path.exists(sys.argv[7]): VideoADescargar.download(sys.argv[7])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.isfile(sys.argv[8])==False and os.path.exists(sys.argv[8]): VideoADescargar.download(sys.argv[8])
                    else: raise IndexError
                except IndexError: VideoADescargar.download()

def DescargarAndComponer(yt:pytube.YouTube, Resolucion:str):
    "Descargar y componer el video y audio"
    yt.streams.filter(res=Resolucion, file_extension="mp4").first().download(filename="video.mp4")
    yt.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio.mp4")
    # -------------- Limpiar el titulo del video de caracteres raros -------------- #
    LetrasNombres=[]
    ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|', '\\']
    for Letra in yt.title:
        if Letra not in ParametrosNoValidos:
            LetrasNombres.append(str(Letra))
        else: pass
    NombreArchivo="".join(LetrasNombres)+".mp4"
    # ----------------------------- Componer el video ---------------------------- #
    try:
        print("[+] Descargado.\n")
        moviepy.video.io.ffmpeg_tools.ffmpeg_merge_video_audio("video.mp4", "audio.mp4", NombreArchivo)
        os.remove("video.mp4")
        os.remove("audio.mp4")
    except:
        print("[*] No se ha podido descargar el video, pero los archivos sin juntar se guardaran en el directorio de ejecucion, por si deseamanualmente componerlos, error se debe al titulo del video.")
        exit()
    return NombreArchivo

def DescargadorArchivoLista(Ubicacion:int, Miniatura:bool=False, Resolucion:str="360p"):
    "Descargar videos usando los links provenientes de un archivo .txt"
    Error=0
    ErrorList=[]
    Archivo=open(sys.argv[Ubicacion], "r")
    try:
        if re.search(".txt", sys.argv[Ubicacion]) is not None and os.path.isfile(sys.argv[Ubicacion]):
            if os.path.getsize(sys.argv[Ubicacion])!=0:
                Contador=1
                Total=len(Archivo.readlines())
                Archivo.seek(0)
                for Url in Archivo:
                    print(f"|-------- Descargando [ {Contador} / {Total} ] --------|\n")
                    try:
                        # --------------------------------- Prueba 1 --------------------------------- #
                        yt=pytube.YouTube(Url.replace("\n", ""), on_progress_callback=on_progress)
                        # --------------------------------- Prueba 2 --------------------------------- #
                        Progresivo=yt.streams.filter(res=Resolucion, file_extension="mp4").first()
                        if Progresivo.is_progressive: pass
                        if os.path.isfile("debug.on"): print("DEBUG-PROGRESIVO: "); print(Progresivo)
                        Saltar=False
                    except pytube.exceptions.RegexMatchError: #Error 1
                        if os.path.isfile("debug.on"): print("DEBUG-5: [*] Url No Valida!\n")
                        else: print("[*] Url No Valida!\n")
                        Error=+1
                        ErrorList.append(Url)
                        Saltar=True
                        sleep(2)
                    except AttributeError: #Error 2
                        if os.path.isfile("debug.on"): print("DEBUG-6: [*] Video no disponible en la resolucion selecionada!")
                        else: print("[*] Video no disponible en la resolucion selecionada!")
                        Error=+1
                        ErrorList.append(Url)
                        Saltar=True
                        sleep(2)
                    if not Saltar:
                        try: MostrarInfo(yt, Miniatura)
                        except pytube.exceptions.VideoUnavailable:
                            if os.path.isfile("debug.on"): print("DEBUG-7: [*] El video especificado no esta disponible!")
                            else: print("[*] El video especificado no esta disponible!")
                            exit()
                        if not Progresivo.is_progressive:
                            # --- Descargar el video individual y el audio aparte para juntarlos y dar un unico archivo --- #
                            NombreArchivo=DescargarAndComponer(yt, Resolucion)
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
                                                if os.path.isfile(sys.argv[9])==False and os.path.exists(sys.argv[9]): shutil.move(NombreArchivo, sys.argv[9])
                                                else: raise IndexError
                                            except IndexError: pass
                        else:
                            # -------------------- Descargar video si ya esta conjunto ------------------- #
                            VideoADescargar=yt.streams.filter(res=Resolucion, file_extension="mp4", progressive=True).first()
                            # --- Descargalo en la ubicacion dicha por el usuario o en la de ejecucion --- #
                            try:
                                if os.path.isfile(sys.argv[3])==False and os.path.exists(sys.argv[3]): VideoADescargar.download(sys.argv[3]) 
                                else: raise IndexError
                            except IndexError:
                                try:
                                    if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): VideoADescargar.download(sys.argv[4])
                                    else: raise IndexError
                                except IndexError:
                                    try:
                                        if os.path.isfile(sys.argv[6])==False and os.path.exists(sys.argv[6]): VideoADescargar.download(sys.argv[6])
                                        else: raise IndexError
                                    except IndexError:
                                        try:
                                            if os.path.isfile(sys.argv[8])==False and os.path.exists(sys.argv[8]): VideoADescargar.download(sys.argv[8])
                                            else: raise IndexError
                                        except IndexError: VideoADescargar.download()
                    os.system("cls")
                    Contador+=1
                if Error==0: print("\n[+] Todos Los videos Descargados :D.")
                else: print(f"\n[+] Todos Los videos Descargados con {Error} Error :(")
            else:
                if os.path.isfile("debug.on"): print("DEBUG-8: [*] Archivo Vacio")
                else: print("[*] Archivo Vacio")
        else: 
            if os.path.isfile("debug.on"): print("DEBUG-9: [*] Formato Invalido - Solo se permiten archivos txt")
            else: print("[*] Formato Invalido - Solo se permiten archivos txt")
    except UnicodeDecodeError:
        if os.path.isfile("debug.on"): print("DEBUG-10: [*] Archivo No Valido!")
        else: print("[*] Archivo No Valido!")
    Archivo.close()
    exit()
    
def VideoOpciones(Rango:int):
    os.system("title UnusualDonwloader - Descargando Videos")
    if Rango>9:
        # ---------- Si el rango es mayor al permitidor se sale el programa ---------- #
        print("[*] Demasiados Valores!")
        exit()

    elif Rango>=4 and Rango<=9:
        def VariosHilos(Ubiacion:int, Imagen:bool, maxHilos:int):
            "Descargar mediante hilos con un limite de 5 hilos activos"
            global Error
            global ErrorLista
            Archivo=open(sys.argv[Ubiacion], "r") # revisar si es un archivo
            if os.path.getsize(sys.argv[Ubiacion])!=0:
                LinksVideos=[]
                Res=RESPERMITIDAS[RESPERMITIDAS.index(sys.argv[3])]
                for Link in Archivo: LinksVideos.append(Link.replace("\n", ""))
                LinksVideos.reverse()
                Total=len(LinksVideos)
                Contador=maxHilos
                ContenedorHilos=[]
                while len(LinksVideos)!=0:
                    if len(LinksVideos)<=maxHilos: maxHilos=len(LinksVideos)
                    print(f"|-------- Descargando [ {Contador} / {Total} ] --------|\n")
                    for _ in range(maxHilos):
                        try:
                            hilo=threading.Thread(target=DescargaHilos, args=(LinksVideos[0], Imagen, Res), daemon=True)
                            hilo.start()
                            ContenedorHilos.append(hilo)
                        except pytube.exceptions.RegexMatchError:
                            if os.path.isfile("debug.on"): print("DEBUG-11: [*] No se ha podido descargar: "+LinksVideos[0])
                            else: print("[*] No se ha podido descargar: "+LinksVideos[0])
                            Error+=1
                            ErrorLista.append(LinksVideos[0])
                        LinksVideos.pop(0)
                    for h in ContenedorHilos:
                        h.join()
                    Contador+=maxHilos
                    os.system("cls")
                    if os.path.isfile("debug.on"): print("DEBUG-HILOS: Vuelta dada")
                if os.path.isdir("temp"):
                    os.removedirs("temp")
                if Error==0:
                    print("\n[+] Todos Los videos Descargados :D.")
                else: 
                    print(f"\n[+] No se han podido descargar {Error} videos: ")
                    for i in ErrorLista: print(i)
            else:
                if os.path.isfile("debug.on"): print("DEBUG-12: [*] Archivo Vacio!")
                else: print("[*] Archivo Vacio!")
            Archivo.close()
            exit()

        if sys.argv[2].lower()=="-r" or sys.argv[2].lower()=="-resolution" or sys.argv[2].lower()=="-res": # Revisar las opciones de resoluciones
            def DescargarPorResolucion(yt, Index):
                "Funcion encargada de descargar un video indicado por el usuario en la resolucion que el especifique, y si mostrar la miniatura si el lo desea tambien."
                print("\n[|] Descargando :)...")
                Progresivo=yt.streams.filter(res=RESPERMITIDAS[Index], file_extension="mp4").first()
                try: 
                    if Progresivo.is_progressive: pass
                except AttributeError:
                    if os.path.isfile("debug.on"): print("DEBUG-13: [*] Video no disponible en la resolucion selecionada!")
                    else: print("[*] Video no disponible en la resolucion selecionada!")
                    exit()
                if not Progresivo.is_progressive:
                    NombreArchivo=DescargarAndComponer(yt, RESPERMITIDAS[Index])
                    # --- Mover el video a la ubicacion dicha por el usuario, siempre y cuando no sea un archivo y exista la direccion --- #
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
                            except IndexError: pass
                else:
                    # ---------------------- Extraer el video ya compuesto --------------------- #
                    VideoADescargar=yt.streams.filter(res=RESPERMITIDAS[Index], progressive=True, file_extension="mp4").first()
                    # ------------- Descargarlo en la ubicacion dicha por el usuario ------------- #
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
                            except IndexError: VideoADescargar.download()
                print("\n[+] Descargado :D.")
                exit()
    
            if sys.argv[3] in RESPERMITIDAS: ResAsignada=True
            else: ResAsignada=False
            if not ResAsignada: # Verifica si la resolucion fue asignada
                try:
                    if sys.argv[3].lower()=="-i" or sys.argv[3].lower()=="-image": 
                        yt=pytube.YouTube(sys.argv[4], on_progress_callback=on_progress)
                        Miniatura=True
                    else:
                        yt=pytube.YouTube(sys.argv[3], on_progress_callback=on_progress)
                        Miniatura=False
                    try: MostrarInfo(yt, Miniatura)
                    except pytube.exceptions.VideoUnavailable:
                        if os.path.isfile("debug.on"): print("DEBUG-14: [*] El video especificado no esta disponible!")
                        else: print("[*] El video especificado no esta disponible!")
                        exit()
                    TempRes=[]
                    for Stream in yt.streams.order_by("resolution"):
                        if Stream.resolution not in TempRes: TempRes.append(Stream.resolution)
                    Id=1
                    print("\n----------Resoluciones Disponibles: ")
                    for Res in TempRes:
                        print(f"[{Id}]---{Res}")
                        Id+=1
                    try:
                        Index=int(input("Que calidad desea descargar?: "))
                        DescargarPorResolucion(yt, Index-1) # Llammar a la funcion
                    except ValueError:
                        if os.path.isfile("debug.on"): print("DEBUG-15: [*] Argumento invalido!")
                        else: print("[*] Argumento invalido!")
                        exit()
                except pytube.exceptions.RegexMatchError:
                    if os.path.isfile("debug.on"): print("DEBUG-16: [*] Url no valida!")
                    else: print("[*] Url no valida!")
                    exit()
            else:
                try:
                    if sys.argv[4].lower()=="-i" or sys.argv[4].lower()=="-image": # Comprobar si desea ver la miniatura
                        if sys.argv[5].lower()=="-t" or sys.argv[5].lower()=="-times":
                            try:
                                if int(sys.argv[6])>=5: maxHilos=5
                                elif int(sys.argv[6])>=2: maxHilos=int(sys.argv[6])
                                elif int(sys.argv[6])==1: DescargadorArchivoLista(7, True, Resolucion=sys.argv[3])
                            except ValueError:
                                print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                                exit()
                            try: VariosHilos(7, True, maxHilos)
                            except OSError:
                                yt=pytube.YouTube(sys.argv[5], on_progress_callback=on_progress)
                                Miniatura=True
                        else:
                            try: DescargadorArchivoLista(5, True, Resolucion=sys.argv[3])
                            except OSError:
                                yt=pytube.YouTube(sys.argv[5], on_progress_callback=on_progress)
                                Miniatura=True
                    else:
                        if sys.argv[4].lower()=="-t" or sys.argv[4].lower()=="-times":
                            try:
                                if int(sys.argv[5])>=5: maxHilos=5
                                elif int(sys.argv[5])>=2: maxHilos=int(sys.argv[5])
                                elif int(sys.argv[5])==1: DescargadorArchivoLista(6, False, Resolucion=sys.argv[3])
                            except ValueError:
                                print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                                exit()
                            try: VariosHilos(6, False, maxHilos)
                            except OSError:
                                yt=pytube.YouTube(sys.argv[4], on_progress_callback=on_progress)
                                Miniatura=False
                        else:
                            try: DescargadorArchivoLista(4, False, Resolucion=sys.argv[3])
                            except OSError:
                                yt=pytube.YouTube(sys.argv[4], on_progress_callback=on_progress)
                                Miniatura=False
                    Index=RESPERMITIDAS.index(sys.argv[3])
                    try: MostrarInfo(yt, Miniatura)
                    except pytube.exceptions.VideoUnavailable:
                        if os.path.isfile("debug.on"): print("DEBUG-17: [*] El video especificado no esta disponible!")
                        else: print("[*] El video especificado no esta disponible!")
                        exit()
                    DescargarPorResolucion(yt, Index) # Llamar funcion
                except UnicodeDecodeError:
                    if os.path.isfile("debug.on"): print("DEBUG-18: [*] Url No Valida!")
                    else: print("[*] Url No Valida!")
                    exit()

    if Rango>=3 and Rango<=5:
        "Descargar videos simplificado"
        if sys.argv[2].lower()=="-i" or sys.argv[2].lower()=="-image":
            try: DescargadorArchivoLista(3, True)
            except OSError:
                try:
                    yt=pytube.YouTube(sys.argv[3], on_progress_callback=on_progress)
                    Miniatura=True
                except pytube.exceptions.RegexMatchError:
                    if os.path.isfile("debug.on"): print("DEBUG-19: [*] Url No Valida!")
                    else: print("[*] Url No Valida!")
                    exit()
        else:
            try:  DescargadorArchivoLista(2, False)
            except OSError:
                try:    
                    yt=pytube.YouTube(sys.argv[2], on_progress_callback=on_progress)
                    Miniatura=False
                except pytube.exceptions.RegexMatchError:
                    if os.path.isfile("debug.on"): print("DEBUG-20: [*] Url No Valida!")
                    else: print("[*] Url No Valida!")
                    exit()
        try:
            MostrarInfo(yt, Miniatura)
        except pytube.exceptions.VideoUnavailable:
            if os.path.isfile("debug.on"): print("DEBUG-21: [*] El video especificado no esta disponible!")
            else: print("[*] El video especificado no esta disponible!")
            exit()
        Afirmacion=input("\nDesea Descargar este Video?(S/n): ").lower()
        if Afirmacion=="s" or Afirmacion=="si" or Afirmacion=="":
            print("\n[|] Descargando :)...")
            try:
                if os.path.isfile(sys.argv[3])==False and os.path.exists(sys.argv[3]): yt.streams.get_highest_resolution().download(sys.argv[3])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): yt.streams.get_highest_resolution().download(sys.argv[4])
                    else: raise IndexError
                except IndexError: yt.streams.get_highest_resolution().download()
            print("###\n[+] Descargado :D.")
        else: print("[*] Descarga Cancelada.")