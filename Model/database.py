from pymongo import MongoClient,errors
from dotenv import load_dotenv, dotenv_values
import os

class MongoDB:

    def __init__(self):
            load_dotenv()
            self.client = None
            self.db = None
            self.collection = None
            try:
                 
                self.connect_to_mongodb()
            except Exception as err:
                print("There is an errrrrrrrrrror!\neroooooooooooooor")

    def connect_to_mongodb(self):
        try:
            atlas_uri = os.getenv("ATLAS_URI")
            db_name = os.getenv("DB_NAME")

            self.client = MongoClient(atlas_uri)
            self.db = self.client[db_name]
            self.collection = self.db["products"]
            # Ping the database to ensure connection is successful
            self.client.admin.command("ping")
            print("Mongodb connected successfully")
        except errors.ServerSelectionTimeoutError as err:
            print(f"Failed to connect to MongoDB: {err}")
        except errors.ConnectionFailure as err:
            print(f"MongoDB connection error: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def get_collection(self):
        return self.collection 


