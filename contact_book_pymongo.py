# NOTE : Adding the new contact in mongodb

from pymongo import MongoClient
from bson import (
    ObjectId,
)  # used to give the access to the ObjectId which is used to delete the unique document from the collection of the database.


# Setting the connection between python and mongodb and creating the database and collection as name mentioned in the [square-brackets]
connectionEstablish = MongoClient("") # TODO: place mongodb connecting string in the brackets
database = connectionEstablish["Contact-Book"]
collection = database["Favouriate-Contacts"]


def AddingNewContact():
    """This function is used to add the new contact in the contact book"""

    # asks for how many contacts do you want to add in document
    no_of_contacts = int(input("How many contancts do you want to save?\n"))
    encounter_variable = 0
    # while loop is used so that user can enters the documents as much as he inputed in the "no_of_contacts" named variable
    while encounter_variable != no_of_contacts:
        # details of the contacts for inputing in the document starts
        contact_name = str(input("Name: "))
        query1 = {"Name": contact_name.title()}
        # used to track the name, if the name is already present in the document then user must have to enter the new name else he can proceeds
        tracked_name = collection.find_one(query1)
        if tracked_name:
            print("WARNING: Entered name is already present, please enter new name\n")
            continue
        else:
            # this inner loop is used to verify that no duplicay of phone number is entered, if found then it will show the WARNING message else it will continue to ask the furthur details.
            while True:
                contact_phone_number = int(input("Phone Number: "))
                query2 = {"Phone Number": contact_phone_number}
                # used to track the phone number, if the phone number is already present in the document then user must have to enter the new phone number else he can proceeds
                tracked_phone_number = collection.find_one(query2)
                if tracked_phone_number:
                    print(
                        "WARNING: Entered phone number is already present, please enter new phone number\n"
                    )
                    continue
                else:
                    contact_address = str(input("Address: "))
                    contact_occupation = str(input("Occupation: "))
                    # details ends here
                    keys = ["Name", "Phone Number", "Address", "Occupation"]
                    values = [
                        contact_name.title(),
                        contact_phone_number,
                        contact_address.title(),
                        contact_occupation.title(),
                    ]
                    document = {}
                    for i in range(4):
                        document.update({keys[i]: values[i]})
                    document_id = collection.insert_one(document)
                    print(f"Document successfully added and it's id is: {document_id}")
                    encounter_variable += 1  # increments the encounter_variable
                    break  # breaks the inner loop and goes to the outer loop after incrementing the encounter_variable



def UpdateContact():
    """ReNaming the contact name,occupation,phone number, address in mongodb"""
     # --------------------------------------------------
    def updateContactName():
        """Updates the name of the contact entered by the user"""
        new_name = str(input("New name: "))
        updated_query = {"$set": {"Name": new_name.title()}}
        old_query = {"Name": edit_contact_name.title()}
        result = collection.update_one(old_query, updated_query)
        if result.modified_count > 0:
            print("Successful😊")
        else:
            print("Unsuccessful☹️, Something went wrong!")
            updateContactName()
     # --------------------------------------------------
    def updateContactPhoneNumber():
        """Updates the phone number of the contact entered by the user"""
        old_phone_number = int(input("Old Phone Number: "))
        query = {"Phone Number": old_phone_number}
        if collection.find_one(query):
            print("Match Found✅")
            new_phone_number = int(input("New Phone Number: "))
            updated_query = {"$set": {"Phone Number": new_phone_number}}
            collection.update_one(query, updated_query)
            print(f"Successful😊")
        else:
            print("Match Not Found❌\nPlease try again!")
            updateContactPhoneNumber()
    # --------------------------------------------------
    def updateContactAddress():
        """Updates the address of the contact entered by the user"""
        old_contact_address = str(input("Old Contact Address: "))
        query = {"Address": old_contact_address.title()}
        if collection.find_one(query):
            print("Match Found✅")
            new_contact_address = str(input("New Contact Address: "))
            updated_query = {"$set": {"Address": new_contact_address.title()}}
            collection.update_one(query, updated_query)
            print(f"Successful😊")
        else:
            print("Match Not Found❌\nPlease try again!")
            updateContactAddress()
    # --------------------------------------------------
    def updateContactOccupation():
        """Updates the occupation of the contact entered by the user"""
        old_occupation = str(input("Old Occupation: "))
        query = {"Occupation": old_occupation.title()}
        if collection.find_one(query):
            print("Match Found✅")
            new_occupation = str(input("New Occupation: "))
            updated_query = {"$set": {"Occupation": new_occupation.title()}}
            collection.update_one(query, updated_query)
            print(f"Successful😊")
        else:
            print("Match Not Found❌\nPlease try again!")
            updateContactOccupation()
    # --------------------------------------------------
    def searchingElementInDocument():
        """This function is used to direct the program to their required functions to perform the task"""
        ask_for_update = str(
            input(
                "Which field do you want to update?\n(name, phone number, address, occupation)\n"
            )
        )
        convert_ask_for_update = ask_for_update.lower()
        if "name" == convert_ask_for_update:
            updateContactName()
        elif "phone number" == convert_ask_for_update:
            updateContactPhoneNumber()
        elif "address" == convert_ask_for_update:
            updateContactAddress()
        elif "occupation" == convert_ask_for_update:
            updateContactOccupation()
    # --------------------------------------------------
    
    # ----------------------------------------------------------------------------
    # Matching the contact name in database, so that we can edit the requirements as per the user.
    edit_contact_name = str(input("Name of the person which you want to update: "))
    query = {
        "Name": edit_contact_name.title()
    }  # Creating the query for searching the document in database.

    # Matching the query in the database and counting the matched contacts
    if collection.find_one(query):
        print("Match Found✅")
        if (
            collection.count_documents(query) > 1
        ):  # counts the number of contacts of same name
            print(f"{collection.count_documents(query)} contacts matched!")
            searchingElementInDocument()
        elif collection.count_documents(query) == 1:
            print(f"{collection.count_documents(query)} contact is matched!")
            searchingElementInDocument()
        else:
            None
    else:
        print("Match Not Found❌")



