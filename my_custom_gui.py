from PyQt5.QtGui import QImage as OriginalQImage, QPixmap as OriginalQPixmap, QFont as OriginalQFont
import os
import screeninfo

# Obtention du chemin absolu du répertoire actuel
current_directory = os.path.dirname(os.path.abspath(__file__))


    
def get_screen_resolution():
    screens = screeninfo.get_monitors()
    for screen in screens:
        return screen.width, screen.height

def get_scale_factor():
    # Résolution de référence (1920x1080)
    ref_width, ref_height = 1920, 1080
    # Récupération de la résolution actuelle de l'écran
    width, height = get_screen_resolution()
    # Calcul du facteur d'échelle
    scale_factor = min(width / ref_width, height / ref_height)
    return scale_factor

scale_factor = get_scale_factor()


class MyQImage(OriginalQImage):
    def scaled(self, aspectRatioMode):
        scale_factor = get_scale_factor()
        newWidth = int(self.width() * scale_factor)
        newHeight = int(self.height() * scale_factor)
        return super().scaled(newWidth, newHeight, aspectRatioMode)

class MyQPixmap(OriginalQPixmap):
    def setGeometry(self, x, y):
        scale_factor = get_scale_factor()
        newWidth = int(self.width() * scale_factor)
        newHeight = int(self.height() * scale_factor)
        super().setGeometry(x, y, newWidth, newHeight)

class MyQFont(OriginalQFont):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisez les paramètres de la police ici, par exemple :
        self.setFamily('Lucida Handwriting')
        self.setPointSize(24)

# Substitution des classes originales par vos classes personnalisées
QImage = MyQImage
QPixmap = MyQPixmap
QFont = MyQFont
