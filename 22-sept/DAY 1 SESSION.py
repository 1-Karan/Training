print("hELLO")

def check_even_odd(num):
    if num % 2 == 0:
        return "number is even"

    else:
        return "number is odd"

number= int(input("enter a number"))
result = check_even_odd(number)
print(result)
