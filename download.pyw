from tkinter import *
import os
import shutil
import itertools
import glob

def download(account):
    command = r"instaloader --post-metadata-txt={likes}" + " " + account
    print(command)
    os.system(command)
    create_update_file(account)
    top_posts(account)

def create_update_file(account):
    path = os.path.join(os.getcwd(), account, 'update.py')
    with open(path, 'w+') as update_file:
        update_file.write("""import os\n\nos.system('instaloader {} --fast-update')""".format(account))

def get_text_files(account):
    path = os.path.join(os.getcwd(), account)
    files = []
    for file in os.listdir(path):
        if file.endswith('.txt') and 'old' not in file:
            files.append(os.path.join(path, file))
    return files

def check_likes(files):
    likes = {}
    for file in files:
        post = os.path.basename(file).split('.')[0]
        with open(file, 'r') as like_count:
            like_value = like_count.read().strip()
            likes[post] = str(like_value)
    return likes

def sort_by_likes(post_likes):
    return {k: v for k, v in sorted(post_likes.items(), key=lambda item: item[1], reverse=True)}

def post_names(files):
    posts = []
    for each in files:
        posts.append(each)
    return posts

def post_paths(names, account):
    path = os.path.join(os.getcwd(), account)
    photo_paths = []
    for name in names:
        photo_path = os.path.join(path, name)
        photos = glob.glob(photo_path + '*.jpg')
        for each in photos:
            photo_paths.append(each)
        #photo_paths.append(os.path.join(path, name + '.jpg'))
    return photo_paths

def build_folder(posts, account):
    dest = os.path.join(os.getcwd(), account, 'Top Posts')
    try:
        os.mkdir(dest)
    except:
        shutil.rmtree(dest)
        os.mkdir(dest)

    for post in posts:
        shutil.copy2(post, dest)

def top_posts(account, count=5):
    files = get_text_files(account)
    sorted_posts = sort_by_likes(check_likes(files))
    sorted_posts = dict(itertools.islice(sorted_posts.items(), count))
    posts = post_names(sorted_posts)
    file_names = post_names(posts)
    posts = post_paths(file_names, account)
    build_folder(posts, account)

root = Tk()

account_name_label = Label(root, text='Enter Account Name or names below')
account_name_label.pack()
account_name = Entry(root)
account_name.pack()

download_button = Button(root, text='Download Posts', command=lambda:download(account_name.get()))
download_button.pack()

#root.bind('<Return>', download(account_name.get()))

root.mainloop() 

