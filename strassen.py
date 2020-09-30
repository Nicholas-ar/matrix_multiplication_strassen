def is_digit(number):
    # verifica se uma string e um digito, string.isdigit() n funciona pra
    # numeros negativos
    try:
        int(number)
        return True
    except ValueError:
        return False


def next_exponent(number):
    powers = 2
    while(True):
        if(number % powers == 0):
            return 0
        elif(number < powers):
            return powers
        else:
            powers = powers*2


def get_dimensions(content):
    # armazena quantidades de linhas e colunas em variaveis
    # usa is digit pq o tamanho da matriz n pode ser negativo
    dimensions = ([int(s) for s in content[0].split() if s.isdigit()])
    lines_first = dimensions[0]
    collumns_first = dimensions[1]
    lines_second = dimensions[2]
    collumns_second = dimensions[3]
    return(lines_first, collumns_first, lines_second, collumns_second)


def add_padding(matrix, expected):
    # completa as matrizes com 0 para que se tornem quadradas
    temp = []
    while(len(temp) < expected):
        temp.append(0)
    for row in matrix:
        while(len(row) < expected):
            row.append(0)
    while(len(matrix) < expected):
        matrix.append(temp)


def generate_square_matrix(size):
    matrix = [[0 for i in range(size)]for j in range(size)]
    return matrix


def matrix_addition(first_matrix, second_matrix):
    length = len(first_matrix)
    result_matrix = generate_square_matrix(length)
    for i in range(length):
        for j in range(length):
            result_matrix[i][j] = first_matrix[i][j] + second_matrix[i][j]
    return result_matrix


def matrix_subtraction(first_matrix, second_matrix):
    length = len(first_matrix)
    result_matrix = generate_square_matrix(length)
    for i in range(length):
        for j in range(length):
            result_matrix[i][j] = first_matrix[i][j] - second_matrix[i][j]
    return result_matrix


def small_matrix_multiplication(first, second):
    result = [[first[0][0]*second[0][0]+first[0][1]*second[1][0],
               first[0][0]*second[0][1]+first[0][1]*second[1][1],],
              [first[1][0]*second[0][0]+first[1][1]*second[1][0],
               first[1][0]*second[0][1]+first[1][1]*second[1][1]]]
    return result


def matrix_split(matrix):
    # divide uma matriz quadrada em 4 pedacos
    length = len(matrix)
    half = length//2
    upper_left = [[matrix[i][j] for j in range(half)] for i in range(half)]
    upper_right = [[matrix[i][j]
                    for j in range(half, length)]for i in range(half)]
    bottom_left = [[matrix[i][j]
                    for j in range(half)]for i in range(half, length)]
    bottom_right = [[matrix[i][j]
                     for j in range(half, length)]for i in range(half, length)]
    return upper_left, upper_right, bottom_left, bottom_right


def strassen(first_matrix, second_matrix):
    
    if(len(first_matrix) == 2):
        return small_matrix_multiplication(first_matrix, second_matrix)
    
    a11, a12, a21, a22 = matrix_split(first_matrix)
    b11, b12, b21, b22 = matrix_split(second_matrix)

    p1 = strassen(a11, matrix_subtraction(b12, b22))#correto
    p2 = strassen(matrix_addition(a11, a12), b22)#correto
    p3 = strassen(matrix_addition(a21, a22), b11)#correto
    p4 = strassen(a22, matrix_subtraction(b21, b11))#correto
    p5 = strassen(matrix_addition(a11, a22), matrix_addition(b11, b22))#
    p6 = strassen(matrix_subtraction(a12, a22), matrix_addition(b21, b22))#
    p7 = strassen(matrix_subtraction(a11, a21), matrix_addition(b11, b12))#
    

    upper_left = matrix_addition(
        matrix_subtraction(matrix_addition(p5, p4), p2), p6)
    upper_right = matrix_addition(p1, p2)
    bottom_left = matrix_addition(p3, p4)
    bottom_right = matrix_subtraction(
        matrix_subtraction(matrix_addition(p5, p1), p3), p7)

    
    result = []
    for i in range(len(upper_left)):
        result.append(upper_left[i]+upper_right[i])
    for i in range(len(bottom_left)):
        result.append(bottom_left[i]+bottom_right[i])
    return result


# abre o arquivo, bota o conteudo em content e fecha
input_filename = open('in.txt', 'r')
if input_filename.mode == 'r':
    content = input_filename.readlines()
input_filename.close()


lines_first, collumns_first, lines_second, collumns_second = get_dimensions(
    content)

output_lines = lines_first
output_collumns = collumns_second

# adiciona cada linha da 1a matriz como uma lista numa lista de listas
temp_matrix = content[1:lines_first+1]
first_matrix = []
for i in range(len(temp_matrix)):
    first_matrix.append([int(s)
                         for s in temp_matrix[i].split() if is_digit(s)])

# adiciona cada linha da 2a matriz como uma lista numa lista de listas
temp_matrix = content[lines_first+1:lines_first+lines_second+1]
second_matrix = []
for i in range(len(temp_matrix)):
    second_matrix.append([int(s)
                          for s in temp_matrix[i].split() if is_digit(s)])

expected_size_first = max(next_exponent(len(first_matrix)),
                          next_exponent(len(first_matrix[0])))
expected_size_second = max(next_exponent(
    len(second_matrix)), next_exponent(len(second_matrix[0])))
final_size = max(expected_size_first, expected_size_second)


add_padding(first_matrix, final_size)
add_padding(second_matrix, final_size)

result_matrix = strassen(first_matrix, second_matrix)
matrix_output = ''


for i in range(output_lines):
    matrix_output += (' '.join([str(result_matrix[i][j])
                                for j in range(output_collumns)]))
    matrix_output += ('\n')


# escreve os resultados no arquivo de saida
output = open('out.txt', 'w')
if output.mode == 'w':
    output.write(n_matricula + '\n' + str(output_lines) +
                 ' ' + str(output_collumns)+'\n' + str(matrix_output))
output.close()