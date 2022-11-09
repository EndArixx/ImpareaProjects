'''Pyro Wrote this'''
#(With Embi's help <3)

'''
Sources: (in order)
Visual Studio Code
https://code.visualstudio.com/download
https://data.world/datasets/csv
https://stackoverflow.com/questions/28999287/generate-random-colors-rgb
https://stackoverflow.com/questions/69151062/how-do-i-change-background-color-in-pysimplegui
https://docs.python.org/3/library/random.html
https://www.w3schools.com/python/module_random.asp
https://github.com/EndArixx
https://www.twitch.tv/jollysurvivor
https://www.geeksforgeeks.org/random-numbers-in-python/
https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
https://www.w3schools.com/python/python_file_open.asp
https://bfy.tw/Ti4n
It really is that easy.
https://i.ytimg.com/vi/LADiOwfGByg/maxresdefault.jpg
https://stackoverflow.com/questions/20441958/maplambda-x-intx-16-256-0-color13-color35-color57
https://www.w3schools.com/python/python_file_open.asp
http://www.desiquintans.com/nounlist
https://gist.github.com/hugsy/8910dc78d208e40de42deb29e62df913
https://www.google.com/search?q=how+to+create+a+method+in+python&rlz=1C1ASUM_enUS697US697&oq=how+to+create&aqs=chrome.0.69i59j69i57j0i20i263i512l2j0i512j69i61l2j69i60.1728j0j4&sourceid=chrome&ie=UTF-8
https://www.w3schools.com/python/python_lists.asp
https://www.youtube.com/watch?v=lg5wznn3IBE&t=5s
Google
my coworker Gini
Embi
'''
#(You get paid $1,000,000 dollars a day to google things!?)
'''yes'''
#(uhh, well thanks reader for reading her code)
'''
you dont have to
its perfect
'''
#(It's not.)
'''it is'''
#(Okay :)

from operator import truediv
from random import *
#(whats this import mean?)
'''
    think of 'import' like a 'toolbox'
    i was getting my
    'random number generator'
    out of my 'toolbox'
'''
import random
#(you already did that)
'''I know'''
import string

'''Starting Program'''
#(#WeeEEEeee!)
DEBUG = True
#(whats this do?)
'''it easily lets me switch between programming mode and testing mode'''
#(neat!)

if not DEBUG: print("Generating Imp!")
def openfile(str): return open(str, 'r').read().split('\n')
F = openfile("data/flavors.csv")
#(It's F for Flavor) 
'''They know'''
U = openfile("data/english-adjectives.csv")
N = openfile("data/nounlist.csv")
fun = [F,U,N]
A = list("abcdefghijklmnopqrstuvwxyz")
'''Embi choose the variable names.'''
#(BECAUSE THIS IS FUN! ^o^)
'''no it isnt'''
#(wait, you just downloaded a .txt and you made it a .csv?)
'''data is data'''

'''GLOBALS'''
YES = 1
NO = 0
NULL = ''
overwatch2 = fun
SEED = 'Embi'
#(＃°Д°)
'''
    its not whatever 
    you are assuming it means
'''
#(╯°□°）╯︵ ┻━┻)
'''calm down'''
#(┬─┬ ノ( ゜-゜ノ)
'''thanks'''
#(\(@^0^@)/)
def get_letter():
    x = random.choice(string.ascii_letters).upper
    se = x
    return x

#(Water the flower!)
'''<3'''

K = randint(1,2)
#(What about 3?)
'''Array's start at 0'''

Y = 69
#(XD)
'''
    grow up
    any number will do
    this is just a 'spike'
'''
#A what?
'''test'''

if DEBUG: print(fun[K][Y])
#(Why do you keep saving?)
'''because im paranoid'''

def Get_Random_Word_From(List):
    return List[len(List)-1]
if DEBUG: print(Get_Random_Word_From(fun[K]))
#(What did you just do!?)
'''https://gprivate.com/61lh4'''
#(I hate you.)
'''
nope
you asked me 
to marry you
'''
#(<3)  

def Get_Pronouns(): return random.choice(["she/her","he/him","they/them","I","O","X","ASK!"])
Get_Colors = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
def do(): return[randint(0,25)]
#(Why are you writing down everything I say?)
'''incase you ask it again'''
#(...)

