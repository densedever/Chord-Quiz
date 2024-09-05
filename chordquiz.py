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

# TODO: make quiz page


import pygame
import os
import re
import random

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

class Button():
    # all these values need tweaking to look nicer
    # going for functionality over looks for now
    def __init__(self, txt, pos):
        self.text     = txt
        self.pos      = pos
        button_width  = 230
        button_height = 40
        self.button   = pygame.rect.Rect((self.pos[0], self.pos[1]), (button_width, button_height))
    
    def draw(self):
        pygame.draw.rect(screen, 'light grey', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark grey', self.button, 5, 5)
        text = font.render(self.text, True, 'black')
        screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))
        
    def check_clicked(self):
        return (self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0])


### tools for building chords

CHORD_COLORS = {
    "maj":  [4, 3],
    "min":  [3, 4],
    "dim":  [3, 3],
    "aug":  [4, 4],
    "sus2": [2, 5],
    "sus4": [5, 2],
    "maj7": [4, 3, 4],
    "min7": [3, 4, 3],
    "dim7": [3, 3, 3],
    "dom7": [4, 3, 3],
    "maj9": [4, 3, 4, 3],
    "min9": [3, 4, 3, 4],
}

class Chord():
    def __init__(self, root, color):
        self.root  = root # root note as sound file
        self.color = color # 'color' means the type of chord
        
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

    def debug(self):
        for n in self.notes:
            print(SOUND_FILE_NAMES[n])





# buttons for navigation and playing the chords
practice = Button("Practice", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - SCREEN_HEIGHT/6))



CHORD_BUTTONS = {
    "maj":  Button("Major",        ((SCREEN_WIDTH/3)*0, (SCREEN_HEIGHT/4)*0)),
    "min":  Button("Minor",        ((SCREEN_WIDTH/3)*1, (SCREEN_HEIGHT/4)*0)),
    "dim":  Button("Diminished",   ((SCREEN_WIDTH/3)*2, (SCREEN_HEIGHT/4)*0)),
    "aug":  Button("Augmented",    ((SCREEN_WIDTH/3)*0, (SCREEN_HEIGHT/4)*1)),
    "sus2": Button("Suspended 2",  ((SCREEN_WIDTH/3)*1, (SCREEN_HEIGHT/4)*1)),
    "sus4": Button("Suspended 4",  ((SCREEN_WIDTH/3)*2, (SCREEN_HEIGHT/4)*1)),
    "maj7": Button("Major 7",      ((SCREEN_WIDTH/3)*0, (SCREEN_HEIGHT/4)*2)),
    "min7": Button("Minor 7",      ((SCREEN_WIDTH/3)*1, (SCREEN_HEIGHT/4)*2)),
    "dim7": Button("Diminished 7", ((SCREEN_WIDTH/3)*2, (SCREEN_HEIGHT/4)*2)),
    "dom7": Button("Dominant 7",   ((SCREEN_WIDTH/3)*0, (SCREEN_HEIGHT/4)*3)),
    "maj9": Button("Major 9",      ((SCREEN_WIDTH/3)*1, (SCREEN_HEIGHT/4)*3)),
    "min9": Button("Minor 9",      ((SCREEN_WIDTH/3)*2, (SCREEN_HEIGHT/4)*3))
}

quiz = Button("Quiz", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SCREEN_HEIGHT/6))
play = Button("Play", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# setting a comfortable hearing range for the chords
random_note_range = random.randint(20, 60)

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
        for v in CHORD_BUTTONS.values():
            v.draw()
        for k, v in CHORD_BUTTONS.items():
            if v.check_clicked():
                for k2, v2 in CHORD_COLORS.items():
                    if k == k2:
                        ch = Chord(random_note_range, v2)
                        ch.play()
                        ch.debug()

    # all events here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()
