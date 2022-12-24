###################################################################
###########           软件名称：HELP 你帮我助             #############
###########                作者：赵鹏飞                 #############
###########          施工时间：2022年12月24日            #############
###        软件功能：用户登录与注册、物品的增加、删除查找和显示等          ###
###                   gui实现方法：tkinter库                       ###
###################################################################


import os
import tkinter as tk
import tkinter.messagebox as msgbox


class ItemManager:
#物品操作类，实现对物品的增删查
    def __init__(self):
        items = open('items.txt', 'r')
        itemQuantity = 0
        while True:
            item_lines = items.readline()
            if item_lines:
                itemQuantity += 1
            else:
                break
        self.itemQuantity = itemQuantity
        #读取现有物品数量并保存
        items.close()

    def findItem(self, name: str):
        items = open('items.txt', 'r')
        while True:
            item_lines = items.readline()
            if item_lines:
                item_inf = item_lines.split()
                if item_inf[0] == str:
                    items.close()
                    return ' '.join(item_inf[1:])
            else:
                items.close()
                break

    def addItem(self, name: str, cat: str, other: str):
        #参数分别为物品名称、物品种类和物品其他信息（包含物品属性）
        record = open('items.txt', 'a')
        if os.path.getsize('items.txt') == 0:
            #如果文件为空，那么直接写入。如果文件非空，那么写入的时候要先换行，后续代码许多地方也是如此
            record.write(' '.join([name, cat, other]))
        else:
            record.write('\n' + ' '.join([name, cat, other]))
        record.close()

        self.itemQuantity += 1

    def delItem(self, number: int):
        #参数指的是目标物品在所有物品中的序号
        items = open('items.txt', 'r')
        item_lines = items.readlines()
        del item_lines[number - 1: number]
        items.close()

        self.itemQuantity -= 1

        items = open('items.txt', 'w')
        items.writelines(item_lines)
        items.close()

    def findCatAttr(self, cat: str):
        #可以显示目标类别的所有属性名称，暂没有使用
        cats = open('itemCats.txt', 'r')
        while True:
            cat_lines = cats.readline()
            if cat_lines:
                cat_inf = cat_lines.split()
                if cat_inf[0] == cat:
                    cats.close()
                    return ' '.join(cat_inf[1:])
            else:
                cats.close()
                break
        return "Didn't find target category"


