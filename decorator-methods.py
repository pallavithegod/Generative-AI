# STATIC MENTHOD
class Utils_:

    @staticmethod                     #decorator - makes fxn universally accessable
    def clean_string(str):
        return [i.strip() for i in str.split(",")]


raw = "pallavi,   jain   , girl"
cleaned  = Utils_.clean_string(raw)
# print(cleaned)  


# CLASS METHOD
class Characteristics:

    def __init__(self, hairs, height, weight):
        self.hairs = hairs
        self.height = height
        self.weight = weight

    @classmethod
    def parse_dict(cls, char_data):
        return cls(
            char_data["hairs"],
            char_data["height"],
            char_data["weight"],
        )
    
    @classmethod
    def parse_str(cls, char_data):
        hairs, height, weight = char_data.split("-")
        return cls(hairs, height, weight)
    

char1 = Characteristics("brown", "short", "thin")
print(char1)
print(char1.__dict__)                        #DUNDER
char3 = Characteristics.parse_str("black-tall-thin")
char2 = Characteristics.parse_dict({'hairs': 'black', 'height': 'tall', 'weight': 'healthy'})
print(char2.__dict__)

