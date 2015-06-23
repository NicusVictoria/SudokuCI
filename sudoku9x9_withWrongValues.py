## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
import random


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
blocks = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            blocks)
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  ## (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  ## Already eliminated
    values[s] = values[s].replace(d, '')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

################ Search ################

def solve(grid): return localSeurchStart(parse_grid(grid)) #was search


def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])


####### Local Search #######
def localSeurch(values, board, wrongValues, score, totalScore):
    #print(totalScore)
    # test = board.copy()
    # for s in squares:
    #     if wrongValues[s] == '':
    #         test[s]= values[s]
    # display(test)
    # board = constructBoard(values)
    # wrongValues = calcWrongValues(values, board, wrongValues, rows, cols)
    # score = evaluation(values, score, rows, cols)
    # totalScore = scoreTotal(score)
    # localSeurch(values, board, wrongValues, score, totalScore)

    for _ in range(0,500): #to prevent never ending loops
        if totalScore == 0:
                return board  ## Solved!
        newBoard, check = smartSeekSwitchBlocks(values, board, wrongValues)
        if check[1]=='':    #if there was no second swich item
            return board ## error no answer
        rowsToCheck = ''.join(vield[0] for vield in check)
        colsToCheck = ''.join(vield[1] for vield in check)
        newScore = evaluation(newBoard, score, rowsToCheck, colsToCheck)
        newTotalScore = scoreTotal(newScore)
        if newTotalScore < totalScore:
            wrongValues = calcWrongValues(values, newBoard, wrongValues, rowsToCheck, colsToCheck)
            return localSeurch(values, newBoard, wrongValues, newScore, newTotalScore)
    board = newBoard
    totalScore = newTotalScore
    return board ##out of time range

def randomWalkLocalSearch(values, board, wrongValues, score, totalScore):
    bestTotalScore = totalScore
    bestBoard = board.copy()
    # bestWrongValues = wrongValues.copy()
    for _ in range(0,5):
        localSeurch(values, board, wrongValues, score, totalScore)
        if totalScore == 0:
            return board  ## Solved!
        if totalScore < bestTotalScore:
            bestTotalScore = totalScore
            bestBoard = board.copy()
            # bestWrongValues = wrongValues.copy()
        board = bestBoard.copy()
        # wrongValues = bestWrongValues.copy()
        print("bestTotal score ",bestTotalScore)

        for _ in range(0,50):#swicht blocks random
            board, check = smartSeekSwitchBlocks(values, board, wrongValues)
            rowsToCheck = ''.join(vield[0] for vield in check)
            colsToCheck = ''.join(vield[1] for vield in check)
            wrongValues = calcWrongValues(values, board, set(), rowsToCheck, colsToCheck)
        score = evaluation(board, score, rows, cols)
        totalScore = scoreTotal(score)
    return board ##out of time range

def randomRestartLocalSearch(values, board, wrongValues, score, totalScore):
    for _ in range(0,5):
        localSeurch(values, board, wrongValues, score, totalScore)
        if totalScore == 0:
            return board  ## Solved!
        boards = []
        for _ in range(0,10):
            b = constructBoard(values)
            s = evaluation(b, score, rows, cols)
            ts = scoreTotal(s)
            boards.append((ts, b))
        totalScore, bestboard = min(boards, key = lambda t: t[0])
        score = evaluation(bestboard, score, rows, cols)
        print("bestboard score ",totalScore)
    return board ##out of time range

def localSeurchStart(values):
    if solved(values):
        return values
    board = constructBoard(values)
    score = dict((s, 9) for s in rows + cols)  # make a dictionary for the score
    score = evaluation(board, score, rows, cols)
    wrongValues = set()  # make a dictionary for the wrongValues (s, '') for s in squares
    wrongValues = calcWrongValues(values, board, wrongValues, rows, cols)
    return randomWalkLocalSearch(values, board, wrongValues, score, scoreTotal(score))

def localSeurchStartBestStart(values):
    if solved(values):
        return values
    boards = []
    score = dict((s, 9) for s in rows + cols)  # make a dictionary for the score
    for _ in range(0,10):
        b = constructBoard(values)
        s = evaluation(b, score, rows, cols)
        ts = scoreTotal(s)
        boards.append((ts, b))
    totalScore, bestboard = min(boards, key = lambda t: t[0])
    score = evaluation(bestboard, score, rows, cols)
    board = bestboard
    wrongValues = set()  # make a dictionary for the wrongValues (s, '') for s in squares
    wrongValues = calcWrongValues(values, board, wrongValues, rows, cols)
    return randomWalkLocalSearch(values, board, wrongValues, score, scoreTotal(score))


