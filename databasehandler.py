import pymongo
import pickle
from datetime import datetime
import pandas as pd


class DataBaseHandler(object):
    """handles MongoDB
    host_port: --host <host> --port <port> -u <user> -p <pwd> # omit the password if you want a prompt
    """

    def __init__(self, db_name, host_port="mongodb://localhost:27017/"):
        client = pymongo.MongoClient(host_port)
        self.db = client[db_name]
        self.cpn = self.db["cpn"]
        self.cats = self.db["cats"]
        self.alloc = self.db["allocation"]

    def fill_update(self, collection, new_data):
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
    
    def fill_cats(self, new_data):
        """deletes and refills the collection cats based on a list of dictionaries,
        adds the nr of the week to each row"""
        self.cats.delete_many({})
        for elem in new_data:
            elem["week"] = datetime.strptime(elem["day"], "%Y-%m-%d").isocalendar()[1]
        self.cats.insert_many(new_data)
        return



if __name__ == '__main__':
    DBH = DataBaseHandler(db_name="test_database")

    # cats from pickle to database
    with open('./datasources/cats.pickle', 'rb') as handle:
        new_data = pickle.load(handle)
    DBH.fill_cats(new_data=new_data)





    # # CPN
    # filepath = "./datasources/database_input.csv"
    # with open(filepath) as infile:
    #     df = pd.read_csv(infile, sep=",")
    #
    # # convert "CPN" to "_id" as string
    # df.CPN = df.CPN.astype(str)
    # df.rename(columns={"CPN": "_id"}, inplace=True)
    # new_data = df.to_dict('records')
    #
    # res = DBH.fill_update(DBH.cpn, new_data)
    # print(res)
    #
    # result = DBH.alloc.find({})
    # for elem in result: print(elem)


