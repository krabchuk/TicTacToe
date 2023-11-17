from IPython.display import clear_output

def show_field(field):
    n = len(field)
    remap = {0: ' ', 1: 'x', -1: 'o'}
    clear_output(wait=True)
    print('    ', end='')
    for i in range(n):
        print(f"{i}   ", end='')
    print()
    for i in range(n):
        print('    ', end='')
        print('-   ' * n)
        print(f"{i} | ", end='')
        print(' | '.join(map(lambda x: remap[x], field[i])) + ' |')
    print('    ' + '-   ' * n)