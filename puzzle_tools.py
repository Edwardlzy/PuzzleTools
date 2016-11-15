"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def remove_fail(lst):
    """
    Delete children which cannot lead to a solution.

    @type lst: list[PuzzleNode]
    @rtype: None
    """
    new_lst = lst[:]
    for item in new_lst:
        if item.fail_fast():
            lst.remove(item)


# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
def depth_first_solve(puzzle, q=deque()):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    Idea inspired by:
    https://algocoding.wordpress.com/2014/08/25/depth-first-search-java-and-python-implementation/

    @type puzzle: Puzzle
    @type q: deque
    @rtype: PuzzleNode
    """
    pnode = PuzzleNode(puzzle)
    q.append(str(puzzle))
    if puzzle.fail_fast():
        return None
    elif puzzle.is_solved():
        return pnode
    else:
        children = puzzle.extensions()
        remove_fail(children)
        if len(children) != 0:
            for child in children:
                if str(child) not in q:
                    q.append(str(child))
                    new = depth_first_solve(child)
                    if new:
                        return PuzzleNode(puzzle, [new])

# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    Idea Reference: http://jeremykun.com/2013/01/22/depth-and-breath-first-search/

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    deque_ = deque([PuzzleNode(puzzle)])
    checked = {str(puzzle)}
    while len(deque_) != 0:
        pnode = deque_.pop()
        if pnode.puzzle.is_solved():
            while pnode.parent:
                # this node is not root node.
                pnode.parent.children = [pnode]
                pnode = pnode.parent
            return pnode
        else:
            for item in pnode.puzzle.extensions():
                if str(item) not in checked:
                    checked.add(str(item))
                    deque_.appendleft(PuzzleNode(item, [], pnode))


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
        Return whether PuzzleNode self is equivalent to other

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
