import pytube
import moviepy
import threading
from time import sleep
from shutil import move
from pytube.cli import on_progress
from moviepy.editor import os, sys


def ConvertirSegundos(SegundosOriginal):
    """Doc: Funcion encargada de convertir los segundos a minutos, de manera que sea mas facil a la vista y lectura, Lo hace diviendo los segundos por 60, y tomando el cociente como minutos y el resto como los segundos."""
    Minutos, Segundos=divmod(SegundosOriginal, 60)
    BaseDecimal=[0,1,2,3,4,5,6,7,8,9]
    if Segundos in BaseDecimal:
        Segundos=str(0)+str(Segundos)
    print("[!] Duración: {}:{}".format(Minutos, Segundos))

def MostrarInfo(yt, Miniatura):
    """Doc: Mostrar la informacion del video a descargar"""
    print("[!] Titulo: "+yt.title)
    ConvertirSegundos(yt.length)
    if Miniatura:
        print("[!] Miniatura: "+yt.thumbnail_url)

def DescargarNoProgresivo(yt ,Resolucion):
    """Doc: Descargar el video y audio separado y unirlos"""
    yt.streams.filter(res=Resolucion, file_extension="mp4").first().download(filename="video")
    yt.streams.filter(only_audio=True, abr="128kbps").first().download(filename="audio")
    # -------------- Limpiar el titulo del video de caracteres raros -------------- #
    LetrasNombres=[]
    ParametrosNoValidos=['/', ':', '*', '?', '"', '<', '>', '|']
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

def DescargadorViaTXT(Url, Miniatura=False, Resolucion="360p", BarraProgreso=False, ErrorVar=0):
    """Doc: Funcion encargada de descargar multiples videos desde un archivo txt, con las opciones de escojer si el usuario quiere ver el link hacia la miniatura del video y la resolucion que sea que todos los videos se descarguen, con la opcion de multidescarga simultanea."""
    print("Descargar via TXT")
        # ---------------- Comprueba que la url sea valida y si se va a usar la barra de progreso ---------------- #
    if BarraProgreso==True: yt=pytube.YouTube(Url, on_progress_callback=on_progress)
    else: yt=pytube.YouTube(Url)
    Saltar=False
    """except:
        if os.path.isfile("debug.on"): print("DEBUG-1: [*] Url No Valida!!!\n")
        else: print("[*] Url No Valida!!!\n")
        ErrorVar+=1
        Saltar=True"""
    if Saltar==False:
        try:
            EsProgresivo=yt.streams.filter(res=Resolucion, file_extension="mp4").first()
            if EsProgresivo.is_progressive: pass
            if os.path.isfile("debug.on"): print("DEBUG-PROGRESIVO: "); print(EsProgresivo)
        except AttributeError:
            if os.path.isfile("debug.on"): print("DEBUG-2: [*] Video no disponible en la resolucion selecionada!!")
            else: print("[*] Video no disponible en la resolucion selecionada!!")
            exit()
        if EsProgresivo.is_progressive==False:
            # --- Descargar el video individual y el audio aparte para juntarlos y dar un unico archivo --- #
            MostrarInfo(yt, Miniatura)
            NombreArchivo=DescargarNoProgresivo(yt, Resolucion)
            try:
                if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): move(NombreArchivo, sys.argv[4])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.isfile(sys.argv[6])==False and os.path.exists(sys.argv[6]): move(NombreArchivo, sys.argv[6])
                    else: raise IndexError
                except IndexError:
                    try:
                        if os.path.isfile(sys.argv[7])==False and os.path.exists(sys.argv[7]): move(NombreArchivo, sys.argv[7])
                        else: raise IndexError
                    except IndexError:
                        try:
                            if os.path.isfile(sys.argv[9])==False and os.path.exists(sys.argv[9]): move(NombreArchivo, sys.argv[9])
                            else: raise IndexError
                        except IndexError: pass
        else:
            # -------------------- Descargar video si ya esta conjunto ------------------- #
            MostrarInfo(yt, Miniatura)
            VideoADescargar=yt.streams.filter(res=Resolucion, file_extension="mp4", progressive=True).first()
            # --- Descargalo en la ubicacion dicha por el usuario o en la de ejecucion --- #
            try:
                if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): VideoADescargar.download(sys.argv[4]) 
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
                            if os.path.isfile(sys.argv[9])==False and os.path.exists(sys.argv[9]): VideoADescargar.download(sys.argv[9])
                            else: raise IndexError
                        except IndexError: VideoADescargar.download()
            print("[+] Descargado.\n")
    sleep(1)
    return ErrorVar

