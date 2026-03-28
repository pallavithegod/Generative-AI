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


