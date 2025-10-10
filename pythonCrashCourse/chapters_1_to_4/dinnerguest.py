#page 41 3-4
guests =['Ralph','Ryan','Kurt','John','William']
#testpush
print(guests)
print ("This is and invitation to dinner for "+ guests[0])
print ("This is and invitation to dinner for "+ guests[1])
print ("This is and invitation to dinner for "+ guests[2])
print ("This is and invitation to dinner for "+ guests[3])
print ("This is and invitation to dinner for "+ guests[4])

#3-5
print ( "John Can't maket it we will invite Sam instead.")
guests.remove("John")
guests.append("Sam")
print(guests)
print ("This is and invitation to dinner for "+ guests[0])
print ("This is and invitation to dinner for "+ guests[1])
print ("This is and invitation to dinner for "+ guests[2])
print ("This is and invitation to dinner for "+ guests[3])
print ("This is and invitation to dinner for "+ guests[4])

# page 45  3-9 
numberOfGuests = len(guests)
print(numberOfGuests)

#page 45 3-10  
cities = ['Atlanta','Chicago','New York City','Houston','New Orleans','Miami']
cities.sort(reverse= True)
print(cities)

print(sorted(cities))
cities.reverse()
print(cities)
cityCount = len(cities)
print(cityCount)



