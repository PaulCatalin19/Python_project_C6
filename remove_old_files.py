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
import stat
import time

try:
    # check path
    assert len(sys.argv) >= 2, "Provide file path!"
    origin_path = sys.argv[1]
    assert os.path.isdir(origin_path), "Path is not a valid dir!"
    assert len(os.listdir(origin_path)) != 0, "Dir is empty!"
    
    # walk dir
    for root, dirs, files in os.walk(origin_path):
        for file in files:
            file_path = root + '\\'+ file
            print(file_path)
            file_stats = os.stat(file_path)
            last_access_time = time.ctime(file_stats[stat.ST_ATIME])
            creation_time = time.ctime(file_stats[stat.ST_CTIME])
            print(f"\t[LAST_ACCESS_TIME]:\t{last_access_time}")
            print(f"\t[CREATION_TIME]:\t{creation_time}\n")
    
except Exception as e:
    print(e)