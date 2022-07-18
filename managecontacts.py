from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from sqlite3 import *

class ManageContactsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        s = Style()

        s.configure('TFrame', background = 'white')
        s.configure('TLabel', background = 'white')

        self.pack(fill = BOTH, expand = TRUE)

        self.con = connect('mycontacts.db')
        self.cur = self.con.cursor()

        self.create_view_all_contacts_frame()

    def fill_contacts_treeview(self):
        for contact in self.contacts_treeview.get_children():
            self.contacts_treeview.delete(contact)
        
        contacts = self.cur.fetchall()

        for contact in contacts:
            self.contacts_treeview.insert("", END, values = contact)
    
        self.contacts_treeview.grid(row = 2, column = 0, columnspan = 2, pady = 10)

    def create_view_all_contacts_frame(self):
        self.view_all_contacts_frame = Frame(self)
        self.view_all_contacts_frame.place(relx = .5, rely = .5, anchor = CENTER)

        add_new_contact_button = Button(self.view_all_contacts_frame,
        text = "Add New Contact", command = self.add_new_contact_button_click)
        add_new_contact_button.grid(row = 0, column = 1, pady = 25, sticky = E)

        name_label = Label(self.view_all_contacts_frame, text = "Name:")
        name_label.grid(row = 1, column = 0)

        self.name_entry = Entry(self.view_all_contacts_frame, width = 97)
        self.name_entry.grid(row = 1, column = 1, pady = 10)
        self.name_entry.bind('<KeyRelease>', self.name_entry_key_release)

        self.contacts_treeview = Treeview(self.view_all_contacts_frame, columns = ('name', 'phone number', 'email_id', 'city'), show = 'headings')
        self.contacts_treeview.heading('name', text = "Name")
        self.contacts_treeview.heading('phone number', text = "Phone Number")
        self.contacts_treeview.heading('email_id', text = "Email Id")
        self.contacts_treeview.heading('city', text = "City")
        self.contacts_treeview.column('name', width = 200)
        self.contacts_treeview.column('phone number', width = 125)
        self.contacts_treeview.column('email_id', width = 200)
        self.contacts_treeview.column('city', width = 100)
        self.contacts_treeview.bind('<<TreeviewSelect>>', self.contacts_treeview_row_selection)

        self.cur.execute("select * from Contact")
        self.fill_contacts_treeview()

    def add_new_contact_button_click(self):
        self.view_all_contacts_frame.destroy()

        self.add_new_contact_frame = Frame(self)
        self.add_new_contact_frame.place(relx = .5, rely = .5, anchor = CENTER)

        name_label = Label(self.add_new_contact_frame, text = "Name:")
        name_label.grid(row = 0, column = 0, sticky = E)

        self.name_entry = Entry(self.add_new_contact_frame, width = 30)
        self.name_entry.grid(row = 0, column = 1, pady = 5)

        phone_number_label = Label(self.add_new_contact_frame, text = "Phone Number:")
        phone_number_label.grid(row = 1, column = 0, sticky = E)

        self.phone_number_entry = Entry(self.add_new_contact_frame, width = 30)
        self.phone_number_entry.grid(row = 1, column = 1, pady = 5)

        email_id_label = Label(self.add_new_contact_frame, text = "Email Id:")
        email_id_label.grid(row = 2, column = 0, sticky = E)

        self.email_id_entry = Entry(self.add_new_contact_frame, width = 30)
        self.email_id_entry.grid(row = 2, column = 1, pady = 5)

        city_label = Label(self.add_new_contact_frame, text = "City:")
        city_label.grid(row = 3, column = 0, sticky = E)

        self.city_combobox = Combobox(self.add_new_contact_frame, width = 27,
        values = ('Greater Noida', 'Noida', 'Delhi', 'Mumbai', 'Banglore'))
        self.city_combobox.grid(row = 3, column = 1, pady = 5)

        add_button = Button(self.add_new_contact_frame, text = "Add",
        width = 30, command = self.add_button_click)
        add_button.grid(row = 4, column = 1, pady = 5)

    def add_button_click(self):
        self.cur.execute("select * from Contact where EmailId = ?", (self.email_id_entry.get(),))
        contact = self.cur.fetchone()

        if contact is None:
            self.cur.execute("insert into Contact values (?, ?, ?, ?)", (self.name_entry.get(), self.phone_number_entry.get(),
            self.email_id_entry.get(), self.city_combobox.get()))
            self.con.commit()
            messagebox.showinfo("Success Message", "Contact details are added successfully")
            self.add_new_contact_frame.destroy()
            self.create_view_all_contacts_frame()
        else:
            messagebox.showerror("Error Message", "Contact details are already added")

    def name_entry_key_release(self, event):
        self.cur.execute("select * from Contact where Name Like ?", ('%' + self.name_entry.get() + '%',))
        self.fill_contacts_treeview()

    def contacts_treeview_row_selection(self, event):
        contact = self.contacts_treeview.item(self.contacts_treeview.selection())['values']

        self.view_all_contacts_frame.destroy()

        self.update_delete_contact_frame = Frame(self)
        self.update_delete_contact_frame.place(relx = .5, rely = .5, anchor = CENTER)

        name_label = Label(self.update_delete_contact_frame, text = "Name:")
        name_label.grid(row = 0, column = 0, sticky = E)

        self.name_entry = Entry(self.update_delete_contact_frame, width = 30)
        self.name_entry.grid(row = 0, column = 1, pady = 5)
        self.name_entry.insert(END, contact[0])

        phone_number_label = Label(self.update_delete_contact_frame, text = "Phone Number:")
        phone_number_label.grid(row = 1, column = 0, sticky = E)

        self.phone_number_entry = Entry(self.update_delete_contact_frame, width = 30)
        self.phone_number_entry.grid(row = 1, column = 1, pady = 5)
        self.phone_number_entry.insert(END, contact[1])

        email_id_label = Label(self.update_delete_contact_frame, text = "Email Id:")
        email_id_label.grid(row = 2, column = 0, sticky = E)

        self.email_id_entry = Entry(self.update_delete_contact_frame, width = 30)
        self.email_id_entry.grid(row = 2, column = 1, pady = 5)
        self.email_id_entry.insert(END, contact[2])
        self.old_email_id = contact[2]

        city_label = Label(self.update_delete_contact_frame, text = "City:")
        city_label.grid(row = 3, column = 0, sticky = E)

        self.city_combobox = Combobox(self.update_delete_contact_frame, width = 27,
        values = ('Greater Noida', 'Noida', 'Delhi', 'Mumbai', 'Banglore'))
        self.city_combobox.grid(row = 3, column = 1, pady = 5)
        self.city_combobox.set(contact[3])

        update_button = Button(self.update_delete_contact_frame, text = "Update",
        width = 15, command = self.update_button_click)
        update_button.grid(row = 4, column = 0, pady = 5)

        delete_button = Button(self.update_delete_contact_frame, text = "Delete",
        width = 15, command = self.delete_button_click)
        delete_button.grid(row = 4, column = 1, pady = 5, sticky = E)

    def update_button_click(self):
        self.cur.execute("update Contact set Name = ?, PhoneNumber = ?, EmailId = ?, City = ? where EmailId = ?",
        (self.name_entry.get(), self.phone_number_entry.get(), self.email_id_entry.get(),
        self.city_combobox.get(), self.old_email_id))
        self.con.commit()
        messagebox.showinfo("Success Message", "Contact details are updated successfully")
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()

    def delete_button_click(self):
        if messagebox.askquestion("Confirmation Message", "Are your sure to delete?") == 'yes':
            self.cur.execute("delete from Contact where EmailId = ?", (self.old_email_id,))
            self.con.commit()
            messagebox.showinfo("Success Message", "Contact details are deleted successfully")
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()
        
        
        


        

        

        
        

        
