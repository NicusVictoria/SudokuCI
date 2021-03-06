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

def cross(aa, bb):
    #"Cross product of elements in A and elements in B."
    return [a+b for a in aa for b in bb]

rows9  = '123456789'
rows16 = '123456789abcdefg'
rows25 = '123456789abcdefghijklmnop'
cols9    = 'ABCDEFGHI'
cols16   = 'ABCDEFGHIJKLMNOP'
cols25   = 'ABCDEFGHIJKLMNOPQRSTUVWXY'

squares9  = cross(rows9, cols9)
squares16 = cross(rows16, cols16)
squares25 = cross(rows25, cols25)

#if(len(squares) == 81):
rows = rows9
cols = cols9
blocks = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = [cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + blocks
squares = squares9
digits  = rows
# elif(len(squares) == 169):
#     blocks = [cross(rs, cs) for rs in ('ABCD','EFGH','IJKL','MNOP') for cs in ('1234','5678','9abc','defg')]
#     unitlist = ([cross(rows, c) for c in cols] +
#                 [cross(r, cols) for r in rows] +
#                  blocks)
#     squares = squares16
#     digits  = cols16
# elif(len(squares) == 625):
#     blocks = [cross(rs, cs) for rs in ('ABCDE','FGHIJ','KLMNO','PQRST','UVWXY') for cs in ('12345','6789a','bcdef','ghijk','lmnop')];
#     unitlist = ([cross(rows, c) for c in cols] +
#                 [cross(r, cols) for r in rows] +
#                 blocks)
#     squares = squares25
#     digits  = cols25

units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))- {s})
             for s in squares)

################ Unit Tests ################

#def test():
#    "A set of tests that must pass."
#    assert len(squares) == 81 | 169 | 625
#    assert len(unitlist) == len(squares)/3
#    assert all(len(units[s]) == 3 for s in squares)
#    assert all(len(peers[s]) == 20 for s in squares)
#    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
#                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
#                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
#    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
#                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
#                               'A1', 'A3', 'B1', 'B3'])
#    print 'All tests pass.'

################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values

def grid_values(grid):
    """Convert grid into a dict of {square: char} with '0' or '.' for empties."""
    chars = [c for c in grid if c in digits or c in '0.']
    #assert len(chars) == 81 | len(chars) == 169 | len(chars) == 625
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
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values

################ Display as 2-D grid ################

def display(values):
    """Display these values as a 2-D grid."""
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print()
    
    # if len(squares) == 81:
    #     width = 1+max(len(values[s]) for s in squares)
    #     line = '+'.join(['-'*(width*3)]*3)
    #     for r in rows9:
    #         print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols9))
    #         if r in 'CF': print(line)
    #
    # if len(squares) == 169:
    #     width = 1+max(len(values[s]) for s in squares)
    #     line = '+'.join(['-'*(width*4)]*4)
    #     for r in rows16:
    #         print(''.join(values[r + c].center(width) + ('|' if c in '48c' else '')
    #                       for c in cols16))
    #         if r in 'DHL': print(line)
    #
    # if len(squares) == 625:
    #     width = 1+max(len(values[s]) for s in squares)
    #     line = '+'.join(['-'*(width*5)]*5)
    #     for r in rows25:
    #         print(''.join(values[r + c].center(width) + ('|' if c in '5afk' else '')
    #                       for c in cols25))
    #         if r in 'EJOT': print(line)
    #
    # print()

################ Search ################

def solve(grid): return display(search(parse_grid(grid)))

def search(values):
    """Using depth-first search and propagation, try all possible values."""
    if values is False:
        print("Failed before search")
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])
                
def localSeurch(values, board, wrongValues, score, totalScore):
    newBoard, check = seekSwitchBlocks(values, board, wrongValues)
    print(check)
    rowsToCheck = (vield[1] for vield in check)
    colsToCheck = (vield[2] for vield in check)
    newScore = evaluation(values, score, rowsToCheck, colsToCheck)
    newTotalScore = scoreTotal(newScore)
    if newTotalScore == 0:
        return values ## Solved!
    if newTotalScore > totalScore:
        wrongValues = calcWrongValues (values, newBoard, wrongValues, rowsToCheck, colsToCheck)
        return localSeurch(values, newBoard, wrongValues, newScore, newTotalScore)


