import sys
from urllib.error import URLError
from os import system

ResolucionesPermitidas=['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p']
Rango=len(sys.argv)

Intento=1

try:
    for i in range(3):
        if Intento!=1: print("[Error]: Intento-"+str(Intento))
        if Rango==1 or sys.argv[1]=="-help":
            """Doc: Si no se especifica ningun valor, el programa enseñara la ayuda o si es introducido el comando '-help'."""
            print("""\nUnusualDownloader.py ([-video] [-audio] [-playlist]) (-r or -resolution) (-i or -image) (-t or -times)
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

        elif sys.argv[1]=="-video":
            "Doc: revisar si el usuario desea descargar un video con la etiqueta '-video'."
            from Assets.Video import VideoOpciones
            try: VideoOpciones(Rango, ResolucionesPermitidas)
            except URLError: print("[*] Error de Conexion a Internet!!!")            
        elif sys.argv[1]=="-audio":
            "Doc: revisar si el usuario desea descargar un audio con la etiqueta '-audio'."
            from Assets.Audio import AudioOpciones
            try: AudioOpciones()
            except URLError: print("[*] Error de Conexion a Internet!!!")            
        elif sys.argv[1]=="-playlist":
            "Doc: revisar si el usuario desea descargar una lista de reproduccion con la etiqueta '-playlist'."
            from Assets.ListaDeReproducion import ListaOpciones
            try: ListaOpciones(ResolucionesPermitidas)
            except URLError: print("[*] Error de Conexion a Internet!!!")            
        else: print("[*] Argumentos no validos!!")
        Intento+=1
        if Intento==3: pass
        else: system("cls")
except KeyboardInterrupt: print("\n[*] Accion Cancelada Por El Usuario!!!")