"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)

def del_fail_children(list_of_puzzle):
    """
    Delete all unsolvable puzzle in list_of_puzzle.

    @type puzzle_node: PuzzleNode
    @rtype: None
    """
    children_list = list_of_puzzle[:]
    for child in children_list:
        if child.fail_fast():
            list_of_puzzle.remove(child)

def depth_first_solve(puzzle, d=deque()):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @type d: deque
    @rtype: PuzzleNode
    """
    # If the puzzle is already solved, return the current node.
    rnode = PuzzleNode(puzzle)
    d.append(str(puzzle))
    if puzzle.is_solved():
        return rnode
    elif puzzle.fail_fast():
        return None
    # If the puzzle is not solved, find all solvable next step. If there
    # are no solvable child, return None. Then call the function again on
    # every solvable child, if the function return a PuzzleNode a, then
    # return a new PuzzleNode that use the PuzzleNode a as its child.
    else:
        children = puzzle.extensions()
        del_fail_children(children)
        if len(children) == 0:
            return None
        else:
            for c in children:
                if str(c) not in d:
                    d.append(str(c))
                    r = depth_first_solve(c)
                    if r is not None:
                        return PuzzleNode(puzzle, [r])
            return None

# TODO
# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque

# def visit_level(puzzle, n):
#     """
#
#     @type puzzle
#     @type n:
#     @rtype:
#     """
#     lst = []
#     if n == 0:
#         return [PuzzleNode(puzzle)]
#     elif n == 1:
#         for c in puzzle.extensions():
#             lst.append(PuzzleNode(c, [], PuzzleNode(puzzle)))
#     else:
#         for c in puzzle.extensions():
#             lst.extend(visit_level(c, n-1, d))
#     return lst


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @type d: deque
    @rtype: PuzzleNode
    """
    # rnode = PuzzleNode(puzzle)
    # n = 0
    # while all([not p.puzzle.is_solved() for p in visit_level(puzzle, n)]):
    #     n += 1
    # a = visit_level(puzzle, n)
    # i = 0
    # while i < len(a) and not a[i].puzzle.is_solved():
    #     i += 1
    # sol = a[i]
    # while n != 1:
    #     for parent in visit_level(puzzle, n-1):
    #         if sol.parent.puzzle == parent.puzzle:
    #             parent.children = \
    #                 [PuzzleNode(sol.puzzle, sol.children.copy(),
    #                             PuzzleNode(sol.parent.puzzle))]
    #             sol = parent
    #     n = n - 1
    # rnode.children.append(sol)
    # return rnode
    d = deque([PuzzleNode(puzzle)])
    checked_puzzle = []
    checked_puzzle.append(str(puzzle))
    while len(d) != 0:
        rnode = d.pop()
        if rnode.puzzle.is_solved():
            while rnode.parent is not None:
                rnode.parent.children = [rnode]
                rnode = rnode.parent
            return rnode
        else:
            ext = rnode.puzzle.extensions()
            for e in ext:
                if str(e) not in checked_puzzle:
                    checked_puzzle.append(str(e))
                    d.appendleft(PuzzleNode(e, [], rnode))


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
