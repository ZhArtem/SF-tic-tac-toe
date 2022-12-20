from random import randint

MAX_FIELD_SIZE = 10


def intro():
    print('''
            Добро пожаловать в игру КРЕСТИКИ-НОЛИКИ!
    Первым ходит Х, вторым О и далее по очереди.
    У вас будет возможность выбрать размеры игрового поля.
    Также игра спросит, хотите ли вы играть с ботом или в два игрока.
    Если выберете игру с ботом, то у вас будет возможность выбора первого хода.      
                        Удачной игры!    
    ''')


def get_field_size():
    while True:
        size = input('Введите размерность поля на котором хотите сыграть: ').strip()
        if not all(i.isdigit() for i in size):
            print('Размерами поля должны быть числа!')
            continue
        if int(size) > MAX_FIELD_SIZE:
            print(f'Размеры поля должны быть не более {MAX_FIELD_SIZE}!')
            continue
        break
    return int(size)


def print_field(fld):
    x_axis = '  ' + ' '.join(map(str, range(field_size)))
    print(x_axis)
    for index, row in enumerate(fld):
        print(index, *row)


def input_bot(fld, char):
    while True:
        a, b = [randint(0, field_size - 1) for _ in '12']
        if fld[a][b] != '-':
            continue
        print(f'Бот поставил "{char}" в координаты {a} {b}:')
        break
    return a, b


def input_user(fld):
    while True:
        coords = input('Введите координаты поля (строка столбец) через пробел: ').split()
        if len(coords) != 2:
            print('Координат должно быть две!')
            continue
        if not all(i.isdigit() for i in coords):
            print('Координатами должны быть числа!')
            continue
        a, b = map(int, coords)
        if any((a < 0, b < 0, a > field_size - 1, b > field_size - 1)):
            print(f'Координатами должны быть числа от 0 до {field_size - 1}!')
            continue
        if fld[a][b] != '-':
            print(f'Поле {a} {b} уже занято!')
            continue
        break
    return a, b


def is_winner(fld, char):
    def check_main_diagonal():
        for i in range(field_size):
            if fld[i][i] != char:
                return False
        return True

    def check_secondary_diagonal():
        for i in range(field_size):
            if fld[field_size - 1 - i][i] != char:
                return False
        return True

    def check_rows():
        for row in fld:
            if row == [char] * field_size:
                return True
        return False

    def check_cols():
        for i in range(field_size):
            if all([fld[j][i] == char for j in range(field_size)]):
                return True
        return False

    return True if any((check_main_diagonal(), check_secondary_diagonal(), check_rows(), check_cols())) else False


intro()
another_game = 'да'
while another_game == 'да':
    total_moves = 0
    field_size = get_field_size()
    field = [['-'] * field_size for _ in range(field_size)]
    bot = input('Для игры с ботом ведите "бот": ').strip().lower() == 'бот'
    if bot:
        while True:
            dig = input('Выберете каким будет ваш ход: первым или вторым? Введите число "1" или "2": ').strip()
            if dig in '12' and len(dig) == 1:
                break
        bot_move = 1 if dig == '1' else 0
    else:
        print('Выбран режим для двух игроков')
    while True:
        player = 'x' if total_moves % 2 == 0 else 'o'
        print_field(field)
        print(f'Ходит игрок {player.upper()}')
        if bot and total_moves % 2 == bot_move:
            x, y = input_bot(field, player)
        else:
            x, y = input_user(field)
        field[x][y] = player
        if is_winner(field, player):
            print_field(field)
            print(f'Выиграл {player.upper()}!!!')
            another_game = input('Чтобы сыграть еще раз введите "да": ').lower().strip()
            break
        total_moves += 1
        if total_moves == field_size ** 2 + 1:
            print_field(field)
            print('Ничья!!!')
            another_game = input('Чтобы сыграть еще раз введите "да": ').lower().strip()
            break

