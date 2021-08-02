import os
from tabulate import tabulate
import magic
import sqlite3
root = 'C:\\Users\\Rimold Rynold\\Desktop\\rimold official'
def analyz(root):
    isDir = os.path.isdir(root)
    if not isDir:
        print(f'path {root} does not exist')
        return None
    id=0
    combine_list=[]
    for path1,subdirs,files in os.walk(root):
        for name in files:
            full_file_name=os.path.join(path1,name)
            replace=full_file_name.replace('\\','/')
            split=replace.split('.')
            file_format=split[-1]
            file_size=round(os.path.getsize(full_file_name) / 1024 / 1024, 2)
            file_type=magic.from_file(full_file_name, mime=True)
            combine_list.append([id,full_file_name,file_format,file_size,file_type])
            id=id+1
    try:
        DB_name = root.split('\\')[-1] + '.db'
        conn = sqlite3.connect(DB_name)
        print(f'database created with name {DB_name}')
        conn.execute('''CREATE TABLE File
        (ID INT PRIMARY KEY NOT NULL,
        file_path TEXT,
        file_format TEXT,
        file_size_in_mb INT,
        file_type TEXT);
        ''')
        print('table created successfully')
        sql = """INSERT INTO File
        (ID, file_path  ,file_format ,file_size_in_mb ,file_type)
        VALUES (?,?,?,?,?); """

        cursor = conn.cursor()
        cursor.executemany(sql, combine_list)
        conn.commit()
        print('multiple insert operation OK')
        cursor.close()

    except sqlite3.Error as e:
        print('error happened due to the', e)

    finally:
        if conn:
            conn.close()
            print('connection closed')

analyz(root)

