import heapq
import math


class Node:
    """A* search node used internally by :class:`AStarPlanner`."""

    def __init__(self, position, g_cost, h_cost, parent=None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost


class AStarPlanner:
    """Grid-based A* planner for OccupancyGrid-style map data.

    The map is indexed as map[y, x], matching OccupancyGrid row-major
    storage. Cells with value 0 are free; occupied and unknown cells are
    treated as blocked. Diagonal moves cannot cut through blocked corners.
    """

    def __init__(self, map_data, resolution, origin):
        self.map = map_data
        self.resolution = float(resolution)
        self.origin = origin
        self.origin_yaw = float(origin[2]) if len(origin) > 2 else 0.0

        if self.map.ndim != 2:
            raise ValueError('map_data must be a 2D array')
        if self.resolution <= 0.0:
            raise ValueError('resolution must be positive')

    def heuristic(self, a, b):
        dx = abs(b[0] - a[0])
        dy = abs(b[1] - a[1])
        diagonal = min(dx, dy)
        straight = max(dx, dy) - diagonal
        return diagonal * math.sqrt(2.0) + straight

    def plan(self, start, goal):
        start = tuple(start)
        goal = tuple(goal)
        if not self.is_valid(start) or not self.is_valid(goal):
            return None

        open_heap = []
        counter = 0
        start_node = Node(start, 0.0, self.heuristic(start, goal))
        heapq.heappush(open_heap, (start_node.f_cost, counter, start_node))
        best_cost = {start: 0.0}
        closed_set = set()

        while open_heap:
            _, _, current = heapq.heappop(open_heap)
            position = current.position

            if position in closed_set:
                continue
            if current.g_cost > best_cost.get(position, math.inf):
                continue
            if position == goal:
                return self.reconstruct_path(current)

            closed_set.add(position)
            for neighbor, move_cost in self.get_neighbors(position):
                if neighbor in closed_set:
                    continue
                tentative_g = current.g_cost + move_cost
                if tentative_g >= best_cost.get(neighbor, math.inf):
                    continue

                best_cost[neighbor] = tentative_g
                counter += 1
                node = Node(
                    neighbor,
                    tentative_g,
                    self.heuristic(neighbor, goal),
                    current,
                )
                heapq.heappush(open_heap, (node.f_cost, counter, node))

        return None

    def get_neighbors(self, position):
        x, y = position
        candidates = [
            ((x - 1, y), 1.0), ((x + 1, y), 1.0),
            ((x, y - 1), 1.0), ((x, y + 1), 1.0),
            ((x - 1, y - 1), math.sqrt(2.0)),
            ((x - 1, y + 1), math.sqrt(2.0)),
            ((x + 1, y - 1), math.sqrt(2.0)),
            ((x + 1, y + 1), math.sqrt(2.0)),
        ]

        neighbors = []
        for neighbor, cost in candidates:
            if not self.is_valid(neighbor):
                continue
            nx, ny = neighbor
            dx, dy = nx - x, ny - y
            if dx and dy:
                # A diagonal is allowed only if both adjacent cardinal cells
                # are free; this prevents cutting through obstacle corners.
                if not self.is_valid((x + dx, y)):
                    continue
                if not self.is_valid((x, y + dy)):
                    continue
            neighbors.append((neighbor, cost))
        return neighbors

    def is_valid(self, position):
        x, y = position
        height, width = self.map.shape
        if x < 0 or y < 0 or x >= width or y >= height:
            return False
        return self.map[y, x] == 0

    def reconstruct_path(self, node):
        path = []
        while node is not None:
            path.append(node.position)
            node = node.parent
        return path[::-1]

    def world_to_map(self, world_coord):
        dx = world_coord[0] - self.origin[0]
        dy = world_coord[1] - self.origin[1]
        cos_yaw = math.cos(self.origin_yaw)
        sin_yaw = math.sin(self.origin_yaw)
        local_x = cos_yaw * dx + sin_yaw * dy
        local_y = -sin_yaw * dx + cos_yaw * dy
        return (
            math.floor(local_x / self.resolution),
            math.floor(local_y / self.resolution),
        )

    def map_to_world(self, map_coord):
        local_x = (map_coord[0] + 0.5) * self.resolution
        local_y = (map_coord[1] + 0.5) * self.resolution
        cos_yaw = math.cos(self.origin_yaw)
        sin_yaw = math.sin(self.origin_yaw)
        return (
            self.origin[0] + cos_yaw * local_x - sin_yaw * local_y,
            self.origin[1] + sin_yaw * local_x + cos_yaw * local_y,
        )
