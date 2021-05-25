import pymongo
import pandas as pd


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["test_database"]

# ------------------------------- collection CPN        -----------------
filepath = "./datasources/database_input.csv"
with open(filepath) as infile:
    df = pd.read_csv(infile, sep=",")

# convert "CPN" to "_id" as string
df.CPN = df.CPN.astype(str)
df.rename(columns={"CPN": "_id"}, inplace=True)
new_data = df.to_dict('records')

collection = db["cpn"]

for element in new_data:
    result = collection.replace_one({"_id": element["_id"]}, element, upsert=True)
    if result.upserted_id:
        print("inserted: {}".format(element))
    elif result.modified_count:
        print("modified: {}".format(element))


# ------------------------------- collection allocation -----------------
filepath = "./datasources/data_table.csv"
with open(filepath) as infile:
    df = pd.read_csv(infile, sep=",")

# convert "CPN" to "_id" as string
df.CPN = df.CPN.astype(str)
df.rename(columns={"CPN": "_id"}, inplace=True)
new_data = df.to_dict('records')
allocation = db["allocation"]

for element in new_data:
    result = allocation.replace_one({"_id": element["_id"]}, element, upsert=True)
    if result.upserted_id:
        print("inserted: {}".format(element))
    elif result.modified_count:
        print("modified: {}".format(element))