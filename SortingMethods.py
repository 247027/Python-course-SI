import numpy as np

example_data = [np.random.randint(0, 100) for i in range(20)]
print(example_data)


def sort1(data):
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] < data[j]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp

    return print(data)


sort1(example_data)



