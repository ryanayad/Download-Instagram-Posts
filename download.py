from tkinter import *
import os

def download(accounts):
    os.system('instaloader {}'.format(accounts))
    create_update_file(accounts)

def create_update_file(account):
    path = os.path.join(os.getcwd(), account, 'update.py')
    with open(path, 'w+') as update_file:
        update_file.write("""import os\n\nos.system('instaloader {}')""".format(account))


root = Tk()

account_name_label = Label(root, text='Enter Account Name or names below\n(Seperate a list of accounts with a comma)').pack()
account_name = Entry(root)
account_name.pack()

download_button = Button(root, text='Download Posts', command=lambda:download(account_name.get()))
download_button.pack()

#hello
root.mainloop()