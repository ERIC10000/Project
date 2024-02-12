from flask import *
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    connection = pymysql.connect(host='localhost', user='root', password='', database='SokoGardenDB')
    print("Success")

    sql = 'select * from products where product_category = "x" '
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    # category y
    sql2 = 'select * from products where product_category = "y" '
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    
    return render_template('home.html', category_x = data, category_y = data2)
    
    
@app.route('/upload', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['name']
        product_desc = request.form['desc']
        product_cost = request.form['cost']
        product_category = request.form['category']
        image_url = request.files['image']
        image_url.save('static/uploads/' + image_url.filename)

        connection = pymysql.connect(
            host='localhost', user='root', password='', database='SokoGardenDB')

        cursor = connection.cursor()

        data = (product_name, product_desc, product_cost,
                product_category, image_url.filename)

        sql = "insert into products (product_name, product_desc, product_cost, product_category, product_image_name) values (%s, %s, %s, %s, %s)"

        cursor.execute(sql, data)
        connection.commit()
        return render_template('upload.html', message='Product Added Successfully')

    else:
        return render_template('upload.html', message='Please Add Product Details')


app.run(debug=True)