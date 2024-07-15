
with open('coding_qual_input.txt', 'r') as file:
    lines = file.readlines()

    input_values = []
    grid = []

    max_x = 0
    max_y = 0

    for line in lines:
        parts = line.split()

        obj_type = parts[0]
        x = int(parts[1])
        y = int(parts[2])

        if x > max_x:
            max_x = x

        if y > max_y:
            max_y = y

        input_values.append((obj_type, x, y))

    grid = [[' ' for i in range(max_x + 1)] for j in range(max_y + 1)]

    for item in input_values:
        x = item[1]
        y = max_y - item[2]

        grid[y][x] = item[0]

    with open('output.txt', 'w') as file:
        for item in grid:
            # test = ''.join(item)
            file.write(''.join(item))
            file.write('\n')
            # print(item)
