import tdl

import numpy


def main():
    screen_width = 102
    screen_height = 74

    pause = True

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
    
    gen = 0
    
    mouse_coordinates = (0, 0)
    place = 0
    
    rps = numpy.random.randint(3, size=(100, 70), dtype=numpy.byte)

    root_console = tdl.init(screen_width, screen_height, title='.*LIPHE*.')
    con = tdl.Console(screen_width, screen_height)
    
    while not tdl.event.is_window_closed():

        play_rps(con, root_console, screen_width, screen_height, rps)

        root_console.draw_str(0, screen_height - 3, "Gen: " + str(gen), (220, 180, 140), (50, 50, 200))
        #print(mouse_coordinates)
        
        tdl.flush()

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                    user_input = event
                    break
            elif event.type == 'MOUSEMOTION':
                mouse_coordinates = event.cell

            elif event.type == 'MOUSEDOWN': # Change cell value
                rps[mouse_coordinates[0] - 1, mouse_coordinates[1] - 1] = place
                print(place)
                print(rps[mouse_coordinates[0], mouse_coordinates[1]])
                #print(mouse_coordinates[0])
                #print(mouse_coordinates[1])
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
            rps = numpy.random.randint(3, size=(100, 70), dtype=numpy.byte)
            play_rps(con, root_console, screen_width, screen_height, rps)

        if pause == False:
            rps = play_rps(con, root_console, screen_width, screen_height, rps)
            gen += 1

def handle_keys(user_input):
    if user_input == None:
        return {}
    if user_input.key == 'SPACE':
        return {'advance': True}

    if user_input.key == 'ENTER':
        return {'new': True}

    return {}

def play_rps(con, root, screen_width, screen_height, a):
    window = tdl.Console(screen_width, screen_height)

    xmax, ymax = a.shape
    b = a.copy()

    red = 0
    green= 0
    blue = 0
    
    window.draw_frame(0, 0, screen_width, screen_height - 2, 177, fg=(50, 50, 255))

    for x in range(xmax):
        for y in range(ymax):
            block = a[max(x - 1, 0):min(x + 2, xmax), max(y - 1, 0):min(y + 2, ymax)]
            if numpy.count_nonzero(block == (a[x,y] + 1) % 3) > 2:
                b[x,y] = (a[x,y] + 1) % 3

    for x in range(xmax):
        for y in range(ymax):
            if b[x, y] == 0:
                green += 1
                window.draw_char(x + 1, y + 1, 176, fg=(0, 150, 0), bg=(0, 0, 100))
            elif b[x, y] == 1:
                blue += 1
                window.draw_char(x + 1, y + 1, 176, fg=(0, 0, 150), bg=(0, 0, 100))
            elif b[x, y] == 2:
                red += 1
                window.draw_char(x + 1, y + 1, 176, fg=(150, 0, 0), bg=(0, 0, 100))
    
    x = 0
    y = 0
    
    #TODO# Ennumerate colors
    window.draw_str(0, screen_height - 2, "Red: " + str(red), (250, 100, 100))
    window.draw_str(11, screen_height - 2, "Green: " + str(green), (100, 250, 100))
    window.draw_str(24, screen_height - 2, "Blue: " + str(blue), (100, 100, 250))
    root.blit(window, x, y, 102, 74, 0, 0)
    
    return b
    
main()
