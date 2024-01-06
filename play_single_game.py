from utils import Board

import time

def play_single_game(agent_x, agent_o, show=False, win_condition=None):
    # Play game and return moves in reversed order

    assert agent_x.board_dim == agent_o.board_dim, 'Agents have different dims'
    b = Board(agent_x.board_dim, win_condition)
    turn = 0
    player = [1, -1]
    agent = (agent_x, agent_o)
    moves = ([], [])
    while b.empty_cells > 0:
        if show:
            b.show()
            time.sleep(1)
        move = agent[turn].get_move(b)
        moves[turn].insert(0, (b.deepcopy(), move))
        result = b.make_move(move, player[turn])
        if result != 0:
            if show:
                b.show()
                remap = {1: 'x', -1: 'o'}
                print(f"Player '{remap[int(result)]}' wins!")
                time.sleep(1)
            return result, moves
        turn += 1
        turn %= 2
    if show:
        b.show()
        print(f'Draw!')
        time.sleep(1)
    return 0, moves

def play_n_games(agent_x, agent_o, n, win_condition=None):
    res = []
    for i in range(n):
        res.append(play_single_game(agent_x=agent_x, agent_o=agent_o, win_condition=win_condition))
    return res