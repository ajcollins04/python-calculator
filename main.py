# Scientific Calculator by Andrew Collins
# v1.0
# Basic frames and placemens taken from https://github.com/bnirankar/Scientific-Calculator---Python-Tkinter-Library

import webbrowser
from tkinter import *
import math
from math import pi, factorial, sqrt, log10 as log
import random
from PIL import Image, ImageTk
from pyboy import PyBoy, WindowEvent

# Trig functions (converts from degrees)
def sin(num):
    return math.sin(math.radians(num))
def cos(num):
    return math.cos(math.radians(num))
def tan(num):
    return math.tan(math.radians(num))


# The invert function that inverts some button controls
def invert_func():
    global invert
    invert = not invert
    if invert == True:
        square_button.button.config(text="x³", command=lambda: choose_num("^3"))
        exponent_btn.button.config(text="x⁻ʸ", command=lambda: choose_num("^-"))
        sin_btn.button.config(text="sin⁻¹", command=lambda: choose_num("asin("))
        cos_btn.button.config(text="cos⁻¹", command=lambda: choose_num("acos("))
        tan_btn.button.config(text="tan⁻¹", command=lambda: choose_num("atan("))
        root_btn.button.config(text="1/x", command=lambda: begin_end("1/(", ")"))
        exp10_btn.button.config(text="eˣ", command=lambda: choose_num("e^"))
        log_btn.button.config(text="ln", command=lambda: choose_num("ln("))
        exp_btn.button.config(text="Snk", command=run_snake)
        mod_btn.button.config(text="Pkmn", command=start_pokemon)

    else:        
        square_button.button.config(text="x²", command=lambda: choose_num("^2"))
        exponent_btn.button.config(text="xʸ", command=lambda: choose_num("^"))
        sin_btn.button.config(text="sin", command=lambda: choose_num("sin("))
        cos_btn.button.config(text="cos", command=lambda: choose_num("cos("))
        tan_btn.button.config(text="tan", command=lambda: choose_num("tan("))
        root_btn.button.config(text=" √x ", command=lambda: choose_num("sqrt("))
        exp10_btn.button.config(text="10ˣ", command=lambda: choose_num("10^"))
        log_btn.button.config(text="log", command=lambda: choose_num("log("))
        exp_btn.button.config(text="Exp", command=lambda: begin_end("(", ")*10^"))
        mod_btn.button.config(text="Mod", command=lambda: choose_num("%"))


# Remove a number
def remove_num():
    if len(data.get()) == 1: 
        data.set("0")
    else: data.set(data.get()[0:-1])


# Create and pack frame 
class Row:
    def __init__(self):
        self.frame = Frame(root, bg="#000000")
        self.frame.pack(expand=TRUE, fill=BOTH)


# Button with parameter for what is added to the input
class SymbButton:
    def __init__(self, row, text, symb=""):
        self.button = Button(row.frame, text=text, font="Segoe 18", relief=RAISED, fg="white", bg="#333333", width=3, command=lambda: choose_num(symb))
        self.button.pack(side=LEFT, expand=TRUE, fill=BOTH)


# Adds the text of the button to the input
class NumButton:
    def __init__(self, row, num):
        self.button = Button(row.frame, text=num, font="Segoe 18", relief=RAISED, fg="white", bg="#333333", width=3, command=lambda: choose_num(num))
        self.button.pack(side=LEFT, expand=TRUE, fill=BOTH)


# Button with parameter for function
class FuncButton:
    def __init__(self, row, text, func=()):
        self.button = Button(row.frame, text=text, font="Segoe 18", relief=RAISED, fg="white", bg="#333333", width=3, command=func)
        self.button.pack(side=LEFT, expand=TRUE, fill=BOTH)


# Buttons for snake game
class SnakeButton:
    def __init__(self, row, text, direction):
        self.button = Button(row, text=text, font="Segoe 18", relief=RAISED, fg="white", bg="#333333", width=3, command=lambda: change_direction(*direction) ) #command=lambda: 
        self.button.pack(side=LEFT, expand=TRUE, fill=BOTH)