class OriginInterface:
    #初始界面
    def __init__(self):
        self.ori = tk.Tk()
        self.ori.title("HELP")
        self.ori.geometry('500x500')

        tts = tk.StringVar()
        tts.set("Welcome to use software 'HELP'")
        ttl = tk.Label(self.ori, anchor='nw', textvariable=tts, fg='black', font=('TimesNewRoman', 19),
                         justify='center', width=50, height=1)
        ttl.place(x=50, y=90)
        #以此处代码举例，大体意思为在50,90处显示一串字"Welcome to use software 'HELP'"，后续则相似
        #变量名均取英文缩写，“ttl”意为title label，其具体名称并不影响代码整体阅读

        sub_tts = tk.StringVar()
        sub_tts.set("Please login")
        sub_ttl = tk.Label(self.ori, anchor='nw', textvariable=sub_tts, fg='black', font=('TimesNewRoman', 15),
                             justify='center', width=50, height=1)
        sub_ttl.place(x=50, y=140)

        uns = tk.StringVar()
        uns.set("user name:")
        unl = tk.Label(self.ori, anchor='nw', textvariable=uns, fg='black', font=('TimesNewRoman', 12),
                         justify='center', width=50, height=1)
        unl.place(x=50, y=260)

        pws = tk.StringVar()
        pws.set("password:")
        pwl = tk.Label(self.ori, anchor='nw', textvariable=pws, fg='black', font=('TimesNewRoman', 12),
                         justify='center', width=50, height=1)
        pwl.place(x=50, y=320)

        var_usr_name = tk.StringVar()
        self.entry_usr_name = tk.Entry(self.ori, textvariable=var_usr_name)
        self.entry_usr_name.place(x=270, y=260)
        #此处意为放置了一个输入str类型的文字输入框，可以收集输入内容作相应处理

        var_usr_pwd = tk.StringVar()
        self.entry_usr_pwd = tk.Entry(self.ori, textvariable=var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=270, y=320)

        regb = tk.Button(self.ori, text='register', width=10, height=1, command=self.register)
        regb.place(x=260, y=380)
        #此处意为放置了一个“register”按钮，按下就会触发此类中的register函数

        cpb = tk.Button(self.ori, text='login', width=6, height=1, command=self.compare)
        cpb.place(x=370, y=380)

    def mainLoop(self):
        #让界面显示出来并框中数据
        self.ori.mainloop()

    def compare(self) -> None:
        #先对比管理员信息，再对比普通用户信息，看其中是否有和目前登录填写的一样的
        #若id错误，则显示无该id；若id正确密码错误，则显示密码错误
        userName = str(self.entry_usr_name.get())
        passWord = str(self.entry_usr_pwd.get())
        ad_exist = False
        cu_exist = False

        admins = open('admins.txt', 'r')
        commonUs = open('commonUsers.txt', 'r')

        while True:
            ad_lines = admins.readline()
            if ad_lines:
                ad_inf = ad_lines.split()
                if ad_inf[0] == userName:
                    ad_exist = True
                    if ad_inf[1] == passWord:
                        msgbox.showinfo("Success", "Administrator login successfully!")
                        admins.close()
                        self.ori.destroy()
                        aif = AdminInterface()
                        aif.mainLoop()
                        break
                    else:
                        msgbox.showwarning("Warning", "Wrong password, please type in again!")
                        break
            else:
                admins.close()
                break

        if ad_exist == False:
            while True:
                cu_lines = commonUs.readline()
                if cu_lines:
                    cu_inf = cu_lines.split()
                    if cu_inf[0] == userName:
                        cu_exist = True
                        if cu_inf[1] == passWord:
                            msgbox.showinfo("Success", "User login successfully!")
                            commonUs.close()
                            self.ori.destroy()
                            cui = CommonUserInterface()
                            cui.mainLoop()
                            break
                        else:
                            msgbox.showwarning("Warning", "Wrong password, please type in again!")
                            break
                else:
                    commonUs.close()
                    break

        if not ad_exist and not cu_exist:
            msgbox.showwarning("Warning", "User id not existed, please login again or register first.")

    def register(self):
        #转到注册页面
        self.ori.destroy()
        reg = RegisterInterface()
        reg.mainLoop()


class RegisterInterface:
    def __init__(self):
        self.reg = tk.Tk()
        self.reg.title("Common User Register")
        self.reg.geometry('500x400')

        tts = tk.StringVar()
        tts.set("Log on a new user")
        ttl = tk.Label(self.reg, anchor='nw', textvariable=tts, fg='black', font=('TimesNewRoman', 19),
                         justify='center', width=50, height=1)
        ttl.place(x=50, y=50)

        stts = tk.StringVar()
        stts.set("Please type in your name, phone number and address in 'inf' box")
        sttl = tk.Label(self.reg, anchor='nw', textvariable=stts, fg='black', font=('TimesNewRoman', 10),
                       justify='center', width=50, height=1)
        sttl.place(x=50, y=100)

        uns = tk.StringVar()
        uns.set("user name:")
        unl = tk.Label(self.reg, anchor='nw', textvariable=uns, fg='black', font=('TimesNewRoman', 12),
                         justify='center', width=50, height=1)
        unl.place(x=50, y=150)

        pws = tk.StringVar()
        pws.set("password:")
        pwl = tk.Label(self.reg, anchor='nw', textvariable=pws, fg='black', font=('TimesNewRoman', 12),
                         justify='center', width=50, height=1)
        pwl.place(x=50, y=200)

        pis = tk.StringVar()
        pis.set("personal information:")
        pil = tk.Label(self.reg, anchor='nw', textvariable=pis, fg='black', font=('TimesNewRoman', 12),
                       justify='center', width=50, height=1)
        pil.place(x=50, y=250)

        var_usr_name = tk.StringVar()
        self.entry_usr_name = tk.Entry(self.reg, textvariable=var_usr_name)
        self.entry_usr_name.place(x=270, y=150)

        var_usr_pwd = tk.StringVar()
        self.entry_usr_pwd = tk.Entry(self.reg, textvariable=var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=270, y=200)

        var_usr_inf = tk.StringVar()
        self.entry_usr_inf = tk.Entry(self.reg, textvariable=var_usr_inf)
        self.entry_usr_inf.place(x=270, y=250)

        lgb = tk.Button(self.reg, text='log on', width=10, height=1, command=self.log_on)
        lgb.place(x=370, y=310)

    def mainLoop(self):
        self.reg.mainloop()

    def log_on(self):
        #传入游客的注册信息，包含账号密码、姓名电话住址，等待管理员通过
        userName = str(self.entry_usr_name.get())
        passWord = str(self.entry_usr_pwd.get())
        personInf = str(self.entry_usr_inf.get())
        if userName and passWord:
            registers = open('registers.txt', 'a')
            if os.path.getsize('./registers.txt') == 0:
                registers.write(userName + ' ' + passWord + ' ' + personInf)
            else:
                registers.write('\n' + userName + ' ' + passWord + ' ' + personInf)
            registers.close()
            msgbox.showinfo("Success", "Logged on successfully, Please wait for approval.")
            self.reg.destroy()
        elif userName:
            msgbox.showwarning("Warning", "Please type in password!")
        else:
            msgbox.showwarning("Warning", "Please type in username!")


