#!/usr/bin/env Python3
# -*- coding: utf-8 -*-


"""
Created on Wed Mar 19 19:26:23 2025

@author: peterstegall_snhu
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse

# Create AnimalShelter class
# used to interact with MongoDB database
class AnimalShelter:
          
    def __init__(self, username=None, password=None):
        # Initialize the DB once for each object instantiation
        self.client = None
        self.dataBase = None
        self._init_db(username, password)

    def _init_db(self, username=None, password=None):
        # URI must be percent escaped as per pymongo documentation
        userName = urllib.parse.quote_plus(username or 'aacuser')
        password = urllib.parse.quote_plus(password or 'abc123')

        # Correct format of the MongoDB URI
        uri = 'mongodb://localhost:27017'

        # Connect to the MongoDB client and initialize the database
        self.client = MongoClient(uri)
        self.dataBase = self.client['CS499']

    # Method to create a record
    def createRecord(self, data):
        if isinstance(data, dict) and data:
            try:
                insertValid = self.dataBase.animals.insert_one(data)
                return insertValid.acknowledged
            except Exception as e:
                print(f"Error inserting record: {e}")
                return False
        else:
            raise ValueError("Invalid data. Must be a non-empty dictionary.")

    # Method to get a document by its ID
    def getRecordById(self, postId):
        try:
            return self.dataBase.animals.find_one({'_id': ObjectId(postId)})
        except Exception as e:
            print(f"Error retrieving record by ID: {e}")
            return None

    # Get records with criteria
    def getRecordCriteria(self, criteria=None):
        try:
            query = criteria if isinstance(criteria, dict) else {}
            return list(self.dataBase.animals.find(query, {'_id': 0}))  # Convert cursor to list
        except Exception as e:
            print(f"Error retrieving records: {e}")
            return []
        
     # Method to update a record based on given criteria
    def updateRecord(self, find_criteria, update_data):
        if isinstance(find_criteria, dict) and isinstance(update_data, dict):
            try:
                result = self.dataBase.animals.update_many(find_criteria, {'$set': update_data})
                return result.modified_count  # Returns the number of documents modified
            except Exception as e:
                print(f"Error updating record: {e}")
                return 0
        else:
            raise ValueError("Both arguments must be dictionaries.")

    # Method to delete a record based on given criteria
    def deleteRecord(self, find_criteria):
        if isinstance(find_criteria, dict):
            try:
                result = self.dataBase.animals.delete_many(find_criteria)
                return result.deleted_count  # Returns the number of documents deleted
            except Exception as e:
                print(f"Error deleting record: {e}")
                return 0
        else:
            raise ValueError("Criteria must be a dictionary.")   
