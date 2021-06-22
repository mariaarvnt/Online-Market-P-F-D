from flask import Flask, request, jsonify, Response, session
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError
import json, os, uuid, time
from datetime import datetime
from bson.objectid import ObjectId

# Connect to our MongoDB
mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

#choose DSMarkets DB, collections
db=client['DSMarkets']
users=db['Users']
products=db['Products']

# Initiate Flask App
app=Flask(__name__)

users_sessions = {}

def create_session(email):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (email, time.time())
    return user_uuid

def is_session_valid(user_uuid):
    return user_uuid in users_sessions

######################################################## USERS OPERATIONS #########################################################

###### 1: Create User ###### 
@app.route('/createUser', methods=['POST'])
def create_user():

    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "name" in data or not "password" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    # Check if there is a user with the same email in the db    
    if users.count_documents({"email":data["email"]})== 0 :
        # create user inserting email, name, password, category
        user = { 
        "email": data['email'],
        "name": data['name'],
        "password": data['password'],
        "category":"user",
        }
        # Add user to the 'users' collection
        users.insert_one(user)
        # successful response
        return Response("User with email " + data['email'] + " was added to the MongoDB", status=200, mimetype='application/json')
    else:
        # unsuccessful response
        return Response("A user with the given email already exists", status=400, mimetype='application/json')

###### 2: User Login ###### 
@app.route('/login', methods=['POST'])
def login():
   
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # search data for specific user
    user_found = users.find_one({"email":data["email"], "password":data["password"]})
    
    # exception handling for creating session
    try:
        # check if there is user with given email and password
        if (data["email"] == user_found["email"] and data["password"] == user_found ["password"]):
            # create a session for this user 
            user_uuid = create_session(user_found["email"])
            # return a uuid and user's email
            res = {"uuid": user_uuid, "email": data['email']}
            return Response(json.dumps(res), status=200, mimetype='application/json') 
    except Exception:
            # return error message if there is no user in db with given email
            return Response('No user found with given email or password', status=400, mimetype='application/json')

###### 3: Search Product ###### 
@app.route('/searchProduct', methods=['GET'])
def search_product():
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    # pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
    
    # check if uuid is the same one with uuid given by user
    if is_session_valid(uuid):
        #search for user with the given email in order to perform operation
        user_session = users.find_one({"email":data["email"]})
        if user_session: #if found
            if user_session["category"] == "user": #check for his category- user category required for this action

                #search by name
                if "p_name" in data:
                    products_list = [] # create a list to store products
                    same_products = list(products.find({"p_name" : {"$regex" : data['p_name']}})) #find products that contain p_name
                    if len(same_products) == 0: #if no products found
                        return Response("No products found with the name " + data['p_name'], status=500, mimetype="application/json")
                    for product in same_products: #else, for every product found
                        product['_id'] = str(product['_id']) #string conversion for _id
                        products_list.append(product) #append product to list
                        products_sorted_list = sorted(products_list,  key=lambda products: data['p_name']) #sort list
                    return Response(json.dumps(products_sorted_list, indent=2), status=200, mimetype='application/json') # successful response
                #search by category
                elif "p_category" in data:
                    products_list = [] # create a list to store students
                    same_c_products = list(products.find({"p_category" : data['p_category']})) #find products with the same p_category as the one given
                    if len(same_c_products) == 0: #if no products found
                        return Response("No products found in requested category ", status=500, mimetype="application/json")
                    for product in same_c_products: #else, for every product found
                        product['_id']=str(product['_id']) #string conversion for _id
                        products_list.append(product) #append product to list
                        products_sorted_list=sorted(products_list,  key=lambda products: product['price']) #sort list
                    return Response(json.dumps(products_sorted_list, indent=2), status=200, mimetype='application/json') # successful response
                #search by _id
                elif "_id" in data:
                    oid_str = data['_id'] #string conversion
                    oid2 = ObjectId(oid_str)
                    found_product = products.find_one({"_id" : oid2}) #find product with given _id
                    if found_product == None:
                        return Response("No product found with given id", status=500, mimetype="application/json")
                    else:
                        product ={"product name": found_product['p_name'], "product category": found_product['p_category'], "stock": found_product['stock'], "description": found_product['descr'], "price": found_product['price']}
                    # successful response
                    return Response(json.dumps(product, indent=2), status=200, mimetype='application/json')
                else:
                    return Response("Insert p_name or p_category or _id to searxh products", status=500, mimetype='application/json')
            else: # unsuccessful response
                return Response("Only users can perform this operation", status=500, mimetype='application/json')
        else: # unsuccessful response
                return Response("No user found with given email", status=500, mimetype='application/json')
    else: # if uuid is not the correct one
        return Response("User not Authenticated",status=401, mimetype='application/json') # return error message

