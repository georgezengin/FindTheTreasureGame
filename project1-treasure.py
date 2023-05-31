# כתוב תוכנית פייטון למשחק מציאת המטמון .שלב ראשון - יצר קובץ חדש (או מחק את הקובץ בעת איתחולו)
# ובתוכו רצף הספרות מ - 0 ועד 9 .כל ספרה תופיע מספר אקראי של פעמים [20-1 [פעמים. אחרי ספרת ה - 9
# האחרונה כתוב את המילה . TREASUREלאחר מכן , שוב כתוב את הספרות בסדר יורד כלומר, מ9- ועד 0 .כל
# ספרה תופיע מספר אקראי של פעמים [20-1 [פעמים .לדוגמא
# - 0000000000000111111111111222222222222223333333333333333444444444
# 5555555555555555555555555555555555555555556666666666666666666777
# 8888888888888999999999999999999999999999999 TREASURE 999999999999
# 9999999999999999999999998888888888888888888888887777777777777777
# 6666666666666666666666666666655555555555555555555555555444444444
# 4444444333333333333333333332222222222222222222221111111111111111
# שלב שני - פתח את הקובץ לקריאה בלבד ותן למשתמש לזוז קדימה או אחורה כרצונו. המשתמש בעצם יזיז
# את הסמן עד אשר יפגע באחד מאותיות ה . TREASURE -בכל פעם הדפס למשתמש את התו "שנחת" עליו .
# אחרי שמצא את האוצר הדפס כמה תורים זה לקח לדוגמא
# Where you want to move? [1- forward 2-backwards]
# 1
# How many characters?
# 30 You hit “1”
# … again … until hit one of the “TREASURE” letters…
# אתגר: נהל טבלה של 10 התוצאות הטובות ביותר (בקובץ). בסוף כל משחק- בדוק אם השחקן הצליח לפגוע
# במספר ניחושים הנמוך מהדירוג ה - 10 בטבלה. אם כן, קלוט את שמו והכנס את תוצאתו לקובץ במקום
# המתאים (כל שורה בקובץ תכיל תוצאה ושם של שחקן( . )כמובן שבפעם הראשונה מכיוון שהקובץ יהיה ריק,
# כל תוצאה תוכנס לקובץ וכו)'
import random
import json
import colordict as colors

matmon = ' TREASURE '

def check_top10(hits, filename):

    try:
        with open(filename, 'r+') as file:
            data       = json.load(file)
            maxrank    = data['max_rank']   # get total number of ranks to keep from json file
            top_ranked = data['top_ranked'] # get ranks recorded in the file from previous attempts
    except (json.JSONDecodeError, KeyError, OSError):
        # This will catch if json file does not exist and create it at the end
        top_ranked = [] # start with empty ranking if error in json (missing section, no json)
        maxrank = 5 # default ranking to store if no json found
    
    # add to the rank file if current number of ranks is less than maximum or if hits is less than any other recorded result in the ranks 
    # (if equal to any, it won't remove existing)
    add2rank = True if len(top_ranked) < maxrank or (len(top_ranked) >=maxrank and any(hits < result['hits'] for i, result in enumerate(top_ranked))) else False

    if add2rank: # yay, we have a winner!
        name = input(f"You're in the top {maxrank}! What is your name? ")
        if name:
            top_ranked.append({ 'name': name, 'hits': hits })
            top_ranked = sorted(top_ranked, key=lambda x: (str(x['hits'])+x['name']).strip(), reverse=False)[:maxrank]
            data = { 'max_rank' : maxrank, 'top_ranked' : top_ranked }

            with open(filename, 'w') as file:
                json.dump(data, file)
        else:
            print(f'This result will not be added to Top {maxrank} list!')

    # print current ranking table in a nice table presentation
    sep = '+' + ('-'*54) + '+'
    blonwh = colors.clrs['BLUE']['B'] + colors.clrs['WHITE']['F']
    print('\n' + sep + f'\n|{f"{blonwh}Current Top {maxrank} Ranking{colors.clr_reset}":^74}|\n' + sep)
    [print(f'| {i+1:>2} -> [{rank["name"]:^20}] did it in [{rank["hits"]:^5}] hits! |') for i, rank in enumerate(top_ranked)]
    print(sep)

def create_treasure(filename): 
    try:
        print(f'*** Creating file: "{filename}" ***\n')
        with open(filename, 'w') as file:
            [ file.write(str(i) * random.randint(1, 20)) for i in range(10) ] # write groups of a number from 0 to 9 repeated a random number of times up to 20
            file.write(matmon) # write treasure
            [ file.write(str(i) * random.randint(1, 20)) for i in range(9,-1,-1) ]  # write groups of a number from 9 to 0 repeated a random number of times up to 20
            file.write('\n')
        return True
    except (OSError):
        print(f'*** Error while generating file "{filename}"')
        return False

def open_treasure(filename):
    try:
        print(f'*** Reading file: "{filename}" ***\n')
        with open(filename, 'r') as file:
            field = file.read() # read the whole file as a string
        return field
    except (OSError):
        print(f'*** Error while trying to read file: "{filename}"')
        return None
    
treasure_file_def = 'treasure.txt'
treasure_file = input(f'Enter name of file ('+colors.clrs["RED"]["F"]+f'[Enter] for default name "{treasure_file_def}"'+colors.clr_reset+') : ')
treasure_file = treasure_file if treasure_file else treasure_file_def
    
playfield = ''
if create_treasure(treasure_file):
    playfield = open_treasure(treasure_file)
    if not playfield:
        exit(0)

    position = 0
    tries = 0
    while playfield and True:
        try:
            steps = int(input(f'Enter number of steps ({colors.clrs["GREEN"]["F"]}Positive-Move Fwd, {colors.clrs["RED"]["F"]}Negative-Move Backwards): {colors.clrs["RESET"]["F"]}'))
            tries += 1
            position = max(min(position + steps, len(playfield)-2), 0)
            if playfield[position] in list(matmon):
                print('\n' + '*'*50 + f'\nFound it! You have hit the letter "{playfield[position]}" in {tries} tries!\n' + '*'*50)
                break
            else:
                print(f'Hit "{playfield[position]}"')
        except ValueError:
            print('Error: not a number')
            continue

    check_top10(tries, 'top10.json')
