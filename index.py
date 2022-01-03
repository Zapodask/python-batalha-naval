import json
import random


class Main:
    red_boats = []
    blue_boats = []

    def __init__(self):
        with open("side.json", "r") as f:
            side = json.load(f)

            self.red_side = side
            self.blue_side = side
            self.turn = random.choice(["red", "blue"])

        self.setBoats(self.turn)

        self.changeTurn()
        
        self.setBoats(self.turn)

        self.changeTurn()

        self.initGame()

    def initGame(self):
        while True:
            print(f"{self.turn} turn")

            move = input("movement: ")

            splitted = list(move)

            col = splitted[0].upper()
            row = splitted[1]

            position = f'{col}{row}'

            match self.turn:
                case "red":
                    if position in self.blue_boats:
                        self.blue_side[col][row] = 3

                        self.blue_boats.remove(position)
                    else:
                        self.blue_boat[col][row] = 1

                case "blue":
                    if position in self.red_boats:
                        self.red_side[col][row] = 3

                        self.red_boats.remove(position)
                    else:
                        self.red_boat[col][row] = 1

            print("Red side:")
            print(self.red_side)

            print("Blue side:")
            print(self.blue_side)

            if self.red_boats == []:
                print('blue side win')

                break

            if self.blue_boats == []:
                print('red side win')

                break

            self.changeTurn()
    
    def changeTurn(self):
        self.turn = "blue" if self.turn == "red" else "red"

    def setBoat(self, side:str, size:int, position:tuple):
        init = position[0]
        final = position[1]

        init_col = init[0].upper()
        final_col = final[0].upper()

        init_col_n = self.getCol(init_col)
        final_col_n = self.getCol(final_col)

        init_row = int(init[1])
        final_row = int(final[1])


        if final_row - init_row + 1 == size or final_col_n - init_col_n + 1 == size:
            validate_list = []

            if init_col == final_col:
                i = init_row

                while i <= final_row:
                    validate_list.append(f"{init_col}{i}")

                    i += 1

            elif init[1] == final[1]:
                i = init_col_n

                while i <= final_col_n:
                    validate_list.append(f"{self.getCol(i)}{init[1]}")

                    i += 1
            
            for item in validate_list:
                if side == "red" and item not in self.red_boats:
                    pass

                elif side == "blue" and item not in self.blue_boats:
                    pass

                else:
                    return f"{item} in use"

            if init_col == final_col:
                i = init_row

                while i <= final_row:
                    match side:
                        case "red":
                            self.red_side[init_col][str(i)] = 2

                            self.red_boats.append(f"{init_col}{i}")

                        case "blue":
                            self.red_side[init_col][str(i)] = 2

                            self.blue_boats.append(f"{init_col}{i}")

                    i += 1

            if init[1] == final[1]:
                i = init_col_n

                while i <= final_col_n:
                    i_n = self.getCol(i)

                    match side:
                        case "red":
                            self.red_side[i_n][init[1]] = 2

                            self.red_boats.append(f"{i_n}{init[1]}")

                        case "blue":
                            self.blue_side[i_n][init[1]] = 2

                            self.blue_boats.append(f"{i_n}{init[1]}")

                    i += 1
            
            return "boat added"
        else:
            return "invalid position"

    def getCol(self, letter: str | int):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        if type(letter) == str:
            index = letters.index(letter)

            return numbers[index]
        else:
            index = numbers.index(letter)

            return letters[index]

    def setBoats(self, side: str):
        boats_sizes = {
            'aircraft carrier': 5,
            'cruiser': 4,
            'destroyer': 3,
            'tug': 2
        }

        boats_quantities = [
            {'name': 'aircraft carrier', 'quantity': 1},
            {'name': 'cruiser', 'quantity': 2},
            {'name': 'destroyer', 'quantity': 2},
            {'name': 'tug', 'quantity': 3}
        ]

        print(f'{side} side choosing')

        for boat in boats_quantities:
            i = 0

            name = boat.get('name')
            size = boats_sizes.get(name)

            while i < boat.get('quantity'):
                l = True
                while l:
                    print(f'size: {size}')
                    a = input('initial position: ')
                    b = input('final position: ')

                    res = self.setBoat(side, size, (a, b))

                    if res == 'boat added':
                        l = False
                        print(f'{name} added')
                    else:
                        print(res)

                i += 1

if __name__ == "__main__":
    Main()
