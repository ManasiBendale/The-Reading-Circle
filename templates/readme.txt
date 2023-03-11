This code defines a function called book_swap that takes a list of book records as input and swaps the "New Owner" field of each record with the "New Owner" field of another randomly selected record in the list, subject to some conditions.

The function first converts each book record into a tuple containing the record's ID, BookId, UserId, and New Owner fields. It then shuffles this list of tuples and uses it to determine which record should be swapped with which other record.

For each record in the original list, the function attempts to swap the "New Owner" field with the corresponding field of the record at the same position in the shuffled list. If the swap violates one of three conditions, the function continues shuffling the list until a valid swap can be made.

The three conditions that must be satisfied for a swap to be valid are:

The same book cannot be swapped twice.
The new owner of the first book cannot be the same as the new owner of the second book.
The user ID of the first book cannot be the same as the user ID of the second book.
The function prints a message for each successful swap and returns the modified list of book records.

Finally, the code checks if all records have been swapped by comparing the number of unique (ID, New Owner, Main Owner) tuples in the modified list to the number of records in the list.

Note that the original list of book records is modified in place by this function, so the caller should make a copy of the list if the original needs to be preserved.