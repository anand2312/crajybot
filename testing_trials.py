#testing,  something seems to be weird
#Popi do be lookin kinda poopi
#dmamb

print("Popi do be lookin kinda poopi")

class nigga:
    def __init__(self,first,last):
      self.first=first
      self.last=last
  
    def full_name(self):
      self.f_name="{} {}".format(self.first,self.last)
      #f_name = f"{self.first} {self.last}"
      print(self.f_name)

    def is_nigga(self):
      if self.f_name == "Shriram Shekar":
        return True

user1 = nigga("Shriram","Shekar")
user1.full_name()
if user1.is_nigga():
  print("popi")
