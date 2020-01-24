import sys#pour recuperer les arguments 
import requests#pour les telechargement 
import os#pour la creation de repertoir
import shutil#pour le traitement des fichier
from tqdm import tqdm# module de telechergement
from bs4 import BeautifulSoup as bs#POUR rechercher des elements specifique dans une page web.


def telechargement(url, repertoire):
    """
        Telecharge toutes les pages d'un chapitre donne par son url `url` et 
        stocke les pages dans le repertoire `repertoire`
    """
    ### Creation du repertoire sous la forme nomManga/numChapitre ###
    os.makedirs(repertoire) #permet de creer le repertoire chapitre dans le repertoir nommanga 
    ##############################
    j=1
    continu = True
    while continu:
        urlfinal= url + str(j)
        ### Extraction de l'url de l'image dans l'url donne en parametre ###
        reponse1=requests.get(urlfinal)
        if reponse1.ok:
            soup = bs(reponse1.content, "html.parser")
            for img in tqdm(soup.find_all("img"), "Extracting images"):
                img_url = img.attrs.get("src")

                if not img_url or "mangapanda.com/" not in img_url:
                    # Donc ce n'est pas la photo du manga
                    continue
            ###############################################

            reponse2 = requests.get(img_url, stream=True)
            reponse2.raw.decode_content = True 

            ### Nom du fichier ###
            ext= str(j) + ".jpg"
            filename = os.path.join(repertoire, ext )
            ######################
            with open(filename, "wb") as f:
                shutil.copyfileobj(reponse2.raw, f)
            j += 1
        else:
            continu = False
       

urldebase= "https://www.mangapanda.com/"
urls = list()
if len(sys.argv) < 3:
    sys.exit("Ce programme nécessite 2 arguments")
else:
    #recuperation du nom du manga 
    nomManga = sys.argv[1].lower()
    #On concatène le nom du manga à l'url du site
    urldebase= urldebase+ nomManga  # a partir dici urldebase= "https://www.mangapanda.com/nommanga/4/"
    if "," in sys.argv[2]:
        chapitres = sys.argv[2].split(',')#tranforme la chaine en list avec comme separateur le caractere donne en parametre.
        for chapitre in chapitres:#pour chaque chapitre contenue dans le tableau des chapitres on contruitt lurl permettant dacceder 
            #a la page du chapitre en ajoutant a lurl de base  puis on stocke ca dans kla listye des urls
            #On ajoute les différents chapitres donnés en paramètre
            urls.append(urldebase+ "/" + chapitre + "/")
    else:
        if "-" in sys.argv[2]:
            chapitres = sys.argv[2].split("-")
            #On ajoute les différents chapitres donnés en paramètre
            for chapitre in range(int( chapitres[0] ) , int( chapitres[1] ) + 1 ):           
                urls.append(urldebase+ "/" + str(chapitre) + "/")
        else:
            #Dans ce cas on a un seul chapitre donne en parametre
            urls.append( urldebase+ "/" + sys.argv[2] + "/")
    
testManga = requests.get(urldebase)#permet d'acceder à une page web
if testManga.ok: ### Le manga donne en parametre existe ###
    ##Telechargement des differents chapitres
    for url in urls:
            #pour obtenir le chemin d'un repertoire on enleve le debut jusqu'a ".com/"
            #ainsi le nom du repertoire sera le 2e element de la liste retournee par url.split('.com/')
        telechargement( url, url.split(".com/")[1] )

    print("Téléchargement reussi!")
else:
    sys.exit("Manga introuvable dans ce site!")


