import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Vertex:
    def __init__(self, name):
        self.name = name
        self.color = None
        self.visited = False

color_map = {
    0: "Yellow",
    1: "Red",
    2: "Green",
    3: "LightBlue",
    4: "Pink",
    5: "White",
    6: "Brown",
    7: "Black",
    8: "Gray",
    9: "Orange"
}

def is_course_exist(course, courses):
    return course in courses

def create_edges(file_data, course_count):
    adj_matrix = [[0 for _ in range(course_count)] for _ in range(course_count)]

    for line in file_data:
        courses_one_student_takes = line.strip().split(':')[1].split(',')
        adj_matrix = create_edge_between(adj_matrix, courses_one_student_takes)

    return adj_matrix

def create_edge_between(adj_matrix, courses_one_student_takes):
    correct_indexes = [0] * len(courses)

    for i, course in enumerate(courses):
        if course in courses_one_student_takes:
            correct_indexes[i] = 1

    for i in range(len(courses)):
        if correct_indexes[i] == 1:
            for j in range(len(courses)):
                if correct_indexes[j] == 1 and i != j:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1

    return adj_matrix

def get_available_colors(graph, course, exam_periods):
    used_colors = set()

    for neighbor in graph[course]:
        if neighbor in exam_periods:
            used_colors.add(exam_periods[neighbor])

    available_colors = [color for color in range(len(courses)) if color not in used_colors]
    return available_colors

def greedy_coloring(graph, courses):
    exam_periods = {}  # Store course assignments for each exam period

    for course in courses:
        available_colors = get_available_colors(graph, course, exam_periods)
        assigned_color = min(available_colors)
        exam_periods[course] = assigned_color

    return exam_periods

def visualize_graph_with_colors(G, color_map,exam_periods):
    pos = nx.spring_layout(G)  # You can change the layout as needed

    node_colors = [color_map[exam_periods[course]] for course in G.nodes]

    # Create a custom colormap for node colors
    cmap = mcolors.ListedColormap(node_colors)

    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=cmap, node_size=500)

    # Create a legend for the colors
    color_labels = list(color_map.values())
    patches = [plt.Line2D([0], [0], marker='o', color=color_map[i], label=label, markersize=10) for i, label in color_map.items()]
    plt.legend(handles=patches, title="Colors", loc='upper right')

    plt.show()

def main(f):
    global courses
    courses = []

    with open(f, "r") as file_ptr:
        file_data = file_ptr.readlines()

    for line in file_data:
        words = line.strip().split(':')
        tokens = words[1].split(',')
        for token in tokens:
            if not is_course_exist(token, courses):
                courses.append(token)

    course_count = len(courses)

    # Create vertices with classes
    vertex_list = [Vertex(course) for course in courses]

    # Create an adjacency list to represent the graph
    graph = {course: [] for course in courses}
    for line in file_data:
        parts = line.strip().split(":")
        courses_one_student_takes = parts[1].split(",")
        for course in courses_one_student_takes:
            for other_course in courses_one_student_takes:
                if course != other_course:
                    graph[course].append(other_course)

    # Create adjacency matrix
    adj_matrix = create_edges(file_data, course_count)

    # Coloring Algorithm
    exam_periods = greedy_coloring(graph, courses)

    # Print the adjacency matrix
    print("Adjacency Matrix:")
    print("\t", end="")
    for course in courses:
        print(course, end="\t")
    print()

    for i in range(course_count):
        print(courses[i], end="\t")
        for j in range(course_count):
            print(adj_matrix[i][j], end="\t")
        print()

    # Coloring Algorithm
    exam_periods = greedy_coloring(graph, courses)

    # Organize courses by exam period
    exam_period_courses = {}
    for course, exam_period in exam_periods.items():
        if exam_period not in exam_period_courses:
            exam_period_courses[exam_period] = []
        exam_period_courses[exam_period].append(course)

    # Print the final exam schedule
    print("\nFinal Exam Schedule:")
    for exam_period, scheduled_courses in exam_period_courses.items():
        print(f"Final Exam Period {exam_period + 1} -> {', '.join(scheduled_courses)}")

    # Create a graph using NetworkX
    G = nx.Graph()
    G.add_nodes_from(courses)

    for i in range(course_count):
        for j in range(i + 1, course_count):
            if adj_matrix[i][j] == 1:
                G.add_edge(courses[i], courses[j])

    # Visualize the graph
    pos = nx.spring_layout(G)  
    nx.draw(G, pos, with_labels=True, node_size=800, node_color="skyblue", font_size=10, font_color="black", font_weight="bold")
    plt.title("Course Graph")
    plt.show()

    # Create a networkx graph to visualize the colored vertices
    G = nx.Graph()

    # Add nodes with colors
    for course in courses:
        G.add_node(course)

    # Add edges
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            if adj_matrix[i][j] == 1:
                G.add_edge(courses[i], courses[j])

    # Visualize the graph with colored vertices
    print("\n")
    print("The graph after coloring")
    visualize_graph_with_colors(G, color_map, exam_periods)
    
if __name__ == "__main__":
    print("\n")
    print("                           EXAM SCHEDULER                   ")
    print("\t                                           DONE BY:       ")
    print("\t                                                   SMRITHI L (22PD33)")
    print("\t                                                   SUNIL J  (22PD36)")
    f=input("Enter the file's name where you have stored the student's details with their courses:")
    print("\n")
    main(f)


