#Récupération de la potentielle sauvegarde
class Save:
    dict_values = {"x_perso":float, "y_perso":float, "speed_perso":float, "health_perso":float, "world_perso":str}
    long_dict = len(dict_values.keys())
    Saved = None

    @staticmethod
    def write_logs(text : str):
        with open('../saves/logs.txt', "a", -1, "utf-8") as logs:
            logs.write(text + "\n")
    
    @classmethod
    def get_save(cls):
        try:
            with open("../saves/save_Python.txt", "r") as fic:
                assert fic.readline() == "___SAUVEGARDE DU PROJET PYTHON___\n"
                for line in fic.readlines():
                    if line=="" or line=="\n": continue
                    key_line = line[:line.index(":")]
                    Save.dict_values[key_line] = line[line.index(":")+1:].replace("\n", "")
                    try: Save.dict_values[key_line] = float(Save.dict_values[key_line])
                    except ValueError: pass
                assert Save.long_dict == len(Save.dict_values)

        except FileNotFoundError:
            Save.Saved = False
            Save.write_logs("Fichier de sauvegarde introuvable")
        except AssertionError:
            Save.Saved = False
            Save.write_logs("Fichier de sauvegarde falacieux")
        except ValueError or IndexError:
            Save.Saved = False
            Save.write_logs("Données du fichier de sauvegarde mal ou non sauvegardées")
        except SyntaxError:
            #éviter que le try except attrape une erreur causé par une erreut dirrectement au niveau du code et qu'elle puisse être réglé au plus vite
            Save.write_logs("Erreur au niveau du programme -> arrêt du code")
            raise SyntaxError
        except:
            Save.Saved = False
            Save.write_logs("Sauvegarde non effectuée dû à une erreur non identifiée")
        else:
            Save.Saved = True
            Save.write_logs(f"Sauvegarde récuperée avec succès ! Stockage de : {Save.dict_values}")