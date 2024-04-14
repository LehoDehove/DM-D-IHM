import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QWidget,QVBoxLayout
from PyQt5.QtCore import Qt,QTimer,QUrl
from qtpy.QtMultimedia import QMediaPlayer, QMediaContent

import os # Pour aller chercher ou est le fichier lancé pusique sans cette methode ça marche pas et ça m'enerve
import sys # Pour ajouter au systeme de biblios

# Ajoutez le chemin du répertoire contenant my_custom_gui au chemin de recherche des modules
repertoire_script = os.path.dirname(os.path.abspath(__file__))
custom_gui_path = os.path.join(repertoire_script, "my_custom_gui.py")
sys.path.append(custom_gui_path)

# Importez les classes personnalisées depuis my_custom_gui la bilbio customisée
from my_custom_gui import QImage, QPixmap, QFont



# chemins des images utilisées stockées dans ce dico
chemins_image = {
   1: os.path.join(repertoire_script, 'images', 'lieu1.jpg'),
   2: os.path.join(repertoire_script, 'images', 'lieu2.jpg'),
   3: os.path.join(repertoire_script, 'images', 'lieu3.jpg'),
   "fille": os.path.join(repertoire_script, 'images', 'fille.png'),
   "quitter": os.path.join(repertoire_script, 'images', 'chat 2.png'),
   "nouvellepartie": os.path.join(repertoire_script, 'images', 'chat 1.png'),
   "assis": os.path.join(repertoire_script, 'images', 'chatassis.png'),
   "dodo": os.path.join(repertoire_script, 'images', 'chatdodo.png'),
   "hint": os.path.join(repertoire_script, 'images', 'hint.png'),
   "lock": os.path.join(repertoire_script, 'images', 'lock.png'),

}


