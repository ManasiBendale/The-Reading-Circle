import random

records =[]
shuffled_records = []

#print("ID , Title, Main Owner, New Owner, BookId, UserId")
l = [["ID 1" , "Title 1", "Main Owner 1", "New Owner 1", "BookId 1", "UserId 1"],
     ["ID 2" , "Title 2", "Main Owner 2", "New Owner 2", "BookId 2", "UserId 2"],
     ["ID 3" , "Title 3", "Main Owner 3", "New Owner 3", "BookId 3", "UserId 3"]]

def shuffle_records(records):
    random.shuffle(records)
    shuffled_records.append(records)
    return shuffled_records
    
def book_swap(l):
    for record in l:
        records.append(record[3])
    result = shuffle_records(records)
    return result

print(book_swap(l))