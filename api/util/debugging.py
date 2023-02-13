# import client
# api_key = client.client['api_key']

# functions for debugging
def printClassAttributes(className):
    for attribute, value in className.__dict__.items():
        print(attribute, '=', value)

def printClassMethods(className):
    method_list = [method for method in dir(className) if method.startswith('__') is False]
    print(method_list)

# conn = pyspectroworks.connect(api_key)
# projects = conn.get_projects()

# printClassAttributes(conn)
# printClassMethods(conn)
# print(dir(conn))

# project = projects[9]
# items = project.get_items()
# item = items[len(items) - 1]

# value = item.sample_attributes['Sample name']
# print("Attribute: ", value)