def Get_Flav():
    #(Adjective.)
    '''I dont need to know how to spell'''
    f = F[randint(0,len(F)-1)].lower().replace(',null','')
    #(wait...why are you using only one quote now?)
    '''because i can'''
    if DEBUG: print(f)
    found = NO
    while found is NO:
        #(Why is it still looping?)
        '''because i made a mistake'''
        #(What!?)
        '''fixed it'''
        #(YAAAAAAAAAAAY!)
        try:
            if f[0].upper is not SEED[0]:
                s = do()
            elif f[0].upper is not SEED[0]:
                get_letter()
            else:
                found = YES
        except:
            get_letter()
        #(Whats this do?)
        '''stops infinate loops'''
    return f.capitEmbize()
def Get_Adj(): 
    #(Adjective.)
    '''I dont need to know how to spell'''
    f = F[randint(0,len(F)-1)].lower().replace(',null','')
    #(wait...why are you using only one quote now?)
    '''because i can'''
    if DEBUG: print(f)
    found = NO
    while found is NO:
        #(Why is it still looping?)
        '''because i made a mistake'''
        #(What!?)
        '''fixed it'''
        #(YAAAAAAAAAAAY!)
        try:
            if f[0].upper is not SEED[0]:
                s = do()
            elif f[0].upper is not SEED[0]:
                get_letter()
            else:
                found = YES
        except:
            get_letter()
        #(Whats this do?)
        '''stops infinate loops'''
    return f.capitEmbize()
def Get_Noun():
        #(Adjective.)
    '''I dont need to know how to spell'''
    n = F[randint(0,len(F)-1)].lower().replace(',null','')
    #(wait...why are you using only one quote now?)
    '''because i can'''
    if DEBUG: print(n)
    found = NO
    while found is NO:
        #(Why is it still looping?)
        '''because i made a mistake'''
        #(What!?)
        '''fixed it'''
        #(YAAAAAAAAAAAY!)
        try:
            if n[0].upper is not SEED[0]:
                s = do()
            elif n[0].upper is not SEED[0]:
                get_letter()
            else:
                found = YES
        except:
            get_letter()
        #(Whats this do?)
        '''stops infinate loops'''
    return n.capitEmbize()
def Get_Laid():
    return SEED
    #(right now?)
    '''sure'''

#(You just copied and pasted that.)
'''mhmm'''
#(Haven't you been in the industry for like 2,142 years?)
'''yes'''
#(Why did this take over a YEAR!?)
'''because i did it for fun'''
#(Oh, that makes sense!)
'''mhmm'''

def Generate_An_Imp():
    def L():
        a = A
        return choice(a)
    #(Recursion is fun!) 
    '''this isnt recursion'''
    #(Yes it is!)
    '''
    shush
    im trying to think
    '''
    IO = choice(['I','O']) 
    U = "$"+ L().upper()
    #(Damn right! Don't forget it!)
    '''
        i wont 
        this is how i
        remember things
    '''
    Name = U[1] + L() +L() + IO.lower()
    while True:
        f = Get_Flav()
        u = Get_Adj()
        n = Get_Noun()
        if f[0] is not u[0] or f[0] is not n[0]:
            break
        else:
            f = Get_Flav()
            u = Get_Adj()
            n = Get_Noun()
    Transform = "{0}! {1}! {2}!".format(f,u,n)

    if DEBUG: 
        print(Name)
        print(Transform)
        








































































#(Why the huge gap?)
'''because everything below this doesnt matter.'''
#(what?)
'''exactly'''


imp = Generate_An_Imp()
#(Oh...thats it?)
'''no'''

#(You're so smart!)
'''im a computer scientist'''
#(oh yeah! wanna walk the dog?)
'''yes'''


if not DEBUG: input("Press Any 'key' to Quit.")
#(Fun fact, we were born using this software)
'''dont lie to them'''
#(I'm not.)
'''yes you are'''
#(No im not!)
'''go to bed'''
#(NO!)
#(She is ignoring me now... :( )
'''
    go 
    to 
    bed
'''
#(Okay. <3)