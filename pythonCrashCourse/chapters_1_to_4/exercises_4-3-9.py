#page 60 
#4-3 count to twenty inclusive list 
numberlist=[]
for value in range(1,21):
    numberlist.append(value)
print(numberlist)
#4-4 loop to a million print each number 
#for value in range(1,1000001): 
#    print(value)

#4-5 sum of millions 
millions=[]
for value in range(1,1000001):
    millions.append(value)
max_million = max(millions)
min_million = min(millions)
sum_million = sum(millions)
print(max_million)
print(min_million)
print(sum_million)

#4-6 odd list 
oddlist=[]
for value in range(1,21,2):
    oddlist.append(value)
print(oddlist)
    
#4-7 multiples of 3 
threelist = []
for value in range(0,31,3):
    threelist.append(value)
print(threelist)
#4-8 cubes
cubes =[]
for value in range(1,11):
    cube = value**3
    cubes.append(cube)
print(cubes)
#4-9 cube comprehension 
cubes2 = [value**3 for value in range(1,11)]
print(cubes2)