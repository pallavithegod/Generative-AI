from functools import wraps

def my_decorator(fxn1):

    @wraps(fxn1)      #preserves actual fucntion's metadata and doesn't change it's name to "wrapper"
    def wrapper_fxn():
        print("first line before fxn")
        fxn1()
        print("second line")
    return wrapper_fxn

@my_decorator   #to be called before fxn, if decorator required
def greet():
    print("inside fxn: hello!!!")

greet()
print(f"function name is : {greet.__name__}")        #dunder name


# ADMINISTRATIVE WORKS
def require_admin(func):
    @wraps(func)
    def checker_wrap(*args, **kwargs):
    # def checker_wrap(role):

        role = args[0]
        if role != "admin":                 #role take values as a tuple due to generic parameters
            print(f"Access denied: Admins Only")
            return None
        else:
            return func(role)
    return checker_wrap

@require_admin
def access_inventory(role):
    print(f"Access granted to the {role}")

access_inventory("user")
access_inventory("admin")
        