from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect('address_book.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
             (name TEXT PRIMARY KEY, address TEXT)''')
conn.execute('PRAGMA journal_mode = WAL')  # Enable WAL mode
conn.commit()
conn.close()


class AddressBook:
    def create_record(self, name, address):
        conn = sqlite3.connect('address_book.db')
        c = conn.cursor()
        c.execute("INSERT INTO records (name, address) VALUES (?, ?)", (name, address))
        conn.commit()
        conn.close()

    def read_record(self, name):
        conn = sqlite3.connect('address_book.db')
        c = conn.cursor()
        c.execute("SELECT address FROM records WHERE name=?", (name,))
        record = c.fetchone()
        conn.close()
        if record:
            return record[0]
        else:
            return None

    def update_record(self, name, new_address):
        conn = sqlite3.connect('address_book.db')
        c = conn.cursor()
        c.execute("UPDATE records SET address=? WHERE name=?", (new_address, name))
        conn.commit()
        conn.close()

    def delete_record(self, name):
        conn = sqlite3.connect('address_book.db')
        c = conn.cursor()
        c.execute("DELETE FROM records WHERE name=?", (name,))
        conn.commit()
        conn.close()



    def reset_all_records(self):
        conn = sqlite3.connect('address_book.db')
        c = conn.cursor()
        c.execute("DELETE FROM records")
        conn.commit()
        conn.close()
    

    def display_records(self):
        conn = sqlite3.connect('address_book.db')
        c = conn.cursor()
        c.execute("SELECT * FROM records")
        records = c.fetchall()
        conn.close()
        return records


address_book = AddressBook()


@app.route('/')
def index():
    return render_template('index.html', records=address_book.display_records())


@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    address = request.form['address']
    address_book.create_record(name, address)
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update_record():
    name = request.form['name']
    new_address = request.form['address']
    address_book.update_record(name, new_address)
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_record():
    name = request.form['name']
    address_book.delete_record(name)
    return redirect(url_for('index'))




@app.route('/reset_all', methods=['POST'])
def reset_all_records():
    address_book.reset_all_records()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
