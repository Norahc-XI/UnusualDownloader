!En este archivo podras ver las distintas funciones y opcines que te permite realizar el script!

## ---Indice---
1---Opciones\
   1.1---Notas\
   1.2---Opciones de Descargas\
2---Uso\
3---Ejemplos\
4---Excepciones

# 1-Opciones   
-help: Este parametro te permite ver las opciones de forma resumida, si no colocas ningun parametro tambien aparecen.

-video: Este parametro especifica que el usuario desea descargar uno o más video. este parametro se puede combinar con otro parametro como: "-resolution" y "-image", tambien permite especificar un archivo .txt para descarga multiples, y un path de salida (Dirrecion donde se desea guardar los videos).

-audio: Este parametro especifica que el usuario solo desea descargar el audio del video o videos especificado, este parametro permite combinar con: "-resolution" y "-image", como tambien un archivo .txt y un path de salida (Dirrecion donde se desea guardar los videos).

-playlist: Este parametro especifica que el usuario desea descargar los videos de una lista de reproduccion, se puede combinar con el parametro "-resolution, -image" y "-only_audio" !Importante! se debe especificar una resolucion para hacertar el parametro, la resolucion se establece una vez, y se descargan los videos en esa resolucion, en caso de no estar disponible el video en la resolucion deseada el programa lo descargara en la que más se aproxime a la especificada, la opcion "-only_audio" solo esta disponible al descargar listas de reproduciones, y no requiere especificar una resolucion.

## 1.1-Notas:
[1] Solo es posible descargar videos, audios y listas de reproduciones publicas o ocultas, si al intentar descargar el programa le indica "[*] Url No Valida!!!" verifique que el video o lista que desea descargar no esten privados.

[2] La velocidad de descarga y la velocidad en la que el programa tarde en analizar las Urls va a depender de su conexion a internet.

[3] Las resoluciones disponibles en las que se puede descargar cualquier video siempre y cuando el video llegue a esa resolucion.\
144p, 240p, 360p, 480p, 720p, 1080p, 1440p (2K), 2160p (4K), 4320p (8K)\
!Tomar en cuenta la nota numero 2!

## 1.2-Opciones de Descargas:
-resolution: Especifica la resolucion en la que desea descargar sus videos, esta opcion funciona tanto en videos, como en lista de reproduccion, al usarse con la opcion "-video" si no se especifica el programa detectara automaticamente las resoluciones disponibles y las mostrara para que el usuario escoja, en la opcion lista de reproduccion esto no funciona de las misma manera, al no especificar una resolucion el programa mostrara un Error.

-image: Al colocar este parametro el programa otorga un link directo a la imagen de la miniatura del video, si la desea visualizar.

-only_audio: (!Esta opcion es solo valida en "-playlist", si desea descargar audio de un video individual use "-audio"!), Si desea descargar solo el audio de los videos en la lista de reproduccion use esta opcion asi el programa descargara solo el audio en formato .mp3

# 2-Uso:
Aqui aprendera como usar las funciones ya vistas.\
"MyVideoDownloader.py ([-video] [-audio] [-playlist]) -resolution -image {-only_audio} [url or File.txt] Path_Salida"\
Ese es el orden en que se debe usar cada parametro en los ejemplos vera cada opcion valida.

