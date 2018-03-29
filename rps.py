import tdl

import numpy


def main():
    screen_width = 52
    screen_height = 54

    pause = True

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
    
    gen = 0
    
    rps = numpy.random.randint(3, size=(50, 50), dtype=numpy.byte)

    root_console = tdl.init(screen_width, screen_height, title='.*LIPHE*.')
    con = tdl.Console(screen_width, screen_height)
    print(rps[0])
    
    while not tdl.event.is_window_closed():

        play_rps(con, root_console, screen_width, screen_height, rps)

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
            rps = numpy.random.randint(3, size=(50, 50), dtype=numpy.byte)
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
    
    window.draw_frame(0, 0, 52, 52, 177, fg=(50, 50, 255))

    for x in range(xmax):
        for y in range(ymax):
            n = numpy.sum(a[max(x - 1, 0):min(x + 2, xmax), max(y - 1, 0):min(y + 2, ymax)]) - a[x, y]
            if a[x, y]:
                if n == 0:
                    b[x, y] = 1
                    #window.draw_char(x + 1, y + 1, 176, fg=(0, 150, 0), bg=(0, 0, 100))
                if n == 1:
                    b[x, y] = 2
                    #window.draw_char(x + 1, y + 1, 176, fg=(0, 0, 150), bg=(0, 0, 100))
                if n == 2:
                    b[x, y] = 0
                    #window.draw_char(x + 1, y + 1, 176, fg=(150, 0, 0), bg=(0, 0, 100))

    for x in range(xmax):
        for y in range(ymax):
            if a[x, y] == 0:
                window.draw_char(x + 1, y + 1, 176, fg=(0, 150, 0), bg=(0, 0, 100))
            elif a[x, y] == 1:
                window.draw_char(x + 1, y + 1, 176, fg=(0, 0, 150), bg=(0, 0, 100))
            elif a[x, y] == 2:
                window.draw_char(x + 1, y + 1, 176, fg=(150, 0, 0), bg=(0, 0, 100))
    
    x = 0
    y = 0
    root.blit(window, x, y, 52, 54, 0, 0)
    
    return b
    
main()
