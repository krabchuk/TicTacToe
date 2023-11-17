vis = {-1: '0', 0: '·', 1: 'X'}
def print_state(state):
    l = int(len(state) ** 0.5)
    for i in range(l):
        out = ''
        for j in range(l):
            out += f' {vis[int(state[i * l + j])]}'
            if j != l - 1:
                out += ' |'
        print(out)
        if i != l - 1:
            print('-' * (l * 4 - 1))