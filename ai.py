import random


def choose_easy_move(game, computer_symbol):
    moves = game.available_moves()
    return random.choice(moves) if moves else None


def find_winning_move(game, symbol):
    for position in game.available_moves():
        game.board[position] = symbol
        won = game.check_winner(symbol)
        game.board[position] = ""

        if won:
            return position

    return None


def choose_medium_move(game, computer_symbol):
    human_symbol = "O" if computer_symbol == "X" else "X"

    move = find_winning_move(game, computer_symbol)
    if move is not None:
        return move

    move = find_winning_move(game, human_symbol)
    if move is not None:
        return move

    if game.board[4] == "":
        return 4

    corners = [position for position in (0, 2, 6, 8) if game.board[position] == ""]
    if corners:
        return random.choice(corners)

    return choose_easy_move(game, computer_symbol)


def choose_hard_move(game, computer_symbol):
    human_symbol = "O" if computer_symbol == "X" else "X"
    best_score = -1000
    best_moves = []

    for position in game.available_moves():
        game.board[position] = computer_symbol
        score = minimax(
            game,
            is_maximising=False,
            computer_symbol=computer_symbol,
            human_symbol=human_symbol,
            depth=0,
        )
        game.board[position] = ""

        if score > best_score:
            best_score = score
            best_moves = [position]
        elif score == best_score:
            best_moves.append(position)

    return random.choice(best_moves) if best_moves else None


def minimax(game, is_maximising, computer_symbol, human_symbol, depth):
    if game.check_winner(computer_symbol):
        return 10 - depth

    if game.check_winner(human_symbol):
        return depth - 10

    if "" not in game.board:
        return 0

    if is_maximising:
        best_score = -1000

        for position in game.available_moves():
            game.board[position] = computer_symbol
            score = minimax(
                game,
                False,
                computer_symbol,
                human_symbol,
                depth + 1,
            )
            game.board[position] = ""
            best_score = max(best_score, score)

        return best_score

    best_score = 1000

    for position in game.available_moves():
        game.board[position] = human_symbol
        score = minimax(
            game,
            True,
            computer_symbol,
            human_symbol,
            depth + 1,
        )
        game.board[position] = ""
        best_score = min(best_score, score)

    return best_score


def choose_move(game, difficulty, computer_symbol):
    if difficulty == "Easy":
        return choose_easy_move(game, computer_symbol)

    if difficulty == "Medium":
        return choose_medium_move(game, computer_symbol)

    return choose_hard_move(game, computer_symbol)