class AdminInterface:
    def __init__(self):
        self.aif = tk.Tk()
        self.aif.title("Administrator")
        self.aif.geometry('500x400')

        tts = tk.StringVar()
        tts.set("Welcome Administrator, what do you need?")
        ttl = tk.Label(self.aif, anchor='nw', textvariable=tts, fg='black', font=('TimesNewRoman', 12),
                       justify='center', width=50, height=1)
        ttl.place(x=100, y=80)

        rab = tk.Button(self.aif, text='registration approval', width=20, height=1, command=self.regApprv)
        rab.place(x=175, y=200)

        veib = tk.Button(self.aif, text='view and exchange items', width=24, height=1, command=self.VEItems)
        veib.place(x=160, y=250)

        acb = tk.Button(self.aif, text='add categories', width=20, height=1, command=self.addCat)
        acb.place(x=175, y=300)

    def mainLoop(self):
        self.aif.mainloop()

    def regApprv(self):
        self.aif.destroy()
        rai = RegApprvInterface()
        rai.mainLoop()

    def VEItems(self):
        self.aif.destroy()
        cui = CommonUserInterface()
        cui.mainLoop()

    def addCat(self):
        self.aif.destroy()
        ica = ItemCatInterface()
        ica.mainLoop()


class RegApprvInterface:
    #供管理员审核注册申请的页面
    def __init__(self):
        reg = open('registers.txt', 'r')

        self.rai = tk.Tk()
        self.rai.title("Registration Approval")
        self.rai.geometry('500x500')

        self.apprv_count = 0
        self.var_list = []
        for i in range(20):
            self.var_list.append(tk.IntVar())
        button_list = []
        while self.apprv_count <= 20:
            rg_lines = reg.readline()
            if rg_lines:
                rg_inf = rg_lines.split()
                text = rg_inf[0] + "      " + rg_inf[1] + "      " + ' '.join(rg_inf[2:])
                button_list.append(tk.Checkbutton(self.rai, text=text, variable=self.var_list[self.apprv_count]))
                self.apprv_count += 1
            else:
                break
        for button in button_list:
            button.pack()

        ab = tk.Button(self.rai, text='approve', width=8, height=1, command=self.approve)
        ab.place(x=400, y=400)

    def mainLoop(self):
        self.rai.mainloop()

    def approve(self):
        apprv_result = []
        for index in range(self.apprv_count):
            apprv_result.append(self.var_list[index].get())
        commonUs = open('commonUsers.txt', 'a')
        register = open('registers.txt', 'r')

        index = 0
        while index < self.apprv_count:
            reg_lines = register.readline()
            if apprv_result[index] == 1:
                reg_inf = reg_lines.split()
                if os.path.getsize('commonUsers.txt') == 0:
                    commonUs.write(' '.join(reg_inf[0: 2]))
                else:
                    commonUs.write('\n' + ' '.join(reg_inf[0: 2]))
            index += 1
        commonUs.close()

        reg_lines = register.readlines()
        for index in range(len(apprv_result)):
            del reg_lines[index: index + 1]
        register.close()

        register = open('registers.txt', 'w')
        register.writelines(reg_lines)
        register.close()

        msgbox.showinfo("Success", "Approve successfully.")
        self.rai.destroy()
        aif = AdminInterface()
        aif.mainLoop()


