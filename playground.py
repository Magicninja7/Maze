import multiprocessing
import concurrent.futures

def q():
    print("Quantum Search")
    print("result found")

def bfs_quant(maze, directions, entry, manager_dict, found_flag, executor):
    if found_flag.value:
        return
    
    x, y = map(int, entry.split(","))
    n, m = len(maze), len(maze[0])
    next_nodes = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m and not manager_dict['visited'][nx][ny]:
            if maze[nx][ny] == 1:
                next_nodes.append(f"{nx},{ny}")
                manager_dict['visited'][nx][ny] = True
                manager_dict['parent'][(nx, ny)] = (x, y)
            elif maze[nx][ny] == 2:
                q()
                with manager_dict['lock']:
                    found_flag.value = True
                    manager_dict['path'] = (nx, ny)
                return

    if not next_nodes:
        return

    for node in next_nodes:
        if not found_flag.value:
            executor.submit(bfs_quant, maze, directions, node, manager_dict, found_flag, executor)

def main():
    maze = [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 1, 2, 0, 1],
        [1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0, 1],
    ]
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    entry = "0,0"

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
            executor.submit(bfs_quant, maze, directions, entry, manager_dict, found_flag, executor)
            executor.shutdown(wait=True)

        if found_flag.value:
            print(f"Path found to: {manager_dict['path']}")
        else:
            print("No path found")

if __name__ == '__main__':
    main()