###### 4: Add Product to Cart ######
@app.route('/addToCart', methods=['PATCH'])
def add_to_cart():

    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "password" in data or not "_id" in data or not "quantity" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    #pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
    
    # check if uuid is the same one with uuid given by user
    if not is_session_valid(uuid):
        cartTotal = 0
        user_session = users.find_one({"email":data["email"]}) #search for user with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"] == "user": #check for his category- user category required for this action
                oid_str = data['_id'] #string conversion
                oid2 = ObjectId(oid_str)
                found_product = products.find_one({"_id" : oid2}) #find product with given _id
                if found_product == None: #if not found
                    return Response("No product found with given id", status=500, mimetype='application/json')
                if int(data['quantity']) <= found_product['stock']: #check if there is enough stock
                    #if user has no total
                    if "Total" not in user_session:
                        users.update_one({"email": data["email"]},{"$set":{ "Total": found_product['price'] * int(data['quantity'])}})
                   #else:
                    if "Total" in user_session: 
                        cartTotal = user_session["Total"]
                        cartTotal +=  found_product['price'] * int(data['quantity'])
                        users.update_one({"email": data["email"]},{"$set":{ "Total": cartTotal}})
                    
                        #make cart
                    users.update_one({"email": data["email"]},{"$push":{ "cart": {"_id":oid2,'p_name':found_product['p_name'], 'p_category':found_product['p_category'], 
                                                                                    'descr':found_product['descr'], 'price':found_product['price'], 'quantity': data['quantity']}}}) #add item to cart
                        #print cart
                    if "cart" in user_session:
                            cartlist = []
                            for i in user_session['cart']:               
                                i["_id"] = str(i['_id'])
                                cartlist.append(i)                                              
                    return Response("Item added. Total is: "+ str(cartTotal),status=200, mimetype='application/json')
                else: #if not enough stock
                    return Response("Out of stock",status=200, mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only users can perform this operation", status=500, mimetype='application/json')
        else: #no user found
            return Response("No user found with this email", status=500, mimetype='application/json')

    # if uuid is not the correct one        
    else: # return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')

###### 5: Show Cart ######
@app.route('/showCart', methods=['GET'])
def show_cart():

    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    #pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
    
    # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]}) #search for user with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"] == "user": #check for his category- user category required for this action
                if "cart" in user_session:
                    cartlist = []
                    for i in user_session['cart']:               
                        i["_id"] = str(i['_id'])
                        cartlist.append(i)
                    # if true
                    return Response(json.dumps(cartlist), status=200, mimetype='application/json')

                else:
                    return Response("Cart is empty", status=500, mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only users can perform this operation", status=500, mimetype='application/json')
        else:
            return Response("No user found with this email", status=500, mimetype='application/json')

    # if uuid is not the correct one        
    else:
        # return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')

###### 6: Remove Item from Cart ######
@app.route('/removeItem', methods=['PATCH'])
def remove_item():
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data or not "_id" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    # pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
    
    # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]}) #search for user with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"] == "user": #check for his category- user category required for this action
                oid_str = data['_id']
                oid2 = ObjectId(oid_str)
                found_product = products.find_one({"_id" : oid2})
                hasCart = users.find_one({"email": data["email"], "cart": {"$exists": "true", "$ne": ""}})
                if hasCart: # if true
                    user_session = users.update_one({"email": data["email"]},
                                                {"$pull":
                                                {
                                                    "cart": {"$elemMatch":{"_id": oid2}}
                                                }
                                                }) #update orderhistory                   
                  
                    return Response("Item with _id "+data['_id']+" was successfully removed from cart", status=200, mimetype='application/json')  
                else:
                    return Response("Cart is empty", status=500, mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only users can perform this operation", status=500, mimetype='application/json')
        else:
            return Response("No user found with this email", status=500, mimetype='application/json')
    # if uuid is not the correct one        
    else:# return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')

###### 7: Purchase ######
@app.route('/purchase', methods=['PATCH'])
def purchase():

    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data or not "card" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    #pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
        # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]}) #search for user with the given email in order to perform operation
        if user_session:#if found
            if user_session["category"]=="user": #check for his category- user category required for this action
                if len(str(data['card'])) == 16 : #check card validity
                    user_session = users.update_one({"email": data["email"]},
                                                {"$set":
                                                {
                                                    "orderHistory": user_session['cart']
                                                }
                                                }) #update orderhistory
                    user_session = users.update_one({"email": data["email"]},
                                                {"$unset":
                                                {
                                                    "cart": 1
                                                }
                                                }) #clear cart
                    return Response("Purchase successful", status=500, mimetype='application/json')
                    
                else:# not valid card number
                    return Response("Card number " + data['card'] + " is not valid", status=500, mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only users can perform this operation", status=500, mimetype='application/json')
        else:
            return Response("No user found with this email", status=500, mimetype='application/json')

    # if uuid is not the correct one        
    else:
        # return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')     

###### 8: Show Order History ######     
@app.route('/showOrderHistory', methods=['GET'])
def show_order_history():

    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    #pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
    
    # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]})#search for user with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"]=="user":#check for his category- user category required for this action
                    if "orderHistory" in user_session:
                        historylist = []
                        for i in user_session['orderHistory']:               
                            i["_id"] = None
                            historylist.append(i)
                    
                        return Response(json.dumps(historylist), status=200, mimetype='application/json')
                    else:
                        return Response("Order History is empty", status=500, mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only users can perform this operation", status=500, mimetype='application/json')
        else:
            return Response("No user found with this email", status=500, mimetype='application/json')

    # if uuid is not the correct one        
    else:
        # return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')

###### 9: Delete Account ######
@app.route('/deleteAcc', methods=['DELETE'])
def delete_account():
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    # pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
    
    # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]})#search for user with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"]=="user":#check for his category- user category required for this action
                try: 
                    if user_session['email'] == data['email'] and user_session['password'] == data['password']:
                        users.delete_one({"email": data["email"]})
                        return Response("Account with email "+ data['email'] +" was successfully deleted",status=500,mimetype='application/json')
                except Exception :
                    return Response("No user found with given email",status=500,mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only users can perform this operation", status=500, mimetype='application/json')
        else:
            return Response("No user found with this email", status=500, mimetype='application/json')
    # if uuid is not the correct one        
    else:
        return Response("User not Authenticated",status=401, mimetype='application/json') # return error message

######################################################## USERS OPERATIONS #########################################################

###### 1: Create Admin ######
@app.route('/addAdmin' , methods=['POST'])
def add_admin():
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "name" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

# Check if there is a user with the same email in the db    
    if users.count_documents({"email":data["email"]})== 0 :
        # create user inserting username, password
        user = { 
        "email": data['email'],
        "name": data['name'],
        "password": data['password'],
        "category":"admin"
        }
        # Add user to the 'users' collection
        users.insert_one(user)
        # successful response
        return Response("Admin with email " + data['email'] + " was added to the MongoDB", status=200, mimetype='application/json')
    else:
        # unsuccessful response
        return Response("An admin with the given email already exists", status=400, mimetype='application/json')

###### 2: Insert Product ######
@app.route('/insertProduct' , methods=['POST'])
def insert_product():
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data or not "p_name" in data or not "p_category" in data or not "stock" in data or not "descr" in data or not "price" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    # pass uuid to the headers of the request
    uuid = request.headers.get('authorization')
    
    # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]}) #search for admin with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"] == "admin": #check for his category- user category required for this action
                # create product inserting product info
                product = { 
                "p_name": data['p_name'],
                "p_category": data['p_category'],
                "stock": data['stock'],
                "descr": data['descr'],
                "price": data['price']
                }
                # Add producy to the 'products' collection
                products.insert_one(product)
                # successful response
                return Response("Product was successfully added to the MongoDB", status=200, mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only admins can perform this operation", status=500, mimetype='application/json')
        else:
            return Response("No admin found with given email", status=500, mimetype='application/json')
    # if uuid is not the correct one        
    else:
        # return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')

###### 3: Delete Product ######
@app.route('/deleteProduct' , methods=['DELETE'])
def delete_product():
    
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "password" in data or not "_id" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    
    # pass uuid to the headers of the request
    uuid = request.headers.get('authorization')

    # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]}) #search for admin with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"] == "admin": #check for his category- user category required for this action
                oid_str = data['_id']
                oid2 = ObjectId(oid_str)
                if products.count_documents({"_id": oid2}) == 0 :
                    return Response("Product not found in db", status=500, mimetype="application/json")
                else:
                    products.delete_one({"_id": oid2})
                    # successful response
                    return Response("Product was successfully deleted from MongoDB", status=200, mimetype='application/json')
            else:
                # unsuccessful response
                return Response("Only admins can perform this operation", status=500, mimetype='application/json')
        else:
            return Response("No admin found with given email", status=500, mimetype='application/json')
    # if uuid is not the correct one        
    else:
        # return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')

###### 4: Update Product ######
@app.route('/updateProduct', methods=['PATCH'])
def update_product():
    
    # Request JSON data
    data = None 
    # exception handling for data loading
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "password" in data or not "_id" in data :
        return Response("Information incomplete", status=500, mimetype="application/json")
    # pass uuid to the headers of the request
    uuid = request.headers.get('authorization')

    # check if uuid is the same one with uuid given by user
    if  not is_session_valid(uuid):
        user_session = users.find_one({"email":data["email"]}) #search for admin with the given email in order to perform operation
        if user_session: #if found
            if user_session["category"] == "admin": #check for his category- user category required for this action
                oid_str = data['_id']
                oid2 = ObjectId(oid_str)
                if products.count_documents({"_id": oid2}) == 0 :
                    return Response("Product not found in db", status=500, mimetype="application/json")
                else:
                    if "p_name" in data: #update product name
                        products.update_one({"_id": oid2},
                                            {"$set": { "p_name": data["p_name"] } }
                                        )
                    if "price" in data: #update product price
                        products.update_one({"_id": oid2},
                                            {"$set": { "price": data["price"] } }
                                        )
                    if "descr" in data: #update product description
                        products.update_one({"_id": oid2},
                                    {"$set": { "descr": data["descr"] } }
                                   )
                    if "stock" in data: #update product stock
                        products.update_one({"_id": oid2},
                                    {"$set": { "stock": data["stock"] } }
                                   )
                return Response("Product was successfully updated", status=200, mimetype='application/json')
       
            else:
                return Response("Only admins can perform this operation", status=500, mimetype='application/json') # unsuccessful response
        else: 
            return Response("No admin found with given email", status=500, mimetype='application/json') # unsuccessful response
    else: # if uuid is not the correct one 
        # return error message
        return Response("User not Authenticated",status=401, mimetype='application/json')

# Εκτέλεση flask service σε debug mode, στην port 5000.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)