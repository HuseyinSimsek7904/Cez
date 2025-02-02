from libs import position_lib
import re


class Move:
    def __init__(self, from_, to, capture):
        self.from_ = from_
        self.to = to
        self.capture = capture

    def copy(self):
        return Move(self.from_.copy(), self.to.copy(), self.capture.copy())

    @property
    def delta(self):
        return self.to - self.from_

    @property
    def name(self):
        if self.to.column == self.from_.column:
            name = str(self.to.row + 1)
        else:
            name = "abcdefgh"[self.to.column]

        if self.capture is None:
            return f"{self.from_}>{name}"

        else:
            return f"{self.from_}x{name}"

    def __repr__(self):
        return self.name

    @property
    def advantage(self):
        if self.capture:
            return self.to.advantage - self.from_.advantage - self.capture.advantage

        else:
            return self.to.advantage - self.from_.advantage


def from_text(move):
    match_ = re.match("^([a-h][1-8])([>x])([a-h1-8])$", move)

    if not match_:
        raise ValueError(f"Invalid syntax '{move}'")

    from_, capture, to = match_.groups()
    from_ = position_lib.from_text(from_)

    try:
        to = position_lib.Position(from_.column, int(to) - 1)

    except ValueError:
        to = position_lib.Position("abcdefgh".index(to), from_.row)

    move = Move(from_, to, None)
    if capture == 'x':
        dif = move.delta

        if dif.column == 2:
            move.capture = position_lib.Position(from_.column + 1, from_.row)
        elif dif.column == 3:
            move.capture = position_lib.Position(from_.column + 2, from_.row)
        elif dif.column == -2:
            move.capture = position_lib.Position(from_.column - 1, from_.row)
        elif dif.column == -3:
            move.capture = position_lib.Position(from_.column - 2, from_.row)

        elif dif.row == 2:
            move.capture = position_lib.Position(from_.column, from_.row + 1)
        elif dif.row == 3:
            move.capture = position_lib.Position(from_.column, from_.row + 2)
        elif dif.row == -2:
            move.capture = position_lib.Position(from_.column, from_.row - 1)
        elif dif.row == -3:
            move.capture = position_lib.Position(from_.column, from_.row - 2)

        else:
            raise ValueError("shit")

    return move


def moves_from_text(moves: str):
    if moves.startswith("[") and moves.endswith("]"):
        moves = moves[1:-1]

    m = []
    for item in moves.split(", "):
        m.append(from_text(item))

    return m
