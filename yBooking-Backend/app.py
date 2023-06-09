# pylint: disable=C0114, W0311, C0301, C0116
from flask import Flask, request
from sql_manager import SQLManager
from mail_manager import MailManager

app = Flask(__name__)

@app.route("/api/sign_up",methods=["POST"])
def sign_up():
    database = SQLManager()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    sql = "SELECT * FROM `user` WHERE email=%s"
    if database.get_one(sql,email) is None:
        sql = "INSERT INTO `user`(`email`, `password`) VALUES (%s, %s)"
        database.moddify(sql,(email,password))
        database.close()
        return { "code": 200, "status": "success", "data": "" }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

@app.route("/api/sign_in",methods=["POST"])
def sign_in():
    database = SQLManager()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    sql = "SELECT * FROM `user` WHERE email=%s and password=%s"
    if database.get_one(sql,(email,password)) is not None:
        database.close()
        return { "code": 200, "status": "success", "data": "" }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

@app.route("/api/lanuch_product",methods=["POST"])
def lanuch_product():
    database = SQLManager()
    data = request.get_json()
    country = data.get('country')
    city = data.get('city')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    price = data.get('price')
    img = data.get('img')
    owner = data.get('owner')
    img = None if img == "" else img
    sql = "INSERT INTO `products` (`country`, `city`, `start_date`, `end_date`, `price`, `img`, `owner`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    database.moddify(sql, (country, city, start_date, end_date, price, img, owner))
    database.close()
    return { "code": 200, "status": "success", "data": "" }

@app.route("/api/get_products",methods=["GET"])
def get_products():
    database = SQLManager()
    sql = "SELECT * FROM `products` WHERE `del_flag` != 1"
    data_list = database.get_list(sql)
    if data_list is not None:
        database.close()
        return { "code": 200, "status": "success", "data": data_list }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

@app.route("/api/get_product",methods=["POST"])
def get_product():
    database = SQLManager()
    data = request.get_json()
    product_id = data.get('product_id')
    sql = "SELECT * FROM `products` WHERE `product_id` = %s and `del_flag` != 1"
    data = database.get_one(sql, product_id)
    if data is not None:
        database.close()
        return { "code": 200, "status": "success", "data": data }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

@app.route("/api/get_likes",methods=["POST"])
def get_likes():
    database = SQLManager()
    data = request.get_json()
    user = data.get('user')
    sql = "SELECT * FROM `like_list` WHERE `user` = %s"
    data_list = database.get_list(sql, user)
    if data_list is not None:
        database.close()
        return { "code": 200, "status": "success", "data": data_list }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }
    
@app.route("/api/get_like",methods=["POST"])
def get_like():
    database = SQLManager()
    data = request.get_json()
    product_id = data.get('product_id')
    user = data.get('user')
    sql = "SELECT * FROM `like_list` WHERE `product_id` = %s and `user` = %s"
    data = database.get_one(sql, (product_id, user))
    if data is not None:
        database.close()
        return { "code": 200, "status": "success", "data": data }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

@app.route("/api/update_likes",methods=["POST"])
def update_likes():
    database = SQLManager()
    data = request.get_json()
    product_id = data.get('product_id')
    user = data.get('user')
    sql = "SELECT * FROM `like_list` WHERE `product_id` = %s and `user` = %s"
    data_list = database.get_list(sql, (product_id, user))
    if len(data_list) != 0:
        sql = "DELETE FROM `like_list` WHERE `product_id`=%s and `user`=%s"
        print("Del")
        database.moddify(sql, (product_id, user))
    else:
        sql = "INSERT INTO `like_list` (`product_id`, `user`) VALUES (%s, %s)"
        print("Ins")
        database.moddify(sql, (product_id, user))

    database.close()
    return { "code": 200, "status": "success", "data": data_list }

@app.route("/api/get_products_and_likes", methods=["POST"])
def get_products_and_likes():
    database = SQLManager()
    data = request.get_json()
    user = data.get('user')
    sql = "SELECT * FROM `like_list` WHERE `user` = %s"
    like_list = database.get_list(sql, user)
    sql = "SELECT * FROM `products` WHERE `del_flag` != 1"
    product_list = database.get_list(sql)

    if like_list is not None and product_list is not None:
        for product in product_list:
            product_id = product['product_id']
            if any(like['product_id'] == product_id for like in like_list):
                product['is_like'] = True
            else:
                product['is_like'] = False
        database.close()
        return { "code": 200, "status": "success", "data": product_list }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

