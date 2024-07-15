
"""
The function that returns the string is called find_connected_sinks()
"""

from collections import deque

# This is used to avoid repetition of these literals
complements_directions = {
    'u': ['║', '╔', '╗', '╠', '╣', '╦', '*'],
    'd': ['║', '╚', '╝', '╠', '╣', '╩', '*'],
    'r': ['═', '╗', '╝', '╣', '╦', '╩', '*'],
    'l': ['═', '╔', '╚', '╠', '╦', '╩', '*'],
}

# A mapping of the different characters and directions they can potentially connect
complements = {
    '*': {
        'u': complements_directions['u'],
        'd': complements_directions['d'],
        'r': complements_directions['r'],
        'l': complements_directions['l'],
    },
    '═': {
        'u': [],
        'd': [],
        'r': complements_directions['r'],
        'l': complements_directions['l'],
    },
    '║': {
        'u': complements_directions['u'],
        'd': complements_directions['d'],
        'r': [],
        'l': [],
    },
    '╔': {
        'u': [],
        'd': complements_directions['d'],
        'r': complements_directions['r'],
        'l': [],
    },
    '╗': {
        'u': [],
        'd': complements_directions['d'],
        'r': [],
        'l': complements_directions['l'],
    },
    '╚': {
        'u': complements_directions['u'],
        'd': [],
        'r': complements_directions['r'],
        'l': [],
    },
    '╝': {
        'u': complements_directions['u'],
        'd': [],
        'r': [],
        'l': complements_directions['l'],
    },
    '╠': {
        'u': complements_directions['u'],
        'd': complements_directions['d'],
        'r': complements_directions['r'],
        'l': [],
    },
    '╣': {
        'u': complements_directions['u'],
        'd': complements_directions['d'],
        'r': [],
        'l': complements_directions['l'],
    },
    '╦': {
        'u': [],
        'd': complements_directions['d'],
        'r': complements_directions['r'],
        'l': complements_directions['l'],
    },
    '╩': {
        'u': complements_directions['u'],
        'd': [],
        'r': complements_directions['r'],
        'l': complements_directions['l'],
    },
}

def find_connected_sinks(file_path):
    # Get the file contents
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize variables used to track size of grid
    max_x = 0
    max_y = 0

    # Used to store the grid and lookup sinks separately.
    sinks = {}
    pipe_system = []
    
    # Create the grid
    for line in lines:
        parts = line.split()
        
        object_type = parts[0]
        x = int(parts[1])
        y = int(parts[2])

        # Bump the value of the max variables if necessary
        max_x = x if x > max_x else max_x
        max_y = y if y > max_y else max_y
        
        # Decide where to put the value
        if object_type == '*':
            source_position = (x, y)
        elif 'A' <= object_type <= 'Z':
            sinks[object_type] = (x, y)
        else:
            pipe_system.append((object_type, x, y))

    # Add the sinks to the pipe system
    for _, (x, y) in sinks.items():
        pipe_system.append(('*', x, y))

    # Function to check if coordinates are within bounds
    def is_within_bounds(x, y):
        return 0 <= x <= max_x and 0 <= y <= max_y
    
    # Directions: Up, Down, Left, Right
    directions = [(0, 1, 'u'), (0, -1, 'd'), (-1, 0, 'l'), (1, 0, 'r')]

    # Function to discover if pipes connect
    def pipes_connect(base_object, next_object, direction):
        if next_object in complements[base_object][direction]:
            return True
        else:
            return False
    
    # Function to find all connected sinks from the source
    def connect_sinks(start_pos):
        visited = set()
        queue = deque([start_pos])
        connected_sinks = set()
        current_object = '*'
        
        while queue:
            current_x, current_y = queue.popleft()

            # Don't go through the work if this node has been checked
            if (current_x, current_y) in visited:
                continue

            visited.add((current_x, current_y))

            # Get the current object
            for o, x, y in pipe_system:
                if (x, y) == (current_x, current_y):
                    current_object = o
                    break
            
            # Check all 4 directions
            for dx, dy, dir in directions:
                nx, ny = current_x + dx, current_y + dy

                if is_within_bounds(nx, ny):

                    # Check if it's a sink
                    for sink, (sx, sy) in sinks.items():
                        if (nx, ny) == (sx, sy):
                            if pipes_connect(current_object, '*', dir):
                                connected_sinks.add(sink)
                                queue.append((nx, ny))
                                break

                    # Also check if it's a pipe that connects
                    for pipe, px, py in pipe_system:
                        if (nx, ny) == (px, py):
                            if pipes_connect(current_object, pipe, dir):
                                queue.append((nx, ny))
                                break
        
        return connected_sinks
    
    # Find connected sinks starting from the source
    connected_sinks = connect_sinks(source_position)
    
    # Return connected sinks as a sorted string of uppercase letters
    return ''.join(sorted(connected_sinks))
