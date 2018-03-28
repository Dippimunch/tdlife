import tdl

import numpy


def main():
    screen_width = 52
    screen_height = 54

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
    
    gen = 0
    
    life = numpy.random.randint(2, size=(50, 50), dtype=numpy.byte)

    root_console = tdl.init(screen_width, screen_height, title='.*LIPHE*.')
    con = tdl.Console(screen_width, screen_height)
    
    while not tdl.event.is_window_closed():

        play_life(con, root_console, screen_width, screen_height, life)

        root_console.draw_str(0, 52, "Gen: " + str(gen), (220, 180, 140))
        
        tdl.flush()

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                    user_input = event
                    break
        else:
            user_input = None

        #if not user_input:
            #continue

        action = handle_keys(user_input)

        advance = action.get('advance')
        new = action.get('new')

        if advance:
            life = play_life(con, root_console, screen_width, screen_height, life)
            gen += 1

        if new:
            gen = 0
            life = numpy.random.randint(2, size=(50, 50), dtype=numpy.byte)
            play_life(con, root_console, screen_width, screen_height, life)

def handle_keys(user_input):
    if user_input == None:
        return {}
    if user_input.key == 'SPACE':
        return {'advance': True}

    if user_input.key == 'ENTER':
        return {'new': True}

    return {}

def play_life(con, root, screen_width, screen_height, a):
    window = tdl.Console(screen_width, screen_height)

    alive = 0

    xmax, ymax = a.shape
    b = a.copy() # copy grid & Rule 2

    window.draw_frame(0, 0, 52, 52, 177, fg=(50, 50, 255))

    for x in range(xmax):
        for y in range(ymax):
            n = numpy.sum(a[max(x - 1, 0):min(x + 2, xmax), max(y - 1, 0):min(y + 2, ymax)]) - a[x, y]
            if a[x, y]:
                if n < 2 or n > 3:
                    b[x, y] = 0 # Rule 1 and 3
            elif n == 3:
                b[x, y] = 1 # Rule 4
                #window.draw_char(x + 1, y + 1, 176, fg=(200, 100, 50), bg=(200, 200, 200))
            if b[x, y] == 1:
                alive += 1
                window.draw_char(x + 1, y + 1, 176, fg=(200, 150, 100), bg=(0, 0, 100))
                window.draw_str(0, 53, "Living: " + str(alive), (220, 180, 140))
    
    x = 0
    y = 0
    root.blit(window, x, y, 52, 54, 0, 0)
    
    return b

    #play_life(con, root, screen_width, screen_height, b)
    
main()
