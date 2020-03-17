import requests
import json


def sorter():
    global L
    L = sorted(L, key=lambda i: (i['artist'].strip("The "), i['title'], i['format']))


def load(x):
    global L
    with open("./" + x, "r") as file:
        data = json.load(file)
        print("Loaded " + str(len(data)) + " entries from JSON")
        L += data


def save(x):
    global L
    sorter()
    with open('./' + x, 'w') as file:
        json.dump(L, file)
        print("Saved " + str(len(L)) + " entries in JSON")


def remDuplicate():
    ids = []
    toRem = []
    for n, i in enumerate(L):
        if i['id'] not in ids:
            ids.append(i['id'])
        else:
            toRem.append(n)

    try:
        toRem.reverse()
        for i in toRem:
            t = L.pop(i)
            print("Removed as duplicate: " + t['id'] + " -- " + t['title'])
        print("Removed " + str(len(toRem)) + " duplicates")
    except Exception as e: print (e)


def printer():
    for n, i in enumerate(L):
        print(str(n+1) + ") " + i['artist'] + " - " + i['title'] + " (" + str(i['year']) + "/ " + i['format'] + ") in "
              + i['owner'] + "'s lib")


L = []
while True:
    A = {"title": None, "artist": None, "year": None, "genre": None, "format": None, "owner": None, "id": None}

    try:
        cmd = input("Next: ")
        while len(cmd) == 0: cmd = input("Next: ")

        if cmd[0] == "/":
            cmd = cmd[1:]

            if cmd == "exit":
                break

            elif cmd == "id":
                cmd = int(input("Index: "))
                print(L[cmd-1]['id'])

            elif cmd == "save":
                save(input("Filename: "))

            elif cmd == "load":
                load(input("Filename: "))
                remDuplicate()
                sorter()

            elif cmd == "del":
                cmd = input("Index: ")
                if cmd == "": L.pop()
                else:
                    try: L.pop(int(cmd)-1)
                    except Exception as e: print(e)
                sorter()

            elif cmd == "sort":
                sorter()

            elif cmd == "clean":
                remDuplicate()
                sorter()

            elif cmd == "list":
                printer()

            else:
                print("Invalid command")

        else:
            if ''.join(cmd.split()).isalnum() and not cmd.isupper(): cmd = " ".join([i.capitalize() for i in cmd.split()])
            A['title'] = cmd

            cmd = input("Artist: ")
            if ''.join(cmd.split()).isalnum() and not cmd.isupper(): cmd = " ".join([i.capitalize() for i in cmd.split()])
            A['artist'] = cmd

            cmd = input("Year: ") + " "
            A['year'] = cmd

            cmd = input("Genre: ") + " "
            if ''.join(cmd.split()).isalnum() and not cmd.isupper(): cmd = " ".join(
                [i.capitalize() for i in cmd.split()])
            A['genre'] = cmd

            cmd = input("Format: ")
            cmd = cmd.lower()
            if cmd == "": cmd = " "
            elif cmd in ["c", "cd"]: cmd = "CD"
            elif cmd in ['t', 'tape', 'cassette']: cmd = "Tape"
            elif cmd in ['lp', 'v', 'vinyl']: cmd = "Vinyl"
            A['format'] = cmd

            cmd = input("Owner: ")
            cmd = cmd.lower()
            if cmd == "":
                cmd = ' '
            elif cmd in ["f", "frank"]:
                cmd = "Frank"
            elif cmd in ['z', 'zoe']:
                cmd = "Zoe"
            elif cmd in ['e', 'eric']:
                cmd = "Eric"
            A['owner'] = cmd

            r = requests.get("https://www.uuidgenerator.net/api/guid")
            while r.status_code != 200: r = requests.get("https://www.uuidgenerator.net/api/guid")
            A['id'] = r.text.strip("\r\n")

            L.append(A)
    except Exception as e:
        print(e)

    print()

print("Goodbye <3")
input()