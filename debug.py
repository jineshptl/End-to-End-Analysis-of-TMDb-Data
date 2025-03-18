import csv

# Function to check and print sample data from nodes.csv and edges.csv
def check_csv_contents():
    print("\n===== Checking File Contents =====")

    print("\nNodes Sample:")
    with open("nodes.csv", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            print(line.strip())  # Print first few lines
            if i > 10:
                break

    print("\nEdges Sample:")
    with open("edges.csv", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            print(line.strip())  # Print first few lines
            if i > 10:
                break

# Function to validate edge connections
def validate_edges():
    nodes_set = set()
    edges_set = set()

    # Load nodes
    with open("nodes.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            nodes_set.add(row[0].strip())

    # Load edges and validate
    with open("edges.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                print(f"❌ Malformed edge row: {row}")
                continue

            source, target = row[0].strip(), row[1].strip()

            if source not in nodes_set or target not in nodes_set:
                print(f"❌ Invalid edge found (non-existent node): {source} -> {target}")

            edges_set.add((source, target))

    print("\n===== VALIDATION RESULTS =====")
    print(f"🔹 Total Nodes: {len(nodes_set)}")
    print(f"🔹 Total Edges: {len(edges_set)}")

# Run checks
check_csv_contents()
validate_edges()
