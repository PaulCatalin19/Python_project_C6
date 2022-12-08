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
import argparse 

# DE MODIFICAT
# (DONE) meniu help
# (DONE) stergere fisiere si dupa vechime in zile nu doar saptamani
# (DONE) parmas --week --days --help
# (DONE) sters toate fisierele cu * in loc de lista de index 0, 1, 2, ...

WEEK_SCORE = 604800 # 1 week in seconds
_weeks = 1
DAY_SCORE = 86400 # 1 day in seconds
_days = 1


def validate_args():
    global _days
    global _weeks
    if not args['path']:
        print("[ERROR] Provide dir path!")
        parser.print_help()

    origin_path = args['path']
    assert os.path.isdir(origin_path), "[ERROR] Path is not a valid dir!"
    assert len(os.listdir(origin_path)) != 0, "Dir is empty!"

    if args['weeks'] and args['days']:
        print("[ERROR] -w(--week) and -d(--days) can not be used at the same time")
        parser.print_help()
        exit()
    elif not args['weeks'] and not args['days']:
        print("[ERROR] Provide number of days/weeks!")
        parser.print_help()
        exit()
    elif args['days']:
        if args["days"] > 0:
            _days = args["days"]
        else:
            print("[ERROR] Provide positive number of days!")
            exit()
    elif args['weeks']:
        if args["weeks"] > 0:
            _weeks = args["weeks"]
        else:
            print("[ERROR] Provide positive number of weeks!")
            exit()


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
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', 
                        help="The path of the folder where the files will be searched.")
    parser.add_argument('-d', '--days', type=int,
                        help="Find files that have not been accessed in the last x days.")
    parser.add_argument('-w', '--weeks', type=int,
                        help="Find files that have not been accessed in the last x weeks.")

    args = vars(parser.parse_args())
    validate_args()
    print("\n[START]")

    # walk dir
    scores = []
    count = 0
    origin_path = args['path']
    for root, dirs, files in os.walk(origin_path):
        for file in files:
            file_path = root + '\\'+ file
            count +=1
            # print(file_path)
            res = compute_file_score(file_path)
            scores += [(file_path, res[0], res[1], res[2])]

    # filter scores by number of days/weeks
    if args['weeks']:
        scores = [elems for elems in scores if elems[3] > _weeks*WEEK_SCORE]
    else:
        scores = [elems for elems in scores if elems[3] > _days*DAY_SCORE]
    scores = sorted(scores, key=lambda elements: elements[3], reverse=True)
    index = 0
    if not len(scores):
        print(f" There are no files that have not been accessed for selected period")
    else:
        print(f"\n[FILES NOT ACCESSED IN SELECTED PERIOD]")
        for file, size, last_access_time, score in scores:
            print(f"{index}) {file}")
            print(f"   SIZE: {size} KB, LAST_ACCESS_TIME: {last_access_time}\n")
            index +=1

        # Ask user wich file to delete
        file_to_del = input("List of indexes coresponding to files (comma as separator) or '*' to DELETE EVERYTHING:")
        if file_to_del.strip() == "*":
            indexes = range(len(scores))
        else:
            file_to_del = file_to_del.split(', ')
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