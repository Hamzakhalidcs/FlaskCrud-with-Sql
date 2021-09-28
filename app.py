import sys
import datetime
from flask import Flask, json, request, jsonify, json
from numpy import record

import pyodbc
import pandas as pd

try:
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-959UNBS;"
        "Database=mydb;"
        "Trusted_Connection=yes;"
    )

    print("Connected Succesfully")

except:
    print("Cannot connect to DB" + str(sys.exc_info()[1]))

app = Flask(__name__)


@app.route("/home", methods=["GET"])
def index():
    return "Hello World"


@app.route("/get_data", methods=["GET"])
def get_data():
    query = "SELECT * FROM [mydb].[dbo].[Table_1] order by PersonID ASC"
    data = pd.read_sql(query, conn).fillna("")
    obj = data.to_dict()
    return jsonify(obj)

@app.route("/post_data", methods=["POST"])
def post_data1():

    req_data = request.get_json()
    if "PersonID" not in req_data:
        return "PersonID is not given"

    if "first_name" not in req_data:
        return "first name is not available"

    if "last_name" not in req_data:
        return "last name is missing"

    print("REQ DATA IS: ", req_data)
    Person_id = req_data["PersonID"]
    first_name = req_data["first_name"]
    last_name = req_data["last_name"]
    modified_date = str(datetime.datetime.today())[:19]

    cursor = conn.cursor()
    query = """
    INSERT INTO [mydb].[dbo].[Table_1]
    (PersonID, FirstName, LastName, ModifiedDate) VALUES ({}, '{}', '{}','{}')
    """.format(
        Person_id, first_name, last_name, modified_date
    )
    print("QUERY: ", query)
    cursor.execute(query)
    cursor.commit()
    cursor.close()
    return jsonify(
        {
            "suscess": True,
            "data": {
                "PersonID": Person_id,
                "First Name": first_name,
                "Last Name": last_name,
                "ModifiedDate": modified_date,
            },
        }
    )


@app.route("/update_data/<person_id>", methods=["GET", "POST"])
def update_data(person_id):
    per_id = person_id
    req_data = request.get_json()
    if "first_name" not in req_data:
        return "first name is not available"

    if "last_name" not in req_data:
        return "last name is missing"

    print("REQ DATA IS: ", req_data)
    
    first_name = req_data["first_name"]
    last_name = req_data["last_name"]

    cursor = conn.cursor()
    update_query = """
    UPDATE [mydb].[dbo].[Table_1]
    SET FirstName= '{}', LastName = '{}' 
    WHERE PersonID={};""".format(first_name, last_name, per_id)
    print("QUERY: ", update_query)

    cursor.execute(update_query)
    cursor.commit()
    cursor.close()
    return jsonify(
        {
            "success": True,
        },
    )

@app.route('/delete_data/<person_id>', methods=["DELETE"])
def del_data(person_id):
    per_id = person_id
    
    cursor = conn.cursor()
    delete_query = """
    DELETE FROM [mydb].[dbo].[Table_1]
    WHERE PersonID={};""".format(per_id)
    print("QUERY: ", delete_query)

    cursor.execute(delete_query)
    cursor.commit()
    cursor.close()
    return jsonify(
        {
            "message" : "Data delete successfully"
        },
    )


if __name__ == "__main__":
    app.run(debug=True)
