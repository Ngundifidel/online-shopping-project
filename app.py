from flask import *

import pymysql

from mpesa import *


app = Flask(__name__)
app.secret_key = " 12345678"

@app.route("/")
def home():
        # connection to DB

        connection = pymysql.connect(host='localhost', user='root', password= '', database='soko_garden_db')

        #  SQL query
        sql = "SELECT * FROM products WHERE product_category = 'phones'"
        sql1 =  "SELECT * FROM products WHERE product_category = 'clothes'"
        sql2 =  "SELECT * FROM products WHERE product_category = 'laptops'"




        cursor = connection.cursor()
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()



        cursor.execute(sql)
        cursor1.execute(sql1)
        cursor2.execute(sql2)


        phones = cursor.fetchall()
        clothes = cursor1.fetchall()
        laptops= cursor2.fetchall()


        return render_template('home.html', phones=phones, clothes = clothes, laptops = laptops) 

  

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
    
 # route for single product
# We will get the product dynamic using product_id
@app.route("/single/<product_id>")
def single(product_id):
      connection = pymysql.connect(host='localhost', user='root', password= '', database='soko_garden_db')
      
     

    #  sql query
      sql = 'select * from products where product_id = %s'

      cursor = connection.cursor()

    #   execute 
      cursor.execute(sql, product_id)

      product = cursor.fetchone()
      return render_template('single.html', product = product )

# regisration route
@app.route("/register",  methods = ['POST', 'GET'])
def register():
      if request.method == 'POST':
             username = request.form ['username']
             email = request.form ['email']
             phone = request.form ['phone']
             password1 = request.form ['password1']
             password2 = request.form ['password2']

             connection = pymysql.connect(host='localhost', user='root', password= '', database='soko_garden_db')
     
            #  check if password length is 8 characters
             if len(password1) < 8 :
                    return render_template('registar.html', error = 'Password is too short')
             elif password1!= password2:
                    return render_template ('registar.html', error = 'Passwords dont match')
             else:
                #   continue to register this person
                    sql = ''' insert into users (username, email, phone, password) values (%s,%s,%s,%s)'''

                    data = (username, email, phone, password1)

                    # Execute SQL and provide values for place holders
                    # curosr is used to execute sqlquesris in python


                    cursor = connection.cursor()
                    cursor.execute(sql, data)


                    #  make the update, write the database
                    connection.commit()
                    return render_template('registar.html',message = ' Registartion successful')

             
                                     
             
                   
     
      else:
        return render_template('registar.html')

     


# route for loggin
@app.route ("/login",  methods = ['POST', 'GET'])
def login():
      if request.method == 'POST':
               email = request.form ['email']
               password = request.form ['password']

            # connection to DB
               connection = pymysql.connect(host='localhost', user='root', password= '', database='soko_garden_db')
               
              #  CURSOR
               cursor = connection.cursor()
               
               sql = "Select * from users where email= %s and password = %s"
               data = (email, password)

              #  execute/run the query
               cursor.execute(sql,data)

               if cursor.rowcount == 0:
                    #  it means lgin credentials are wrong
                         return render_template ("login.html", error= 'invalid credentials')
               else:
                    #  it means the suer input is correct
                     
                     session['key'] = email
                     
                     
                     
                     return redirect("/")




            
      else:
            
          return render_template ("login.html")
      


      # route for mpesa payment
@app.route('/mpesa', methods =['POST'])
def mpesa():
      #  receive phone and amount from singel.html from
       phone = request.form['phone']
       Amount = request.form['amount']
   

# call the stk push from mpesa.py
# the stk_push function takes 2 arguments
# Argument 1 is phone , Argument 2 is amount
       
       stk_push(phone, Amount)

      
       return "Mpesa payment"


      # log out th suer
@app.route("/logout")
def logout ():
            # clear the session

            session.clear()

            return redirect("/")





if __name__ == '__main__':
    app.run(debug=True)