#Menu 
class MenuPrincipal(QMainWindow):
   def __init__(self):
      super().__init__()
      self.temps_ecoule = 0  # Initialisation de la variable temps_ecoule
      # On fixe les parametres de la page
      self.setWindowTitle("Retrouve mes chats")
      self.setGeometry(50, 25, 1700, 1000)
      font = QFont('Lucida Handwriting', 24)
      #On skip le layout car on n'utilise que des images et des textes flottants

      # Image bouton nouvelle partie
      self.lbl_nouvelle_partie = QLabel(self)
      pixmap_nouvelle_partie = QPixmap(chemins_image["nouvellepartie"]).scaled(525,525)
      self.lbl_nouvelle_partie.setPixmap(pixmap_nouvelle_partie)
      self.lbl_nouvelle_partie.setGeometry(325, 600, pixmap_nouvelle_partie.height(), pixmap_nouvelle_partie.width())
      self.lbl_nouvelle_partie.setAlignment(Qt.AlignCenter)
      self.lbl_nouvelle_partie.mousePressEvent = self.nouveaujeu

      # Texte pour l'image bouton nouvelle partie
      self.lbl_texte_nouvelle_partie = QLabel("Nouvelle Partie", self)
      self.lbl_texte_nouvelle_partie.setGeometry(320, 725, 501, 261)
      self.lbl_texte_nouvelle_partie.setAlignment(Qt.AlignCenter)
      self.lbl_texte_nouvelle_partie.setFont(font)
      self.lbl_texte_nouvelle_partie.mousePressEvent = self.nouveaujeu

      # Image bouton quitter
      self.lbl_quitter = QLabel(self)
      pixmap_quitter = QPixmap(chemins_image["quitter"]).scaled(525,525)
      self.lbl_quitter.setPixmap(pixmap_quitter)
      self.lbl_quitter.setGeometry(925, 600, pixmap_quitter.height(), pixmap_quitter.width())
      self.lbl_quitter.setAlignment(Qt.AlignCenter)
      self.lbl_quitter.mousePressEvent =self.quitter

      # Texte pour l'image bouton quitter
      self.lbl_texte_quitter = QLabel("Quitter", self)
      self.lbl_texte_quitter.setGeometry(925, 675, 501, 261)
      self.lbl_texte_quitter.setAlignment(Qt.AlignCenter)
      self.lbl_texte_quitter.setFont(font)
      self.lbl_texte_quitter.mousePressEvent = self.quitter
      

      #On affiche le but de jeu
      self.lbl_rules = QLabel("Aide moi à retrouver mes chats.\nIl y a des chats qui dorment, et d'autres assis.\n Ne te trompe pas de chats, il y en a beaucoup dehors", self)
      self.lbl_rules.setGeometry(200,150,1000,450)
      self.lbl_rules.setFont(font)

      # Image triste
      self.lbl_fille = QLabel(self)
      pixmap_fille = QPixmap(chemins_image["fille"])
      self.lbl_fille.setPixmap(pixmap_fille)
      self.lbl_fille.setGeometry(1200, 50, pixmap_fille.height(), pixmap_fille.width())
      self.lbl_fille.setAlignment(Qt.AlignCenter)

      self.show()

      self.chrono = 0
      self.ndodo=[0,0,0,0]
      self.nassis=[0,0,0,0]

      # Image bouton aide
      self.lbl_chathint = QLabel(self)
      pixmap_chathint = QPixmap(chemins_image["hint"]).scaled(100,100)
      self.lbl_chathint.setPixmap(pixmap_chathint)
      self.lbl_chathint.setGeometry(0,0, pixmap_chathint.height(), pixmap_chathint.width())
      self.lbl_chathint.setAlignment(Qt.AlignCenter)
      self.lbl_chathint.mousePressEvent = self.afficher_aide

      # Texte pour l'image bouton aide
      self.lbl_hint = QLabel("Besoin d'une aide ?", self)
      self.lbl_hint.setGeometry(110, 20, 1000, 30)
      self.lbl_hint.setFont(font)
      self.lbl_hint.mousePressEvent = self.afficher_aide

      # Pour afficher le nombre de chats retrouvés
      self.lbl_chats_dodo = QLabel(f"Chats qui dorment retrouvés : {self.ndodo[0]} / {self.ndodo[1]+self.ndodo[2]+self.ndodo[3]}", self)
      self.lbl_chats_dodo.setGeometry(300, 650, 1000, 30)
      self.lbl_chats_dodo.setFont(font)

      # Image exemple dodo
      self.lbl_chatdodoex = QLabel(self)
      pixmap_chatdodoex = QPixmap(chemins_image["dodo"]).scaled(100,100)
      self.lbl_chatdodoex.setPixmap(pixmap_chatdodoex)
      self.lbl_chatdodoex.setGeometry(1000,600, pixmap_chatdodoex.height(), pixmap_chatdodoex.width())
      self.lbl_chatdodoex.setAlignment(Qt.AlignCenter)

      #pour afficher le nombre de chats retrouvés
      self.lbl_chats_assis = QLabel(f"Chats assis retrouvés : {self.nassis[0]} / {self.nassis[1]+self.nassis[2]+self.nassis[3]}", self)
      self.lbl_chats_assis.setGeometry(300, 750, 1000, 30)
      self.lbl_chats_assis.setFont(font)

      # Image exemple assis
      self.lbl_chatassisex = QLabel(self)
      pixmap_chatassisex = QPixmap(chemins_image["assis"]).scaled(100,100)
      self.lbl_chatassisex.setPixmap(pixmap_chatassisex)
      self.lbl_chatassisex.setGeometry(850,700, pixmap_chatassisex.height(), pixmap_chatassisex.width())
      self.lbl_chatassisex.setAlignment(Qt.AlignCenter)

      # Image bouton lieu1
      self.lbl_lieu1 = QLabel(self)
      pixmap_lieu1 = QPixmap(chemins_image[1]).scaled(400,350)
      self.lbl_lieu1.setPixmap(pixmap_lieu1)
      self.lbl_lieu1.setGeometry(250,50, pixmap_lieu1.height(), pixmap_lieu1.width())
      self.lbl_lieu1.setAlignment(Qt.AlignCenter)

      # Texte pour l'image bouton lieu1
      self.lbl_texte_lieu1 = QLabel("Lieu 1", self)
      self.lbl_texte_lieu1.setGeometry(350, 450, 200, 80)
      self.lbl_texte_lieu1.setAlignment(Qt.AlignCenter)
      self.lbl_texte_lieu1.setFont(font)

      #Image bouton lieu2
      self.lbl_lieu2 = QLabel(self)
      pixmap_lieu2 = QPixmap(chemins_image[2]).scaled(400,350)
      self.lbl_lieu2.setPixmap(pixmap_lieu2)
      self.lbl_lieu2.setGeometry(675,50, pixmap_lieu2.height(), pixmap_lieu2.width())
      self.lbl_lieu2.setAlignment(Qt.AlignCenter)

      # Texte pour l'image bouton lieu2
      self.lbl_texte_lieu2 = QLabel("Lieu 2", self)
      self.lbl_texte_lieu2.setGeometry(750, 450, 200, 80)
      self.lbl_texte_lieu2.setAlignment(Qt.AlignCenter)
      self.lbl_texte_lieu2.setFont(font)

      #Image bouton lieu3
      self.lbl_lieu3 = QLabel(self)
      pixmap_lieu3 = QPixmap(chemins_image[3]).scaled(400,350)
      self.lbl_lieu3.setPixmap(pixmap_lieu3)
      self.lbl_lieu3.setGeometry(1100,50, pixmap_lieu3.height(), pixmap_lieu3.width())
      self.lbl_lieu3.setAlignment(Qt.AlignCenter)

      # Texte pour l'image bouton lieu3
      self.lbl_texte_lieu3 = QLabel("Lieu 3", self)
      self.lbl_texte_lieu3.setGeometry(1175, 450, 200, 80)
      self.lbl_texte_lieu3.setAlignment(Qt.AlignCenter)
      self.lbl_texte_lieu3.setFont(font)

      # Image bouton quitter
      self.lbl_quitter2 = QLabel(self)
      pixmap_quitter2 = QPixmap(chemins_image["quitter"]).scaled(525,525)
      self.lbl_quitter2.setPixmap(pixmap_quitter2)
      self.lbl_quitter2.setGeometry(900, 600, pixmap_quitter2.height(), pixmap_quitter2.width())
      self.lbl_quitter2.setAlignment(Qt.AlignCenter)
      self.lbl_quitter2.mousePressEvent = lambda : self.quitter

      # Texte pour l'image bouton quitter
      self.lbl_texte_quitter2 = QLabel("Quitter", self)
      self.lbl_texte_quitter2.setGeometry(900, 675, 501, 261)
      self.lbl_texte_quitter2.setAlignment(Qt.AlignCenter)
      self.lbl_texte_quitter2.setFont(font)
      self.lbl_texte_quitter2.mousePressEvent = self.quitter

      # Affichage du chrono
      self.lbl_chronometre = QLabel(self)
      self.lbl_chronometre.setGeometry(10, 950, 150, 30)
      self.lbl_chronometre.setText("Temps écoulé : 00:00")

      #Image locker lieu1
      self.lock_lieu1 = QLabel(self)
      pixmap_lock_lieu1 = QPixmap(chemins_image["lock"]).scaled(400,350)
      self.lock_lieu1.setPixmap(pixmap_lock_lieu1)
      self.lock_lieu1.setGeometry(250,50, pixmap_lock_lieu1.height(), pixmap_lock_lieu1.width())
      self.lock_lieu1.setAlignment(Qt.AlignCenter)
      self.lock_lieu1.mousePressEvent = lambda event: self.ouvrir_locker(1) # les var event sont simplement définies comme paramètres et ignorées par la suite. C'est pourquoi on utilise lambda pour appeler ces méthodes sans rien fournir.

      #Image locker lieu2
      self.lock_lieu2 = QLabel(self)
      pixmap_lock_lieu2 = QPixmap(chemins_image["lock"]).scaled(400,350)
      self.lock_lieu2.setPixmap(pixmap_lock_lieu2)
      self.lock_lieu2.setGeometry(675,50, pixmap_lock_lieu2.height(), pixmap_lock_lieu2.width())
      self.lock_lieu2.setAlignment(Qt.AlignCenter)
      self.lock_lieu2.mousePressEvent = lambda event: self.ouvrir_locker(2) #same que line198

      #Image locker lieu3
      self.lock_lieu3 = QLabel(self)
      pixmap_lock_lieu3 = QPixmap(chemins_image["lock"]).scaled(400,350)
      self.lock_lieu3.setPixmap(pixmap_lock_lieu3)
      self.lock_lieu3.setGeometry(1100,50, pixmap_lock_lieu3.height(), pixmap_lock_lieu3.width())
      self.lock_lieu3.setAlignment(Qt.AlignCenter)
      self.lock_lieu3.mousePressEvent = lambda event: self.ouvrir_locker(3) #same que line198

   #Fonction pour fermer
   def quitter(self,event):
      self.close()

   #Fonction pour jouer au cadenas
   def ouvrir_locker(self,lieu):
      self.play_sound(os.path.join(repertoire_script, 'sons',f"mew{random.randint(1,4)}.mp3"))
      cadenas_fenetre = Cadenas(lieu, self)  # Passer les informations nécessaires
      cadenas_fenetre.show()
   
   #Focntion pour deverrouiller un lieu en fonction du lieu cliqué
   def unlock(self,lieu):
      if lieu ==1 : 
         self.lock_lieu1.hide() 
         self.lbl_lieu1.mousePressEvent = lambda event: self.ouvrir_jeu(1) #same que line198
         self.lbl_texte_lieu1.mousePressEvent = lambda event: self.ouvrir_jeu(1) #same que line198
      if lieu == 2 :
         self.lock_lieu2.hide() 
         self.lbl_lieu2.mousePressEvent =lambda event: self.ouvrir_jeu(2) #same que line198
         self.lbl_texte_lieu2.mousePressEvent = lambda event: self.ouvrir_jeu(2) #same que line198
      if lieu ==3 : 
         self.lock_lieu3.hide() 
         self.lbl_lieu3.mousePressEvent = lambda event: self.ouvrir_jeu(3) #same que line198
         self.lbl_texte_lieu3.mousePressEvent = lambda event: self.ouvrir_jeu(3) #same que line198

   #Focntion pour MaJ le chrono et bien l'afficher
   def actualiser_chronometre(self):
      self.temps_ecoule += 1
      minutes = self.temps_ecoule // 60
      secondes = self.temps_ecoule % 60
      temps_affichage = f"{minutes:02}:{secondes:02}"
      self.lbl_chronometre.setText(f"Temps écoulé : {temps_affichage}")
      
   #Focntion pour afficher de l'aide dans un pop up   
   def afficher_aide(self, event): #same que line198
      self.play_sound(os.path.join(repertoire_script, 'sons',f"mew{random.randint(1,4)}.mp3"))
      QMessageBox.information(self, "Aide", f"Il reste {len(self.positions_assis[1])+len(self.positions_dodo[1])} chats dans le lieu 1, {len(self.positions_assis[2])+len(self.positions_dodo[2])} chats dans le lieu 2, et {len(self.positions_assis[3])+len(self.positions_dodo[3])} chats dans le lieu 3.")


   # fonction pour ouvrir la fenetre de jeu    
   def nouveaujeu(self,event): #same que line198
      self.play_sound(os.path.join(repertoire_script, 'sons',f"mew{random.randint(1,4)}.mp3"))
      # générer les nombres et les positions des chats
      self.generer_chats(event) #same que line198
      # on cache tout ce qui est sur la fenetre
      for widget in menu_principal.findChildren(QWidget):
         widget.hide()

      # on montre ce qu'on souhaite
      self.lbl_chronometre.show()
      self.lbl_chathint.show()
      self.lbl_hint.show()
      self.lbl_chats_dodo.show()
      self.lbl_chatdodoex.show()
      self.lbl_chats_assis.show()
      self.lbl_chatassisex.show()
      self.lbl_lieu1.show()
      self.lbl_texte_lieu1.show()
      self.lbl_lieu2.show()
      self.lbl_texte_lieu2.show()
      self.lbl_lieu3.show()
      self.lbl_texte_lieu3.show()
      self.lbl_quitter2.show()
      self.lbl_texte_quitter2.show()
      self.lock_lieu1.show()
      self.lock_lieu2.show()
      self.lock_lieu3.show()

      # on commence le timer allant de sec en sec
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.actualiser_chronometre)
      self.timer.start(1000)

   # generation des chats et leurs pos
   def generer_chats(self,event): #same que line198

      # nombre de chats dodo total en 0 puis dans lieu 1 en 1, puis...
      self.ndodo = [0, random.randint(3, 6), random.randint(3, 6), random.randint(3, 6)]
      # nombre de chats assis total en 0 puis dans lieu 1 en 1, puis...
      self.nassis = [0, random.randint(3, 6), random.randint(3, 6), random.randint(3, 6)]
      # créer des listes pour stocker les informations sur les positions des chats dans chaque lieu
      self.positions_assis = {1: {}, 2: {}, 3: {}}
      self.positions_dodo = {1: {}, 2: {}, 3: {}}
      # self.positions du type de chats [lieu] [nombre de chat] [positions x,y]   

      for lieu in range(1, 4): # comme ca ca passe 3 fois, car 3 = nbr de lieux

         for i in range(1, self.ndodo[lieu] + 1):
            self.positions_dodo[lieu][i] = [random.randint(1, 1650), random.randint(1, 950)]

         for i in range(1, self.nassis[lieu] + 1):
            self.positions_assis[lieu][i] = [random.randint(1, 1650), random.randint(1, 950)]


      # on actualise le compteur sans ajouter au compteur
      self.actualiser_labels_chats(None)

   # actualiser le compteur en ajoutant 1 si lieu renseigné
   def actualiser_labels_chats(self,typedechattrouve):
      if typedechattrouve=="assis": self.nassis[0] +=1
      if typedechattrouve=="dodo": self.ndodo[0] +=1
      self.lbl_chats_dodo.setText(f"Chats qui dorment retrouvés : {self.ndodo[0]} / {self.ndodo[1]+self.ndodo[2]+self.ndodo[3]}")
      self.lbl_chats_assis.setText(f"Chats assis retrouvés : {self.nassis[0]} / {self.nassis[1]+self.nassis[2]+self.nassis[3]}")

   # fonction pour ouvrir les lieux
   def ouvrir_jeu(self, lieu):
      self.play_sound(os.path.join(repertoire_script, 'sons',f"mew{random.randint(1,4)}.mp3"))
      self.hide()  # Masquer la fenêtre du menu
      jeu_window = FenetreJeu(chemins_image[lieu], self.ndodo, self.nassis, self.positions_dodo, self.positions_assis, lieu, self)  # Passer les informations nécessaires
      jeu_window.show()  # Afficher la fenêtre du jeu
   
   #Fonction pour faire un retour au menu à partir de la fenetre jeu (on la set ici pour une connexion plus facile)
   def retour(self, ndodo, nassis, positions_dodo, positions_assis):
      self.hide()  # Cacher la fenêtre de jeu
      self.ndodo = ndodo
      self.nassis = nassis
      self.positions_dodo = positions_dodo
      self.positions_assis = positions_assis
      self.show()  # Afficher le menu principal avec le même état qu'auparavant

   # Fonction pour stopper le chrono à la fin
   def stop_chronometre(self):
      self.timer.stop()
      minutes, secondes = divmod(self.temps_ecoule, 60)
      temps_affichage = f"{minutes:02}:{secondes:02}"
      QMessageBox.information(self, "Temps écoulé", f"Votre temps est de {temps_affichage}.")

   # Fonction necessaire pour emetre un son
   def play_sound(self, soundfile):
      url = QUrl.fromLocalFile(soundfile)
      content = QMediaContent(url)
      player = QMediaPlayer(self)
      player.setMedia(content)
      player.play()



