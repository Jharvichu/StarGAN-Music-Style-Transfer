import gdown
import tarfile
import os
import sys
import warnings

warnings.filterwarnings("ignore")

# Colores
verdeColor = "\033[1;32m"
finColor = "\033[0m"
rojoColor = "\033[1;31m"
amarilloColor = "\033[1;33m"
moradoColor = "\033[1;35m"
turquesaColor = "\033[1;36m"

# Archivo en Google Drive
FILE_ID = '1n9utlZKgG68RI0nG8jfnmOpdUptbYgQV'
URL = f'https://drive.google.com/uc?id={FILE_ID}'
ARCHIVO_DESTINO = 'lpd_5_cleansed.tar.gz'

def main():
    print(f"{turquesaColor}[+] Descargando dataset desde Google Drive...{finColor}")
    try:
        # Descargar el archivo
        gdown.download(URL, ARCHIVO_DESTINO, quiet=False)
        print(f"\t{verdeColor}[+] Descarga completada con éxito.{finColor}")
        print(f"\n{turquesaColor}[+] Descomprimiendo archivos...{finColor}")
        # Descomprimir el archivo .tar.gz
        with tarfile.open(ARCHIVO_DESTINO, 'r:gz') as tar:
            tar.extractall()
        print(f"\t{verdeColor}[+] Descompresión exitosa. Dataset: lpd_5{finColor}")
        # Borrar el archivo comprimido para ahorrar espacio
        os.remove(ARCHIVO_DESTINO) 
        print(f"\t{amarilloColor}[!] Archivo temporal .tar.gz eliminado.{finColor}\n")
    except KeyboardInterrupt:
        print(f"\n\n{amarilloColor}[!] Saliendo...{finColor}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{rojoColor}[-] Error: {e}{finColor}\n")

if __name__ == '__main__':
    main()