from random import random;
from random import randint;
from dotnode import Node;
from copy import deepcopy;
class AI_Player:
    def __init__(self, playNum):
        self.alpha = 0.5;
        self.gamma = 0.9;
        self.epsilon = 0.1;
        self.playNum = playNum;
        self.q = {};
        self.thisState = None;
        self.thisAction = None;

    def getActions(self, board):
        actions = [];
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if j + 1 < len(board[i]) and not board[i][j].hasNeighbor(board[i][j + 1]):
                    actions.append((i, j, i, j + 1));
                if i + 1 < len(board) and not board[i][j].hasNeighbor(board[i + 1][j]):
                    actions.append((i, j, i + 1, j));
        return actions;
    
    def chooseAction(self, state, actions):
        Q = [self.q.get((state, a), 0.0) for a in actions];
        maxQ = max(Q);

        if random() < self.epsilon:
            mag = max(abs(min(Q)), abs(maxQ));
            Q = [self.q.get((state, a), 0.0) + random() * mag - 0.5*mag for i in actions];
            maxQ = max(Q);

        
        best = [actions[i] for i in range(0, len(Q)) if Q[i] == maxQ];
        pick = best[0] if len(best) <= 1 else best[randint(0, len(best) - 1)];

        return pick;

    def act (self, board):
        actions = self.getActions(board);
        state = tuple([tuple(i) for i in board]);
        self.thisState = state;
        self.thisAction = self.chooseAction(state, actions);
        boardCopy = [list(t) for t in self.thisState];
        conn1 = boardCopy[self.thisAction[0]][self.thisAction[1]];
        conn2 = boardCopy[self.thisAction[2]][self.thisAction[3]];
        conn1.addNeighbor(conn2, self.playNum);
        conn2.addNeighbor(conn1, self.playNum);
        return boardCopy;

    def learn(self, reward):
        boardCopy = [list(t) for t in self.thisState];
        conn1 = boardCopy[self.thisAction[0]][self.thisAction[1]];
        conn2 = boardCopy[self.thisAction[2]][self.thisAction[3]];
        conn1.addNeighbor(conn2, self.playNum);
        conn2.addNeighbor(conn1, self.playNum);
        nextState = tuple([tuple(i) for i in boardCopy]);
        nextActions = self.getActions(boardCopy);

        Qsa = self.q.get((self.thisState, self.thisAction), 0);
        futureQ = [self.q.get((nextState, a), 0) for a in nextActions]
        if len(futureQ) == 0:
            futureQ = [0];
        gammaTerm = self.gamma * max(futureQ);
        self.q[(self.thisState, self.thisAction)] = Qsa + self.alpha*(reward + gammaTerm - Qsa);
                                     
