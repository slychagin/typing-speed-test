import csv
import os
import random
import sys
from tkinter import *
from tkinter import ttk, Text

# CONSTANTS
OLIVE = '#DFE8CC'
LIGHT_GREEN = '#F6FBF4'
MARK_TEXT = '#C7F2A4'
FONT_NAME = "Courier"
entered_words = []
data_words = []
proper_words = 0
error_words = 0
word = 1
type_timer = 60
timer = ''


def set_text(*args, file):
    """
    Read data file, shuffle words and load first 200 words to UI
    :param args:
    :param file:
    :return: 200 shuffled words
    """
    global data_words
    with open(file, encoding="utf-8") as data_file:
        data = csv.reader(data_file)
        data_words = [''.join(row).strip() for row in data]
        random.shuffle(data_words)
        text = '\n'.join(data_words[:200]).strip().lower()
        return text


def rus_dict(*args):
    """
    Change dictionary on russian
    :param args:
    :return:
    """
    # Set 1000 russian common words
    set_text(file='rus_words.csv')
    text_field['state'] = 'normal'
    text_field.delete('1.0', 'end')
    text_field.insert('1.0', set_text(file='rus_words.csv'))
    text_field.tag_add('mark_text', '1.0 wordstart', '1.0 wordend')
    text_field.tag_configure('mark_text', background=MARK_TEXT)
    text_field['state'] = 'disabled'

    # Translate UI
    lang_label.configure(text='Словарь:')
    timer_label.configure(text='Время:')
    proper_words_label.configure(text='Верные слова:')
    error_words_label.configure(text='Ошибки:')
    restart_button.configure(text='Сброс')
    confirm_label.configure(text='Нажимайте ПРОБЕЛ для подтверждения слова')
    text_entry.config(state='normal')
    text_entry.delete('0', 'end')
    text_entry.insert('0', 'Для начала нажмите ВВОД')
    text_entry.config(state='disabled')


def confirm_words(*args):
    """
    Add confirmed words to proper or error words, highlight text
    :param args:
    :return:
    """
    global word
    global proper_words
    global error_words

    entered_words.append(text_entry.get().strip())

    if entered_words.pop() in data_words:
        proper_words += 1
        canvas.itemconfig(words_points, text=f'{proper_words}')
    else:
        error_words += 1
        canvas.itemconfig(errors_points, text=f'{error_words}')

    text_entry.delete('0', 'end')
    word += 1

    text_field.tag_add('demark_text', f'{word - 1}.0 wordstart', f'{word - 1}.0 wordend')
    text_field.tag_configure('demark_text', background=LIGHT_GREEN)
    text_field.tag_add('mark_text', f'{word}.0 wordstart', f'{word}.0 wordend')
    text_field.tag_configure('mark_text', background=MARK_TEXT)

    if word % 7 == 0:
        text_field.see(f'{word + 4}.0')


def count_down(count):
    """
    Starts a timer
    :param count:
    :return:
    """
    global timer
    global entered_words
    lang_label_text = lang_label['text']
    text_entry.bind('<Return>', lambda e: 'break')
    rus_button.configure(state='disabled')
    uk_button.configure(state='disabled')

    text_entry.configure(state='enabled')
    text_entry.focus()
    timer = mainframe.after(1000, count_down, count - 1)

    if count >= 10:
        canvas.itemconfig(timer_text, text=f'{count}')
    elif 0 < count < 10:
        canvas.itemconfig(timer_text, text=f'0{count}', fill='red')
    else:
        mainframe.after_cancel(timer)
        canvas.itemconfig(timer_text, text='0')

        text_field.destroy()
        text_entry.destroy()
        confirm_label.destroy()
        timer_label.destroy()
        uk_button.destroy()
        rus_button.destroy()
        lang_label.destroy()
        canvas.itemconfig(errors_points, text='')
        canvas.itemconfig(words_points, text='')

        proper_words_label.destroy()
        error_words_label.destroy()
        canvas.itemconfigure(timer_text, text='')

        if lang_label_text == 'Dictionary:':
            points = ttk.Label(mainframe, text=f'Congratulations!\n\nYour speed {proper_words} words/min!',
                               foreground='#3D8361', background=OLIVE, justify='center', font=(FONT_NAME, 25, 'bold'))
        else:
            points = ttk.Label(mainframe, text=f'Поздравляем!\n\nВаша скорость {proper_words} слов/мин!',
                               foreground='#3D8361', background=OLIVE, justify='center', font=(FONT_NAME, 25, 'bold'))
            restart_button.configure(text='Еще раз!')

        points.grid(column=0, row=0, sticky='N', pady=100, padx=(50, 0))
        restart_button.grid(column=0, row=1, sticky='WSE', pady=30, padx=(165, 140))


