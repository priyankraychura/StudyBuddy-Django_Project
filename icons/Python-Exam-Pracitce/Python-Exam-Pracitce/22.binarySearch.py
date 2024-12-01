def binary_search(item_list, item):
    first = 0
    last = len(item_list) - 1
    found = False

    while first <= last and not found:
        mid = (first + last)//2

        if item_list[mid] == item:
            found = True
        else:
            if item_list[mid]:
                last = mid - 1
            else:
                first = mid + 1

    return found

list = [12, 55, 85, 96, 10, 44]
print(binary_search(list, 85))
print(binary_search(list, 21))