#Lockers
class Cadenas(QMainWindow):
   def __init__(self, lieu, parent=None):
      super().__init__(parent)
      self.lieu = lieu
      self.setWindowTitle("Cadenas")
      # On place la fenetre en fonction de quel cadenas on parle
      if lieu == 1: 
         self.setGeometry(275, 100, 400, 350)
      elif lieu == 2: 
         self.setGeometry(700, 100, 400, 350)
      elif lieu == 3: 
         self.setGeometry(1125, 100, 400, 350)
        
      # On pose un layout pour utiliser les widget pushbuttons contrairement à precedemment
      layout = QVBoxLayout()

      # Suite de la class simple et lisible

      self.consigne = QLabel("Pour débloquer ce lieu, il va falloir être rapide.\nClique sur tous ces boutons en moins de 4,5 secondes !")
      self.consigne.setAlignment(Qt.AlignCenter)
      layout.addWidget(self.consigne)

      self.tenter = QPushButton("Tenter sa chance")
      self.tenter.clicked.connect(self.start_game)
      layout.addWidget(self.tenter)

      central_widget = QWidget()
      central_widget.setLayout(layout)
      self.setCentralWidget(central_widget)

      self.timer = QTimer(self)
      self.timer.timeout.connect(self.game_over)
      self.points_clicked = 0

   def start_game(self):
      self.points_clicked = 0
      self.timer.start(4500)  #4,5 seconds pour que etout le monde puisse y arriver
      self.generate_point()
      self.consigne.hide()
      self.tenter.hide()

   def generate_point(self):
      for i in range(10):  # 10 points
         x = random.randint(50, 350)
         y = random.randint(50, 300)
         button = QPushButton(self) 
         button.setGeometry(x, y, 50, 50)
         button.clicked.connect(self.point_clicked)
         button.show()

   def point_clicked(self):
      self.points_clicked += 1
      self.sender().deleteLater()
      if self.points_clicked == 10:
         self.game_won()

   def game_won(self):
      self.timer.stop()
      self.unlock(self.lieu)
      self.hide()

   def game_over(self):
      self.timer.stop()
      self.hide()
      
   def unlock(self, lieu):
      self.hide()
      self.parent().unlock(lieu)

