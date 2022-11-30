"""
C6
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

_min_score = 604_800 # 1 week in seconds

def compute_file_score(file_path):
    '''score = today - last_access'''
    file_stats = os.stat(file_path)
    return (round(file_stats[stat.ST_SIZE]/1024, 2),          # size in KB
            time.ctime(file_stats[stat.ST_ATIME]), 
            time.time()-file_stats[stat.ST_ATIME])

def is_number(num_param):
    try:
        int(num_param)
        return True
    except ValueError:
        return False

try:
    # check path
    assert len(sys.argv) >= 2, "Provide file path!"
    origin_path = sys.argv[1]
    assert os.path.isdir(origin_path), "Path is not a valid dir!"
    assert len(os.listdir(origin_path)) != 0, "Dir is empty!"
    # _min_score will be multiplied by num param (if necessary)
    if len(sys.argv) == 3 and is_number(sys.argv[2]):
        _min_score = _min_score*int(sys.argv[2])
    
    # walk dir
    scores = []
    count = 0
    for root, dirs, files in os.walk(origin_path):
        for file in files:
            file_path = root + '\\'+ file
            count +=1
            # print(file_path)
            res = compute_file_score(file_path)
            scores += [(file_path, res[0], res[1], res[2])]

    scores = [elems for elems in scores if elems[3] > _min_score]
    scores = sorted(scores, key=lambda elements: elements[3])
    for file, size, last_access_time, score in scores:
        print(f"{size} KB -> {file}")
        print(f"  LAST_ACCESS_TIME: {last_access_time}, SCORE: {score}\n")

    
except Exception as e:
    print(e)