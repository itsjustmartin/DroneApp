import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((360,240))
#get keypress
def getkey(keyName):
    ans = False
    for eve in pygame.event.get() : pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans

def main() :
    if getkey("LEFT") :
        print("left key")
    if getkey("RIGHT") :
        print("right key")

# if iam running as main file
if __name__== '__main__' :
 init()
 while True :
     main()




