# import sys

# value = 2
# # print("value is " , value)
# # print(f"vlaue is : {value}")
# print(sys.float_info)

# kettle_boiled = True

fxn1 = ''' def get_input():
    name = input("Enter name")
    age = int(input("Enter age"))
    return name, age

def validate_input(age):
    if(age>18):
        return "valid"
    else:
        return "invalid"
    
def save(answer):
    return ("user is :" + answer)

def register_user():
    name, age = get_input()
    answer = validate_input(age)
    db = save(answer)
    return db


database = register_user()
print(f"answer is that the {database}")

'''

comprehentions = """

characteristics = {
    "pallavi" : ["analytical", "irritable", "caring"],
    "ga" : ["loyal", "composed", "caring"],
    "lakshay" : ["irritable", "analytical", "disciplined"]
}

unique = {quality for person in characteristics.values() for quality in person}
print(unique)

# infinite generators (comprehensions)

def print_coupons():
    print(f"welcome to coupon printing")
    count = 1
    while True:               #infinite loop, but still runs till specified, saving m/m
        print(f"generating coupon: ")
        yield f"coupon number {count} printed"
        count += 1

reprint = print_coupons()
for _ in range(5):
    print(next(reprint))

"""