class Filler:
    def __init__(self, row):
        self.label = Button(row, bg="#333333", width=3, font="Segoe 18", state="disabled")
        self.label.pack(side=LEFT, expand=TRUE, fill=BOTH)


class PokemonButton:
    def __init__(self, row, text, press, release):
        self.button = Button(row, text=text, font="Segoe 18", relief=RAISED, fg="white", bg="#333333", width=3) 
        self.button.pack(side=LEFT, expand=TRUE, fill=BOTH)
        self.button.bind("<ButtonPress-1>", lambda _: pyboy.send_input(press))
        self.button.bind("<ButtonRelease-1>", lambda _: pyboy.send_input(release))



# Adds a number to the input
def choose_num(num):
    if data.get() == '0' or data.get() == "Error":
        data.set(num)
    else:
        data.set(data.get() + num)


# The equals button logic, evaluates the input
def equals():
    try:
        for letter in data.get()[::-1]:
            if letter == ")":
                break
            if letter == "(":
                data.set(data.get() + ")")  

        equation = data.get().replace("÷", "/").replace("×", "*").replace("^", "**").replace("π", "pi")
        data.set(str(eval(equation)))

        if data.get()[-2:] == ".0":
            data.set(data.get()[:-2])
    except:
        data.set("Error")

# Adds to the beginning and end
def begin_end(begin, end):
    data.set(begin + data.get() + end)

# Change snake direction
def change_direction(x, y):
    global new_x
    global new_y
    global changing_direction

    if changing_direction == False:
        changing_direction = True
        new_x = x
        new_y = y


# Snake Loop
def snake_loop():
    global changing_direction
    global delta_x
    global delta_y
    global snake_running

    # Breaks out of the loop once the game isn't in the window anymore
    if snake_running == False:
        return

    # Changes the direction
    if changing_direction == True:
        if delta_x != -new_x: delta_x = new_x
        if delta_y != -new_y: delta_y = new_y
        changing_direction = False

    # Removes fruit and creates another one
    ate_fruit = False
    for point in snake_points:
        for fruit_point in fruit_points:
            if point == fruit_point:
                ate_fruit = True
                fruit_points.remove(fruit_point)
                fruit_points.append((random.randint(0, int(snake_canvas.winfo_width() / 10 - 1)), random.randint(0, int(snake_canvas.winfo_height() / 10 - 1))))

    # If you hit yourself 
    for point in snake_points[0:-1]:
        if snake_points[-1][0] == point[0] and  snake_points[-1][1]  == point[1]:
            game_over()
            return
    
    # If you hit a wall
    if (snake_points[-1][0] < 0 or snake_points[-1][0] > snake_canvas.winfo_width() / 10 - 1) or (snake_points[-1][1] < 0 or snake_points[-1][1] > snake_canvas.winfo_height() / 10 - 1):
        game_over()
        return

    # Moves the end to the front unless you ate a fruit
    if ate_fruit == False: snake_points.remove(snake_points[0])
    snake_points.append((snake_points[-1][0] + delta_x, snake_points[-1][1] + delta_y))

    # Draws fruit and snake to the canvas
    snake_canvas.delete("all")
    for point in fruit_points:
        snake_canvas.create_rectangle(point[0] * 10 + 2, point[1] * 10 + 2, point[0] * 10 + 11, point[1] * 10 + 11, outline="red", fill="red")
    for point in snake_points:
        snake_canvas.create_rectangle(point[0] * 10 + 2, point[1] * 10 + 2, point[0] * 10 + 11, point[1] * 10 + 11, outline="green", fill="green")

    # Loops again
    root.after(100, snake_loop)

# Start/restart snake game
def start():
    global snake_points
    global fruit_points
    global changing_direction
    global new_x
    global new_y
    global delta_x
    global delta_y

    snake_points = [(0, 0), (1, 1)]
    fruit_points = [(random.randint(0, int(snake_canvas.winfo_width() / 10 - 1)), random.randint(0, int(snake_canvas.winfo_height() / 10 - 1)))]

    changing_direction = False
    new_x = 0
    new_y = 0

    delta_x = 1
    delta_y = 0

    root.after(100, snake_loop)

