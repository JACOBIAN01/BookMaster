from flask import Flask , request , render_template , jsonify
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("BookList.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn



@app.route('/books',methods=['GET','POST'])
def book():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method=='GET':
        cursor = conn.execute(" SELECT * FROM BookList")
        Books_List = [
            dict(id=row[0],title=row[1],author =row[2],year=row[3])
            for row in cursor.fetchall()
        ]
        return jsonify(Books_List)


    if request.method == 'POST':
        new_author = request.form['author']
        new_title = request.form['title']
        new_year = request.form['year']
        #insert new book into the database
        sql = """INSERT INTO BookList(title,author,year) VALUES (? ,?,?)"""
        cursor.execute(sql,(new_author,new_title,new_year))
        conn.commit()

        return f"Book with id:{cursor.lastrowid} created successfully .",201

    

@app.route('/books/<int:BookId>',methods=['GET','PUT','DELETE'])
def single_book(BookId):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM BookList WHERE id = ?",(BookId,))
        row = cursor.fetchone()
        if row:
            book =dict(id=row[0],title=row[1],author =row[2],year=row[3])
            return jsonify(book) ,200
        else:
            return "Book Not Found",404

    if request.method == 'PUT':
        new_title = request.form['title']
        new_author = request.form['author']
        new_year = request.form['year']

        sql = """UPDATE BookList SET title=?, author=?,year=? WHERE id =?"""
        cursor.execute(sql,(new_title,new_author,new_year,BookId))
        conn.commit()

        if cursor.rowcount > 0:
            return f"Book with id {BookId} updated successfully.", 200
        else:
            return "Book not found.", 404

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM BookList WHERE id=?",(BookId,))
        conn.commit()

        
        if cursor.rowcount > 0:
            return f"Book with id: {BookId} updated successfully.", 200
        else:
            return "Book not found.", 404



if __name__=='__main__':
    app.run(debug=True) 
