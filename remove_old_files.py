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


WEEK_SCORE = 604800 # 1 week in seconds
_weeks = 1

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


def try_to_remove_file(scores, index):
    try:
        # add extra prefilters (exists index and file can be removed)
        assert index<len(scores), f"[ERROR] Index {index} does NOT exist!"
        file_path = scores[index][0]
        os.remove(file_path)
    except Exception as e:
        print(e)
        return False
    else:
        print(f"File with index {index} was removed!")
        return True

try:
    print("\n[START]")
    # check path
    assert len(sys.argv) >= 2, "[ERROR] Provide file path!"
    origin_path = sys.argv[1]
    assert os.path.isdir(origin_path), "[ERROR] Path is not a valid dir!"
    assert len(os.listdir(origin_path)) != 0, "Dir is empty!"
    # _min_score will be multiplied by num param (if necessary)
    if len(sys.argv) == 3 and is_number(sys.argv[2]):
        _weeks = int(sys.argv[2])
    
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

    scores = [elems for elems in scores if elems[3] > _weeks*WEEK_SCORE]
    scores = sorted(scores, key=lambda elements: elements[3], reverse=True)
    index = 0
    if not len(scores):
        print(f" There are no files that have not been accessed in the last {_weeks} weeks")
    else:
        print(f"\n[FILES NOT ACCESSED {_weeks} WEEK(S)]")
        for file, size, last_access_time, score in scores:
            print(f"{index}) {file}")
            print(f"   SIZE: {size} KB, LAST_ACCESS_TIME: {last_access_time}\n")
            index +=1

        # Ask user wich file to delete
        file_to_del = input("Enter list of indexes coresponding to files that should be deleted (use just comma as separator):").split(', ')
        indexes = [int(index) for index in file_to_del if is_number(index)]
        if not len(indexes):
            print("Nothing to delete")
        else:
            # start removing process
            inedx_errors = []
            for index in indexes:
                if not try_to_remove_file(scores, index):
                    inedx_errors.append(index)

            assert len(inedx_errors)==0, f"[ERROR] Files with indexes: {inedx_errors} could not be deleted!"
except Exception as e:
    print(e)
else:
    print("[FINISHED SUCCESSFULLY]")