# Snake game over
def game_over():
    snake_canvas.delete("all")

    # Gets the drawn points from the image for manipulation
    game_over_points = []
    for pos, point in enumerate(img_points):
        if point[3] == 255:
            game_over_points.append((pos % img_size[0], math.floor(pos / img_size[0])))
    
    # Scales the text up to the canvas size
    x_scale = math.floor(snake_canvas.winfo_width() / img_size[0])
    if img_size[1] * x_scale > snake_canvas.winfo_height():
        x_scale = math.floor(snake_canvas.winfo_height() / img_size[1])

    # Draws game over
    for point in game_over_points:
        x1 = point[0] * x_scale + 2
        y1 = point[1] * x_scale + 2

        # Centers text
        x1 = x1 + snake_canvas.winfo_width() / 2 - img_size[0] * x_scale / 2
        y1 = y1 + snake_canvas.winfo_height() / 2 - img_size[1] * x_scale / 2

        x2 = x1 + x_scale
        y2 = y1 + x_scale         

        snake_canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black")

    # Starts the game 
    root.after(2000, start)

# Run snake
def run_snake():
    global snake_canvas
    global snake_running

    def resize(_):
        w,h = math.floor(root.winfo_width()), math.floor(root.winfo_height() - 200)
        snake_canvas.config(width=w, height=h)

    for row in rows:
        row.frame.pack_forget()
    disp.pack_forget()

    snake_canvas = Canvas(root, bg="mistyrose", width=root.winfo_width(), height=root.winfo_height() - 200)
    snake_canvas.pack()

    root.bind('<Configure>', resize)

    snkrow1.pack(expand=TRUE, fill=BOTH)
    snkrow2.pack(expand=TRUE, fill=BOTH)

    snake_running = True
    start()

def end_snake():
    global snake_running

    snake_running = False
    snake_canvas.pack_forget()
    snkrow1.pack_forget()
    snkrow2.pack_forget()

    disp.pack(expand=TRUE, fill=BOTH)
    for row in rows:
        row.frame.pack(expand=TRUE, fill=BOTH)


def start_pokemon():
    global pyboy
    global pokemon_running
    global pokemon_canvas


    def run_pokemon():
        pyboy.tick()
        root.after(13, run_pokemon)

        try:
            screen_stuff = manager.screen().screen_image()

            canvas_width = int(pokemon_canvas.winfo_width())
            canvas_height = int(pokemon_canvas.winfo_height())

            img_width = canvas_width
            img_height =  int(canvas_width * 9 / 10)

            if img_height > canvas_height:
                img_height = canvas_height
                img_width = int(canvas_height * 10 / 9)


            screen_stuff = screen_stuff.resize((img_width, img_height), resample=0)
            image = ImageTk.PhotoImage(screen_stuff)


            pokemon_canvas.delete("all")
            pokemon_canvas.create_image(canvas_width / 2 - img_width / 2, canvas_height / 2 - img_height / 2, image=image, anchor='nw')
            pokemon_canvas.image = image
        except: pass



    def resize(_):
        w,h = math.floor(root.winfo_width()), math.floor(root.winfo_height() - 200)
        pokemon_canvas.config(width=w, height=h)    
        
    def key_press(e):
        if e.char == "z": pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        if e.char == "x": pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
        if e.char == "d": pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
        if e.char == "s": pyboy.send_input(WindowEvent.PRESS_BUTTON_SELECT)
        if e.keysym == "Left": pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
        if e.keysym == "Right": pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        if e.keysym == "Down": pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
        if e.keysym == "Up": pyboy.send_input(WindowEvent.PRESS_ARROW_UP)


    def key_release(e):
        if e.char == "z": pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        if e.char == "x": pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)
        if e.char == "d": pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
        if e.char == "s": pyboy.send_input(WindowEvent.RELEASE_BUTTON_SELECT)
        if e.keysym == "Left": pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        if e.keysym == "Right": pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        if e.keysym == "Down": pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
        if e.keysym == "Up": pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)


    for row in rows:
        row.frame.pack_forget()
    disp.pack_forget()

    pokemon_canvas = Canvas(root, width=160, height=144, bg="black")
    pokemon_canvas.pack()

    pkmnrow1.pack(expand=TRUE, fill=BOTH)
    pkmnrow2.pack(expand=TRUE, fill=BOTH)

    root.bind('<KeyPress>', key_press)
    root.bind('<KeyRelease>', key_release)


    root.bind('<Configure>', resize)


    pokemon_running = True
    pyboy = PyBoy('pokemon.gb', window_type="headless", sound=True)  
    pyboy.set_emulation_speed(1)
    manager = pyboy.botsupport_manager()

    root.after(100, run_pokemon)


