"""
Creati un script care primeste de la linia de comanda un path catre un director
Acesta se va uita in director la fisiere (recursiv in tot folderul) si va lua 
cateva fisiere care au fost accesate cu cel mai mult timp in urma. 
Apoi le va indica utilizatorului, ii va spune cand au fost accesate si cat 
spatiu ocupa (intr-un format intuitiiv: de ex. 3.1KB, 1.5MB, 2.1GB) si il va 
intreba pe care doreste sa le stearga. In functie de raspuns, acesta face 
actiunea respectiva
"""
import sys
import os


try:
    # check path
    assert len(sys.argv) >= 2, "Provide file path!"
    path = sys.argv[1]
    assert os.path.isdir(path), "Path is not a valid dir!"
    assert len(os.listdir(path)) != 0, "Dir is empty!"
    
except Exception as e:
    print(e)