from tkinter import *
from tkinter import ttk
from pymongo import *
from tkinter import messagebox

class Product_Management_Tool():
    def __init__(self):
        self.Lis=[]
        self.window = Tk()
        self.window.title("MyApp")
        self.window.geometry("1050x350")
        self.window.resizable(width=False, height=False)

        # DB Connection
        self.mongo_client = MongoClient("mongodb://localhost:27017")
        self.db = self.mongo_client["ProductManagementTool"]
        self.col = self.db["process"]



        # Phần tiêu đề
        self.Tieude = Label(master=self.window, text="Product Management Tool", fg="blue", font=("Arial", 20, "bold"))
        self.Tieude.place(x=350, y=10)

        # Phần tên
        self.NameLabel = Label(master=self.window, text="Name", font=("Arial", 10, "bold"))
        self.name = StringVar()
        self.NameEntry = Entry(master=self.window, width=30,textvariable=self.name)

        self.NameLabel.place(x=30, y=50)
        self.NameEntry.place(x=130, y=52)

        # Phần giá cả
        self.PriceLabel = Label(master=self.window, text="Price", font=("Arial", 10, "bold"))
        self.PriceEntry = Entry(master=self.window, width=30)

        self.PriceLabel.place(x=30, y=80)
        self.PriceEntry.place(x=130, y=82)

        # Phần miêu tả
        self.DescriptionLabel = Label(master=self.window, text="Description: ", font=("Arial", 10, "bold"))
        self.DescriptionText = Text(master=self.window, width=30, height=8, bg="black", fg="white", borderwidth=5)

        self.DescriptionLabel.place(x=30, y=150)
        self.DescriptionText.place(x=130, y=120)

        # Phần danh sách sản phẩm
        self.ListOfProducts = Label(master=self.window, text="List of products:", font=("Arial", 10, "bold"))
        self.tree = ttk.Treeview(master=self.window, columns=("name", "price", "description"), height=10)
        self.tree.bind('<Double-ButtonRelease-1>', self.selectItem)
        self.load_data()

        self.tree.heading("name", text="Name")
        self.tree.heading("price", text="Price")
        self.tree.heading("description", text="Description")
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)

        self.ListOfProducts.place(x=400, y=50)
        self.tree.place(x=400, y=80)

        # Phần nút bấm
        self.Save = Button(master=self.window, text="Save", font=("Arial", 10, "bold"),command=self.save)
        self.Update = Button(master=self.window, text="Update", font=("Arial", 10, "bold"),command=self.update)
        self.Delete = Button(master=self.window, text="Delete", font=("Arial", 10, "bold"),command=self.delete)
        self.Reset = Button(master=self.window, text="Reset", font=("Arial", 10, "bold"),command=self.reset)

        self.Save.place(x=40, y=280)
        self.Update.place(x=95, y=280)
        self.Delete.place(x=165, y=280)
        self.Reset.place(x=230, y=280)

    def load_data(self):
        cur = self.col.find({})
        for d in cur:
            p_name = str(d['name'].encode('utf-8').decode('utf-8'))
            p_price = float(d['price'])
            p_des = str(d['description'].encode('utf-8').decode('utf-8'))
            self.tree.insert("","end",values=(p_name,p_price,p_des))

    def save(self):
        # Name = self.NameEntry.get()
        # Price=self.PriceEntry.get()
        # Des= self.DescriptionText.get("1.0","end-1c")
        # self.tree.insert('','end',values=(Name,Price,Des))
        data = {"name": self.name.get(),"price": self.PriceEntry.get(),"description": self.DescriptionText.get("1.0","end-1c")}
        doc = self.col.insert_one(data)
        if doc.inserted_id:
            messagebox.showinfo("Insert","Success!")
            self.clear_tree_view()
            self.load_data()

    def clear_tree_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def update(self):
        new_data ={"price":self.PriceEntry.get(),"description":self.DescriptionText.get("1.0","end-1c")}
        print(new_data)
        print(self.NameEntry.get())
        self.col.update_one({"name": self.NameEntry.get()},{"$set":new_data})
        self.clear_tree_view()
        self.load_data()

    def delete(self):
        if messagebox.askokcancel("Confirm","Delete?"):
            self.col.delete_one({"name": self.NameEntry.get()})
        self.update()

    def selectItem(self,a):
        # curItem = self.tree.focus()
        # lis =self.tree.item(curItem)['values']
        #
        # self.NameEntry.delete(0,END)
        # self.NameEntry.insert(0,lis[0])
        #
        # self.PriceEntry.delete(0,END)
        # self.PriceEntry.insert(0,lis[1])
        #
        # self.DescriptionText.delete("1.0","end-1c")
        # self.DescriptionText.insert("1.0",lis[2])

        current_item = self.tree.focus()
        self.NameEntry.set(self.tree.item(current_item)['values'][0])
        self.NameEntry.configure(state="disabled")
        self.PriceEntry.set(self.tree.item(current_item)['values'][1])
        self.DescriptionText.delete("1.0","end-1c")
        self.DescriptionText.insert("1.0",self.tree.item(current_item)['values'][2])

    # def Delete(self):
    #     selected = self.tree.focus()
    #     self.tree.delete(selected)
    #
    # def Update(self):
    #     selected = self.tree.focus()
    #     self.tree.item(selected,values=(self.NameEntry.get(),self.PriceEntry.get(),self.DescriptionText.get("1.0","end-1c")))

    def reset(self):
        self.NameEntry.delete(0,END)
        self.PriceEntry.delete(0,END)
        self.DescriptionText.delete("1.0","end-1c")

if __name__ == "__main__":
    app = Product_Management_Tool()
    app.window.mainloop()

