def return_biggest_product(list):
    list.sort(reverse=True)
    product=list[0]*list[1]*list[2]
    return product

print(return_biggest_product([1, 10, 2, 6, 5, 3]))