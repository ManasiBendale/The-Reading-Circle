def swap_table(l):
    import random

    swapped_with =[]
    def shuffle_records(records):
        shuffled_records = random.sample(records, len(records))
        return shuffled_records

    def book_swap(l):
        records = [(record[0], record[3], record[5], record[2]) for record in l]
        shuffled = shuffle_records(records)
        swapped = set()
        
        #swapped table
        for i, record in enumerate(l):
            temp = record[3]
            # print("Previous owner : ",temp)
            while (record[0], shuffled[i][1]) in swapped or shuffled[i][1] == record[2] or shuffled[i][3] == record[3]:
                random.shuffle(shuffled)
            print("shuffled[i][1]",shuffled[i][1])
            record[3] = shuffled[i][1]
            swapped.add((record[0], record[3]))
            # print([record[3],temp])
            swapped_with.append([record[3],temp])
        return l,swapped_with

    l, swapped_books = book_swap(l)
    return l, swapped_books

l = [["ID 1" , "Title 1", "Main Owner 1", "New Owner 1", "BookId 1", "UserId 1"],
         ["ID 2" , "Title 2", "Main Owner 2", "New Owner 2", "BookId 2", "UserId 2"],
         ["ID 3" , "Title 3", "Main Owner 3", "New Owner 3", "BookId 3", "UserId 3"],
         ["ID 4" , "Title 4", "Main Owner 4", "New Owner 4", "BookId 4", "UserId 4"],
         ["ID 5" , "Title 5", "Main Owner 5", "New Owner 5", "BookId 5", "UserId 5"],
         ["ID 6" , "Title 6", "Main Owner 6", "New Owner 6", "BookId 6", "UserId 6"]]

l, swapped_with = swap_table(l)

# checking values
# print("\n",l)
# print("\n",swapped_with)