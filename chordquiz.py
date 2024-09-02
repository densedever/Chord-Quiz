"""
URLs I referenced while developing:
    https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    https://www.geeksforgeeks.org/python-list-files-in-a-directory/
    https://pythonprogramming.net/adding-sounds-music-pygame/
    https://opensource.com/article/20/9/add-sound-python-game
    http://nedbatchelder.com/blog/200712/human_sorting.html

What I learned/was reminded of while developing:
    cumulative sums are a thing
    make sure files are correctly sorted!

Names in uppercase denote constants
Names are in snake_case otherwise.
"""

# TODO: make list/dict of supported chord colors and display them when played


import pygame
import os
import re

### setup
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.2) # don't blow your speakers out

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
WHITE         = (255, 255, 255)
NOTE_DURATION = 1000 # 2 second default play time

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font('freesansbold.ttf', 32)
pygame.display.set_caption("Chord Quiz")


## magic numbers for navigation
TOPLVL     = 1 # main menu
PRACTICE   = 2
QUIZ       = 3
navigation = TOPLVL # which screen you're on


# needed for playing included sound files

# sort a list in the way humans count. 1, 2, 3, 10 instead of 1, 10, 2, 3
# works by breaking string into number/text chunks with re,
# converting the chunk to int if needed, and sorting by that number
def human_sort(l):
    return sorted(l, key=lambda s:[(int(c) if c.isdigit() else c) for c in re.split('([0-9]+)', s)])
    
SOUND_FILE_NAMES = human_sort([file for file in os.listdir(".\\sounds\\")])
NOTES = [pygame.mixer.Sound(".\\sounds\\" + file) for file in SOUND_FILE_NAMES]


### tools for building chords

class Chord():
    def __init__(self, root, color):
        self.root  = root # root note as sound file
        self.color = color # 'color' means the type of chord
        #self.name  = "" # display name of chord, such as 'Eb-9'
        
        # the following calculates the notes played on a piano
        # using a cumulative sum stored in self.notes
        # the notes are integer values from 0 to 87
        # representing the 88 keys of a standard piano
        sums = []
        current_sum = self.root
        for note in self.color:
            current_sum += note
            sums.append(current_sum)
        
        self.notes = [self.root] + sums # notes in the chord

    # will add arpeggiation as a passed-in value later
    def play(self):
        for n in self.notes:
            NOTES[n].play(1, NOTE_DURATION)
    
    # here because sounds weren't playing right, and I might need later.
    """
    def debug(self):
        for n in self.notes:
            print(SOUND_FILE_NAMES[n])
    """

class Button():
    # all these values need tweaking to look nicer
    # going for functionality over looks for now
    def __init__(self, txt, pos):
        self.text     = txt
        self.pos      = pos
        button_width  = 200
        button_height = 40
        self.button   = pygame.rect.Rect((self.pos[0], self.pos[1]), (button_width, button_height))
    
    def draw(self):
        pygame.draw.rect(screen, 'light grey', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark grey', self.button, 5, 5)
        text = font.render(self.text, True, 'black')
        screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))
        
    def check_clicked(self):
        return (self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0])


# buttons for navigation and playing the chords
practice = Button("Practice", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - SCREEN_HEIGHT/6))
quiz     = Button("Quiz", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SCREEN_HEIGHT/6))
play     = Button("Play", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# a test value and later more chord colors to pass into the Chord() class
MAJOR_TRIAD = [4, 3]

# C4 major triad starting at root 39, going up by 4 and then 3 semitones 
example_chord = Chord(39, MAJOR_TRIAD) 

### main
running = True
while running:
    screen.fill(WHITE) # do burn your eyes out!
    
    if navigation == TOPLVL:
        practice.draw()
        quiz.draw()
        if practice.check_clicked():
            navigation = PRACTICE
        if quiz.check_clicked():
            navigation = QUIZ
    
    if navigation == PRACTICE:
        play.draw()
        if play.check_clicked():
            example_chord.play()

    # all events here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()
