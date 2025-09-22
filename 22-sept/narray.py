import numpy as np

arr1 = np.array([10,20,30,40,50])

arr2= np.array([[10,20,30],[10,20,30]])

print(arr1)
print(arr2)

marks= np.array([80,70,60,31,42])
print(min(marks))
print(marks.min())

print("first 2 elements: ", marks[::2])
print("highest to lowest marks: ", np.sort(marks)[::-1])