class ItemCatInterface:
    #供管理员添加/修改物品类别的界面
    def __init__(self):
        self.ica = tk.Tk()
        self.ica.title("Add&Alt Categories")
        self.ica.geometry('500x400')

        tts = tk.StringVar()
        tts.set("Please type in a new category or a category you want to alter:")
        ttl = tk.Label(self.ica, anchor='nw', textvariable=tts, fg='black', font=('TimesNewRoman', 12),
                       justify='center', width=50, height=1)
        ttl.place(x=30, y=50)

        cat_name = tk.StringVar()
        self.entry_cat_name = tk.Entry(self.ica, textvariable=cat_name, width=10)
        self.entry_cat_name.place(x=80, y=180)

        cat_attr = tk.StringVar()
        self.entry_cat_attr = tk.Entry(self.ica, textvariable=cat_attr, width=20)
        self.entry_cat_attr.place(x=250, y=180)

        ab = tk.Button(self.ica, text='add category', width=15, height=1, command=self.add_cat)
        ab.place(x=320, y=240)

        rb = tk.Button(self.ica, text='return', width=10, height=1, command=self.exit)
        rb.place(x=320, y=310)

    def mainLoop(self):
        self.ica.mainloop()

    def add_cat(self):
        catName = str(self.entry_cat_name.get())
        catAttr = str(self.entry_cat_attr.get())

        cats = open('itemCats.txt', 'r')
        count = 0
        while True:
            cat_lines = cats.readline()
            if cat_lines:
                cat_inf = cat_lines.split()
                if cat_inf[0] == catName:
                    cat_lines_tmp = cats.readlines()
                    del cat_lines_tmp[count: count + 1]
                    #如果输入的类别已有，那么视为更新，先删除原有类别
                    cats.close()
                    cats = open('itemCats.txt', 'a')
                    cats.writelines(cat_lines_tmp)
                    break
                count += 1
            else:
                break
        cats.close()

        cats = open('itemCats.txt', 'a')
        if os.path.getsize('itemCats.txt') == 0:
            cats.write(' '.join([catName, catAttr]))
            #添加新类别和拥有的属性
        else:
            cats.write('\n' + ' '.join([catName, catAttr]))
        cats.close()

        msgbox.showinfo("Success", "Add or alter category successfully")
        self.ica.destroy()
        aif = AdminInterface()
        aif.mainLoop()

    def exit(self):
        self.ica.destroy()
        aif = AdminInterface()
        aif.mainLoop()

class CommonUserInterface:
    #管理员选择了查看或变更物品信息、普通用户登陆成功都会跳转到这个页面
    def __init__(self):
        self.agent = ItemManager()
        self.cui = tk.Tk()
        self.cui.title('HELP')
        self.cui.geometry('500x500')

        tts1 = tk.StringVar()
        tts1.set("You can select a category")
        ttl1 = tk.Label(self.cui, anchor='nw', textvariable=tts1, fg='black', font=('TimesNewRoman', 16),
                       justify='center', width=50, height=1)
        ttl1.place(x=50, y=90)

        tts2 = tk.StringVar()
        tts2.set("to get more information")
        ttl2 = tk.Label(self.cui, anchor='nw', textvariable=tts2, fg='black', font=('TimesNewRoman', 16),
                       justify='center', width=50, height=1)
        ttl2.place(x=80, y=120)

        tts3 = tk.StringVar()
        tts3.set("Or just view all items or categories")
        ttl3 = tk.Label(self.cui, anchor='nw', textvariable=tts3, fg='black', font=('TimesNewRoman', 16),
                       justify='center', width=50, height=1)
        ttl3.place(x=50, y=150)

        scs = tk.StringVar()
        scs.set("select a category:")
        scl = tk.Label(self.cui, anchor='nw', textvariable=scs, fg='black', font=('TimesNewRoman', 12),
                       justify='center', width=50, height=1)
        scl.place(x=50, y=300)

        cat_name = tk.StringVar()
        self.entry_cat_name = tk.Entry(self.cui, textvariable=cat_name, width=10)
        self.entry_cat_name.place(x=200, y=300)

        sb = tk.Button(self.cui, text='select', width=7, height=1, command=self.select)
        sb.place(x=350, y=300)

        vib = tk.Button(self.cui, text='view items', width=10, height=1, command=self.view)
        vib.place(x=150, y=400)

        vcb = tk.Button(self.cui, text='view categories', width=15, height=1, command=self.viewCat)
        vcb.place(x=300, y=400)

    def mainLoop(self):
        self.cui.mainloop()

    def select(self):
        #需要先选择一个物品类别
        catName = self.entry_cat_name.get()
        cat_exist = False
        cats = open('itemCats.txt', 'r')
        while True:
            cat_lines = cats.readline()
            if cat_lines:
                cat_inf = cat_lines.split()
                if cat_inf[0] == catName:
                    cat_exist = True
                    cats.close()
                    self.cui.destroy()
                    ioi = ItemOprInterface(catName)
                    ioi.mainLoop()
                    break
            else:
                cats.close()
                break
        if cat_exist == False:
            msgbox.showwarning("Warning", "No such category existed.")

    def view(self):
        #查看所有物品
        ivi = ItemViewInterface()
        ivi.mainLoop()

    def viewCat(self):
        #查看所有物品类别
        cvi = CatViewInterface()
        cvi.mainLoop()