def DescargarPorResolucion(yt, ResolucionesPermitidas, Index):
    """Doc: Funcion encargada de descargar un video indicado por el usuario en la resolucion que el especifique, y si mostrar la miniatura si el lo desea tambien."""
    print("\n[|] Descargando :)...")
    EsProgresivo=yt.streams.filter(res=ResolucionesPermitidas[Index], file_extension="mp4").first()
    try: 
        if EsProgresivo.is_progressive: pass
    except AttributeError:
        if os.path.isfile("debug.on"): print("DEBUG-3: [*] Video no disponible en la resolucion selecionada!!")
        else: print("[*] Video no disponible en la resolucion selecionada!!")
        exit()
    if EsProgresivo.is_progressive==False:
        NombreArchivo=DescargarNoProgresivo(yt, ResolucionesPermitidas[Index])
        # --- Mover el video a la ubicacion dicha por el usuario, siempre y cuando no sea un archivo y exista la direccion --- #
        try:
            if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): move(NombreArchivo, sys.argv[4])
            else: raise IndexError
        except IndexError:
            try:
                if os.path.isfile(sys.argv[5])==False and os.path.exists(sys.argv[5]): move(NombreArchivo, sys.argv[5])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.isfile(sys.argv[6])==False and os.path.exists(sys.argv[6]): move(NombreArchivo, sys.argv[6])
                    else: raise IndexError
                except IndexError: pass
    else:
        # ---------------------- Extraer el video ya compuesto --------------------- #
        VideoADescargar=yt.streams.filter(res=ResolucionesPermitidas[Index], progressive=True, file_extension="mp4").first()
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
    
