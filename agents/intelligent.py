import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class AgentNN(nn.Module):
    def __init__(self, board_dim=3, hidden_size=64):
        super().__init__()
        self.board_dim = board_dim
        self.hidden_size = hidden_size

        self.input = nn.Linear(board_dim ** 2, hidden_size)
        self.hidden = nn.Linear(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, board_dim ** 2)

    def forward(self, x):
        x = self.input(x)
        x = F.relu(x)
        x = self.hidden(x)
        x = F.relu(x)
        return self.out(x)

    def save(self, file_name):
        torch.save(self, file_name)


class IntelligentAgent:
    def __init__(self, nn_filename=None, board_dim=3, hidden_size=64):
        self.board_dim = board_dim

        if nn_filename is None:
            self.brain = AgentNN(board_dim, hidden_size)
        else:
            self.brain = torch.load(nn_filename)

        self.optimizer = optim.AdamW(self.brain.parameters(), amsgrad=True)
        self.brain.to(device)
        self.brain.eval()

        self.remap_move = {}
        pos = 0
        for i in range(board_dim):
            for j in range(board_dim):
                self.remap_move[pos] = (i, j)
                pos += 1

    def get_move(self, board):
        with torch.no_grad():
            thought = self.brain(torch.FloatTensor(board.board.flatten()).to(device))
            #print(thought, file=sys.stderr)
            return self.remap_move[thought.to('cpu').argmax().item()]

    def get_move_batch(self, boards):
        thoughts = self.brain(torch.stack([torch.FloatTensor(b[0].board.flatten()) for b in boards]).to(device))
        return thoughts

    def save(self, file_name):
        self.brain.save(file_name)

    def train(self, moves, results):
        self.brain.train()
        actual_moves = self.get_move_batch(moves)
        z = torch.zeros(actual_moves.shape[0], self.board_dim ** 2)
        for i, j in zip(range(actual_moves.shape[0]), actual_moves.argmax(dim=1)):
            z[i,j] = results[i]
        loss = F.cross_entropy(actual_moves, z.to(device))
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        self.brain.eval()