class ItemOprInterface():
    def __init__(self, cat: str):
        self.agent = ItemManager()
        self.cat = cat
        self.ioi = tk.Tk()
        self.ioi.title('Items operate')
        self.ioi.geometry('600x500')

        tts = tk.StringVar()
        tts.set("What do you need?")
        ttl = tk.Label(self.ioi, anchor='nw', textvariable=tts, fg='black', font=('TimesNewRoman', 19),
                       justify='center', width=50, height=1)
        ttl.place(x=40, y=50)

        stts1 = tk.StringVar()
        stts1.set("If you are adding, please type in attributes and your personal information")
        sttl1 = tk.Label(self.ioi, anchor='nw', textvariable=stts1, fg='black', font=('TimesNewRoman', 10),
                       justify='center', width=55, height=1)
        sttl1.place(x=40, y=120)

        stts2 = tk.StringVar()
        stts2.set("Your personal information includes name, phone number,")
        sttl2 = tk.Label(self.ioi, anchor='nw', textvariable=stts2, fg='black', font=('TimesNewRoman', 10),
                        justify='center', width=50, height=1)
        sttl2.place(x=40, y=160)

        stts3 = tk.StringVar()
        stts3.set("address and description of item")
        sttl3 = tk.Label(self.ioi, anchor='nw', textvariable=stts3, fg='black', font=('TimesNewRoman', 10),
                         justify='center', width=50, height=1)
        sttl3.place(x=55, y=200)

        ais = tk.StringVar()
        ais.set("add an item:")
        ail = tk.Label(self.ioi, anchor='nw', textvariable=ais, fg='black', font=('TimesNewRoman', 12),
                       justify='center', width=50, height=1)
        ail.place(x=50, y=250)

        add_item_name = tk.StringVar()
        self.entry_add_item_name = tk.Entry(self.ioi, textvariable=add_item_name, width=10)
        self.entry_add_item_name.place(x=200, y=250)

        add_item_inf = tk.StringVar()
        self.entry_add_item_inf = tk.Entry(self.ioi, textvariable=add_item_inf, width=20)
        self.entry_add_item_inf.place(x=300, y=250)

        ab = tk.Button(self.ioi, text='add', width=7, height=1, command=self.add_item)
        ab.place(x=500, y=250)

        dis = tk.StringVar()
        dis.set("delete an item:")
        dil = tk.Label(self.ioi, anchor='nw', textvariable=dis, fg='black', font=('TimesNewRoman', 12),
                       justify='center', width=50, height=1)
        dil.place(x=50, y=300)

        del_item_index = tk.StringVar()
        self.entry_del_item_index = tk.Entry(self.ioi, textvariable=del_item_index, width=10)
        self.entry_del_item_index.place(x=250, y=300)

        db = tk.Button(self.ioi, text='delete', width=7, height=1, command=self.del_item)
        db.place(x=500, y=300)

        sis = tk.StringVar()
        sis.set("search for an item:")
        sil = tk.Label(self.ioi, anchor='nw', textvariable=sis, fg='black', font=('TimesNewRoman', 12),
                       justify='center', width=50, height=1)
        sil.place(x=50, y=350)

        ser_item_name = tk.StringVar()
        self.entry_ser_item_name = tk.Entry(self.ioi, textvariable=ser_item_name, width=10)
        self.entry_ser_item_name.place(x=250, y=350)

        sb = tk.Button(self.ioi, text='search', width=7, height=1, command=self.find_item)
        sb.place(x=500, y=350)

        rb = tk.Button(self.ioi, text='return', width=7, height=1, command=self.exit)
        rb.place(x=460, y=420)

    def mainLoop(self):
        self.ioi.mainloop()

    def add_item(self):
        itemName = self.entry_add_item_name.get()
        itemCat = self.cat
        itemInf = self.entry_add_item_inf.get()
        self.agent.addItem(itemName, itemCat, itemInf)
        msgbox.showinfo("Success", "Item added successfully.")

    def del_item(self):
        itemIndex = self.entry_del_item_index.get()
        self.agent.delItem(int(itemIndex))
        msgbox.showinfo("Success", "Item deleted successfully.")

    def find_item(self):
        itemName = self.entry_ser_item_name.get()
        isi = ItemSerInterface(self.cat, itemName)
        isi.mainLoop()

    def exit(self):
        self.ioi.destroy()
        cui = CommonUserInterface()
        cui.mainLoop()


