#page 58
squares=[]
for value in range(1,11):
    square = value**2
    squares.append(square)
    
print(squares)

#append directly 
squares2=[]
for value in range(1,11):
    squares2.append(value**2)
    
print(squares2)

#statistics page 59
digits = [1,2,3,4,5,6,7,8,9,0]
print(min(digits))
print(max(digits))
print(sum(digits))