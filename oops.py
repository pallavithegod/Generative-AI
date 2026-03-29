class Dog:
    breed = "pomerian"

    def __init__(self, color, size = "medium"):         #constructor
        self.color = color
        self.size = size

    def __str__(self):                                  #for displaying
        return f"{self.breed} : {self.size}, {self.color}"

    
dog1 = Dog("White", "Small")
dog1.breed = "Chihuahua"
print(dog1)
    
dog2 = Dog("Brown")
print(dog2)

# GETTER AND SETTER
class Sparrow:

    def __init__(self, age):
        self._age = age        # _age used as pvt var : so differentiate easily, preventing an infinite loop of calling getter and setter
    
    @property                  #GETTER
    def age(self):
        return self._age + 2
    
    @age.setter                #SETTER
    def age(self, value):      #value = age passed
        if 1<= value <= 5:
            self._age = value
        else:
            raise ValueError("Age must be b/w 1 to 5 years")    


bird1 = Sparrow(2)
print(bird1.age)

bird2 = Sparrow(5)       #GETTER
print(bird2.age)       
bird2.age = 6            #SETTER = VALUE ERROR