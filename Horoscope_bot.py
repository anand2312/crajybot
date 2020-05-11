#testing,  something seems to be weird
#Popi do be lookin kinda poopi
#dmamb

print("Popi do be lookin kinda poopi")

class nigga:
  
  def __init__(self,first,last):
    self.first=first
    self.last=last
  
  def full_name(self):
    f_name="{} {}".format(self.first,self.last)
    return f_name
    
  def is_nigga(self,name):
    if name=="Shriram Shekar":
      return True

user1=nigga("Shriram","Shekar")
name = user1.full_name()
if user1.is_nigga(name):
  print("popi")
