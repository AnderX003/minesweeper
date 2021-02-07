from random import choice
from tkinter import *
from tkinter import ttk
import pickle


class Cell:  # Класс клетки
    def __init__(self, master, row, column):
        """инициализация класса клетки"""
        self.button = Button(master, text="   ", bg=col_white, activebackground=col_white_active, activeforeground=col_white, pady=0, padx=0, width=2, height=1, relief="flat", bd=0, font="Bahnschrift 12")
        if (row + column) % 2 == 1:
            self.button.configure(bg=col_white_sub)  # немного затемнённый не прожатый
        self.mine = False  # Наличие мины в клетке
        self.value = 0  # Кол-во мин вокруг
        self.viewed = False  # Открыто/закрыто
        self.flag = 0  # 0 - флага нет, 1 - флаг стоит, 2 - стоит "?"
        self.around = []  # Массив, содержащий координаты соседних клеток
        self.clr = col_white  # Цвет текста
        self.bg = col_main_sub  # С циферкой
        if (row + column) % 2 == 1:
            self.bg = col_main  # немного затемнённый прожатый
        self.abg = col_main_active  # активный с цыферкой
        self.row = row  # Строка
        self.column = column  # Столбец

    def set_around(self):
        """заполнение массива around каждой клетки"""
        if self.row == 0:
            self.around.append([self.row + 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row + 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row + 1, self.column - 1])
        elif self.row == len(buttons) - 1:
            self.around.append([self.row - 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row - 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
                self.around.append([self.row - 1, self.column - 1])
        else:
            self.around.append([self.row - 1, self.column])
            self.around.append([self.row + 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row + 1, self.column - 1])
                self.around.append([self.row - 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row + 1, self.column - 1])
                self.around.append([self.row - 1, self.column + 1])
                self.around.append([self.row - 1, self.column - 1])

    def view(self, event):
        """при нашатии на кнопку игрового поля"""
        if not mines:  # При первом нажатии
            bombs_generator(0, self.around, self.row, self.column)

        if self.mine and not self.viewed and not self.flag:  # Если в клетке есть мина, она еще не открыта и на ней нет флага
            # print("bomb", self.value)
            self.button.configure(text="B", fg=col_white, bg=col_bomb, activebackground=col_bomb_active)  # мина r
            self.viewed = True  # Говорим, что клетка раскрыта
            for q in mines:
                try:
                    buttons[q[0]][q[1]].view("<Button-1>")  # Я сейчас буду вскрывать ВСЕ мины
                except:
                    pass

            global c
            if not c:
                c = True
                win_or_loose(False)  # Вызываем окно проигрыша

        elif not self.viewed and not self.flag:  # Если мины нет, клетка не открыта и флаг не стоит
            try:
                self.button.configure(text=self.value, fg=self.clr, bg=self.bg, activebackground=self.abg)  # выводим в текст клетки значение
                self.viewed = True
                if self.value == 0:  # Если вокруг нет мин
                    self.button.configure(text="   ")
                    for k in self.around:
                        buttons[k[0]][k[1]].view("<Button-1>")  # Открываем все клетки вокруг
            except TclError:
                pass

    def set_flag(self, event):
        """при нажатии левой клавишей миши на кнопку игрового поля"""
        if mines:
            if self.flag == 0 and not self.viewed:  # Если клетка не открыта и флага нет
                self.flag = 1  # Ставим флаг
                self.button.configure(text="F", fg=col_white, bg=col_flag, activebackground=col_flag_active)  # флаг
                flags.append([self.row, self.column])  # Добавляем в массив флагов
            elif self.flag == 1:  # Если флаг стоит
                self.flag = 2  # Ставим значение "?"
                self.button.configure(text="?", fg=col_white, bg=col_guess, activebackground=col_guess_active)  # ?
                flags.pop(flags.index([self.row, self.column]))  # Удаляем флаг из массива флагов
            elif self.flag == 2:  # Если ?
                self.flag = 0  # Устанавливаем на отсутствие флага
                self.button.configure(text="   ", bg=col_white, activebackground=col_white_active)  # пустой
                if (self.row + self.column) % 2 == 1:
                    self.button.configure(bg=col_white_sub)
            if sorted(mines) == sorted(flags) and mines != []:  # если массив флагов идентичен массиву мин
                win_or_loose(True)


def close_windows(*windows):
    """закрывает переданные окна"""
    for window in windows:
        try:
            window.destroy()
        except TclError:
            pass


def win_or_loose(case=False):
    """открывает окно победы или поражения
    запукает сохранение рекордов"""
    def on_close_windows():
        close_windows(win_or_loose_window, game_window)
        menu(user)

    global data, score, game_window

    # data[user][12] = False

    for flag in flags:
        if flag in mines:
            score += 1
        else:
            score -= 1

    data[user][2], data[user][3], data[user][4], data[user][5], data[user][6], data[user][7], data[user][8], data[user][9], data[user][10], data[user][11] = score, data[user][2], data[user][3], data[user][4], data[user][5], data[user][6], data[user][7], data[user][8], data[user][9], data[user][10]

    if score > int(data[user][1]):
        # print("score>saved")
        data[user][1] = str(score)
        # print(data)
        update_data(data)
    else:
        update_data(data)

    win_or_loose_window = Tk()
    win_or_loose_window["bg"] = col_white
    win_or_loose_window.geometry("400x200+750+200")
    win_or_loose_window.title("Minesweeper")

    win_or_loose_text = Label(win_or_loose_window, text="Game Over!", bg=col_white, font="Bahnschrift 40", fg="gray22")

    score_text = Label(win_or_loose_window, height=1, text="Your Score: " + str(score), bg=col_white, font="Bahnschrift 20", fg="gray22")

    close_button = Button(win_or_loose_window, text="Ok", command=on_close_windows, bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 20", relief="flat", fg="gray22", width=6, height=1)

    if case:
        win_or_loose_text.config(text="You won!")

    win_or_loose_text.place(relx=0.5, rely=0.2, anchor=CENTER)
    score_text.place(relx=0.5, rely=0.4, anchor=CENTER)
    close_button.place(relx=0.5, rely=0.75, anchor=CENTER)
    win_or_loose_window.resizable(False, False)
    win_or_loose_window.mainloop()


def bombs_generator(current_bombs_quantity, around, row, column):
    """функция генерации мин в зависимости от к-ва бомб"""
    if current_bombs_quantity == bombs:
        for i in buttons:
            for j in i:
                for k in j.around:
                    if buttons[k[0]][k[1]].mine:
                        buttons[buttons.index(i)][i.index(j)].value += 1
        return
    a = choice(buttons)
    b = choice(a)

    if [buttons.index(a), a.index(b)] not in mines and [buttons.index(a), a.index(b)] not in around and [buttons.index(a), a.index(b)] != [row, column]:
        b.mine = True
        mines.append([buttons.index(a), a.index(b)])
        bombs_generator(current_bombs_quantity + 1, around, row, column)
    else:
        bombs_generator(current_bombs_quantity, around, row, column)


def cheat():
    """функция для установки всех плагов там где мины"""
    for t in mines:
        buttons[t[0]][t[1]].set_flag("")


def game(high, length):
    """ф-я создания игрового окна и генерации массива с кнопками"""
    global c, score, game_window, buttons, mines, flags
    c = False
    score = 0
    game_window = Tk()
    game_window.title("Minesweeper")
    if bombs == 10:
        game_window.geometry("+790+200")
    elif bombs == 40:
        game_window.geometry("+670+200")
    else:
        game_window.geometry("+670+0")

    flags = []
    mines = []
    buttons = [[Cell(game_window, row, column) for column in range(high)] for row in range(length)]
    for i in buttons:
        for j in i:
            j.button.grid(column=i.index(j), row=buttons.index(i), ipadx=7, ipady=3)
            j.button.bind("<Button-1>", j.view)
            j.button.bind("<Button-3>", j.set_flag)
            j.set_around()
    buttons[0][0].button.bind("<Control-Button-1>", lambda alpha: cheat())

    game_window.resizable(False, False)
    game_window.mainloop()


def bomb_counter(level):
    """присваивание высоты и ширины в зависимости от к-ва бомб и запуск игры"""
    global bombs

    if level == 0:
        bombs = 10
        high = length = 9
    elif level == 1:
        bombs = 40
        high = length = 16
    elif level == 2:
        bombs = 90
        high = 16
        length = 30
    else:
        bombs = 10
        high = length = 9

    menu_window.destroy()

    game(high, length)  # Начинаем игру, передавая кол-во полей


def show_ones_stats(login, window):
    """показывает окно с рейтинго конкретного игрока"""
    def on_back():
        close_windows(stats_user_window)
        show_stats()

    print(login)
    close_windows(window)
    stats_user_window = Tk()
    stats_user_window.title("Minesweeper")
    stats_user_window["bg"] = col_white
    stats_user_window.geometry("600x150+650+0")

    user_stats_text1 = Label(stats_user_window, height=1, text=f"{login} best "f": {data[login][1]}", bg=col_white, font="Bahnschrift 20", fg="gray22")
    user_stats_text2 = Label(stats_user_window, height=1, text=f"last 10 games scores: {str(data[login][2:12])[1:-1]}", bg=col_white, font="Bahnschrift 15", fg="gray22")
    back_button = Button(stats_user_window, text="Back", command=on_back, bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)
    back_button.place(relx=0.5, rely=0.75, anchor="center")
    user_stats_text1.place(relx=0.5, rely=0.2, anchor="center")
    user_stats_text2.place(relx=0.5, rely=0.4, anchor="center")
    stats_user_window.resizable(False, False)
    stats_user_window.mainloop()


class ListButton:
    """класс кнопки списка рейтинга игроков"""
    def __init__(self, login, master, close):
        self.login = login
        self.button = Button(master, text=login, command=lambda: show_ones_stats(login, close), bg=col_white, activebackground=col_white_sub, activeforeground="gray22", font="Bahnschrift 12", relief="flat", fg="gray22")
        if login == user:
            self.button.configure(bg=col_main_sub, fg=col_white, activebackground=col_main, activeforeground=col_white)
        self.button.place(relx=0.15, rely=0.5, anchor="w")


def show_stats():
    """окно списка рейтинга игроков"""
    def on_back():
        close_windows(stats_window)
        menu(user)

    close_windows(menu_window)

    stats_window = Tk()
    stats_window.title("Minesweeper")
    stats_window["bg"] = col_white

    user_text = Label(stats_window, height=1, text="User", bg=col_white, font="Bahnschrift 16", fg="gray22")
    score_text = Label(stats_window, height=1, text="Score", bg=col_white, font="Bahnschrift 16", fg="gray22")
    user_text.place(relx=0.1, y=30, anchor="w")
    score_text.place(relx=0.9, y=30, anchor="e")
    pos = 80
    for login in (sorted(data, key=lambda alpha: int(data[alpha][1])))[::-1]:
        user_frame = Frame(stats_window, height=40, width=260, bg=col_white)
        ListButton(login, user_frame, stats_window)
        user_score_text = Label(user_frame, height=1, text=data[login][1], bg=col_white, font="Bahnschrift 12", fg="gray22")
        if login == user:
            user_frame.configure(bg=col_main_sub)
            user_score_text.configure(bg=col_main_sub, fg=col_white)
        user_frame.place(relx=0.5, y=pos, anchor="center")
        user_score_text.place(relx=0.8, rely=0.5, anchor="e")
        pos += 40

    back_button = Button(stats_window, text="Back", command=on_back, bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)
    back_button.place(relx=0.5, y=pos + 10, anchor="center")

    stats_window.geometry(f"260x{pos + 40}+820+0")
    stats_window.resizable(False, False)
    stats_window.mainloop()


def menu(login):
    """окно меню из которого можно начать игру, выбрать сложжность, открыть окно рейтинга"""
    global user, menu_window
    user = login
    menu_window = Tk()
    menu_window.title("Minesweeper")
    menu_window.geometry("400x200+750+200")
    menu_window["bg"] = col_white

    def on_back():
        close_windows(menu_window)
        sign_in()

    best_score_text = Label(menu_window, height=1, text=f"{user} best: {data[user][1]}", bg=col_white, font="Bahnschrift 25", fg="gray22")
    choose_text = Label(menu_window, height=1, text="Choose difficulty:", bg=col_white, font="Bahnschrift 15", fg="gray22")
    choose_combo = ttk.Combobox(menu_window, values=["Beginner", "Amateur", "Professional"])
    choose_combo.current(0)
    choose_button = Button(menu_window, text="Start", command=lambda: bomb_counter(choose_combo.current()), bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)
    back_button = Button(menu_window, text="Back", command=on_back, bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)
    close_button = Button(menu_window, text="Close", command=lambda: close_windows(menu_window), bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)
    stats_button = Button(menu_window, text="Stats", command=show_stats, bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)

    best_score_text.place(relx=0.5, rely=0.12, anchor="center")
    choose_text.place(relx=0.5, rely=0.32, anchor="center")
    choose_combo.place(relx=0.5, rely=0.47, anchor="center")
    choose_button.place(relx=0.6, rely=0.77, anchor="center")
    back_button.place(relx=0.8, rely=0.77, anchor="center")
    close_button.place(relx=0.2, rely=0.77, anchor="center")
    stats_button.place(relx=0.4, rely=0.77, anchor="center")
    menu_window.resizable(False, False)
    menu_window.mainloop()


def update_data(local_data):
    """сохранение рекорда"""
    # print("update_data")
    # print(local_data)
    with open("data.pkl", "wb") as data_pickle:
        pickle.dump(local_data, data_pickle)


def authenticate(login, password):
    """ф-я добавляет новых пользователей и свяряет пароли с введенными"""
    global data
    if data:
        # print("data")
        if login in data:
            # print("in")
            if password == data[login][0]:
                # print("true password")
                return True
            else:
                # print("false password")
                return False
        else:
            # # print("not in")
            data[login] = [password, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            with open("data.pkl", "wb") as data_pickle:
                pickle.dump(data, data_pickle)
            return True
    else:
        # print("not data")
        data[login] = [password, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        with open("data.pkl", "wb") as data_pickle:
            pickle.dump(data, data_pickle)
        return True


def handle(login, password, window):
    """ф-я обрабатывает введенные данные убирая из них " " ", " ' ", "   " и отправляет их в authenticate()"""
    # print("handle")

    new_login = ""
    for elem in login:
        if elem != " " and elem != "'" and elem != '"':
            new_login += elem

    new_password = ""
    for elem in password:
        if elem != " " and elem != "'" and elem != '"':
            new_password += elem

    if new_login == "" or new_password == "":
        error_text.configure(text="Empty login or password")
    else:
        best_score = authenticate(new_login, new_password)
        if not best_score:
            # print("back_sign_in")
            error_text.configure(text="Invalid password")
        else:
            # print("call_start")
            window.destroy()
            menu(login)


def sign_in():
    """ф-я строит окно аутентификации со всеми кнопками
    при поттержении отправляет введенные данные в handle()"""
    # print("sign_in")
    authenticate_window = Tk()
    authenticate_window.title("Minesweeper")
    authenticate_window.geometry("300x250+800+200")
    authenticate_window["bg"] = col_white

    choose_text = Label(authenticate_window, height=1, text="Sing in or create new account", bg=col_white, font="Bahnschrift 15", fg="gray22")
    enter_login_text = Label(authenticate_window, height=1, text="Enter login:", bg=col_white, font="Bahnschrift 15", fg="gray22")
    input_login = Entry(authenticate_window)
    enter_password_text = Label(authenticate_window, height=1, text="Enter password:", bg=col_white, font="Bahnschrift 15", fg="gray22")
    input_password = Entry(authenticate_window)
    sign_in_button = Button(authenticate_window, text="Log in", command=lambda: handle(input_login.get(), input_password.get(), authenticate_window), bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)
    authenticate_window.bind("<Return>", lambda event: handle(input_login.get(), input_password.get(), authenticate_window))
    authenticate_window.bind("<Escape>", lambda event: handle("1", "1", authenticate_window))
    close_button = Button(authenticate_window, text="Close", command=lambda: close_windows(authenticate_window), bg=col_white_sub, activebackground=col_white_active, font="Bahnschrift 15", relief="flat", fg="gray22", width=6)

    global error_text
    error_text = Label(authenticate_window, height=1, text="", bg=col_white, font="Bahnschrift 15", fg=col_bomb)

    choose_text.place(relx=0.5, rely=0.1, anchor=CENTER)
    enter_login_text.place(relx=0.5, rely=0.25, anchor=CENTER)
    input_login.place(relx=0.5, rely=0.35, anchor=CENTER)
    enter_password_text.place(relx=0.5, rely=0.45, anchor=CENTER)
    input_password.place(relx=0.5, rely=0.55, anchor=CENTER)
    error_text.place(relx=0.5, rely=0.65, anchor=CENTER)
    sign_in_button.place(relx=0.35, rely=0.82, anchor=CENTER)
    close_button.place(relx=0.65, rely=0.82, anchor=CENTER)
    authenticate_window.resizable(False, False)
    authenticate_window.mainloop()


def read_data():
    """открывает данные на компбютере и запускает sign_in()"""
    # print("read data")
    global data
    try:
        with open("data.pkl", "rb") as data_pickle:
            data = pickle.load(data_pickle)
        if not data:
            data = {}
    except FileNotFoundError:
        data = {}
    print(data)
    sign_in()


global data, user, buttons, mines, flags, score, bombs, game_window, menu_window, error_text, c
col_main = "#167C80"
col_main_sub = "#2B888B"
col_main_active = "#0D4A4D"
col_white = "#FAFAFA"
col_white_sub = "#F0F0F0"
col_white_active = "#606060"
col_bomb = "#D0422D"
col_bomb_active = "#7D0017"
col_flag = "#8330B3"
col_flag_active = "#744080"
col_guess = "#CC8A0E"
col_guess_active = "#99670B"

if __name__ == "__main__":
    read_data()