@app.route("/api/order_product",methods=["POST"])
def order_product():
    database = SQLManager()
    data = request.get_json()
    product_id = data.get('product_id')
    user = data.get('user')
    sql = "INSERT INTO `product_order`(`product_id`, `user`) VALUES (%s, %s)"
    database.moddify(sql, (product_id, user))
    sql = "UPDATE `products` SET `del_flag`= %s WHERE `product_id`= %s"
    database.moddify(sql, (1, product_id))
    database.close()
    return { "code": 200, "status": "success", "data": data }

@app.route("/api/get_order_product",methods=["POST"])
def get_order_product():
    database = SQLManager()
    data = request.get_json()
    user = data.get('user')
    sql = "SELECT * FROM `products` WHERE `product_id` IN (SELECT `product_id` FROM `product_order` WHERE `user`=%s)"
    data_list = database.get_list(sql, user)
    database.close()
    return { "code": 200, "status": "success", "data": data_list }

@app.route("/api/cancel_order",methods=["POST"])
def cancel_order():
    database = SQLManager()
    data = request.get_json()
    product_id = data.get('product_id')
    user = data.get('user')
    sql = "UPDATE `products` SET `del_flag` = 0 WHERE `product_id` IN (SELECT `product_id` FROM `product_order` WHERE `user`=%s)"
    database.moddify(sql, user)
    sql = "DELETE FROM `product_order` WHERE `product_id` = %s"
    database.moddify(sql, product_id)
    database.close()
    return { "code": 200, "status": "success", "data": "" }

@app.route("/api/get_own_product",methods=["POST"])
def get_own_product():
    database = SQLManager()
    data = request.get_json()
    user = data.get('user')
    sql = "SELECT * FROM `products` WHERE `owner`= %s"
    data_list = database.get_list(sql, user)
    if data is not None:
        database.close()
        return { "code": 200, "status": "success", "data": data_list }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

@app.route("/api/cancel_launch",methods=["POST"])
def cancel_launch():
    database = SQLManager()
    data = request.get_json()
    product_id = data.get('product_id')
    user = data.get('user')
    sql = "DELETE FROM `products` WHERE `product_id` = %s and `owner` = %s"
    database.moddify(sql, (product_id, user))
    database.close()
    return { "code": 200, "status": "success", "data": "" }

@app.route("/api/edit_product",methods=["POST"])
def edit_product():
    database = SQLManager()
    data = request.get_json()
    product_id = data.get('product_id')
    country = data.get('country')
    city = data.get('city')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    price = data.get('price')
    user = data.get('user')
    sql = "UPDATE `products` SET `country`= %s,`city`= %s,`start_date`= %s,`end_date`= %s, `price`= %s WHERE `product_id` = %s and `owner` = %s"
    database.moddify(sql, (country, city, start_date, end_date, price, product_id, user))
    database.close()
    return { "code": 200, "status": "success", "data": "" }

@app.route("/api/search_product",methods=["POST"])
def search_product():
    database = SQLManager()
    data = request.get_json()
    keyword = data.get('keyword')
    sql = "SELECT * FROM `products` WHERE `country` LIKE %s OR `city` LIKE %s"
    data_list = database.get_list(sql, (f"%{keyword}%", f"%{keyword}%"))
    if data_list is not None:
        database.close()
        return { "code": 200, "status": "success", "data": data_list }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }
 
@app.route("/api/send_password",methods=["POST"])
def send_password():
    mail = MailManager(app)
    database = SQLManager()
    data = request.get_json()
    user = data.get('user')
    sql = "SELECT `password` FROM `user` WHERE `email` = %s"
    data = database.get_one(sql, user)
    if data is not None:
        mail.send_email(user, '【yBooing】 Your Password', f"Hi,\nYour password: {data['password']}")
        database.close()
        return { "code": 200, "status": "success", "data": data }
    else:
        database.close()
        return { "code": 400, "status": "failure", "data": "" }

if __name__ == '__main__':
    app.debug = False
    app.run()