def end_pokemon():
    global pokemon_running

    pyboy.stop()

    pokemon_running = False
    pokemon_canvas.pack_forget()
    pkmnrow1.pack_forget()
    pkmnrow2.pack_forget()

    disp.pack(expand=TRUE, fill=BOTH)
    for row in rows:
        row.frame.pack(expand=TRUE, fill=BOTH)


# Snake game over stuff
game_over_img = Image.open("game-over.png", "r")
img_points = list(game_over_img.getdata())
img_size = game_over_img.size

# Invert variable for buttons
invert = False

# Creates window
root = Tk()
root.geometry("350x500")
root.title("Scientific Calculator")

# Keyboard bindings
root.bind('1', lambda _: choose_num("1"))
root.bind('2', lambda _: choose_num("2"))
root.bind('3', lambda _: choose_num("3"))
root.bind('4', lambda _: choose_num("4"))
root.bind('5', lambda _: choose_num("5"))
root.bind('6', lambda _: choose_num("6"))
root.bind('7', lambda _: choose_num("7"))
root.bind('8', lambda _: choose_num("8"))
root.bind('9', lambda _: choose_num("9"))
root.bind('+', lambda _: choose_num("+"))
root.bind('-', lambda _: choose_num("-"))
root.bind('*', lambda _: choose_num("×"))
root.bind('/', lambda _: choose_num("÷"))
root.bind('(', lambda _: choose_num("("))
root.bind(')', lambda _: choose_num(")"))
root.bind('^', lambda _: choose_num("^"))

root.bind("<Left>", lambda _: change_direction(-1, 0))
root.bind("<Right>", lambda _: change_direction(1, 0))
root.bind("<Up>", lambda _: change_direction(0, -1))
root.bind("<Down>", lambda _: change_direction(0, 1))

root.bind('<BackSpace>', lambda _: remove_num())

root.bind('!', lambda _: begin_end("factorial(", ")"))


root.bind('=', lambda _: equals())
root.bind('<Return>', lambda _: equals())
root.bind('<Escape>', lambda _: data.set("0"))




# Input data and display
data = StringVar(value="0")
disp = Button(root, font="Verdana 20", fg="black", bg="mistyrose",
             bd=0, justify=RIGHT, anchor="e", textvariable=data, command=lambda: webbrowser.open_new("https://www.youtube.com/watch?v=wpV-gGA4PSk"))
disp.pack(expand=TRUE, fill=BOTH)

# Row 1 Buttons

btnrow1 = Row()

square_button = SymbButton(btnrow1, "x²", "^2")
exponent_btn = SymbButton(btnrow1, "xʸ", "^")
sin_btn = SymbButton(btnrow1, "sin", "sin(")
cos_btn = SymbButton(btnrow1, "cos", "cos(")
tan_btn = SymbButton(btnrow1, "tan", "tan(")

# Row 2 Buttons

btnrow2 = Row()

root_btn = SymbButton(btnrow2, " √x ", "sqrt(")
exp10_btn = SymbButton(btnrow2, "10ˣ", "10^")
log_btn = SymbButton(btnrow2, "log", "log(")
exp_btn = FuncButton(btnrow2, "Exp", lambda: begin_end("(", ")*10^"))
mod_btn = SymbButton(btnrow2, "Mod", "%")

