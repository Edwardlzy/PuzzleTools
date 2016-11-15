from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # implement __eq__ and __str__
    # __repr__ is up to you
    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> start_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> p1 = MNPuzzle(start_grid, target_grid)
        >>> p2 = MNPuzzle(start_grid1, target_grid)
        >>> p1.__eq__(p2)
        False
        >>> p3 = MNPuzzle(start_grid, target_grid)
        >>> p1.__eq__(p3)
        True
        """
        return (type(self) == type(other) and self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> p1 = MNPuzzle(start_grid, target_grid)
        >>> print(p1)
        *23
        145
        """
        result = ''
        for i in self.from_grid:
            for j in i:
                result += j
            result += '\n'
        result = result[:-1]
        return result

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"
    def extensions(self):
        """
        Return a list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("1", "2", "3"), ("4", "*", "5"))
        >>> p1 = MNPuzzle(start_grid, target_grid)
        >>> L1 = p1.extensions()
        >>> print(len(L1))
        3
        """
        if self.is_solved():
            return[]
        else:
            result = []
            i, j = 0, 0
            new_start_grid = [list(x) for x in self.from_grid]
            for x in range(len(new_start_grid)):
                for y in range(len(new_start_grid[x])):
                    if new_start_grid[x][y] == "*":
                        i = x
                        j = y

            if i - 1 >= 0:
                # swap with the one above.
                start1 = [x[:] for x in new_start_grid]
                temp = start1[i - 1][j]
                start1[i - 1][j] = "*"
                start1[i][j] = temp
                new_start = tuple(tuple(x for x in y) for y in start1)
                result.append(MNPuzzle(new_start, self.to_grid))
            if i + 1 < len(new_start_grid):
                # swap with the one below.
                start2 = [x[:] for x in new_start_grid]
                temp = start2[i + 1][j]
                start2[i + 1][j] = "*"
                start2[i][j] = temp
                new_start = tuple(tuple(x for x in y) for y in start2)
                result.append(MNPuzzle(new_start, self.to_grid))
            if j - 1 >= 0:
                # swap with the one to the left.
                start3 = [x[:] for x in new_start_grid]
                temp = start3[i][j - 1]
                start3[i][j - 1] = "*"
                start3[i][j] = temp
                new_start = tuple(tuple(x for x in y) for y in start3)
                result.append(MNPuzzle(new_start, self.to_grid))
            if j + 1 < len(new_start_grid[i]):
                # swap with the one to the right.
                start4 = [x[:] for x in new_start_grid]
                temp = start4[i][j + 1]
                start4[i][j + 1] = "*"
                start4[i][j] = temp
                new_start = tuple(tuple(x for x in y) for y in start4)
                result.append(MNPuzzle(new_start, self.to_grid))
            return result

    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid
    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool

        >>> start_grid = (("1", "2", "3"), ("4", "*", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> p1 = MNPuzzle(start_grid, target_grid)
        >>> p1.is_solved()
        False
        >>> start_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> p2 = MNPuzzle(start_grid1, target_grid)
        >>> p2.is_solved()
        True
        """
        return self.from_grid == self.to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
