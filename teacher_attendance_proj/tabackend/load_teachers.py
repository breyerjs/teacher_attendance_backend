from . import logic
import json

"""
This script takes in a json list of teachers (like the example below) and
loads them into the database.

It expects a json dump that looks like:
[
    {
          "username": "jacksonnnn",
          "email":  "jbreeyer@practicefusion.com",
          "password": "guest",
          "firstName": "Jackson",
          "lastName": "Breyer",
          "school_name": "Home",
          "school_city": "McLean"
    },
    ...
]

"""
def load_teachers(filename):
    _logic = logic.Logic()
    file_to_load = open(filename)
    text = file_to_load.readlines()
    text = "" .join([line.strip() for line in text])
    loaded_json = json.loads(text)
    num_loaded = 0
    num_errors = 0
    for teacher_blob in loaded_json:
        error = _logic.create_teacher(teacher_blob)
        username = teacher_blob.get('username')
        if error:
            num_errors += 1
            print("")
            print("Error loading {}:".format(username))
            print(error)
            print("")
        else:
            print("Successfully loaded {}".format(username))
            num_loaded += 1

    print("LOAD COMPLETE")
    print("Number of Teachers Loaded: {}".format(num_loaded))
    print("Number of Errors (teacher failed to load): {}".format(num_errors))