# 3-Ejemplo:
[1] MyVideoDownloader.py -video https://Url.com\
[2] MyVideoDownloader.py -video https://Url.com C:\Username\Descargas  
[3] MyVideoDownloader.py -video -image https://Url.com\
[4] MyVideoDownloader.py -video -image https://Url.com C:\Username\Descargas\
[5] MyVideoDownloader.py -video -resolution https://Url.com\
[6] MyVideoDownloader.py -video -resolution https://Url.com C:\Username\Descargas\
[7] MyVideoDownloader.py -video -resolution 720p https://Url.com\
[8] MyVideoDownloader.py -video -resolution 720p https://Url.com C:\Username\Descargas\
[9] MyVideoDownloader.py -video -resolution 720p -image https://Url.com\
[10] MyVideoDownloader.py -video -resolution 720p -image https://Url.com C:\Username\Descargas\
[11] MyVideoDownloader.py -video Archivo.txt\
[12] MyVideoDownloader.py -video Archivo.txt C:\Username\Descargas\
[12] MyVideoDownloader.py -video -image Archivo.txt\
[13] MyVideoDownloader.py -video -image Archivo.txt C:\Username\Descargas\
[14] MyVideoDownloader.py -video -resolution 720p Archivo.txt\
[15] MyVideoDownloader.py -video -resolution 720p Archivo.txt C:\Username\Descargas\
[16] MyVideoDownloader.py -video -resolution 720p -image Archivo.txt\
[17] MyVideoDownloader.py -video -resolution 720p -image Archivo.txt C:\Username\Descargas

[18] MyVideoDownloader.py -audio https://Url.com\
[19] MyVideoDownloader.py -audio https://Url.com C:\Username\Descargas\
[20] MyVideoDownloader.py -audio -image https://Url.com\
[21] MyVideoDownloader.py -audio -image https://Url.com C:\Username\Descargas\
[22] MyVideoDownloader.py -audio Archivo.txt\
[23] MyVideoDownloader.py -audio Archivo.txt C:\Username\Descargas\
[24] MyVideoDownloader.py -audio -image Archivo.txt\
[25] MyVideoDownloader.py -audio -image Archivo.txt C:\Username\Descargas

[26] MyVideoDownloader.py -playlist https://Url.com\
[27] MyVideoDownloader.py -playlist https://Url.com C:\Username\Descargas\
[28] MyVideoDownloader.py -playlist -image https://Url.com\
[29] MyVideoDownloader.py -playlist -image https://Url.com C:\Username\Descargas\
[30] MyVideoDownloader.py -playlist -resolution 720p https://Url.com\
[31] MyVideoDownloader.py -playlist -resolution 720p https://Url.com C:\Username\Descargas\
[32] MyVideoDownloader.py -playlist -resolution 720p -image https://Url.com\
[33] MyVideoDownloader.py -playlist -resolution 720p -image https://Url.com C:\Username\Descargas\
[34] MyVideoDownloader.py -playlist -only_audio https://Url.com\
[35] MyVideoDownloader.py -playlist -only_audio https://Url.com C:\Username\Descargas\
[36] MyVideoDownloader.py -playlist -image -only_audio https://Url.com\
[37] MyVideoDownloader.py -playlist -image -only_audio https://Url.com C:\Username\Descargas\

# 4-Excepciones:
[!]: Esta señal le indicara informacion sobre el video o las lista que desea descargar, le indicara cosas como: El nombre del video o lista de reproduccion, el link para visualizar la miniatura, la duracion del video y la cantidad de videos que contiene una lista de reproduccion.\
Ejemplos:\
---[!] Titulo:\
---[!] Miniatura:\
---[!] Duracion:\
---[!] Peso de Archivo:\
---[|] Descargando ;)...\
---[+] Descargado :D.

[*]: Esta señal le indicara que hubo un error al ejecutar el programa, si es un error controlado el programa le especificara la causa, si no es asi te invito amablemente a notificarmelo, en README.md esta mi forma de contacto.
Ejemplos:\
---[\*] Url No Valida!!!:\
---[\*] Argumentos no validos!!!\
---[\*] Accion Cancelada Por El Usuario!!!\
---[\*] Error de Conexion a Internet!!\
---[\*] Url No Valida!!!\
---[\*] Demasiados Valores!!!\
---[\*] Archivo No Valido!!!\
---[\*] Archivo Vacio\
---[\*] Argumento invalido!!\
---[\*] El Video que Desea Descargar No Esta Disponible En La Resolucion Selecionada!!!\
---[\*] No se ha podido descargar el video, pero los archivos sin juntar se guardaran en el directorio de ejecucion, por si desea manualmente componerlos, el error se debe al titulo del video.
