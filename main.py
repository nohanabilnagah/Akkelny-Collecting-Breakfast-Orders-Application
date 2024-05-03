from flask import Flask , render_template , request , redirect , session
import sqlite3 

DATABASE_NAME = "akkelny.db"
def db_control(query, fetch=True):
    connection = sqlite3.connect(DATABASE_NAME)
    cur = connection.cursor()
    cur.execute(query)
    if fetch:
        result = cur.fetchall()
        connection.commit()
        return result
    connection.commit()
    connection.close()


app =Flask(__name__)
app.secret_key= "akkelny"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/food")
def food():
    user_name = session.get("user_name" , None)
    workspace_id = session.get("workspace_id" , None)
    return render_template("food.html", info  = [user_name , workspace_id])

@app.route("/orders")
def orders():
    workspace_id = session.get("workspace_id" , None)
    if workspace_id != None :
        table_columns = [ "user_name", "Ta3meya" , "Ta3meya M7sheya" , "Ta3meya Ors" , "Sawab3" , "Fries" , "Fool Sada" , "Fool Eskandarany" , "Fool Taba2" , "Btengaan" , "Chipsy" ]
        table_data = db_control(f"SELECT  user_name ,  Ta3meya  ,  Ta3meya_M7sheya  ,  Ta3meya_Ors  ,  Sawab3  ,  Fries  ,  Fool_Sada  ,  Fool_Eskandarany  ,  Fool_Taba2  ,  Btengaan  ,  Chipsy  FROM orders WHERE workspace_id = {workspace_id} ")
        result = [dict(zip(table_columns , row))for row in table_data]
        workspace_name = db_control(f"select name FROM workspace WHERE id = '{workspace_id}'")
        return render_template("orders.html" , data= result , workspace = workspace_name)
    return render_template("orders.html")


# Handel add Workspace
@app.route("/add-workspace" , methods=["POST"])
def add_workspace():
    data = request.form
    user_name = data.get("user_name", None)
    workspace = data.get("Workspace_name", None)
    select_query  =f"""select id , name FROM workspace WHERE name = '{workspace}' """
    result = db_control(select_query)
    if len(result) != 0 :
        # if workspace is Exitis
        if result[0][1] == workspace :
            session["workspace_id"] = result[0][0]
            session["user_name"] = user_name
            return redirect("/food")
    else :
         #  Create New Workspace
     query = f"""INSERT INTO workspace (name , user_name) VALUES ( '{workspace}' ,' {user_name}')"""
     db_control(query=query , fetch=False)
     select_query  =f"""select id  FROM workspace WHERE name = '{workspace}' """ 
     id =  db_control(query=select_query)
     session["workspace_id"] = id[0][0]
     session["user_name"] = user_name
     return redirect("/food")

# Handel add Order add-order/Mohamed/6
@app.route("/add-order/<name>/<id>" , methods=["POST"])
def add_order(name , id ) :
    data =request.form
    Btengaan = data.get("Btengaan" , None)
    Chipsy = data.get("Chipsy" , None)
    Fool_Eskandarany = data.get("Fool Eskandarany" , None)
    Fool_Sada = data.get("Fool Sada" , None)
    Fool_Taba2 = data.get("Fool Taba2" , None)
    Fries = data.get("Fries" , None)
    Sawab3 = data.get("Sawab3" , None)
    Ta3meya_M7sheya = data.get("Ta3meya M7sheya" , None)
    Ta3meya_Ors = data.get("Ta3meya Ors" , None)
    Ta3meya = data.get("Ta3meya" , None)
    if name != "None" and id != "None":
            query = f""" INSERT INTO orders (user_name , workspace_id , Ta3meya , Ta3meya_M7sheya , Ta3meya_Ors , Sawab3 , Fries , Fool_Sada , Fool_Eskandarany , Fool_Taba2 ,Btengaan , Chipsy ) VALUES ( '{name}',  '{id}', '{Ta3meya}', '{Ta3meya_M7sheya}', '{Ta3meya_Ors}', '{Sawab3}', '{Fries}', '{Fool_Sada}', '{Fool_Eskandarany}', '{Fool_Taba2}', '{Btengaan}', '{Chipsy}'); """
            db_control(query , fetch=False)
    return redirect ("/orders")

# Submit Order 
@app.route("/submit-data")
def submit_order():
    workspace_id = session.get("workspace_id" , None)
    if workspace_id != None :
        workspace_id = session.get("workspace_id" , None)
        query = f""" DELETE FROM orders WHERE workspace_id = {workspace_id} """
        db_control(query , fetch=False)
        query = f""" DELETE FROM workspace WHERE id = {workspace_id} """
        db_control(query , fetch=False)
        session.pop("workspace_id" , None)
        session.pop("user_name" , None)
        return redirect("/")
    return redirect("/")


if __name__== "__main__" :
    app.run(host="127.0.0.1"  , port=5050 , debug=True)
