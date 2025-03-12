from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json
import os
import sys
from PIL import Image, ImageTk

###TODO: add a scroll bar to images added to image frame
###TODO: Adjust the Image display frame to have a max width size before height is reshaped.
###TODO: Scrollbar on directory
###TODO: Add scrollbar to miniset in image frame


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

os.chdir(application_path)

def save_local(tuple, img_name, new_list):
    if tuple != ():
        n = 0
        for img in tuple:
            n += 1
            s = img.split('.')
            fmt = f'{s[-1]}'
            newname = f'{img_name}{n}.{fmt}'
            new_list.append(newname)
            image = Image.open(img)
            image.save(f'{os.getcwd()}\\art\\{newname}')

class Art:
    def __init__(self, master=None, cover=None, name=None, price=None, make=None, sell=None, custname=None, custaddress=None, custemail=None, custphone=None, type=None, images = None, notes=None):

        self.master = master
        self.cover = cover
        self.name = name
        self.price = price
        self.make = make
        self.sell = sell
        self.custname = custname
        self.custaddress = custaddress
        self.custemail = custemail
        self.custphone = custphone
        self.type = type
        self.images = images
        self.notes = notes

    #Load JSONs
        with open('art_directory.json', 'r') as load:
            self.art_dict = json.load(load)

        with open('art_namelist.json', 'r') as load:
            self.art_names = json.load(load)

#Function to set img scale
    def img_scale(self, img_link, size, dict, num):
        self.pic = Image.open(img_link)
        scale = size/self.pic.height
        self.scaleW = int(self.pic.width*scale)
        self.scaleH = size
        self.resized = self.pic.resize((self.scaleW,self.scaleH), Image.Resampling.LANCZOS)
        dict.update({num:ImageTk.PhotoImage(self.resized)})

