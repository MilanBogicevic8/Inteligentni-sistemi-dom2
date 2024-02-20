def count_consecutive_zeros(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    def has_four_consecutive_zeros(sequence):
        return '0000' in ''.join(map(str, sequence))

    def check_sequence(sequence):
        return has_four_consecutive_zeros(sequence) and all(bit == 0 for bit in sequence)

    def check_rows():
        count = 0
        for row in matrix:
            for j in range(num_cols - 3):
                if check_sequence(row[j:j+4]):
                    count += 1
        return count

    def check_cols():
        count = 0
        for j in range(num_cols):
            col_values = [matrix[i][j] for i in range(num_rows)]
            for i in range(num_rows - 3):
                if check_sequence(col_values[i:i+4]):
                    count += 1
        return count

    def check_diagonals():
        count = 0
        for i in range(num_rows - 3):
            for j in range(num_cols - 3):
                # Check diagonally (from top-left to bottom-right)
                diagonal_values = [matrix[i+x][j+x] for x in range(4)]
                if check_sequence(diagonal_values):
                    count += 1

                # Check diagonally (from top-right to bottom-left)
                diagonal_values = [matrix[i+x][j+3-x] for x in range(4)]
                if check_sequence(diagonal_values):
                    count += 1

        return count

    return check_rows() + check_cols() + check_diagonals()
def number_to_matrix(number):
    binary_representation = format(number, '0' + str(6 * 7) + 'b')
    matrix = [[int(bit) for bit in binary_representation[i * 7:(i + 1) * 7]] for i in range(6)]
    return matrix

# Primer unos broja i generisanje matrice
broj = 439753 # Primer broja
matrix_example = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 0, 0]
]

# Poziv funkcije

rezultat = count_consecutive_zeros(matrix_example)
print("Broj slučajeva gde postoje 4 uzastopne nule:", rezultat)
