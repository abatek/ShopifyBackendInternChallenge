import sqlite3

def create_image_table(conn):
    conn.execute('CREATE TABLE images (key TEXT, image BLOB)')

def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def add_image(conn, key, path_to_image):
    try:
        cur = conn.cursor()

        image_blob = convert_to_binary_data(path_to_image)
        print(image_blob)
        cur.execute("INSERT INTO images (key, image)VALUES(?, ?);", (key, image_blob))
        print('executed add')

        conn.commit()
        print('executed commit')
    except Exception as e:
        print(e)
        conn.rollback()
        print('failed to add')


def retrieve_image(conn, key, path):
    try:
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM images WHERE key="{key}"')
        key, binary_image = cur.fetchone()
        print(binary_image)

        write_file(binary_image, f'output_images/{key}.png')

    except:
        conn.rollback()
        print('failed to retrieve')


if __name__ == '__main__':
    conn = sqlite3.connect('pythonsqlite.db')

    create_image_table(conn)

    conn.close()
