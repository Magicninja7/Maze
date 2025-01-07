import sys
import json
import concurrent.futures
import multiprocessing

def maze_gen():
    n = int(input("Enter the number of rows in the maze: "))
    maze = []

    print("Enter each row of the maze as space-separated numbers:")
    for _ in range(n):
        row = list(map(int, input().split()))  # Convert input row to a list of integers
        maze.append(row)
    return maze

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]



def print_visited_bfs(visited, maze):
    rows, cols = len(maze), len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 2:
                print("X", end=" ")
            elif (i, j) in visited:
                print(".", end=" ")
            else:
                print(maze[i][j], end=" ")
        print()



def print_path(path, maze):
    n = len(maze)
    for i in range(n):
        for j in range(n):
            if maze[i][j] == 2:
                print("X", end=" ")
            elif (i, j) in path:
                print(".", end=" ")
            else:
                print(maze[i][j], end=" ")
        print()


##### BFS
#####
#####
def bfs(entry, maze):
    kolej = []

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
                    return path, visited, kolej.reverse()

                if maze[nx][ny] == 1:
                    kolej.append((nx, ny))
                    queue.append((nx, ny))
                    visited[nx][ny] = True
                    parent[(nx, ny)] = (x, y)
    return "No path found"
#####
#####
##### BFS





##### DFS
#####
#####
def dfs_solve(entry, maze):
    kolej = []
    x, y = map(int, entry.split(","))
    rows, cols = len(maze), len(maze[0])
    visited = []
    path = []

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in visited or maze[r][c] == 0:
            return False
        visited.append((r, c))
        path.append((r, c))
        kolej.append((r, c))
        if maze[r][c] == 2:
            return True
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            if dfs(r + dr, c + dc):
                return True
        path.pop()
        return False

    if dfs(x, y):
        return visited, path, kolej.reverse()
    else:
        return "No path found"
#####
#####
##### DFS





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

def maii(entry_point, maze):
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

def qaunt_run(entry, maze):
    maii(entry, maze)
#####
#####
##### quantum search




def main():
    maze = maze_gen()
    entry = input("whats the entry? ")
    print()


    print("\n1. DFS")
    visited, path, kolej = dfs_solve(entry, maze)
    print("Path: ")
    print_path(path, maze)
    print()


    print("2. BFS")
    path, visited, kolej = bfs(entry, maze)
    print_visited_bfs(path, maze)
    print()

    print("\n3. Quantum Search")
    qaunt_run(entry, maze)

    


def solve_maze(maze, alg):
    entry = '0,0'
    if alg == 'bfs':
        path, visited, kolej = bfs(entry, maze)
        return path
    else:
        visited, path, kolej = dfs_solve(entry, maze)
        return path






if __name__ == '__main__':
    main()

