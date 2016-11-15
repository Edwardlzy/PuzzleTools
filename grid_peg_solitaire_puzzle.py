from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # implement __eq__, __str__ methods
    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", ".", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> g = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(g)
        *****
        *****
        *****
        **.**
        *****
        """
        result = []
        for row in self._marker:
            for item in row:
                result.append(item)
            result.append("\n")
        s = result[:-1]
        return ''.join(s)

    # __repr__ is up to you
    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = [["*", "*", "*", "*", "*"],\
                     ["*", "*", "*", "*", "*"],\
                     ["*", "*", "*", "*", "*"],\
                     ["*", "*", ".", "*", "*"],\
                     ["*", "*", "*", "*", "*"]]
        >>> grid2 = [["#", "*", "*", "*", "*"],\
                     ["*", "*", "*", "*", "*"],\
                     ["*", "*", "*", "*", "*"],\
                     ["*", "*", ".", "*", "*"],\
                     ["*", "*", "*", "*", "*"]]
        >>> g1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> g2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> g1.__eq__(g2)
        False
        >>> g3 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> g3.__eq__(g2)
        True
        """
        return (type(self) == type(other) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def extensions(self):
        """
        Return a list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = [[".", ".", "."]]
        >>> grid += [["*", "*", "."]]
        >>> g = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> L1 = list(g.extensions())
        >>> grid[-1][-1] = "*"
        >>> grid[-1][-3] = "."
        >>> grid[-1][-2] = "."
        >>> L2 = [GridPegSolitairePuzzle(grid, {"*", ".", "#"})]
        >>> len(L1) == len(L2)
        True
        >>> all([s in L2 for s in L1])
        True
        >>> all([s in L1 for s in L2])
        True
        """
        # convenient names
        marker, marker_set = self._marker, self._marker_set
        if self.is_solved():
            # return an empty list
            return []
        else:
            result = []
            for i in range(len(marker)):
                for j in range(len(marker[i])):
                    if marker[i][j] == ".":
                        if i - 2 >= 0 and marker[i - 2][j] == "*":
                            if marker[i - 1][j] == "*":
                                copy1 = [x[:] for x in marker]
                                copy1[i - 2][j] = "."
                                copy1[i - 1][j] = "."
                                copy1[i][j] = "*"
                                result.append(GridPegSolitairePuzzle(copy1, {"*", ".", "#"}))
                        if i + 2 < len(marker) and marker[i + 2][j] == "*":
                            if marker[i + 1][j] == "*":
                                copy2 = [x[:] for x in marker]
                                copy2[i + 2][j] = "."
                                copy2[i + 1][j] = "."
                                copy2[i][j] = "*"
                                result.append(GridPegSolitairePuzzle(copy2, {"*", ".", "#"}))
                        if j + 2 < len(marker[i]) and marker[i][j + 2] == "*":
                            if marker[i][j + 1] == "*":
                                copy3 = [x[:] for x in marker]
                                copy3[i][j + 2] = "."
                                copy3[i][j + 1] = "."
                                copy3[i][j] = "*"
                                result.append(GridPegSolitairePuzzle(copy3, {"*", ".", "#"}))
                        if j - 2 >= 0 and marker[i][j - 2] == "*":
                            if marker[i][j - 1] == "*":
                                copy4 = [x[:] for x in marker]
                                copy4[i][j - 2] = "."
                                copy4[i][j - 1] = "."
                                copy4[i][j] = "*"
                                result.append(GridPegSolitairePuzzle(copy4, {"*", ".", "#"}))
            return result

    # override is_solved
    # A configuration is solved when there is exactly one "*" left
    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = [[".", ".", "."]]
        >>> grid += [["*", "*", "."]]
        >>> g = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> g.is_solved()
        False
        >>> grid1 = [[".", ".", "."]]
        >>> grid1 += [[".", ".", "*"]]
        >>> a = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> a.is_solved()
        True
        """
        num = 0
        for row in self._marker:
            for item in row:
                if item == "*":
                    num += 1
        if num == 1:
            return True
        return False

    # def fail_fast(self):
    #     """
    #     Return True iff GridPegSolitairePuzzle can never be solved.
    #
    #     @type self: GridPegSolitairePuzzle
    #     @rtype: bool
    #
    #     """
    #     if not self.extensions():
    #         if not self.is_solved():
    #             return True
    #     return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
