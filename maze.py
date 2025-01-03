import sys
import json
import concurrent.futures
import multiprocessing


maze = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 1, 2, 0, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1],
]
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def print_path(path):
    n = len(maze)
    for i in range(n):
        for j in range(n):
            if (i, j) in path:
                print(".", end=" ")
            else:
                print(maze[i][j], end=" ")
        print()


def bfs():
    entry = input("Enter the entry point (x, y): ")

    x, y = map(int, entry.split(","))
    n = len(maze)
    visited = [[False] * n for _ in range(n)]
    parent = {}

    queue = [(x, y)]
    visited[x][y] = True
    parent[(x, y)] = None

    while queue:
        x, y = queue.pop(0)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                if maze[nx][ny] == 2:
                    parent[(nx, ny)] = (x, y)
                    path = []
                    while (nx, ny) is not None:
                        path.append((nx, ny))
                        if parent[(nx, ny)] == None:
                            break
                        nx, ny = parent[(nx, ny)]
                        
                    path.reverse()
                    return path

                if maze[nx][ny] == 1:
                    queue.append((nx, ny))
                    visited[nx][ny] = True
                    parent[(nx, ny)] = (x, y)
    return "No path found"



n = len(maze)
visited = [[False] * n for _ in range(n)]
parent = {}
parent[(x, y)] = None


'''
How quantum search would theoretically work:
'''
def bfs_quant(maze, directions, entry):
    global parent, visited
    n, m = len(maze), len(maze[0])
    x, y = map(int, entry.split(","))
    next = []


    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if visited[nx][ny]:
            continue
        if maze[nx][ny] == 1:
            next.append((nx, ny))
            visited[nx][ny] = True
            parent[(nx, ny)] = (x, y)

        if maze[nx][ny] == 2:

            
            





    


    


    with multiprocessing.Manager() as manager:
        found_flag = manager.Namespace()
        found_flag.value = False
        found_flag.path = None
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            while queue:
                cx, cy = queue.pop(0)
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        if maze[nx][ny] == 2:
                            return f"Path found to target at {(nx, ny)}"
                        if maze[nx][ny] == 1:
                            future = executor.submit(search_path, maze, (nx, ny), directions, found_flag)
                            futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            if found_flag.value:
                executor.shutdown(cancel_futures=True)
                return found_flag.path
            

    return "No path found"






#end of quantum search





def q():
    print("Quantum Search")
    print("result found")





def main():
    print("1. BFS")
    path = bfs()
    print_path(path)

    print("\n2. Quantum Search")
    entry = input("Enter the entry point (x, y): ")

    path = bfs_quant()
    print(path)


if __name__ == '__main__':
    main()