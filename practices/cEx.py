class User():
    def __init__(self, name,age):
    	self.name = name
    	self.age = age

    def speakName(self):
    	print(f"I am {self.name} and {self.age} years Old!")

    def changeName(self, newName):
    	self.name = newName

def main():
	firstUser = User("Name", 999)
	firstUser.speakName()

if __name__ == "__main__":
	main()