def VideoOpciones(Rango, ResolucionesPermitidas):
    os.system("title UnusualDonwloader - Descargando Videos")
    if Rango>9:
        # ---------- Si el rango es mayor al permitidor se sale el programa ---------- #
        print("[*] Demasiados Valores!!!")
        exit()

    elif Rango>=4 and Rango<=9:
        def UnHilo(Ubicacion, Imagen):
            from win10toast import ToastNotifier # Importar libreria
            Notificacion=ToastNotifier()
            Archivo=open(sys.argv[Ubicacion], "r") # revisar si es un archivo
            if os.path.getsize(sys.argv[Ubicacion])!=0:
                Index=0
                for Resolucion in ResolucionesPermitidas: # Comprobrar que la resolucion sea valida
                    if Resolucion==sys.argv[3]: break
                    else: Index+=1
                ResolucionADescargar=ResolucionesPermitidas[Index]
                N=1
                Total=len(Archivo.readlines())
                Archivo.seek(0)
                for Url in Archivo:
                    # ------------------------------ Llamar funcion ------------------------------ #
                    print("|-------- Descargando [ "+str(N)+" / "+str(Total)+" ] --------|\n")
                    Errores=DescargadorViaTXT(Url[:-1], Miniatura=Imagen, Resolucion=ResolucionADescargar, Barra=True)
                    N+=1
                    os.system("cls")
                if Errores==0:
                    print("\n[+] Todos Los videos Descargados :D.")
                    Notificacion.show_toast("Descargas Terminadas","Se han descargado tus Videos",duration=10)
                else: 
                    print("\n[+] Se han descargado tu videos con "+str(Errores)+" Errores.")
                    Notificacion.show_toast("Descargas Terminadas","Se han descargado tu videos con "+str(Errores)+" Errores.",duration=10)
            else:
                if os.path.isfile("debug.on"): print("DEBUG-4: [*] Archivo Vacio")
                else: print("[*] Archivo Vacio")
            exit()

        def VariosHilos(Ubiacion, Imagen):
            from win10toast import ToastNotifier
            Archivo=open(sys.argv[Ubiacion], "r") # revisar si es un archivo
            if os.path.getsize(sys.argv[Ubiacion])!=0:
                Index=0
                for Resolucion2 in ResolucionesPermitidas: # Comprobrar que la resolucion sea valida
                    if Resolucion2==sys.argv[3]: break
                    else: Index+=1
                Resolucion_A_Descargar=ResolucionesPermitidas[Index]
                LinksVideos=[]
                for Link in Archivo:
                    LinksVideos.append(Link)
                Errores=0
                Total=len(LinksVideos)
                Iterador=len(LinksVideos)-1
                Descargados=len(LinksVideos)
                N=HilosMaximos
                while True:
                    if len(LinksVideos)>=HilosMaximos: Hilos=HilosMaximos
                    else: Hilos=len(LinksVideos)
                    print("|-------- Descargando [ "+str(N)+" / "+str(Total)+" ] --------|\n")
                    for X in range(Hilos):
                        try:
                            hilo=threading.Thread(target=DescargadorViaTXT, args=(LinksVideos[Iterador], Imagen, Resolucion_A_Descargar))
                            hilo.start()
                        except:
                            if os.path.isfile("debug.on"): print("DEBUG-5: [*] No se ha podido descargar: "+LinksVideos[Iterador])
                            else: print("[*] Url No Valida!!!")
                            Errores+=1
                        LinksVideos.remove(LinksVideos[Iterador])
                        Iterador-=1
                        Descargados-=1
                    hilo.join()
                    if Descargados==0:
                        break
                    else:
                        N+=Hilos
                        os.system("cls")
                        if os.path.isfile("debug.on"): print("DEBUG-HILOS: Vuelta dada")
            else:
                if os.path.isfile("debug.on"): print("DEBUG-?: [*] Archivo Vacio!")
                else: print("[*] Archivo Vacio!")
                exit()
            print("\n[+] Todos Los videos Descargados :D.")
            exit()

        if sys.argv[2].lower()=="-r" or sys.argv[2].lower()=="-resolution": # Revisar las opciones de resoluciones
            for Resolucion in ResolucionesPermitidas:
                if sys.argv[3]==Resolucion: ResolucionAsignada=True; break
                else: ResolucionAsignada=False
            if ResolucionAsignada==False: # Verificar si la resolucion fue asignada
                try:
                    if sys.argv[3].lower()=="-i" or sys.argv[3].lower()=="-image": 
                        yt=pytube.YouTube(sys.argv[4], on_progress_callback=on_progress)
                        Miniatura=True
                    else:
                        yt=pytube.YouTube(sys.argv[3], on_progress_callback=on_progress)
                        Miniatura=False
                    print("\n[------------------------------ UnusualDownloader ------------------------------]")
                    MostrarInfo(yt, Miniatura)
                    ResolucionesVideo=[]
                    # -------------- Guardar las resoluciones disponibles del video -------------- #
                    for Stream in yt.streams.order_by("resolution"):
                        if Stream.resolution not in ResolucionesVideo:
                            ResolucionesVideo.append(Stream.resolution)
                    print("\n----------Resoluciones Disponibles: ")
                    N=1
                    for Resolucion_A_Mostrar in ResolucionesVideo:
                        print("["+str(N)+"]---"+Resolucion_A_Mostrar)
                        N+=1
                    try:
                        Index=int(input("Que calidad desea descargar?: "))
                        DescargarPorResolucion(yt, ResolucionesPermitidas, Index-1) # Llammar a la funcion
                    except ValueError:
                        if os.path.isfile("debug.on"): print("DEBUG-6: [*] Argumento invalido!!!")
                        else: print("[*] Argumento invalido!!!")
                        exit()
                except pytube.exceptions.RegexMatchError:
                    if os.path.isfile("debug.on"): print("DEBUG-7: [*] Url no valida!!!")
                    else: print("[*] Url no valida!!!")
                    exit()
            else:
                try:
                    if sys.argv[4].lower()=="-i" or sys.argv[4].lower()=="-image": # Comprobar si desea ver la miniatura
                        if sys.argv[5].lower()=="-t" or sys.argv[5].lower()=="-times":
                            if int(sys.argv[6])>=5: HilosMaximos=5
                            elif int(sys.argv[6])>=2: HilosMaximos=int(sys.argv[6])
                            elif int(sys.argv[6])==1: UnHilo(7, True)
                            else:
                                print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                                exit()
                            try: VariosHilos(7, True)
                            except OSError:
                                yt=pytube.YouTube(sys.argv[5], on_progress_callback=on_progress)
                                Miniatura=True
                        else:
                            try: UnHilo(5, True)
                            except OSError:
                                yt=pytube.YouTube(sys.argv[5], on_progress_callback=on_progress)
                                Miniatura=True
                    else:
                        if sys.argv[4].lower()=="-t" or sys.argv[4].lower()=="-times":
                            if int(sys.argv[5])>=5: HilosMaximos=5
                            elif int(sys.argv[5])>=2: HilosMaximos=int(sys.argv[5])
                            elif int(sys.argv[5])==1: UnHilo(6, False)
                            else:
                                print("[*] Debe colocar un numero valido de Descargas Simultaneas!")
                                exit()
                            try: VariosHilos(6, False)
                            except OSError:
                                yt=pytube.YouTube(sys.argv[4], on_progress_callback=on_progress)
                                Miniatura=False
                        else:
                            try: UnHilo(4, False)
                            except OSError:
                                yt=pytube.YouTube(sys.argv[4], on_progress_callback=on_progress)
                                Miniatura=False
                    Index=0
                    for Resolucion in ResolucionesPermitidas: # Comprobrar que la resolucion sea valida
                        if Resolucion==sys.argv[3]: break
                        else: Index+=1
                    MostrarInfo(yt, Miniatura)
                    DescargarPorResolucion(yt, ResolucionesPermitidas, Index) # Llamar funcion
                except pytube.exceptions.RegexMatchError:
                    if os.path.isfile("debug.on"): print("DEBUG-8: [*] Url No Valida!!!")
                    else: print("[*] Url No Valida!!!")
                    exit()

    if Rango>=3 and Rango<=5:
        """Doc: Descarga un video de la manera mas rapida, permite ver la miniatura si el usuario lo desea y pide una confirmacion a la hora de descargar el video, para estar seguro que el video es el correcto usando como guia el titulo o la miniatura del video."""
        def MultiDescargas(Ubiacion, Imagen):
            from win10toast import ToastNotifier # Importar libreria
            Notificacion=ToastNotifier()
            Archivo=open(sys.argv[Ubiacion], "r")
            if os.path.getsize(sys.argv[Ubiacion])!=0:
                N=1
                Total=len(Archivo.readlines())
                Archivo.seek(0)
                for Url in Archivo:
                    print("|-------- Descargando [ "+str(N)+" / "+str(Total)+" ] --------|\n")
                    Errores=DescargadorViaTXT(Url, Miniatura=Imagen, BarraProgreso=True)
                    N+=1
                    os.system("cls")
                    print("DEBUG-TEMP: VUELTA")
                print("SALIDA FOR")
                if Errores==0:
                    print("\n[+] Todos Los videos Descargados :D.")
                    Notificacion.show_toast("Descargas Terminadas","Se han descargado tus Videos",duration=10)
                else: 
                    print("\n[+] Todos Los videos Descargados con %s Error :(", Errores)
                    Notificacion.show_toast("Descargas Terminadas","Se han descargado tus Videos con Errores",duration=10)
            else: print("[*] Archivo Vacio")
            exit()

        try:
            if sys.argv[2].lower()=="-i" or sys.argv[2].lower()=="-image":
                try: MultiDescargas(3, True)
                except OSError:
                    try:
                        yt=pytube.YouTube(sys.argv[3], on_progress_callback=on_progress)
                        Miniatura=True
                    except pytube.exceptions.RegexMatchError:
                        if os.path.isfile("debug.on"): print("DEBUG-9: [*] Url No Valida!!!")
                        else: print("[*] Url No Valida!!!")
                        exit()
            else:
                try:  MultiDescargas(2, False)
                except OSError:
                    try:    
                        yt=pytube.YouTube(sys.argv[2], on_progress_callback=on_progress)
                        Miniatura=False
                    except pytube.exceptions.RegexMatchError:
                        if os.path.isfile("debug.on"): print("DEBUG-10: [*] Url No Valida!!!")
                        else: print("[*] Url No Valida!!!")
                        exit()
        except UnicodeDecodeError:
            if os.path.isfile("debug.on"): print("DEBUG-11: [*] Archivo No Valido!!!")
            else: print("[*] Archivo No Valido!!!")
            exit()
        print("\n[------------------------------ UnusualDownloader ------------------------------]")
        print("[!] Titulo: "+yt.title)
        ConvertirSegundos(yt.length)
        if Miniatura==True:
            print("[!] Miniatura: "+yt.thumbnail_url)
        Afirmacion=input("\nDesea Descargar este Video?(S/n): ").lower()
        if Afirmacion=="s" or Afirmacion=="":
            print("\n[|] Descargando :)...")
            try:
                if os.path.isfile(sys.argv[3])==False and os.path.exists(sys.argv[3]): yt.streams.get_highest_resolution().download(sys.argv[3])
                else: raise IndexError
            except IndexError:
                try:
                    if os.path.isfile(sys.argv[4])==False and os.path.exists(sys.argv[4]): yt.streams.get_highest_resolution().download(sys.argv[4])
                    else: raise IndexError
                except IndexError:
                    yt.streams.get_highest_resolution().download()
            print("###\n[+] Descargado :D.")
        else:
            print("[*] Descarga Cancelada.")