from flask import Flask,render_template,jsonify,request
from pymongo import MongoClient
from bson import ObjectId
import json
database = MongoClient('localhost',27017)
myfolder = database["My_API"]
db = myfolder["Datas"]


app = Flask(__name__)


@app.route("/" ,methods=["GET"])
def HomePage():
    return render_template("index.html")



@app.route("/create" ,methods=["POST","GET"])
def create():
    in_data = request.get_json()


    try:
        name = in_data['Name']
        age = in_data['Age']
        db.insert_one({"Name":name,"Age":age})
        My_Response = jsonify({
            "Message": " Data Add In Data BAse "
                })

    except:
        My_Response = jsonify({
            "Message": " Error In Create API  "
                })
    return "My_Response"

@app.route("/read" ,methods=["GET"])
def read():

    data = db.find({})
    list_data = []
    for i in data:
        id=str(i["_id"])

        list_data.append({"Name":i['Name'],"Age":i['Age'],"Id":id})

    My_Response = jsonify({
        "Message": " Read ",
        "Data":list_data
            })
    return My_Response


@app.route("/update/<id>",methods=["GET","POST"])
def update(id):
    #  UPDATE

    data = request.get_json()

    name = data['Name']
    age = data['Age']
    myid = data['ID']
    db.update_one(
            {'_id':ObjectId(myid)},
            {'$set':{"Name":name,"Age":age}}
            )

    My_Response = jsonify({
        "Message": " Update "
            })
    return My_Response

@app.route("/delete/<id>" ,methods=["GET","POST"])
def delete(id):
    db.delete_one({"_id":ObjectId(id)})
    My_Response = jsonify({
        "Message": " Delete  Suceesfully",
            })
    return My_Response

if __name__=='__main__':
    app.run(debug=True)