def DeletingExistingContact():
    """Deleting the contact present in the mongodb database"""
    name_to_be_deleted = str(input("Enter the name which you want to delete-\n"))
    # sets the query which is used to track the document in the collection and delete it smoothly
    query = {"Name": (name_to_be_deleted).title()}
    # this conditional statement checks that whether the entered document is present in the database or not
    if collection.find_one(query):
        print("Match Found✅")
        if (
            collection.count_documents(query) > 1
        ):  # This will execute only if matches are more than 1
            # this for* loop is used to print all the matched dacument present in the collection
            all_documents = collection.find(query)
            i = 1  # encounter variable
            for documents in all_documents:
                print(f"{i}. {documents}\n\n")
                i += 1

            document_id = str(
                input(
                    "Enter the id of the contact to delete it: \nNOTE: Only enter the content written in the single inverted commas ''\n"
                )
            )  # this is used to uniquely identify the document and delete the corresponding document

            tracked_document = collection.find_one(
                {"_id": ObjectId(document_id)}
            )  # this is used to track the document in the collection and the conditional statements are written so that if the document is found then in that case it will delete it and returns a confirmation message to the user else notify the user that no such document is found in the database
            if tracked_document:
                collection.delete_one(tracked_document)
                print("Contact deleted successfully")
            else:
                print("No such contact is founded in the contact book")

        else:  # This will only execute if match count is 1
            
            # asking for valid input from the user if user enters the absurd input then this loop will continuously run and if the input is valid then matched document will delete and loop will break out with a confirmation message
            while True:
                confirmation = str(
                input(f"Are you sure that you want to delete it?\nyes or no: ")
            )
                if "y" in confirmation.lower():
                    collection.delete_one(query)
                    print("Document successfully deleted")  # confirmation message
                    break
                elif "n" in confirmation.lower():
                    print("Document is not deleted!")
                    break
                else:
                    print("Please enter the valid input")
                    continue
    else:
        print("Match Not Found❌")



# Below piece of code is used to call the above functions according to the user choice and exit from the program

def ExitingFromFunction():
    """This function is used to exit from the program"""
    ask_user = str(input("Do you want to exit?\n"))
    if "y" in ask_user.lower() :
        exit(0)
    elif "n" in ask_user.lower():
        ContactBook()
    else:
        ExitingFromFunction()

def ContactBook():
    while True:
        user_choice = str(input("What do you want to do?\n1. Adding New Contact\n2. Update Contact\n3. Deleting Existing Contact\n"))
        if "ad" in user_choice.lower():
            AddingNewContact()
            ExitingFromFunction()
            break
        elif "up" in user_choice.lower():
            UpdateContact()
            ExitingFromFunction()
            break
        elif "de" in user_choice.lower():
            DeletingExistingContact()
            ExitingFromFunction()
            break
        else :
            print("Invalid Input!")
            continue


# Calling the contact book code 
ContactBook()