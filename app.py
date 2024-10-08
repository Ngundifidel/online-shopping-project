from flask import *

import pymysql


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/upload", methods = ['POST', 'GET'])

def upload():
    if request.method == 'POST':
        # POST O DB
        product_name = request.form ['product_name']
        product_desc = request.form ['product_desc']
        product_cost = request.form ['product_cost']
        product_category = request.form ['product_category']
        product_image_name = request.files ['product_image_name']
        
        # The product image name is stores in the db while the image file is stored in static folder
        # the below line saves the iamge itself in static folder

        product_image_name.save("static/images/" + product_image_name.filename)



            # sql to save all the vaiable to our database
            # connect to DB
                 

        connection = pymysql.connect(host='localhost', user='root', password= '', database='soko_garden_db')

        #  Prepare the data to insert 
        data = (product_name, product_desc, product_cost, product_category, product_image_name.filename )

        # write SQL

        sql = ''' insert into products (product_name, product_desc, product_cost, product_category, product_image_name) values (%s,%s,%s,%s,%s)'''

        # Execute SQL and provide values for place holders
        # curosr is used to execute sqlquesris in python


        cursor = connection.cursor()
        cursor.execute(sql, data)


        #  make the update, write the database
        connection.commit()
        return render_template('upload.html', message = 'product upload successful')


    else:
         return render_template('upload.html')





if __name__ == '__main__':
    app.run(debug=True)

