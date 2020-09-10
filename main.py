from flask import Flask, render_template, redirect, request
from functools import reduce

app = Flask(__name__)


def is_hamming_valid(message):
    digits_activation = dict(zip([i for i in range(16)], [int(digit) for digit in message]))
    positions = [position for position, digit in digits_activation.items() if digit]
    if len(positions) == 0:
        return True
    if len(positions) % 2 == 1:
        return False
    error_position = reduce(lambda x, y: x ^ y, positions)
    return error_position == 0


@app.route('/')
def index():
    return render_template('index.html')


class Cell():
    def __init__(self, id, type, value):
        self.id = id
        self.type = type
        self.value = value


def fill_cells(values):
    grid_size = int(len(values) / 4)
    cells = []
    for i in range(grid_size ** 2):
        id = bin(i)[2:].rjust(grid_size, '0')
        if i == 0:
            type = '0'
        elif len([i for i in id if i == '1']) == 1:
            type = 'question'
        else:
            type = 'message'
        cells.append(Cell(id, type, values[i]))
    return cells


@app.route('/encoding/', methods=['POST', 'GET'])
def encoding():
    grid_size = 4

    if request.method == 'POST':
        try:
            message = request.form['message']
            if len(message) != grid_size ** 2:
                info = 'ERROR: All cells should be filled with a 0 or a 1.'
            elif not all(input == '0' or input == '1' for input in message):
                info = 'ERROR: Cells should only contain 0s and 1s.'
            elif (is_hamming_valid(message)):
                info = 'Ok!'
            else:
                info = 'Wrong!'
            return render_template('encoding.html', cells=fill_cells(message), validation_info=info)
        except:
            grid_size = int(request.form['grid_size'])
            if grid_size < 4 or grid_size % 2 == 1:
                info = "Grid size should be an even number equal or greater than 4."
                return render_template('encoding.html', setup_info=info)
            message = ''.rjust(grid_size ** 2, '?')
            return render_template('encoding.html', cells=fill_cells(message))
    else:
        return render_template('encoding.html')


if __name__ == "__main__":
    app.run(debug=True)
