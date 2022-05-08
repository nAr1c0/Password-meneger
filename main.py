import tkinter as tk
import base64
import json
import os

class Passw_meng():
    salt = os.urandom(32).hex()
    app = tk.Tk()
    app.title("Менджер паролей")
    app["bg"] = "grey80"
    app.resizable(width=False, height=False) 
    pasws = []
    f_top = tk.Frame(app, bg="grey80")
    f_top.pack()
    f_bot = tk.Frame(app, bg="grey80")
    f_bot.pack()

###################################################################################

    def cr_data(self):
        self.main_lb = tk.Listbox(self.f_top)
        self.show_data_bt = tk.Button(self.f_bot, text="Показать данные", command=self.show_data)
        self.del_bt = tk.Button(self.f_bot, text = "Удалить", command=self.delete)
        file = open("passwords.json", "r")
        data = json.load(file)
        for item in data:
            self.pasws.append(item['name'])
        for i in self.pasws:
            self.main_lb.insert(tk.END, i)
        self.pasws.clear()
        self.main_lb.pack(side=tk.LEFT)
        self.show_data_bt.pack(side=tk.LEFT)
        self.del_bt.pack(side=tk.LEFT)
    
    def cr_show_data(self):
        self.log_lb = tk.Label(self.f_top, text = "Логин")
        self.log_ent = tk.Entry(self.f_top)
        self.passw_lb = tk.Label(self.f_top, text = "Пароль")
        self.passw_entry = tk.Entry(self.f_top)
        self.show_bt = tk.Button(self.f_top, text = "Показать пароль")
        self.change_bt = tk.Button(self.f_top,text = "Изменить", command=self.change)
        self.show_bt = tk.Button(self.f_top, text = "Отобразить пароль", command=self.show_passw)
        self.del_bt = tk.Button(self.f_top, text = "Удалить", command=self.delete)
        
        self.log_lb.pack(side=tk.TOP)
        self.log_ent.pack(side=tk.TOP)
        self.passw_lb.pack(side=tk.TOP)
        self.passw_entry.pack(side=tk.TOP)
        self.show_bt.pack(side=tk.TOP)
        self.change_bt.pack(side=tk.TOP)
    
    def cr_hand_wr(self):
        self.name_lb = tk.Label(self.f_bot, text = "Название")
        self.name_ent = tk.Entry(self.f_bot)
        self.login_lb = tk.Label(self.f_bot, text = "Логин")
        self.login_ent = tk.Entry(self.f_bot)
        self.passw_label = tk.Label(self.f_bot, text = "Пароль")
        self.passw_ent = tk.Entry(self.f_bot)
        self.make_bt = tk.Button(self.f_bot, text = "Добавить", command=self.new_passw)
        self.make_bt.pack(side=tk.BOTTOM)
        self.passw_ent.pack(side=tk.BOTTOM)
        self.passw_label.pack(side=tk.BOTTOM)
        self.login_ent.pack(side=tk.BOTTOM)
        self.login_lb.pack(side=tk.BOTTOM)
        self.name_ent.pack(side=tk.BOTTOM)
        self.name_lb.pack(side=tk.BOTTOM)
    
 ###########################################################################

    def new_passw(self):
        file = open("passwords.json", "r")
        data = json.load(file)
        name = self.name_ent.get()
        login = self.login_ent.get()
        passw = self.passw_ent.get()
        passw = passw.encode("UTF-8")
        passw = base64.b64encode(passw)
        passw = passw.decode("UTF-8")
        new_passw = {
            "name": f"{name}",
            "login": f"{login}",
            "passw": f"{passw}"
        }
        data.append(new_passw)
        file = open("passwords.json", "w")
        json.dump(data, file)

        file = open("passwords.json", "r")
        data = json.load(file)
        for i in data:
            self.pasws.append(i['name'])

        self.main_lb.insert(tk.END, self.pasws[-1])
        self.pasws.clear()
        self.login_ent.delete(0, tk.END)
        self.name_ent.delete(0, tk.END)
        self.passw_ent.delete(0, tk.END)

    def delete(self):
        a = self.main_lb.get(self.main_lb.curselection())
        self.main_lb.delete(tk.ANCHOR)
        data = json.load(open("passwords.json"))
        for i in range(len(data)):
            if data[i]['name'] == a:
                data.pop(i)
                break
        open("passwords.json", "w").write(json.dumps(data, sort_keys=True, indent=3, separators=(',', ': ')))
    
    def show_data(self):
        self.log_ent.delete(0, tk.END)
        self.passw_entry.delete(0, tk.END)
        self.name = self.main_lb.get(tk.ANCHOR)
        data = json.load(open("passwords.json", "r"))
        for i in range(len(data)):
            if data[i]["name"] == self.name:
                login = data[i]["login"]
                passw = data[i]["passw"]
                passw = passw.encode("UTF-8")
                passw = base64.b64decode(passw)
                passw = passw.decode("UTF-8")
                passw = len(passw)
                self.log_ent.insert(0, login)
                for j in range(passw + 1):
                    self.passw_entry.insert(0, "*")
                break

    def show_passw(self):
        data = json.load(open("passwords.json", "r"))
        for i in range(len(data)):
            if data[i]["name"] == self.name:
                passw = data[i]["passw"]
                passw = passw.encode("UTF-8")
                passw = base64.b64decode(passw)
                passw = passw.decode("UTF-8")
                self.passw_entry.delete(0, tk.END)
                self.passw_entry.insert(0, passw)


    
    def change(self):
        data = json.load(open("passwords.json", "r"))
        for i in range(len(data)):
            if data[i]["name"] == self.name:
                self.main_lb.delete(tk.ANCHOR)
                data.pop(i)
                
                login = self.log_ent.get()
                passw = self.passw_entry.get()
                passw = passw.encode("UTF-8")
                passw = base64.b64encode(passw)
                passw = passw.decode("UTF-8")
                new_passw = {
                    "name": f"{self.name}",
                    "login": f"{login}",
                    "passw": f"{passw}"
                }
                data.append(new_passw)
                file = open("passwords.json", "w")
                json.dump(data, file)

                file = open("passwords.json", "r")
                data = json.load(file)
                for i in data:
                    self.pasws.append(i['name'])

                self.main_lb.insert(tk.END, self.pasws[-1])
                self.pasws.clear()
                self.log_ent.delete(0, tk.END)
                self.passw_entry.delete(0, tk.END)
                break

##############################################################################################

main_app = Passw_meng()
main_app.cr_data()
main_app.cr_show_data()
main_app.cr_hand_wr()

main_app.app.mainloop()