class ItemSerInterface:
    #如果在物品操作页面选择了查找物品，那么会跳出来这个带有滑动条的页面，显示查到的物品信息
    def __init__(self, cat: str, itemName: str):
        self.isi = tk.Tk()
        self.isi.title('Item Found')
        self.isi.geometry('500x500')

        scrollbar = tk.Scrollbar(self.isi)
        scrollbar.pack(side='right', fill='y')
        text = tk.Text(self.isi, width=40, height=40)
        text.config(yscrollcommand=scrollbar.set)
        text.pack(expand=1, fill='both')

        items = open('items.txt', 'r')
        count = 0
        while True:
            item_lines = items.readline()
            if item_lines:
                item_inf = item_lines.split()
                if item_inf[0] == itemName and item_inf[1] == cat:
                    text.insert('end', item_lines)
                    count += 1
            else:
                items.close()
                break
        if count == 0:
            text.insert('end', "No such item found")

    def mainLoop(self):
        self.isi.mainloop()

class ItemViewInterface:
    #如果在普通用户界面选择了查看物品，那么会跳出来这个带有滑动条的页面，显示所有物品信息
    def __init__(self):
        self.ivi = tk.Tk()
        self.ivi.title('Items')
        self.ivi.geometry('500x500')

        scrollbar = tk.Scrollbar(self.ivi)
        scrollbar.pack(side='right', fill='y')
        text = tk.Text(self.ivi, width=40, height=40)
        text.config(yscrollcommand=scrollbar.set)
        text.pack(expand=1, fill='both')

        items = open('items.txt', 'r')
        item_lines = items.readlines()
        index = 0
        for line in item_lines:
            text.insert('end', str(index + 1) + ' ')
            text.insert('end', line)
            text.insert('end', '\n')
            index += 1
        scrollbar.config(command='cb')

    def mainLoop(self):
        self.ivi.mainloop()


class CatViewInterface:
    #如果在普通用户界面选择了查看物品类别，那么会跳出来这个带有滑动条的页面，显示所有物品类别和属性信息
    def __init__(self):
        self.cvi = tk.Tk()
        self.cvi.title('Categories')
        self.cvi.geometry('500x500')

        scrollbar = tk.Scrollbar(self.cvi)
        scrollbar.pack(side='right', fill='y')
        text = tk.Text(self.cvi, width=40, height=40)
        text.config(yscrollcommand=scrollbar.set)
        text.pack(expand=1, fill='both')

        cats = open('itemCats.txt', 'r')
        cat_lines = cats.readlines()
        index = 0
        for line in cat_lines:
            text.insert('end', line)
            text.insert('end', '\n')
            index += 1
        scrollbar.config(command='cb')

    def mainLoop(self):
        self.cvi.mainloop()
