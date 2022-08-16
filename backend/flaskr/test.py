data = [{1:"ebimo"}, {2:"hannah"}]
data.pop(0)
print(data)
xy =0
for x in data:
    if data[xy]:
        print(data[xy])

        if data[xy] == {2: 'Hannah'} :
            print("2")
        xy+=1
