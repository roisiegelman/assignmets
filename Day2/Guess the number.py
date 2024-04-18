import random 
y=int(random.randint(1,20))
z=0 
while (z==0):
    x=int(input("What is your guess?" )) 
    if x == y: 
        z=1 
        print(f"Congrats! The number was {y} \n") 
    elif x < y: 
        print("Guess again, your number is too small! \n")
    elif x > y: 
        print("Guess again, your number is too large! \n")