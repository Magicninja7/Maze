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



##### quantum search
#####
#####
def bfs_quant(maze, directions, entry, manager_dict, found_flag):
    if found_flag.value:
        return
    
    x, y = map(int, entry.split(","))
    n, m = len(maze), len(maze[0])
    next_nodes = []
    if not manager_dict['visited'][x][y]:
        manager_dict['visited'][x][y] = True

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m and not manager_dict['visited'][nx][ny]:
            if maze[nx][ny] == 1:
                next_nodes.append(f"{nx},{ny}")
                manager_dict['visited'][nx][ny] = True
                manager_dict['parent'][(nx, ny)] = (x, y)
            elif maze[nx][ny] == 2:
                with manager_dict['lock']:
                    found_flag.value = True
                    manager_dict['path'] = (nx, ny)
                manager_dict['parent'][(nx, ny)] = (x, y)
                return

    return next_nodes

def maii(entry_point):
    entry = entry_point

    with multiprocessing.Manager() as manager:
        manager_dict = manager.dict()
        manager_dict['visited'] = manager.list([ [False]*len(maze[0]) for _ in maze ])
        manager_dict['parent'] = manager.dict()
        manager_dict['lock'] = manager.Lock()
        manager_dict['path'] = None

        manager_dict['visited'][0][0] = True
        manager_dict['parent'][(0, 0)] = None

        found_flag = manager.Value('b', False)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(bfs_quant, maze, directions, entry, manager_dict, found_flag)]
            while futures:
                done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                for future in done:
                    next_nodes = future.result()
                    futures.remove(future)
                    if next_nodes and not found_flag.value:
                        for node in next_nodes:
                            futures.append(executor.submit(bfs_quant, maze, directions, node, manager_dict, found_flag))

        if found_flag.value:
            print(f"Path found to: {manager_dict['path']}")
        else:
            print("No path found")

def qaunt_run():
    entry = input("Enter the entry point (x, y): ")
    maii(entry)
##### quantum search
#####
#####


def main():
    print("1. BFS")
    path = bfs()
    print_path(path)

    print("\n2. Quantum Search")
    qaunt_run()    




if __name__ == '__main__':
    main()




