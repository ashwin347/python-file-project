import os
from tabulate import tabulate
import magic
import sqlite3
root = 'C:\\Program Files\\7-Zip'
def analyz(root):
    isDir = os.path.isdir(root)
    if not isDir:
        print(f'path {root} does not exist')
        return None

    new_files = []
    file_size = []
    file_type = []
    for path1,subdirs,files in os.walk(root):
        for name in files:
            new_files.append(os.path.join(path1,name))

    file_format = []
    replace=[]
    split = []
    for i in new_files:
        replace=i.replace('\\','/')
        split=replace.split('.')

        file_format.append(split[-1])
        file_size.append(round(os.path.getsize(i) / 1024 / 1024, 2))
        file_type.append(magic.from_file(i, mime=True))

    # table = {'file_path' :new_files,'file_format' :file_format,'file_size in mb':file_size,'file_type':file_type}
    # print(tabulate(table, headers='keys', tablefmt='fancy_grid'))
    ID_list = []
    starting = 0
    for i in range(len(new_files)):
        starting = i+1
        ID_list.append(starting)
    combine_list = list(zip(ID_list,new_files,file_format,file_size,file_type))

    try:

        DB_name =root.split('\\')[-1]+'.db'
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