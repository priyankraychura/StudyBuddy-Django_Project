def insertion_sort(inputList):
    for i in range(1, len(inputList)):
        j = i - 1
        nxt_element = inputList[i]

        while(inputList[j] > nxt_element) and (j >= 0):
            inputList[j+1] = inputList[j]
            j =  j - 1
            inputList[j+1] = nxt_element

list = [12, 58, 5, 47, 11, 26, 3, 8, 99]
insertion_sort(list)
print(list)