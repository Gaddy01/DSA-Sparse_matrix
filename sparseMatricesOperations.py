class SparseMatrix:
    # Create a sparse matrix that stores only non-zero values.
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.values = {}  # store the non-zero values in format {(row, col): value}

    # Add a non-zero value at a specific (row, col) position.
    def set(self, row, col, value):
        if value != 0:
            self.values[(row, col)] = value

    # Fetch the value at a specific position.
    def get(self, row, col):
        return self.values.get((row, col), 0)

    # The method that performs addition of the two matrices
    def add(self, other):
        result = SparseMatrix(self.rows, self.cols)
        keys = set(self.values.keys()).union(other.values.keys())
        print('Operation in progress...')
        for key in keys:  # keys is the union of all coordinates with non-zero values in either matrix.
            val = self.get(*key) + other.get(*key)  # Add two values with the same coordinates
            if val != 0:
                result.set(*key, val) # If the sum value is not 0, save it.
        return result

    # The method that performs substraction of the two matrices. Same logic as the add method.
    def subtract(self, other):
        result = SparseMatrix(self.rows, self.cols)
        keys = set(self.values.keys()).union(other.values.keys())
        print('Operation in progress...')
        for key in keys:
            val = self.get(*key) - other.get(*key)
            if val != 0:
                result.set(*key, val)
        return result

    # The method that performs multiplication of the two matrices
    def multiply(self, other):
        # Check if the matrices are of the shapes: axb, bxc respectively.
        if self.cols != other.rows:
            raise Exception("Matrix dimensions are not compatible for multiplication")

        result = SparseMatrix(self.rows, other.cols)

        # Build a mapping from rows in 'other' to their non-zero (col, value) entries
        other_row_map = {}  # key: row index in B, value: list of (col, value)
        print('Operation in progress...')
        for (row, col), val in other.values.items():
            if row not in other_row_map:
                other_row_map[row] = []
            other_row_map[row].append((col, val))

        # Multiply only matching non-zero entries. This is important to reduce computational time.
        for (i, k), val_a in self.values.items():
            if k in other_row_map:
                for j, val_b in other_row_map[k]:
                    prev = result.get(i, j)
                    result.set(i, j, prev + val_a * val_b)

        return result

    # Save the results to a new .txt file
    def save_to_file(self, filepath):
        with open(filepath, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for (row, col), val in sorted(self.values.items()):
                f.write(f"({row}, {col}, {val})\n")

# This function splits the first two lines in the .txt documents.
def parse_int_value(line):
    parts = line.strip().split('=')
    return int(parts[1]) if len(parts) == 2 else None

# # This function splits the other lines correcponding to the non-zero values of the matrices.
def parse_entry(line):
    line = line.strip()
    if line.startswith('(') and line.endswith(')'):
        line = line[1:-1]
        parts = line.split(',')
        if len(parts) == 3:
            row = int(parts[0].strip())
            col = int(parts[1].strip())
            val = int(parts[2].strip())
            return row, col, val
    return None

# This function reads the file and constructs two SparseMatrix instances.
def load_sparse_matrix(filepath):
    with open(filepath, 'r') as file:
        lines = [line for line in file if line.strip() != '']

    rows = parse_int_value(lines[0])
    cols = parse_int_value(lines[1])
    matrix = SparseMatrix(rows, cols)

    for line in lines[2:]:
        entry = parse_entry(line)
        if entry:
            row, col, val = entry
            matrix.set(row, col, val)

    return matrix

def main():
    # The location paths of the two matrices.
    path_matrix_a = r'input_data/sparse_matrix_1.txt'
    path_matrix_b = r'input_data/sparse_matrix_2.txt'

    print("Which operation do you want to perform?")
    print("1 - Addition")
    print("2 - Subtraction")
    print("3 - Multiplication")
    choice = input("Enter the number (1/2/3): ").strip()

    A = load_sparse_matrix(path_matrix_a)
    B = load_sparse_matrix(path_matrix_b)

    if choice == '1':
        result = A.add(B)
        output_file = r'output_data/result_add.txt' # The location path of the output files
    elif choice == '2':
        result = A.subtract(B)
        output_file = r'output_data/result_sub.txt'
    elif choice == '3':
        try:
            result = A.multiply(B)
            output_file = r'output_data/result_mul.txt'
        except Exception as e:
            print("Multiplication error:", e)
            return
    else:
        print("Invalid choice.")
        return

    result.save_to_file(output_file)
    print(f"Operation completed. Result saved in '{output_file}' file.")

if __name__ == "__main__":
    main()