def restart():
    refresh = sys.executable
    os.execl(refresh, refresh, *sys.argv)


# GUI
root = Tk()
root.title('Type speed test')
root.resizable(False, False)

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky='NWSE')

# CANVAS
canvas = Canvas(mainframe, width=600, height=650, bg=OLIVE, highlightthickness=0)
timer_text = canvas.create_text(510, 77, text='60', font=(FONT_NAME, 30, 'bold'), fill='#3D8361')
words_points = canvas.create_text(280, 79, text='0', font=(FONT_NAME, 25, 'bold'), fill='#3D8361')
errors_points = canvas.create_text(185, 118, text='0', font=(FONT_NAME, 25, 'bold'), fill='#CC3636')
canvas.grid(column=0, row=0, columnspan=4, rowspan=6)

# LABELS
timer_label = ttk.Label(mainframe, text='Timer:', foreground='#3D8361', background=OLIVE, font=(FONT_NAME, 25, 'bold'))
timer_label.grid(column=2, row=1, sticky='WN', columnspan=2, pady=(15, 0))
proper_words_label = ttk.Label(mainframe, text='Proper words:', foreground='#3D8361', background=OLIVE,
                               font=(FONT_NAME, 20, 'bold'))
proper_words_label.grid(column=0, row=1, padx=(50, 0), pady=(20, 0), sticky='WN')
error_words_label = ttk.Label(mainframe, text='Errors:', foreground='#CC3636', background=OLIVE,
                              font=(FONT_NAME, 20, 'bold'))
error_words_label.grid(column=0, row=2, sticky='WN', padx=(50, 0))
confirm_label = ttk.Label(mainframe, text='Press space to confirm the word', foreground='grey', background=OLIVE,
                          font=(FONT_NAME, 17))
confirm_label.grid(column=0, row=5, columnspan=4, pady=(20, 30))
lang_label = ttk.Label(mainframe, text='Dictionary:', foreground='grey', background=OLIVE, font=(FONT_NAME, 17))
lang_label.grid(column=0, row=0, columnspan=2, sticky='E')

# TEXT FIELD
text_field = Text(mainframe, width=22, height=7, background=LIGHT_GREEN, font=(FONT_NAME, 25), wrap='word', padx=20, pady=30)
text_field.insert('1.0', set_text(file='uk_words.csv'))
text_field.tag_add('mark_text', '1.0 wordstart', '1.0 wordend')
text_field.tag_configure('mark_text', background=MARK_TEXT)
text_field['state'] = 'disabled'
text_field.grid(column=0, row=3, columnspan=4, pady=(30, 10))

# ENTRY FIELD
text_entry = ttk.Entry(mainframe, width=24, background=LIGHT_GREEN, font=(FONT_NAME, 25), justify='center')
text_entry.insert('0', 'Press ENTER to start')
text_entry.config(state='disabled')
text_entry.bind('<FocusIn>', lambda args: text_entry.delete('0', 'end'))
text_entry.bind('<space>', confirm_words)
text_entry.grid(column=0, row=4, columnspan=4, pady=(20, 10))

# START TIMER
root.bind('<Return>', (lambda event: count_down(type_timer)))

# BUTTONS
restart_button = ttk.Button(mainframe, text='Restart', command=restart)
restart_button.grid(column=2, row=2, columnspan=2, sticky='WN', padx=(0, 50))

uk_flag = PhotoImage(file='flags_img/uk_flag.png')
uk_button = ttk.Button(mainframe, image=uk_flag, command=restart)
uk_button.grid(column=2, row=0, sticky='EN', pady=(10, 0), padx=(20, 0))

rus_flag = PhotoImage(file='flags_img/rus_flag.png')
rus_button = ttk.Button(mainframe, image=rus_flag, command=rus_dict)
rus_button.grid(column=3, row=0, sticky='WN', pady=(10, 0), padx=(0, 20))

root.mainloop()