#Jeu :
class FenetreJeu(QMainWindow):
   def __init__(self, chemin_fond, ndodo, nassis, positions_dodo, positions_assis, lieu, parent):
      super().__init__(parent)
      # On importe nos valeurs de MenuPrincipal à la fenetre de jeu
      self.ndodo = ndodo
      self.nassis = nassis
      self.positions_dodo = positions_dodo
      self.positions_assis = positions_assis
      self.lieu = lieu

      # Paramètres de la fenêtre
      self.setWindowTitle("Jeu")
      self.setGeometry(50, 25, 1700, 1000)

      # Fond d'écran du lieu
      self.lbl_fond = QLabel(self)
      pixmap_fond = QPixmap(chemin_fond).scaled(1700, 1000)
      self.lbl_fond.setPixmap(pixmap_fond)
      self.lbl_fond.setGeometry(0, 0, 1700, 1000)
      self.lbl_fond.setAlignment(Qt.AlignCenter)

      self.generer_chats(self.lieu)  # On fait spawn nos chats en fonctions du lieu dans lequel on se trouve

      # Bouton de retour
      self.bouton_retour = QPushButton("Retour", self)
      self.bouton_retour.setGeometry(50, 50, 100, 30)
      self.bouton_retour.setStyleSheet("background-color: black; color: white; border-radius: 15px;")
      self.bouton_retour.clicked.connect(self.retour)

      self.show()
      
   # Focntion pour faire apparaitre les chats
   def generer_chats(self, lieu):
      #On attribue une identité avec les positions à chaque pixmap pour pouvoir les identifiés au clique et les enlevés facilement ensuite de la liste des positions
      for identite, position in self.positions_dodo.get(lieu, {}).items():
         label_dodo = QLabel(self)
         label_dodo.setObjectName(f"label_dodo_{identite}") # On nomme l'identité
         label_dodo.clicked = False #On definie le pixmap comme pas cliqué / trouvé
         taille = random.randint(50, 80) #LA taille des chats varients entre 50 et 80 pxls
         pixmap_dodo = QPixmap(chemins_image["dodo"]).scaled(taille, taille) #Suite est connue, c'est comme avant, on place l'image
         label_dodo.setPixmap(pixmap_dodo)
         label_dodo.setGeometry(position[0], position[1], pixmap_dodo.width(), pixmap_dodo.height())
         label_dodo.setAlignment(Qt.AlignCenter)
         label_dodo.mousePressEvent = lambda event, id=identite: self.clique_chat_dodo(id) #same que line198
         label_dodo.show()

      #On attribue une identité avec les positions à chaque pixmap pour pouvoir les identifiés au clique et les enlevés facilement ensuite de la liste des positions
      for identite, position in self.positions_assis.get(lieu, {}).items():
         label_assis = QLabel(self)
         label_assis.setObjectName(f"label_assis_{identite}") # On nomme l'identité
         label_assis.clicked = False #On definie le pixmap comme pas cliqué / trouvé
         taille = random.randint(50, 80) #LA taille des chats varients entre 50 et 80 pxls
         pixmap_assis = QPixmap(chemins_image["assis"]).scaled(taille, taille) #Suite est connue, c'est comme avant, on place l'image
         label_assis.setPixmap(pixmap_assis)
         label_assis.setGeometry(position[0], position[1], pixmap_assis.width(), pixmap_assis.height())
         label_assis.setAlignment(Qt.AlignCenter)
         label_assis.mousePressEvent = lambda event, id=identite: self.clique_chat_assis(id)#same que line198
         label_assis.show()

   #Si un chat dodo est cliqué
   def clique_chat_dodo(self, identite):
      #on fait un miaou aleatoire
      self.parent().play_sound(os.path.join(repertoire_script, 'sons',f"mew{random.randint(1,4)}.mp3"))
      #on identifie lequel est cliqué
      label = self.findChild(QLabel, f"label_dodo_{identite}")
      #si pas encore trouvé/cliqué alors on le set à trouvé/ciqué, puis on enleve sa position pour pas le reafficher plus tard et on le cache des maintenant, et on ajoute 1 au compteur de chats assis trouvés.
      if label is not None and not label.clicked:
         label.clicked = True
         label.hide()
         self.parent().actualiser_labels_chats("dodo")
         self.supprimer_position_chat("dodo", identite)
      # on verifie les Conditions de victoires 
      if len(self.positions_assis[1])==0 and len(self.positions_assis[2])==0 and len(self.positions_assis[3])==0 and len(self.positions_dodo[1])==0 and len(self.positions_dodo[2])==0 and len(self.positions_dodo[3])==0: self.fin()

   #Si un chat assis est cliqué
   def clique_chat_assis(self, identite):
      #on fait un miaou aleatoire
      self.parent().play_sound(os.path.join(repertoire_script, 'sons',f"mew{random.randint(1,4)}.mp3"))
      #on identifie lequel est cliqué
      label = self.findChild(QLabel, f"label_assis_{identite}")
      #si pas encore trouvé/cliqué alors on le set à trouvé/ciqué, puis on enleve sa position pour pas le reafficher plus tard et on le cache des maintenant, et on ajoute 1 au compteur de chats assis trouvés.
      if label is not None and not label.clicked:
         label.clicked = True
         label.hide()
         self.parent().actualiser_labels_chats("assis")
         self.supprimer_position_chat("assis", identite)
      # on verifie les Conditions de victoires 
      if len(self.positions_assis[1])==0 and len(self.positions_assis[2])==0 and len(self.positions_assis[3])==0 and len(self.positions_dodo[1])==0 and len(self.positions_dodo[2])==0 and len(self.positions_dodo[3])==0: self.fin()

   #On a une fonction pour supprimer le chat de la liste des positions en fonction de sont identité attribuee et du type de chat
   def supprimer_position_chat(self, type_chat, chat_id):

      #on cherche le chat en question
      if type_chat == "dodo":
         #et on le suppr
         del self.positions_dodo[self.lieu][chat_id]

      #on cherche le chat en question
      elif type_chat == "assis":
         #et on le suppr
         del self.positions_assis[self.lieu][chat_id]

   #fonction de retour au sein de la fenetre jeu
   def retour(self):
      self.hide()
      self.parent().retour(self.ndodo, self.nassis, self.positions_dodo, self.positions_assis)  # Appeler la méthode retour du MenuPrincipal

   #fonction pour la fin du jeu
   def fin(self):
      self.parent().stop_chronometre()
      self.retour()
      self.hide()
      QMessageBox.information(self, "Merci!", f"Vous m'avez entierement aidée !\n Merci beaucoup :D !")

      # Masquer les boutons et labels spécifiques au jeu
      for widget in menu_principal.findChildren(QWidget):
         widget.hide()

      # Afficher les boutons et labels du menu principal
      self.parent().show()
      self.parent().lbl_rules.show()
      self.parent().lbl_fille.show()
      self.parent().lbl_nouvelle_partie.show()
      self.parent().lbl_texte_nouvelle_partie.show()
      self.parent().lbl_quitter.show()
      self.parent().lbl_texte_quitter.show()
      self.parent().temps_ecoule = 0

if __name__ == '__main__':
   app = QApplication(sys.argv)
   menu_principal = MenuPrincipal()
   sys.exit(app.exec_())
