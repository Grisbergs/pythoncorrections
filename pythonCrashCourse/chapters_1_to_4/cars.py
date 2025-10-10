cars = ['bmw','audi','toyota', 'subaru']
cars.sort()
print(cars)
cars.sort(reverse=True)
print(cars)

cars = ['bmw','audi','toyota', 'subaru']
print("Here is the original list:")
print(cars)
print("\nHere is the sorted liste:")
print(sorted(cars))
print("\nHere is the original list again:")
print(cars)

cars.reverse()
print(cars)

len(cars)
#page 45  TIY  
#3-8 seeing world create list 
places= ['england','france','japan','russia','canada','austrailia','germany']
print("\nPlaces:")
#print in order
print(places)
#print sorted 
print("\n Sorted Places:")
print(sorted(places))
#show not changed 
print("\n places still the same:")
print(places)
#reverse order  
print("\nplaces in reverse:")
places.reverse()
print(places)
print("\nplaces returned:")
places.reverse()
print(places)
#print sorted alph list 
print("\nplaces sorted Alpha:")
places.sort()
print(places)
#reverse sort alpha
print("\nplaces sorted in revers alpha:")
places.sort(reverse=True)
print(places)
