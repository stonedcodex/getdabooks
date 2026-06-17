from pathlib import Path
import shutil 
import time
exts = ['pdf', 'doc', 'epub', 'mobi', 'azw3', 'lrf', 'zip']
books = Path(f'C:\\Users\\kamot\\Downloads\\books')
folder = Path().cwd()
def move_books():
    for file in folder.glob('*'):
        name = file.name
        ext =name.split('.')[-1]
        if ext in exts:
            size1 = file.stat().st_size
            time.sleep(2)
            size2 = file.stat().st_size

            if size1 == size2:
                shutil.move(file, books)
                print(file)
                

if __name__ == "__main__":
    move_books()