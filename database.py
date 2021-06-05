# not needed anymore, using databasehandler.py instead
# still useful to refresh the database from csv if something got wrong


import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["test_database"]


def fill_update(collection, new_data):
    """ updates collection based on dictionary"""
    upserted = []
    modified = []
    for element in new_data:
        # result = collection.update_one({"_id": element["_id"]}, {'$currentDate':  {"lastModified": {'$type': 'date'}}}, upsert=True)
        result = collection.replace_one({"_id": element["_id"]}, element, upsert=True)
        if result.upserted_id:
            # print("inserted: {}".format(element))
            upserted.append(element["_id"])
            collection.update_one({"_id": element["_id"]}, {'$currentDate': {"lastModified": {'$type': 'date'}}})
        elif result.modified_count:
            # print("modified: {}".format(element))
            modified.append(element["_id"])
            collection.update_one({"_id": element["_id"]}, {'$currentDate': {"lastModified": {'$type': 'date'}}})
    return {"upserted": upserted, "modified": modified}


# ------------------------------- collection CPN        -----------------
filepath = "./datasources/database_input.csv"
with open(filepath) as infile:
    df = pd.read_csv(infile, sep=",")

# convert "CPN" to "_id" as string
df.CPN = df.CPN.astype(str)
df.rename(columns={"CPN": "_id"}, inplace=True)
cpn_dict = df.to_dict('records')

cpn = db["cpn"]

res = fill_update(collection=cpn, new_data=cpn_dict)
print(res)

# ------------------------------- collection allocation -----------------
filepath = "./datasources/data_table.csv"
with open(filepath) as infile:
    df = pd.read_csv(infile, sep=",")

# convert "CPN" to "_id" as string
df.CPN = df.CPN.astype(str)
df.rename(columns={"CPN": "_id"}, inplace=True)
alloc_dict = df.to_dict('records')
allocation = db["allocation"]

res = fill_update(collection=allocation, new_data=alloc_dict)
print(res)