def localSeurchStart(values):
    board = constructBoard(values)
    score = dict((s, 9) for s in rows + cols)#make a dictionary for the score
    score = evaluation(board, score, rows, cols)
    wrongValues = dict((s, '') for s in squares)#make a dictionary for the wrongValues
    wrongValues = calcWrongValues(values, board, wrongValues, rows, cols)
    localSeurch(values, board, wrongValues, score, scoreTotal(score))


def calcWrongValues    (values, board, oldWrongValues, rowsToCheck, colsToCheck):
    wrongValues = oldWrongValues
    for r in rowsToCheck: #only check the changed rows and cols
        for c in cols:
            s = r+c
            if len(values[s]) > 1: #if there are no multiple options for a position in cant be wrong
                if board[s] not in values[s]: #if the value is not in is's possible values in never van be right
                    wrongValues[s] = board[s]
                elif board[s] not in (values[peer] for peer in peers[s]):    #if this value also is in it's peers
                    wrongValues[s] = board[s]
                else:
                    wrongValues[s] = ''
    for c in colsToCheck:
        for r in rows:
            s = r+c
            if len(values[s]) > 1:
                if board[s] not in values[s]:
                    wrongValues[s] = board[s]
                elif board[s] not in (values[peer] for peer in peers[s]):
                    wrongValues[s] = board[s]
                else:
                    wrongValues[s] = ''
    return wrongValues

def constructBoard(values):
    for block in blocks:
        possible = digits
        toDo = []
        for i in range(0, len(block)-1): #always place the first of the possible values
            vield = block[i]
            if len(values[vield])>0 : #if there is nothing possible in should be given the rest value
                value = values[vield][0]
                for j in range(i, len(block)-1):
                    values[block[j]] = values[block[j]].replace(value,'')
                values[vield] = value
                possible = possible.replace(values[r+c],'')
            else:
                toDo.add(vield)
        for i in range(0, len(toDo)-1):
            values[toDo[i]] = possible[i]
    return values;

def evaluation(values, score, rowsToCheck, colsToCheck):
    for r in rowsToCheck: #check witch number is not there in each row and column and count the length
        possible = digits
        score[r] += len(possible.replace(values[r+c],'') for c in cols)
    for c in colsToCheck:
        possible = digits
        score[c] += len(possible.replace(values[r+c],'') for r in rows)
    return score

def scoreTotal(score):
    return sum(s for s in score)

def seekSwitchBlocks(values, board, wrongValues):
    rndblocks = random.shuffle(blocks)
    for block in rndblocks:
        rndvields = random.shuffle(block)
        for vield in rndvields:
            if wrongValues[vield] != '':
                for swichVield in rndvields:
                    if swichVield != vield and board[vield] in values[swichVield]:
                    #can be better by checking if also board[swichVield] in values[vield] but then it can hafe no autput
                        board[vield] = board[swichVield]
                        board[swichVield] = wrongValues[vield]
                        break
    return board, [vield, swichVield]
                        
                          
                
################ Utilities ################

def some(seq):
    """Return some element of seq that is true."""
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    """Parse a file into a list of strings, separated by sep."""
    return open(filename).read().strip().split(sep)

def shuffled(seq):
    """Return a randomly shuffled copy of the input sequence."""
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
        t = time.clock()-start
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
    """A puzzle is solved if each unit is a permutation of the digits 1 to 9."""
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
        if len(ds) >= N and len(set(ds)) >= 8 and len(squares) == 81:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
            
        if len(ds) >= N and len(set(ds)) >= 15 and len(squares) == 169:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
            
        if len(ds) >= N and len(set(ds)) >= 24 and len(squares) == 625:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
            
    return random_puzzle(N) ## Give up and make a new puzzle

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
if __name__ == '__main__':
    #test()
    solve_all(from_file("easy50.txt", '========'), "easy", None)
    solve_all(from_file("top95.txt"), "hard", None)
    solve_all(from_file("hardest.txt"), "hardest", None)
    solve_all([random_puzzle() for _ in range(99)], "random", 100.0)

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
