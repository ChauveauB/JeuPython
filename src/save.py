#Récupération de la potentielle sauvegarde
class Save():
    
    def __init__(self):
        try:
            self.fic = open('../saves/save_Pythonjeu.txt', "r")
            self.fic.readline() #La ligne indiquant "___SAUVEGARDE DU PROJET PYTHON___"
            self.x_perso, self.y_perso, self.speed_perso, self.health_perso, self.world_perso = tuple(self.fic.readlines())
            self.x_perso = float(self.x_perso.replace("\n", ""))
            self.y_perso = float(self.y_perso.replace("\n", ""))
            self.speed_perso = int(self.speed_perso.replace("\n", ""))
            self.health_perso = int(self.health_perso.replace("\n", ""))
            self.world_perso = str(self.world_perso.replace("\n", ""))

            self.fic.close
        except:
            self.Saved = False
            logs = open("../saves/logs.txt", "a")
            logs.write("Fichier de sauvegarde inexistant ou invalide\n")
            logs.close
        else:
            self.Saved = True
            logs = open("../saves/logs.txt", "a")
            logs.write(f"Sauvegarde récuperee avec succes ! Pour x : {self.x_perso}; y : {self.y_perso}; speed : {self.speed_perso}; health : {self.health_perso} et enfin dans le monde : {self.world_perso}\n")
            logs.close