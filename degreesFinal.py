import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

"""
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
"""

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(r"C:\Users\MyPC\Documents\CS50\degrees\small\people.csv", "rt", encoding="utf-8") as f2:
         reader = csv.DictReader(f2)
         for row in reader: 
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(r"C:\Users\MyPC\Documents\CS50\degrees\small\movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
             movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(r"C:\Users\MyPC\Documents\CS50\degrees\small\stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found 2.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(str(degrees) + " degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
           # print("{i + 1}: {person1} and {person2} starred in {movie}")
            print(str(i + 1) + " : " + str(person1) + " and " + str(person2) + " starred in " + str(movie))

"""
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
"""
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

def shortest_path( source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
        """
    frontier = QueueFrontier()
    frontier.add(Node(source, None, None))
    nodesExplored = set()
    if source == target:
        raise Exception("Can't choose the same actor twice!")
    while True:
        if frontier.empty():
            return None
        node = frontier.remove()
        if node.state == target:
            solutions = []
            while node.parent is not None:
                solutions.append((node.action, node.state))
                node = node.parent
            solutions.reverse()
            return solutions
        nodesExplored.add(node.state)
        for movie_id, person_id in neighbors_for_person(node.state):
            if not (person_id in nodesExplored):
                child = Node(person_id, node, movie_id)
                frontier.add(child)
















        """
    frontier = StackFrontier()
    frontier.add(source)
        # TODO
        #raise NotImplementedError
    explored = set()
    goal = target
    num_explored = 0
    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # If node is the goal, then we have a solution
        if node == goal:
            actions = []
            cells = []
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            solution = (actions, cells)
            return

            # Mark node as explored
            self.explored.add(node.state)

        # Add neighbors to frontier
        for action, state in neighbors(node):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)




"""




def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print("Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print("ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