#Function to pack an instance of Art
    def place(self, num):

        'Place your art onto a frame.\nNUM is used for iterating through globdict\nSCALE is used for image scale for the icons.  Default is 100 pixels.'

    #Mouse Over functions
        def highlight(event):
            highlight_size = pic.resize((int(scaleW*1.1), int(scaleH*1.1)), resample = Image.Resampling.LANCZOS)
            img_dict.update({f'img{num}':ImageTk.PhotoImage(highlight_size)})
            self.label.config(image = img_dict[f'img{num}'])

        def hl_return(event):
            normal_size = pic.resize((scaleW,scaleH), resample=Image.Resampling.LANCZOS)
            img_dict.update({f'img{num}':ImageTk.PhotoImage(normal_size)})
            self.label.config(image = img_dict[f'img{num}'])

    #Variables
        img_dict = {}

    #Define Pic and Scale
        #THIS IS A REPEAT OF IMG_SCALE BECAUSE THE SELF.PIC KEEPS CHANGING EVERY TIME THE FUNC IS CALLED FOR, REPEAT CODE TO KEEP THE COVER IMAGE STATIC UNTIL SAVED
        pic = Image.open(f'{os.getcwd()}\\art\\{self.cover}')
        scale = 100/pic.height
        scaleW = int(pic.width*scale)
        scaleH = 100
        resized = pic.resize((scaleW,scaleH), Image.Resampling.LANCZOS)
        img_dict.update({num:ImageTk.PhotoImage(resized)})
    
    #Pack Images
        self.frame = ttk.Frame(self.master, width = scaleW+20, height = scaleH+40)
        self.frame.pack_propagate(False)
        self.frame.grid(row = num//6, column = num%6, padx = 0, pady = 0, sticky = 'n')

        self.label = ttk.Label(self.frame, image = img_dict[num], text = self.name, compound = 'top', font = ('Gabriola', 12))
        self.label.pack(side = BOTTOM)

    #Bindings
        self.label.bind('<Button-1>', lambda x: self.art_click())
        self.label.bind('<Enter>', highlight)
        self.label.bind('<Leave>', hl_return)


#Function when Art Cover is clicked
    def art_click(self):

    #Func to make large picture
        def big_img(loc):
            self.img_scale(loc, 300, self.big_dict, 0)
            disp_img.config(image = self.big_dict[0])

    #Func to make small picture reel
        def mini_set(loc, num):

            self.img_scale(loc[num], 40, self.mini_imgs, num)

            self.mini_labels.update({num:ttk.Label(self.mini_imgframe, image = self.mini_imgs[num])})
            self.mini_labels[num].pack(side = LEFT)
            self.mini_labels[num].bind('<Button>', lambda x: big_img(loc[num]))
            if len(loc) > num+1:
                mini_set(loc,num+1)

    #Function to Edit Art Info
        def info_edit():
            name.config(state = ACTIVE)
            price.config(state = ACTIVE)
            make.config(state = ACTIVE)
            sell.config(state = ACTIVE)
            custname.config(state = ACTIVE)
            custaddress.config(state = ACTIVE)
            custemail.config(state = ACTIVE)
            custphone.config(state = ACTIVE)
            type.config(state = ACTIVE)
            notes.config(state = NORMAL, background= 'white', relief = 'sunken')
            edit_save.config(text = 'Save', command = lambda: info_save())
            close_cancel.config(text = 'Close Without Saving')
            self.editimg_bt = ttk.Button(img_frame, text = 'Edit Images', command = lambda: img_edit())
            self.editimg_bt.grid(row = 2)

   #Function to edit Art Image Selection
        def img_edit():

        #Pack self.editframe with imgs
            def list_pack(loc, num):

            #Click Image Function/Activate buttons for the selected image
                def select(event):
                    label.config(text = f'{templist[num]}')
                    del_bt.config(state = ACTIVE, command = lambda: delete(num))
                    
            #List Org Func
                def list_setup(fileloclist, filenamelist, add_img):
                    #Create Set and remove Nulls
                    self.tempset = set(templist)
                    if 'null' in self.tempset:
                        self.tempset.remove('null')

                    #Append to Loc List and Name List
                    for img in self.image_locs:
                        fileloclist.append(img)
                    for img in self.tempset:
                        filenamelist.append(img)
                    for img in add_img:
                        x = 'C:'
                        a = img.split('/')
                        for word in a:
                            if word == 'C:':
                                pass
                            else:
                                x = f'{x}\\{word}'
                        fileloclist.append(x)
                        t = img.split('/')
                        filenamelist.append(t[-1])

                    #Save updated Lists to final seat
                    self.image_locs = fileloclist #File Locations
                    self.namelist = tuple(filenamelist)  #Names

            #Remove Null entires from self.image_locs
                def remove_loc_null():
                    list = []
                    for img in self.image_locs:
                        if img == 'null':
                            pass
                        else:
                            list.append(img)
                    self.image_locs = list

            #Add New Images
                def add():
                    #Remove Null from Image_Locs
                    remove_loc_null()

                    #Organize Lists
                    list_setup([],[],filedialog.askopenfilenames(parent = edit_img, filetypes = [('All Files', '*'), ('JPEG', '.jpg'), ('PNG', '.png'), ('Bitmap', '.bmp')]))

                    #Reboot Edit_Img
                    edit_img.destroy()
                    img_edit()

            #Delete Button Func
                def delete(num):
                    #Pop Img Out
                    templist.pop(num)
                    templist.insert(num, 'null')
                    self.image_locs.pop(num)
                    self.image_locs.insert(num, 'null')

                    #Insert Red X
                    self.img_scale(f'{os.getcwd()}\\art\\red_x.png', 75, self.red_x, num)                    
                    label_dict[num].config(image = self.red_x[num])

                    #Organize lists
                    list_setup([],[],[])

                    #Disable Delete Button
                    del_bt.config(state = DISABLED)
                
            #Confirm Images
                def confirm():
                    #Remove Null from Image_Locs
                    remove_loc_null()

                    #Replace Deleted with Red X
                    if self.image_locs == []:
                        self.image_locs.append(f'{os.getcwd()}\\art\\no_img.png')

                    #Rebuild Img_Frame
                    self.mini_imgframe.destroy()
                    self.mini_imgframe = ttk.Frame(img_frame)
                    self.mini_imgframe.grid(row = 1)
                    mini_set(self.image_locs, 0)
                    big_img(self.image_locs[0])
                    edit_img.destroy()
                    
            #Stack the pictures
                #Label Update
                self.img_scale(loc, 75, list_dict, num)
                label_dict.update({num:ttk.Label(self.editframe, image = list_dict[num])})
                label_dict[num].grid(row = num//5, column = num%5, padx = 5, pady = 5)
                label_dict[num].bind('<Button>', select)

                #Button Config
                add_bt.config(state = ACTIVE, command = lambda: add())
                confirm_bt.config(state=NORMAL, command = lambda: confirm())

                #Repeat
                if len(templist) > num+1:
                    list_pack(self.image_locs[num+1], num+1)

        #Top Level and Frames
            edit_img = Toplevel()
            edit_img.minsize(width = 350, height = 150)
            edit_img.title('Edit Image Selection')
            ttk.Label(edit_img, text = 'Select Images', font = ('Gabriola', 16)).pack(pady = 5)
            self.editframe = ttk.Frame(edit_img, relief = 'sunken')
            self.editframe.pack(ipady = 5, fill = X, padx = 10)
            optionframe = ttk.Frame(edit_img, relief= 'sunken', height = 50)
            optionframe.pack(ipady = 5, ipadx = 5, fill = X, anchor = 'center', padx = 10, pady = 10)
            
        #Variables
            list_dict = {}
            label_dict = {}
            self.red_x = {}
            templist = []
            for img in self.image_locs:
                s = img.split('\\')
                templist.append(s[-1])

        #Edittable Label
            label = ttk.Label(optionframe)
            label.place(relx = 0.5, rely = 0.25, anchor = 'center')

        #Buttons
            del_bt = ttk.Button(optionframe, text = 'Delete', state = DISABLED)
            del_bt.place(relx = 0.67, rely = 0.7, anchor = 'center')
            add_bt = ttk.Button(optionframe, text = 'Add Image(s)')
            add_bt.place(relx = 0.33, rely = 0.7, anchor = 'center')
            confirm_bt = ttk.Button(edit_img, text = "Confirm Selection", state = DISABLED)
            confirm_bt.pack(pady = 5)

            list_pack(self.image_locs[0],0)

    #Function to save data to art_directory.json
        def info_save():

        #Function to Delete Image Overhang
            def del_overhang(num):
                list = []
                format = ['png', 'jpg', 'bmp']
                for fmt in format:
                    path = f'{os.getcwd()}\\art\\{self.name}{num}.{fmt}'
                    if os.path.exists(path):
                        list.append(path)
                        del_overhang(num+1)
                check_set = set(list)
                loc_set = set(self.image_locs)
                diff_set = check_set.difference(loc_set)
                for path in diff_set:
                    print(f'REMOVING {path}')
                    os.remove(path)
                    
            #Delete the overhang       
            del_overhang(1)

            #Save new images locally
            self.replacelist = []
            save_local(self.image_locs, self.name, self.replacelist)

            #Save editted information to new dict
            new_dict = {name.get():{}}
            new_dict[name.get()].update({'Name':name.get()})
            new_dict[name.get()].update({'Price':price.get()})
            new_dict[name.get()].update({'Creation Date':make.get()})
            new_dict[name.get()].update({'Sold Date':sell.get()})
            new_dict[name.get()].update({'Customer Name':custname.get()})
            new_dict[name.get()].update({'Customer Address':custaddress.get()})
            new_dict[name.get()].update({'Customer Email':custemail.get()})
            new_dict[name.get()].update({'Customer Phone':custphone.get()})
            new_dict[name.get()].update({'Type':type.get()})
            new_dict[name.get()].update({'Images':self.replacelist})
            new_dict[name.get()].update({'Notes':notes.get('1.0','end')})

            #Save to JSON
            with open('art_directory.json', 'r') as loaded:
                art_dict = json.load(loaded)
                art_dict.pop(self.name)
                art_dict.update(new_dict)
                updated_dict = json.dumps(art_dict, indent = 4)

            with open('art_directory.json', 'w') as loaded:
                loaded.write(updated_dict)


            #Save Name to JSON
            with open('art_namelist.json', 'r') as loaded:
                name_data = json.load(loaded)
                data_set = set(name_data['all_names'])
                data_set.remove(self.name)
                data_set.add(name.get())
                data_list = list(data_set)
                name_data = {'all_names': data_list}
                updated_data = json.dumps(name_data, indent = 4)

            with open('art_namelist.json', 'w') as loaded:
                loaded.write(updated_data)



            #End Editting State
            name.config(state = DISABLED)
            price.config(state = DISABLED)
            make.config(state = DISABLED)
            sell.config(state = DISABLED)
            custname.config(state = DISABLED)
            custaddress.config(state = DISABLED)
            custemail.config(state = DISABLED)
            custphone.config(state = DISABLED)
            type.config(state = DISABLED)
            notes.config(state = DISABLED, background= '#f0f0f0', relief = 'flat')
            edit_save.config(text = 'Edit', command = lambda: info_edit())
            close_cancel.config(text = 'Close Window', command = lambda: art_menu.destroy())

            #Remove Edit Image Button
            self.editimg_bt.destroy()


    #Frames and Toplevel
        art_menu = Toplevel()
        art_menu.title(f'{self.name}') 

        menu_frame = ttk.Frame(art_menu)
        menu_frame.pack()

        img_frame = ttk.Frame(menu_frame)
        img_frame.grid(row = 0, column = 0, rowspan = 9, columnspan = 2)

        button_frame = ttk.Frame(menu_frame)
        button_frame.grid(row = 11, column = 0, columnspan = 4, pady = 10)

    #Image Widgets

        #Variables
        self.mini_imgs = {}
        self.mini_labels = {}
        self.big_dict = {}
        self.namelist = []

        self.image_locs = []
        for img in self.images:
            self.image_locs.append(f'{os.getcwd()}\\art\\{img}')

        #Frames
        display_frame = ttk.Frame(img_frame, width = 550, height = 300)
        display_frame.pack_propagate(False)
        display_frame.grid(row = 0, sticky = 'w')
        self.mini_imgframe = ttk.Frame(img_frame)
        self.mini_imgframe.grid(row = 1)

        #Labels
        disp_img = ttk.Label(display_frame)
        disp_img.pack() 

        #Called Functions
        big_img(self.image_locs[0])
        mini_set(self.image_locs, 0) 
         
    #Labels
        ttk.Label(menu_frame, text = "Name: ").grid(row = 0, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Price: ").grid(row = 1, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Creation Date: ").grid(row = 2, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Sold Date: ").grid(row = 3, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Customer Name: ").grid(row = 4, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Customer Address: ").grid(row = 5, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Customer Email: ").grid(row = 6, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Customer Phone: ").grid(row = 7, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Type: ").grid(row = 8, column = 2, sticky = 'w', padx = 5)
        ttk.Label(menu_frame, text = "Notes: ").grid(row = 9, column = 0, sticky = 'w', padx = 25, pady = 5)

    #Entries

        #Name
        name = ttk.Entry(menu_frame)
        name.insert(0, self.name)
        name.config(state = DISABLED)
        name.grid(row = 0, column = 3, sticky = 'w', padx = 10)

        #Price
        price = ttk.Entry(menu_frame)
        price.insert(0, self.price)
        price.config(state = DISABLED)
        price.grid(row = 1, column = 3, sticky = 'w', padx = 10)
        
        #Make
        make = ttk.Entry(menu_frame)
        make.insert(0, self.make)
        make.config(state = DISABLED)
        make.grid(row = 2, column = 3, sticky = 'w', padx = 10)
        
        #Sell
        sell = ttk.Entry(menu_frame)
        sell.insert(0, self.sell)
        sell.config(state = DISABLED)
        sell.grid(row = 3, column = 3, sticky = 'w', padx = 10)
        
        #Custname
        custname = ttk.Entry(menu_frame)
        custname.insert(0, self.custname)
        custname.config(state = DISABLED)
        custname.grid(row = 4, column = 3, sticky = 'w', padx = 10)
        
        #Custaddress
        custaddress = ttk.Entry(menu_frame, width = 40)
        custaddress.insert(0, self.custaddress)
        custaddress.config(state = DISABLED)
        custaddress.grid(row = 5, column = 3, sticky = 'w', padx = 10)
        
        #Custemail
        custemail = ttk.Entry(menu_frame, width = 30)
        custemail.insert(0, self.custemail)
        custemail.config(state = DISABLED)
        custemail.grid(row = 6, column = 3, sticky = 'w', padx = 10)
        
        #Custphone
        custphone = ttk.Entry(menu_frame)
        custphone.insert(0, self.custphone)
        custphone.config(state = DISABLED)
        custphone.grid(row = 7, column = 3, sticky = 'w', padx = 10)

        #Type
        type = ttk.Combobox(menu_frame, values = ('Painting','Assemblage'),width = 17)
        type.set(self.type)
        type.config(state = DISABLED)
        type.grid(row = 8, column = 3, sticky = 'w', padx = 10)

        #Type
        notes = Text(menu_frame, height = 8, width = 110, wrap = 'word', background = '#f0f0f0', relief = 'flat')
        notes.insert(('1.0'), self.notes)
        notes.config(state = DISABLED)
        notes.grid(row = 10, column = 0, columnspan = 4)

    #Buttons
        edit_save = ttk.Button(button_frame, text = 'Edit', command = lambda: info_edit())
        edit_save.pack(side = LEFT, padx = 5)
        close_cancel = ttk.Button(button_frame, text = 'Close Window', command = lambda: (art_menu.destroy()))
        close_cancel.pack(side = LEFT, padx = 5)









#Application Class
class App:
    def __init__(self, master):
        master.title('Robin Popp Studio Art Directory')
        master.geometry('800x600+100+50')
        master.resizable(False, False)

    #Styles
        self.style = ttk.Style()
        self.style.configure('Art.TLabel', font = ('Gabriola', 12, 'normal'), justify = LEFT, foreground = 'black')
        self.style.configure('Bold.Art.TButton', font = ('Gabriola', 13, 'bold'))
        self.style.configure('Art.TButton', font = ('Gabriola', 12))
        self.style.configure('Art.TCombobox', relief = 'flat')

    #Variables
        art_dict = {}

        top_menu = ttk.Frame(master)
        ttk.Label(top_menu, text = 'Robin Popp Studio Art Directory', style = 'Art.TLabel').pack()
        ttk.Label(top_menu, text = 'Beta Version 0.9.0').pack()

        ttk.Button(top_menu, text = 'Art Entry', command = lambda: enter_art()).pack()
        ttk.Button(top_menu, text = 'Art Directory', command = lambda: build_directory()).pack()

        def make_menu():
            top_menu.pack()

    #Enter New Art Piece Form
        def enter_art():
        #Top Level Window, Frame and Title
            art_entry = Toplevel()
            art_entry.title('Enter a New Painting')
            art_form = ttk.Frame(art_entry, height = 550, width = 450)
            art_form.grid_propagate(False)
            art_form.pack(anchor = CENTER, padx = 10, pady = 5)
            ttk.Label(art_form, text = 'Enter a New Painting', font = ('Gabriola', 16, 'bold')).grid(row = 0, column = 0, columnspan = 4, pady = 5)

        #Variables
            self.imagetuple = ()
            self.imagelist = []

        #Mutable Labels
            art_namelabel = ttk.Label(art_form, text = 'Name*:', style = 'Art.TLabel')
            art_namelabel.grid(row = 1, column = 0, pady = 5, sticky = 'w')
            art_pricelabel = ttk.Label(art_form, text = 'Price*:', style = 'Art.TLabel')
            art_pricelabel.grid(row = 2, column = 0, pady = 5, sticky = 'w')
            art_makelabel = ttk.Label(art_form, text = 'Created*:', style = 'Art.TLabel')
            art_makelabel.grid(row = 3, column = 0, pady= 5, sticky = 'w')

        #Immutable Labels
            ttk.Label(art_form, text = 'Customer Name:', style = 'Art.TLabel').grid(row = 1, column = 2, sticky = 'w')
            ttk.Label(art_form, text = 'Customer Phone:', style = 'Art.TLabel').grid(row = 2, column = 2, sticky = 'w')
            ttk.Label(art_form, text = 'Customer Email:', style = 'Art.TLabel').grid(row = 3, column = 2, sticky = 'w')
            ttk.Label(art_form, text = 'Customer Address:', style = 'Art.TLabel').grid(row = 4, column = 2, sticky = 'w')
            ttk.Label(art_form, text = 'Painting/Assemblage', style = 'Art.TLabel').grid(row = 5, column = 0,columnspan = 2, sticky = 'w')
            ttk.Label(art_form, text = 'Notes:', style = 'Art.TLabel').grid(row = 6, column = 0, sticky = 'w')
        
        #Name and Price Entries
            art_name = ttk.Entry(art_form)
            art_name.grid(row = 1, column = 1, sticky = 'e', padx = 5)
            art_priceframe = ttk.Frame(art_form)
            art_priceframe.grid(row = 2, column = 1, sticky = 'e', padx = 5)
            ttk.Label(art_priceframe, text = '$').pack(side = LEFT)
            art_price = ttk.Entry(art_priceframe)
            art_price.pack(side = LEFT)

        #Make Entries    
            art_make_frame = ttk.Frame(art_form)
            art_make_mon = ttk.Combobox(art_make_frame, width = 2, values = [str(i) for i in range(1,13)], style = 'Art.TCombobox')
            art_make_mon.set('1')
            art_make_mon.pack(side = LEFT)
            art_make_day = ttk.Combobox(art_make_frame, width = 2, values = [str(i) for i in range(1,32)],style = 'Art.TCombobox')
            art_make_day.set('1')
            art_make_day.pack(side = LEFT)
            art_make_year = ttk.Combobox(art_make_frame, width = 4, values = [str(i) for i in range(2000,2100)], style = 'Art.TCombobox')
            art_make_year.set('1900')
            art_make_year.pack(side = LEFT)
            art_make_frame.grid(row = 3, column = 1, sticky = 'e', padx = 5)

        #Sold Entries
            sold = BooleanVar()
            sold.set(False)

            art_soldlabel_frame = ttk.Frame(art_form)
            art_soldlabel_frame.grid(row = 4, column = 0, pady = 5, sticky = 'w')
            art_sell_frame = ttk.Frame(art_form)
            art_sell_frame.grid(row = 4, column = 1, sticky = 'e', padx = 5)

            ttk.Label(art_soldlabel_frame, text = 'Sold?:', style = 'Art.TLabel').pack(side = LEFT)
            art_sell_ck = ttk.Checkbutton(art_soldlabel_frame, variable = sold, onvalue = True, offvalue = False, command = lambda: no_sell())
            art_sell_ck.pack(side = LEFT)
            
            art_sell_mon = ttk.Combobox(art_sell_frame, width = 2, values = [str(i) for i in range(1,13)], style = 'Art.TCombobox', state = 'disabled')
            art_sell_mon.set('1')
            art_sell_mon.pack(side = LEFT)
            art_sell_day = ttk.Combobox(art_sell_frame, width = 2, values = [str(i) for i in range(1,32)],style = 'Art.TCombobox', state = 'disabled')
            art_sell_day.set('1')
            art_sell_day.pack(side = LEFT)
            art_sell_year = ttk.Combobox(art_sell_frame, width = 4, values = [str(i) for i in range(2000,2100)], style = 'Art.TCombobox', state = 'disabled')
            art_sell_year.set('1900')
            art_sell_year.pack(side = LEFT)

        #Sold Button Toggle Function
            def no_sell():
                if sold.get() == False:
                    art_sell_mon.configure(state = 'disabled')
                    art_sell_mon.set('1')
                    art_sell_day.configure(state = 'disabled')
                    art_sell_day.set('1')
                    art_sell_year.configure(state = 'disabled')
                    art_sell_year.set('1900')
                elif sold.get() == True:
                    art_sell_mon.configure(state = 'enabled')
                    art_sell_day.configure(state = 'enabled')
                    art_sell_year.configure(state = 'enabled')

        #Customer Entries
            art_custname = ttk.Entry(art_form)
            art_custname.grid(row = 1, column = 3, sticky = 'e', padx = 5)
            art_custaddress = ttk.Entry(art_form)
            art_custaddress.grid(row = 2, column = 3, sticky = 'e', padx = 5)
            art_custemail = ttk.Entry(art_form)
            art_custemail.grid(row = 3, column = 3, sticky = 'e', padx = 5)
            art_custphone = ttk.Entry(art_form)
            art_custphone.grid(row = 4, column = 3, sticky = 'e', padx = 5)

        #Painting or Assemblage Choice
            art_type = ttk.Combobox(art_form, width = 12, values = ('Painting', 'Assemblage', 'Both', 'Other'), state = 'readonly')
            art_type.set('Painting')
            art_type.grid(row = 5, column = 2)

        #Notes Text Block
            art_notes = Text(art_form, width = 52, height = 8, wrap = 'word')
            art_notes.place(relx = 0.5, rely = 0.525, anchor = 'n')


        #Image Selection Widget
            def make_imgframe():
                self.art_img_frame = Frame(art_form, width = 450, height = 30, relief = 'sunken', background = '#EBE3C5', border= 1)
                self.art_img_frame.pack_propagate(False)
                self.art_img_frame.place(relx = 0.5, rely = 0.91, anchor = 's')
            
            make_imgframe()

            ttk.Label(art_form, text = 'Select Images', style = 'Art.TLabel').place(relx = 0.1, rely = 0.79, anchor = 'n')
            ttk.Label(art_form, text = '(maximum of 5):', font = ('Gabriola', 12, 'italic'), foreground = 'red').place(relx = 0.277, rely = 0.79, anchor = 'n')
            ttk.Button(art_form, text = 'Browse', command = lambda: open_image()).place(relx = 0.85, rely = 0.8, anchor = 'n')

        #Image Selection Function
            def open_image():
                self.art_img_frame.destroy()
                make_imgframe()
                
                self.imagetuple = filedialog.askopenfilenames(parent = art_entry, filetypes= [('All Files', '*'), ('JPEG','.jpg'), ('PNG','.png'), ('Bitmap','.bmp')])

                length = len(self.imagetuple)

            #Function to place the image names
                def image_place(x):
                    s = self.imagetuple[x].split('/')
                    ttk.Label(self.art_img_frame, text = s[-1], style = 'TButton', background = '#EBE3C5').pack(side = LEFT)

                    if length > x+1:
                        image_place(x+1)
                    else:
                        pass
            
            #Defines image number limits
                if length == 0:
                    pass

                if 0 < length:
                    image_place(0)

        #Submit Label
            ttk.Button(art_form, text = 'Submit', style = 'Bold.Art.TButton', command = lambda: submit_art(art_name)).place(relx = 0.5, rely = 0.95, anchor = 'center')

        #Submit Function
            def submit_art(name):

                price = art_price.get()
                if price[0] == '$':
                    price = price[1:]

            #Consolidates dates 
                make_date = f'{art_make_mon.get()}/{art_make_day.get()}/{art_make_year.get()}'
                sell_date = f'{art_sell_mon.get()}/{art_sell_day.get()}/{art_sell_year.get()}'

            #Submission Requirements
                if art_name.get() and art_price.get() and make_date != '1/1/1900':
                    
                #Iterate through imagetuple and save images locally
                    save_local(self.imagetuple, name.get(), self.imagelist)

                #Mark if not art has no sell date
                    if sell_date == '1/1/1900':
                        sell_date = 'Not Sold Yet'

                    if self.imagelist == []:
                        self.imagelist = ['no_img.png']

                #Populat Art_Dict
                    art_dict.update(
                        {name.get(): {
                            'Name':name.get(),
                            'Price':price,
                            'Creation Date':make_date,
                            'Sold Date':sell_date,
                            'Customer Name':art_custname.get(),
                            'Customer Address':art_custaddress.get(),
                            'Customer Email':art_custemail.get(),
                            'Customer Phone':art_custphone.get(),
                            'Type':art_type.get(),
                            'Images':self.imagelist,
                            'Notes':art_notes.get('1.0',END)
                            }
                        })

                #Update Art JSON
                    with open('art_directory.json', 'r') as art_data:
                        loaded_dict = json.load(art_data)
                        loaded_dict.update(art_dict)
                        new_art_data = json.dumps(loaded_dict, indent = 4)

                    with open('art_directory.json', 'w') as art_data:
                        art_data.write(new_art_data)

                #Update Names JSON
                    with open('art_namelist.json', 'r') as name_data:
                        loaded_names = json.load(name_data)
                        if name.get() not in loaded_names["all_names"]:
                            loaded_names["all_names"].append(name.get())
                        else:
                            pass
                        json_names = json.dumps(loaded_names, indent = 4)

                    with open('art_namelist.json', 'w') as name_data:
                        name_data.write(json_names)

                    messagebox.showinfo(parent = art_entry, title = 'New Art Added', message = f'{name.get()} has been added to the directory!')
                        
                    art_entry.destroy()


            #Gatekeep if not all parameters are fulfilled for submission
                else:
                    ttk.Label(art_form, text = 'Fields marked with (*) are required', foreground = 'red').place(relx = 0.5, rely = 0.09, anchor = 'center')

                    if art_name.get():
                        art_namelabel.config(foreground = 'black', font = ('Gabriola', 12,'normal'))
                    else:
                        art_namelabel.config(foreground = 'red', font = ('Gabriola', 12,'bold'))

                    if art_price.get():
                        art_pricelabel.config(foreground = 'black', font = ('Gabriola', 12,'normal'))
                    else:
                        art_pricelabel.config(foreground = 'red', font = ('Gabriola', 12,'bold'))

                    if make_date == '1/1/1900':
                        art_makelabel.config(foreground = 'red', font = ('Gabriola', 12,'bold'))
                    else:
                        art_makelabel.config(foreground = 'black', font = ('Gabriola', 12,'normal'))

    #Art Directory
        def build_directory():

        #Place Art Cover Pics
            def art_place(name, num):
                
                root = base.art_dict[name]

                piece = Art(self.art_col, root['Images'][0], root['Name'], root['Price'], root['Creation Date'], root['Sold Date'], root['Customer Name'], root['Customer Address'], root['Customer Email'], root['Customer Phone'], root['Type'], root['Images'], root['Notes'])

                piece.place(num)

                num += 1
                length = (len(piece.art_names['all_names']))

                if length > num:
                    art_place(base.key_sort[num][0], num)
                else:
                    pass

        #Function to sort through Cover Pics
            def sort_func(key):

                base.key_list = []

                for name in base.art_names['all_names']:
                    base.key_list.append([name, f'{base.art_dict[name][key]}'.casefold()])

                base.key_sort = sorted(base.key_list, key = lambda k: k[1])

                self.art_col.destroy()
                build_art_col()
                art_place(base.key_sort[0][0],0)
            
        #Function to build art_col
            def build_art_col():
                self.art_col = ttk.Frame(art_dir, relief = 'ridge', padding=5)
                self.art_col.pack(ipadx=10,ipady=10)


        #Build Widgets for Art Directory
            top_menu.forget()
            art_dir = ttk.Frame(master)
            art_dir.pack()

            build_art_col()

            ttk.Label(art_dir, text = 'Art Directory', font = ('Gabriola', 20, 'bold')).pack()
            sort_frame = ttk.Frame(art_dir, width = 700, height = 40)
            sort_frame.pack_propagate(False)
            sort_frame.pack()
            ttk.Button(sort_frame, text = 'Sort', command = lambda: sort_func(sort_entry.get()), width = 6).pack(side = RIGHT)

            ttk.Button(art_dir, text = "back", command = lambda: (art_dir.forget(), make_menu())).pack(side = BOTTOM)
            sort_entry = ttk.Combobox(sort_frame, values = ['Name','Price','Creation Date','Sold Date'], width = 12, state = 'readonly')
            sort_entry.pack(side = RIGHT)
            sort_entry.set('Name')
            ttk.Label(sort_frame, text = 'Sort By:').pack(side = RIGHT, padx = 5)

        #Pack Art into art_col
            base = Art()

            sort_func('Name')


        make_menu()




def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':main()