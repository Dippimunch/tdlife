import tdl
import random
import numpy


def main():
    screen_width = 52
    screen_height = 54

    pause = True

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
    
    gen = 0
    
    life = numpy.random.randint(2, size=(50, 50), dtype=numpy.int)
    colors = numpy.random.randint(1,3, size=(50,50), dtype=numpy.int)*life

    root_console = tdl.init(screen_width, screen_height, title='.*LIPHE*.')
    con = tdl.Console(screen_width, screen_height)
    
    #print(life[:20,:20])
    #print(colors[:20,:20])
    #print(life[:20,:20] - colors[:20,:20])
    
    #quit()
    
    while not tdl.event.is_window_closed():

        play_life(con, root_console, screen_width, screen_height, life, colors)

        root_console.draw_str(0, 52, "Gen: " + str(gen), (220, 180, 140))
        
        tdl.flush()

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                    user_input = event
                    break
        else:
            user_input = None

        action = handle_keys(user_input)

        advance = action.get('advance')
        new = action.get('new')

        if advance:
            pause = not pause

        if new:
            pause = True
            gen = 0
            life = numpy.random.randint(2, size=(50, 50), dtype=numpy.int)
            colors = numpy.random.randint(1,3, size=(50,50), dtype=numpy.int)*life
            play_life(con, root_console, screen_width, screen_height, life, colors)

        if pause == False:
            life, colors = play_life(con, root_console, screen_width, screen_height, life, colors)
            gen += 1

def handle_keys(user_input):
    if user_input == None:
        return {}
    if user_input.key == 'SPACE':
        return {'advance': True}

    if user_input.key == 'ENTER':
        return {'new': True}

    return {}

def play_life(con, root, screen_width, screen_height, a, color):
    window = tdl.Console(screen_width, screen_height)

    alive = 0

    xmax, ymax = a.shape
    b = a.copy() # copy grid & Rule 2
    bcolor = numpy.zeros((50, 50), dtype=numpy.int)

    window.draw_frame(0, 0, 52, 52, 177, fg=(50, 50, 255))
    #print(b[:20,:20])
    #print(color[:20,:20])
    #print(b[:20,:20] - color[:20,:20])

    for x in range(xmax):
        for y in range(ymax):
            block = a[max(x - 1, 0):min(x + 2, xmax), max(y - 1, 0):min(y + 2, ymax)]
            n = numpy.sum(block) - a[x, y]
            if a[x, y]:
                if n < 2 or n > 3:
                    b[x, y] = 0 # Rule 1 and 3
            elif n == 3:
                b[x, y] = 1 # Rule 4
            if b[x, y] == 1:
                alive += 1
                colorblock = block*color[max(x - 1, 0):min(x + 2, xmax), max(y - 1, 0):min(y + 2, ymax)]
                colorcounts = [numpy.count_nonzero(colorblock == j) for j in range(1, 3)]
                #print(x, y)
                #print(block)
                #print(colorblock)
                #colormax = numpy.argmax(colorbins[1:])
                #bcolor[x,y] = colormax+1
                
                if colorcounts[0] > colorcounts[1]:
                    colormax = 1
                elif colorcounts[0] < colorcounts[1]:
                    colormax = 2
                else:
                    colormax = random.randint(1,3)
                
                bcolor[x,y] = colormax
                if colormax == 1:
                    window.draw_char(x + 1, y + 1, 176, fg=(200, 150, 100), bg=(0, 0, 100))
                if colormax == 2:
                    window.draw_char(x + 1, y + 1, 176, fg=(100, 75, 50), bg=(0, 0, 100))

                #window.draw_char(x + 1, y + 1, 176, fg=(200, 150, 100), bg=(0, 0, 100))
                window.draw_str(0, 53, "Living: " + str(alive), (220, 180, 140))
    
    x = 0
    y = 0
    root.blit(window, x, y, 52, 54, 0, 0)
    
    #print(b[:20,:20])
    #print(bcolor[:20,:20])
    #print(b[:20,:20] - color[:20,:20])
    
    return b, bcolor
    
main()
