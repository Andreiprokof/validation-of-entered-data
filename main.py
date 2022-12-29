from tkinter import *
from tkinter.ttk import Combobox
import pypyodbc
from tkcalendar import DateEntry

def connecnt_sql():
    db_host = 'degtyarev'   #подключение к бд
    db_name = 'AFOND_DB'
    db_user = 'SA'
    db_password = '1'
    global connection
    connection = pypyodbc.connect('Driver=SQL Server;Server='+ db_host + ';Database=' \
                                  + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';')
def request_users():
    cursor = connection.cursor()
    mySQLQuery = ("SELECT SURNAME_PATRON FROM dbo.USER_CL WHERE \
                SURNAME_PATRON='Прокофьев Андрей Александрович' or \
                SURNAME_PATRON='Гладченко И.Ю.' or \
                SURNAME_PATRON='Мартынюк Светлана Сергеевна'")  #запрос на вывод пользователей БД АХ
    cursor.execute(mySQLQuery)
    results_name_users = cursor.fetchall()
    return results_name_users
    cursor.close()
def read_date():
    date_starting = cal1.get_date()
    date_end = cal2.get_date()
    users = combo.get()[1:-1] # извлечение данных выьранной строки в combo и исключение {] из вывода
    criterion_request = combo1.get()
    txt.replace("1.0", END, request(users, date_starting, date_end,criterion_request)) #вызов функции для финального результата,передача на вывыод
def request(users, date_starting, date_end,criterion_request):
    if users == 'Прокофьев Андрей Александрович': #преобразуем выбранные имена пользователей бд в код для бд.
        number_user = 378235
    elif users =='Мартынюк Светлана Сергеевна':
        number_user = 432524
    elif users =='Гладченко И.Ю.':
        number_user = 111830
    elif users =='Все':
        number_user,number_user1,number_user2, = 378235, 111830, 111830
    if criterion_request == 'Единицы хранения': # проверка характера запроса и формирования критерия для него
        criterion1, criterion2, criterion3 = 'U', 'I', 'I'
    elif criterion_request == 'Описи':
        criterion1, criterion2, criterion3 = 'O', 'I', 'I'
    elif criterion_request == 'Фонды':
        criterion1, criterion2, criterion3 = 'F', 'I', 'I'
    date_s, date_e = date_starting.isoformat().split('-'), date_end.isoformat().split('-') #смена позиций переменных для корректной передачи в SQL
    date_s[1], date_s[2] = date_s[2], date_s[1]
    date_e[1], date_e[2] = date_e[2], date_e[1]
    date_e, date_s = '-'.join(date_e), '-'.join(date_s) #перевод в текстовую строку с разделителем
    cursor1 = connection.cursor()
    mySQLQuery_final = f"""SELECT * FROM AFOND_DB .dbo.PROT \
                WHERE "Table_id"='{criterion1}' AND "Oper_id"='{criterion2}' AND "Suboper_id"='{criterion3}' \
                AND "User_isn"={number_user} AND "Time_stamp" >= '{date_s} 00:00:00' AND "Time_stamp" <='{date_e} 00:00:00';  """  # формирования запроса
    cursor1.execute(mySQLQuery_final)
    result_request = cursor1.fetchall()
    return len(result_request) #вывод количества записей
    cursor1.close()
window = Tk()
window.title("Приложение по просмотру введенных данных в АХ-4")
lbl = Label(window, text="Форма для проверки введеных данных в архивный фонд", font=("times new roman", 14), command=connecnt_sql())
lbl.grid(column=0, row=0)
lbl.place(x=0.2, y=4)
window.geometry('700x700')  #размер окна
txt1 = Label(window, text="Выберите дату запроса от", font=("times new roman", 12))
txt1.grid(column=0, row=0)
txt1.place(x=0.2, y=260)
txt = Text(window, font=("times new roman", 28), width=15, height=4) # вывод данных из запроса
txt.grid(column=0, row=1)
txt.place(x=10, y=50)
txt2 = Label(window, text="до", font=("times new roman", 12))
txt2.grid(column=0, row=0)
txt2.place(x=280, y=260)
combo = Combobox(window, width=35, height=10)
combo['values'] = request_users() #вывод полученного резултата из запроса
combo.grid(column=0, row=0)
combo.place(x=400,y=60.5)
combo.current(1) #По умолчанию выбирается первый элимент
combo1 = Combobox(window, width=35, height=10)
combo1['values'] = 'Фонды', 'Единицы хранения', 'Описи' #вывод полученного резултата из запроса
combo1.grid(column=0, row=0)
combo1.place(x=2,y=310)
combo1.current(1) #По умолчанию выбирается первый элимент
cal1 = DateEntry(window, width=12, year=2022, month=1, day=1, background='darkblue', foreground='white', borderwidth=2) #вызов календаря и выбор даты
cal1.pack(padx=10, pady=10)
cal1.place(x=185, y=264)
cal2 = DateEntry(window, width=12, year=2022, month=1, day=1, background='darkblue', foreground='white', borderwidth=2)
cal2.pack(padx=10, pady=10)
cal2.place(x=300, y=264)
but1=Button(window,text='Выполнить',command=read_date).place(x=240,y=350)
window.mainloop()

