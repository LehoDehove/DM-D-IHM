Le code n'est pas optimisé du tout mais il reste lisible justement

Vous avez accès à mes differentes versions d'avancement sur le projet pour constater la construction

Avec Camille CASTET nous avons exactement les mêmes idées de bonus, donc tant pis 

Il y a un easter egg un peu (beaucoup) degeu (dans le code "avec le caca")
Fripouille est un boss 
Mais je bloque sur l'appelation des données, et je commence à fatiguer de ce code donc je vais aller au plus simple.

Il y a un bouton d'aide, c'est pas grand chose mais c'est sympa pour les cas où on bloque
Y a un timer pour connaitre son temps à la fin. J'ai du mal avec la biblio time pour record le best time donc je fais juste le chrono pour la session actuelle.
Y a aussi du son quand on attrape un chat, ça rajoute de la vie.

Finallement je vais quand même faire un bonus complexe :
J'ai integré un docteur maboule aléatoire pour deverouiller mes lieux et ajouter de la difficulté et du contenu au jeu. Le code est INFAME 
Bon au final j'ai pas réussi à implementer mon maze dans le code qui marche donc à la poubelle.

J'ai mis un delai de 4,5s pour le locker pour que ce sois faisable par n'importe qui à la souris. De base j'avais mis 2sec pour un peu de challenge.
J'hésite presque à mettre 6sec puisque pour ceux au pavé tactile c'est trop dur.

Est ce que je peux garder l'idée de debloquer les lieux ? 
Je test juste les cadenas du coup
C'est ok j'ai un jeu de reflex plutot simple, et j'ai réussi à l'implementer.

En le faisant tester sur les pc des copains, je me suis rendu compte que j'avais un grand écran.
Je suis dégouté d'avoir fait le code pour du 1920x1080 17", maintenant faut appliquer un ratio dans tout le code et les bots ne le font pas bien :(.
J'ai réussi sur un bout de code, mais il faut l'appliquer sur tout le reste, et je fais des fautes d'innatentions donc j'abandonne l'adaptation auto.
Il faudra utiliser du 1920x1080 17" pour profiter entierement du jeu.
J'ai essayer de creer une biblio customisée pour alterer un petit peu les fonction QPixmap QImage QFont mais j'ai un soucis de prise en compte des fonctions.

Tous mes brouillons se trouvent dans le dossier 'versions' 