def calcWrongValues(values, board, wrongValues, rowsToCheck, colsToCheck):
    for r in rowsToCheck:  # only check the changed rows and cols
        for c in cols:
            s = r + c
            wrongValues.discard(s)
            if len(values[s]) > 1:  # if there are no multiple options for a position in cant be wrong
                if board[s] not in values[s]:  # if the value is not in is's possible values in never van be right
                    wrongValues.add(s)
                elif board[s] in (board[peer] for peer in peers[s]):  # if this value also is in it's peers
                    wrongValues.add(s)
    for c in colsToCheck:
        for r in rows:
            s = r + c
            if r not in rowsToCheck:
                wrongValues.discard(s)
            if len(values[s]) > 1:
                if board[s] not in values[s]:
                    wrongValues.add(s)
                elif board[s] in (board[peer] for peer in peers[s]):
                    wrongValues.add(s)
    return wrongValues


def constructBoard(values):
    board = values.copy()
    for block in blocks:
        vields = dict([s, board[s]] for s in block)
        toDo = set(s for s in block if len(board[s]) > 1)
        ans = constuctBlock(vields, toDo, [])
        for s in block:
            board[s] = ans[s]
    return board

def constuctBlock(vields, toDo, ans):
    if len(toDo) == 0:
        return vields
    # minLengt, vield = min((len(vields[vield]), vield) for vield in toDo)
    # if minLengt == 0:
    #     return False
    vield = random.choice(list(toDo))
    if len(vields[vield]) == 0:
        return False
    rndvalue = list(vields[vield])
    random.shuffle(rndvalue)
    for value in rndvalue:
        newVields = vields.copy()
        newToDo = toDo.copy()
        for v in toDo:
           newVields[v] = newVields[v].replace(value, '')
        newVields[vield] = value
        newToDo.discard(vield)
        ans = constuctBlock(newVields, newToDo, ans)
        if ans:
            return ans


def evaluation(values, score, rowsToCheck, colsToCheck):
    for r in rowsToCheck:  # check witch number is not there in each row and column and count the length
        possible = digits
        for c in cols:
            possible = possible.replace(values[r + c], '')
        score[r] = len(possible)
    for c in colsToCheck:
        possible = digits
        for r in rows:
            possible = possible.replace(values[r + c], '')
        score[c] = len(possible)
    return score


def scoreTotal(score):
    return sum(score.values())


def seekSwitchBlocks(board):
    block = random.choice(blocks)
    vield, switchVield = random.sample(block, 2)
    for switchVield in block:
        if switchVield != vield:
            tmp = board[vield]
            board[vield] = board[switchVield]
            board[switchVield] = tmp
            break
    return board, [vield, switchVield]

def smartSeekSwitchBlocks(values, board, wrongValues):
    random.shuffle(blocks)
    for block in blocks:
        random.shuffle(block)
        for vield in block:
            if vield in wrongValues:
                #random.shuffle(block)
                for switchVield in block:
                    if switchVield != vield and board[vield] in values[switchVield]:
                        switched = board[vield]
                        board[vield] = board[switchVield]
                        board[switchVield] = switched
                        return board, [vield, switchVield]

def tosmartSeekSwitchBlocks(values, board, wrongValues):
    switchVield = ''
    switched = ''
    random.shuffle(blocks)
    for block in blocks:
        random.shuffle(block)
        for vield in block:
            if vield in wrongValues:
                for switchVield in block:
                    if switchVield != vield:
                        bestVield = vield
                        bestSwitchVield = switchVield
                        if board[vield] in values[switchVield]:
                            bestVield = vield
                            bestSwitchVield = switchVield
                            if board[switchVield] in values[vield]:
                                # can be better by checking if also board[swichVield] in values[vield] but then it can hafe no autput
                                switched = board[vield]
                                board[vield] = board[switchVield]
                                board[switchVield] = switched
                                break
    if switched == '':
        try:
            switched = board[bestVield]
            board[bestVield] = board[bestSwitchVield]
            board[bestSwitchVield] = switched
        except:
            return
    return board, [vield, switchVield]

################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)


def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ System test ################

import time, random


def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))


def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unitsolved(unit) for unit in unitlist)


def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s]) == 1 else '.' for s in squares)
    return random_puzzle(N)  ## Give up and make a new puzzle


grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

if __name__ == '__main__':
    #test()
    #display(parse_grid(hard1))
    solution = localSeurchStart(parse_grid(hard1))
    display(solution)
    #solve_all(from_file("easy50.txt", '========'), "easy", None)
    #solve_all(from_file("top95.txt"), "hard", None)
    # solve_all(from_file("hardest.txt"), "hardest", None)
    # solve_all([random_puzzle() for _ in range(99)], "random", 100.0)

    ## References used:
    ## http://www.scanraid.com/BasicStrategies.htm
    ## http://www.sudokudragon.com/sudokustrategy.htm
    ## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
    ## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