# Row 3 Buttons

btnrow3 = Row()

inverse_btn = FuncButton(btnrow3, "↑", invert_func)
clear_entry = FuncButton(btnrow3, " Rnd ", lambda: begin_end("round(", ")"))
clear_btn = FuncButton(btnrow3, "C", lambda: data.set("0"))
del_btn = FuncButton(btnrow3, "⌫", remove_num)
divide_btn = NumButton(btnrow3, "÷")

# Row 4 Buttons

btnrow4 = Row()

pi_btn = NumButton(btnrow4, "π")
btn7 = NumButton(btnrow4, "7")
btn8 = NumButton(btnrow4, "8")
btn9 = NumButton(btnrow4, "9")
mult_btn = NumButton(btnrow4, "×")

# Row 5 Buttons

btnrow5 = Row()

factorial_btn = FuncButton(btnrow5, "n!", lambda: begin_end("factorial(", ")"))
btn4 = NumButton(btnrow5, "4")
btn5 = NumButton(btnrow5, "5")
btn6 = NumButton(btnrow5, "6")
minus_btn = NumButton(btnrow5, "-")

# Row 6 Buttons

btnrow6 = Row()

negate_btn = FuncButton(btnrow6, "±", lambda: begin_end("-(", ")"))
btn1 = NumButton(btnrow6, "1")
btn2 = NumButton(btnrow6, "2")
btn3 = NumButton(btnrow6, "3")
plus_btn = NumButton(btnrow6, "+")

# Row 7 Buttons

btnrow7 = Row()

start_parenthesis = SymbButton(btnrow7, " ( ", "(")
end_parenthesis = SymbButton(btnrow7, " ) ", ")")
btn0 = NumButton(btnrow7, "0")
decimal_btn = SymbButton(btnrow7, " . ", ".")
equals_btn = FuncButton(btnrow7, "=", equals)

# Snake Row 1

snkrow1 = Frame(root, bg="#000000")

snk_back = Button(snkrow1, text="Back", font="Segoe 18", relief=RAISED, fg="white", bg="#333333", width=3, command=end_snake)
snk_back.pack(side=LEFT, expand=TRUE, fill=BOTH)

up_arrow = SnakeButton(snkrow1, "▲", (0, -1))
filler2 = Filler(snkrow1)

# Snake Row 2

snkrow2 = Frame(root, bg="#000000")

left_arrow = SnakeButton(snkrow2, "◀", (-1, 0))
down_arrow = SnakeButton(snkrow2, "▼", (0, 1))
right_arrow = SnakeButton(snkrow2, "▶", (1, 0))

# Pokemon Row 1

pkmnrow1 = Frame(root, bg="#000000")

pkmn_back = Button(pkmnrow1, text="Back", font="Segoe 18", relief=RAISED, fg="white", bg="#333333", width=3, command=end_pokemon)
pkmn_back.pack(side=LEFT, expand=TRUE, fill=BOTH)

pkmn_up = PokemonButton(pkmnrow1, "▲", WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP)
filler3 = Filler(pkmnrow1)

pkmn_select = PokemonButton(pkmnrow1, "Select", WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT)
pkmn_start = PokemonButton(pkmnrow1, "Start", WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START)

# Pokemon Row 2

pkmnrow2 = Frame(root, bg="#000000")

pkmn_left = PokemonButton(pkmnrow2, "◀", WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT)
pkmn_down = PokemonButton(pkmnrow2, "▼", WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN)
pkmn_right = PokemonButton(pkmnrow2, "▶", WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT)

pkmn_b = PokemonButton(pkmnrow2, "B", WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B)
pkmn_a = PokemonButton(pkmnrow2, "A", WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A)



# Calculator rows
rows = [btnrow1, btnrow2, btnrow3, btnrow4, btnrow5, btnrow6, btnrow7]

root.mainloop()
