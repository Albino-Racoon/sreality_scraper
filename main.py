from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    conn = psycopg2.connect(database='postgres', user='postgres', password='jasajernej', host='localhost', port='5436')
    cursor = conn.cursor()
    cursor.execute('SELECT title, image_url FROM sreality_scraper_items; ')
    ads = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', ads=ads)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
