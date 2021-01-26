from flask import Flask, flash, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
# from dataBase.MyDataBase import DataBase
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'secret_key_by_jmat'

# Connect to Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'FlaskProject'

mysql = MySQL(app)

# context processor


@app.context_processor
def date_now():
    return{'now': datetime.now()}


def search_article(article_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Articles WHERE id = %s", (article_id,))
    article = cursor.fetchall()
    cursor.close()
    return article


# def search_article_with(myapp, article_id):
#     with DataBase(myapp, article_id):
#         article = DataBase.query
#         # ToConnect.commit()
#     return article


@app.route('/')
def index():
    string1 = "a simple string"
    string2 = "<h3> passing a html code </h3>"
    return render_template("index.html", string1=string1, string2=string2)


@app.route('/info')
@app.route('/info/<string:name>')
def info(name: str = "Jose"):
    return render_template("info.html", name=name)


@app.route('/contact')
@app.route('/contact/<redirect_to>')
def contact(redirect_to=None):
    if redirect_to is not None:
        return redirect(url_for('things'))
    return render_template("contact.html")


@app.route('/building')
def things():
    return render_template("things.html")


@app.route('/article', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        price = request.form['price']
        city = request.form['city']

        # return f"{brand}{model}{price}{city}"
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Articles VALUES(NULL,%s,%s,%s,%s)", (brand, model, price, city))
        cursor.connection.commit()
        cursor.close()
        flash("New article was successfully created")
        return redirect(url_for('index'))

    return render_template("articles.html")


@app.route('/list')
def list_article():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Articles ORDER BY id DESC")
    articles = cursor.fetchall()
    cursor.close()
    return render_template("listOfArticles.html", articles=articles)


@app.route('/page_article/<article_id>')
def page_article(article_id):
    article = search_article(article_id)
    return render_template("article.html", article=article[0])


@app.route('/delete_article/<article_id>')
def delete_article(article_id):
    # article = search_article_with(app, article_id)
    article = search_article(article_id)
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM Articles WHERE id = {article_id}")
    mysql.connection.commit()
    cursor.connection.commit()
    cursor.close()

    # toShow = article[0][1:]
    # str(toShow)[1:-1]

    to_show = ','.join(str(a) for a in article[0][1:])
    flash(f"Article {to_show} was successfully deleted")
    return redirect(url_for('list_article'))


@app.route('/edit_article/<article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        price = request.form['price']
        city = request.form['city']

        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Articles SET 
            brand=%s, model=%s, price=%s, city=%s WHERE id = %s''', (brand, model, price, city, article_id))
        cursor.connection.commit()
        cursor.close()
        article = search_article(article_id)
        flash("The article {0} was successfully updated".format(article[0][1]))
        return redirect(url_for('list_article'))

    article = search_article(article_id)
    return render_template("articles.html", article=article[0])


if __name__ == "__main__":
    app.run(debug=True)
