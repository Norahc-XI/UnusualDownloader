import os
import sys
from shutil import rmtree
from urllib.error import URLError

Rango=len(sys.argv)

"""---Mejoreas pendientes---
+Intentar optimizar más si es posible
+archivo que almacene los links en casoq que se caiga la red, reanude la descarga donde quedo
+descargador de miniatura (listas de reproduciones, video, archivos .txt [con links])
+actualizar readme y doc
"""

if Rango==1 or sys.argv[1]=="-help":
    "Si no se especifica ningun valor, el programa enseñara la ayuda o si es introducido el comando '-help'."
    print("""\nUnusualDownloader.py ([-video or -v] [-audio or -a] [-playlist or -p]) (-r or -resolution) (-i or -image) (-t or -times)
    {-o or -only_audio} [url or File.txt] Path_Salida
     
    Descarga tus videos favoritos de Youtube.
     
    -help                   Muestra la documentación, si no se es especifica ningun valor aparecera igual.

    Opciones:
    -video                  Indica al programa que sea descargar un video
    -audio                  Indica al programa que sea descargar el audio de un video
    -playlist               Indica al programa que sea descargar los videos o audios de una lista de reproduccion

    Notas:
    [1]Solo puedes descargar video o listas de reproducciones publicas o ocultas.
    [2]La velocidad de descarga va a depender de su conexion a internet.

    Opciones de Descargas:
    -resolution             Especifica la resolucion en la que quieres descargar tus videos.
                            Ejemplo: * -resolution 1080p https://

    -image                  Esta opcion indica que desea ver la miniatura del video a descargar, por lo cual
                            el programa le otorga un link directo a la miniatura del video.

    -t or times             Son las descargas simultaneas que desee colocar, el maximo son 5 descargas a la misma vez.
                            !Solo valido al usar archivso de texto o descargar listas de reproduccion!

    -only_audio             Especifia que solo desea descargar el audio de los videos en la lista de reproduccion.
                            !Solo util en descargas de listas de reproduccion!
     
    Creado y Programado por: @Norahc_XI""")
    exit()

try:
    for Intento in range(1, 4):
        try: 
            if Intento!=1: print(f"[Error]: Intento-{Intento}")
            if sys.argv[1]=="-video" or sys.argv[1]=="-v":
                "Revisa si el usuario desea descargar un video con la etiqueta '-video'."
                from Assets.Video import VideoOpciones
                VideoOpciones(Rango); break          
            elif sys.argv[1]=="-audio" or sys.argv[1]=="-a":
                "Revisa si el usuario desea descargar un audio con la etiqueta '-audio'."
                from Assets.Audio import AudioOpciones
                AudioOpciones(Rango); break          
            elif sys.argv[1]=="-playlist" or sys.argv[1]=="-p":
                "Revisa si el usuario desea descargar una lista de reproduccion con la etiqueta '-playlist'."
                from Assets.ListaDeReproducion import ListaOpciones
                ListaOpciones(Rango); break        
            else: print("[*] Argumentos no validos!!")
            if Intento!=3: os.system("cls")
        except URLError: print("[*] Error de Conexion a Internet!!!")
except KeyboardInterrupt: 
    print("\n[*] Accion Cancelada Por El Usuario!!!")
    if os.path.isdir("temp"): rmtree("temp")
if os.path.isdir("Assets/__pycache__"): rmtree("Assets/__pycache__")