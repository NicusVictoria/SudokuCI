import random, time

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
grid4  = '0900000e060g00b0000000003080001g0000ca0b09003000000005610afb00d070000300006100fb0c0f740d00200001000000a0000de0000e30000000000400004080000056000f0b00000000001050610000c000408e0000006000f00ad7009070000300000000a0000d70000001050000a00c000400e00000000000000004'
grid5  = 'b...dh3.ig...8....5l.6en.2..3.b.7.1io..mh.d9k5..a.n169..k....7.a......4...f........84..5.3aj..o7.m..le.hp.n.c.....4m.1...2..8.i..c.e.k3...mg.p.....d.a.....cg42of..ji8..h............m....ke..o3.6....1...a..i.b1.4.93p..gfn...l.84be26...n1..h7..ac...p.g.lf...j.o....b.e..k........pi9.....cl...d4h86...3j3og..52...a.1nk7l9.....ph.b.m..hglf....o.........7621....8.9...p.fin....be.h...6..e7.5....1.fi.839okc..dija.4.2m..h5..n..l7......fn...md3.icp9....e56.k5..3.o1.l..a.nj28..d....age....h6....7.....c.b..4...2.m1l...8...3o.......9o.m.g...dhk9..b..i2.e76...f.6..83.2.5n.d...jp........8a9co.6.4..2k1e.m.i..dp.....5....1.c..8l....kgo'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

cols3 = '123456789'
cols4 = '123456789abcdefg'
cols5 = '123456789abcdefghijklmnop'

rows3 = 'ABCDEFGHI'
rows4 = 'ABCDEFGHIJKLMNOP'
rows5 = 'ABCDEFGHIJKLMNOPQRSTUVWXY'

unitcols3 = ('123','456','789')
unitcols4 = ('1234','5678','9abc','defg')
unitcols5 = ('12345','6789a','bcdef','ghijk','lmnop')

unitrows3 = ('ABC','DEF','GHI')
unitrows4 = ('ABCD','EFGH','IJKL','MNOP')
unitrows5 = ('ABCDE','FGHIJ','KLMNO','PQRST','UVWXY')

def createunit(grid):
    if len(grid) == 81:
        unitlist = ([cross(rows3, c) for c in cols3] +
            [cross(r, cols3) for r in rows3] +
            [cross(rs, cs) for rs in unitrows3 for cs in unitcols3])
        return dict((s, [u for u in unitlist if s in u])
             for s in cross(rows3,cols3))

    if len(grid) == 256:
        unitlist = ([cross(rows4, c) for c in cols4] +
            [cross(r, cols4) for r in rows4] +
            [cross(rs, cs) for rs in unitrows4 for cs in unitcols4])
        return dict((s, [u for u in unitlist if s in u])
             for s in cross(rows4,cols4))

    if len(grid) == 625:
        unitlist = ([cross(rows5, c) for c in cols5] +
            [cross(r, cols5) for r in rows5] +
            [cross(rs, cs) for rs in unitrows5 for cs in unitcols5])
        return dict((s, [u for u in unitlist if s in u])
             for s in cross(rows5,cols5))

def solve(grid): return search(parse_grid(grid), grid)

def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    
    
    def time_solve(grid):
    
        if len(grid) == 81:
            rows = rows3
            cols = cols3

        if len(grid) == 256:
            rows = rows4
            cols = cols4

        if len(grid) == 625:
            rows = rows5
            cols = cols5
    
        start = time.clock()
        values = solve(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid, cols, rows), grid)
            if values: display(values,grid)
            print '(%.2f seconds)\n' % t
        return (t, solved(values),grid)
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solved(values, grid):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    
    if len(grid) == 81:
        rows = rows3
        cols = cols3
        unitrows = unitrows3
        unitcols = unitcols3

    if len(grid) == 256:
        rows = rows4
        cols = cols4
        unitrows = unitrows4
        unitcols = unitcols4

    if len(grid) == 625:
        rows = rows5
        cols = cols5
        unitrows = unitrows5
        unitcols = unitcols5
            
            
    unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in unitrows for cs in unitcols])        
    
            
    def unitsolved(unit): return set(values[s] for s in unit) == set(cols)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: cols}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    
    if len(grid) == 81:
        print "9x9 grid detected"
        values = dict((s, cols3) for s in cross(rows3,cols3))
        cols = cols3
        rows = rows3

    elif len(grid) == 256:
        print "16x16 grid detected"
        values = dict((s, cols4) for s in cross(rows4,cols4))
        cols = cols4
        rows = rows4

    elif len(grid) == 625:
        print "25X25 grid detected"
        values = dict((s, cols5) for s in cross(rows5,cols5))
        cols = cols5
        rows = rows5
    else:
        print len(grid)
        return None

    units = createunit(grid)
    peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in cross(rows,cols))
    
    for s,d in grid_values(grid, cols, rows).items():
        if d in cols and not assign(values, s, d, peers, grid):
            return False ## (Fail if we can't assign d to square s.)
    return values

