number = input("Enter a number: ")
# assume the user enters 5.0
try:
 x = int(number)
 print("x is the integer", x)
except:
 x = float(number)
 print("x is the float", x)
