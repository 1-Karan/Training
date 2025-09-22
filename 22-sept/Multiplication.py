def multitable(num):

    print("the mutiplication table of number is: ")

    for i in range(1, 11):
        Result =0
        Result = i * num
        print(Result)

number= int(input("enter your number: "))
multitable(number)

def multilpication_table(num):
    print(f"multiplication table of {num}")
    for i in range(1,11):
        print(f"{num}x{i} = {num * i}")

number=int(input("enter your number: "))
multilpication_table(number)