def grid_values(grid, cols, rows):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in cols or c in '0.']
    # assert len(chars) == 81
    return dict(zip(cross(rows,cols), chars))

def assign(values, s, d, peers, grid):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2, peers, grid) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d, peers, grid):
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
        if not all(eliminate(values, s2, d2, peers, grid) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    units = createunit(grid)
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d, peers, grid):
                return False
    return values

def display(values, grid):
    "Display these values as a 2-D grid."
    if len(grid) == 81:
        for r in rows3:
            for c in cols3:
                print values[r+c],
                if c in '36': print '|',
            print
            if r in 'CF': print '-'*6 + '+' + '-'*7 + '+' + '-'*6
        print

    if len(grid) == 256: 
        for r in rows4:
            for c in cols4:
                print values[r+c],
                if c in '48c': print '|',
            print
            if r in 'DHL': print '-'*8 + '+' + '-'*9 + '+' + '-'*9 + '+' + '-'*8
        print

    if len(grid) == 625: 
        for r in rows5:
            for c in cols5:
                print values[r+c],
                if c in '5afk': print '|',
            print
            if r in 'EJOT': print '-'*10 + '+' + '-'*11 + '+' + '-'*11 + '+' + '-'*11 + '+' + '-'*10
        print

def search(values, grid):
    "Using depth-first search and propagation, try all possible values."
    if len(grid) == 81:
        rows = rows3
        cols = cols3

    if len(grid) == 256:
        rows = rows4
        cols = cols4

    if len(grid) == 625:
        rows = rows5
        cols = cols5

    units = createunit(grid)
    peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in cross(rows,cols))
    
    if values is False:
        print "failed."
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in cross(rows,cols)):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in cross(rows,cols) if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d, peers, grid), grid)
                for d in values[s])

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def random_puzzle(unitsize):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    if unitsize == 81:
        rows = rows3
        cols = cols3
        N = 17
        D = 8

    elif unitsize == 256:
        rows = rows4
        cols = cols4
        N = 55
        D = 15

    elif unitsize == 625:
        rows = rows5
        cols = cols5
        N = 151
        D = 24

    else:
        print "Unitsize invalid"
        return None

    grid = generate_emptygrid(unitsize)
    units = createunit(grid)
    peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in cross(rows,cols))
    values = dict((s, cols) for s in cross(rows,cols))
    for s in shuffled(cross(rows,cols)):
        if not assign(values, s, random.choice(values[s]), peers, grid):
            break
        ds = [values[s] for s in cross(rows,cols) if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= D:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in cross(rows,cols))
    return random_puzzle(N) ## Give up and make a new puzzle

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

def generate_emptygrid(unitsize):
    return '.'*unitsize
    
def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return file(filename).read().strip().split(sep)
    
#if __name__ == '__main__':
#    solve_all(from_file("easy50.txt", '========'), "easy", None)
#    solve_all(from_file("top95.txt"), "hard", None)
#    solve_all(from_file("hardest.txt"), "hardest", None)
#    solve_all([random_puzzle(81) for _ in range(99)], "random", 100.0)
#    solve_all([random_puzzle(256) for _ in range(99)], "random", 100.0)
#    solve_all([random_puzzle(625) for _ in range(99)], "random", 100.0)
    
