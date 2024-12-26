from collections import deque


def find_shortest_path_with_teleports(grid, start, end, teleports):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and grid[x][y] != '#'

    q_start = deque([start])
    q_end = deque([end])
    visited_start = {start: None}
    visited_end = {end: None}

    while q_start and q_end:

        if bfs_step(q_start, visited_start, visited_end, teleports, directions, is_valid):
            return reconstruct_path(visited_start, visited_end, start, end)

        if bfs_step(q_end, visited_end, visited_start, teleports, directions, is_valid):
            return reconstruct_path(visited_start, visited_end, start, end)

    return None


def bfs_step(queue, visited, other_visited, teleports, directions, is_valid):
    for _ in range(len(queue)):
        x, y = queue.popleft()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))
                if (nx, ny) in other_visited:
                    return True

        if (x, y) in teleports:
            tx, ty = teleports[(x, y)]
            if (tx, ty) not in visited:
                visited[(tx, ty)] = (x, y)
                queue.append((tx, ty))
                if (tx, ty) in other_visited:
                    return True
    return False


def reconstruct_path(visited_start, visited_end, start, end):
    path = []
    intersection = next(cell for cell in visited_start if cell in visited_end)
    cell = intersection
    while cell:
        path.append(cell)
        cell = visited_start[cell]
    path.reverse()

    cell = visited_end[intersection]
    while cell:
        path.append(cell)
        cell = visited_end[cell]

    return path


grid = [
    ['.', '.', '.', 'T', '.'],
    ['#', '#', 'T', '#', '.'],
    ['.', '.', '.', '#', 'E'],
    ['.', '#', '.', 'E', '#'],
    ['.', '.', '.', '.', '.']
]
start = (0, 0)
end = (4, 4)
teleports = {(0, 3): (2, 4),(1,2):(3,3)}

path = find_shortest_path_with_teleports(grid, start, end, teleports)
if path:
    print("Найден путь:", path)
    print("Длина пути:", len(path) - 1)
else:
    print("Путь не найден")
