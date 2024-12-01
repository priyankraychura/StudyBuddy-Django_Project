def shellSort(input_list):
    gap = len(input_list)//2

    while gap > 0:
        for i in range(gap, len(input_list)):
            temp = input_list[i]
            j  = i

            while j >= gap and input_list[j - gap] > temp:
                input_list[j] = input_list[j - gap]
                j = j - gap
                input_list[j] = temp

        gap = gap//2

list = [12, 25, 88, 45, 66, 85, 20]
shellSort(list)
print(list)