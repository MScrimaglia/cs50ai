import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.discard(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_safe(cell)

    # Check if a sentence has known mines or safes and returns True if so
    def check_sentence(self, sentence):
        if len(sentence.cells) == sentence.count:
            while len(sentence.cells) > 0:
                mine = sentence.cells.pop()
                self.mines.add(mine)
                sentence.mark_mine(mine)
            self.knowledge.remove(sentence)
            return True
        elif sentence.count == 0:
            while len(sentence.cells) > 0:
                safe = sentence.cells.pop()
                self.safes.add(safe)
                sentence.mark_safe(safe)
            self.knowledge.remove(sentence)
            return True
        return False
    
    def add_sentence(self, sentence):
        self.mines = self.mines.union(sentence.known_mines())
        self.safes = self.safes.union(sentence.known_safes())
        self.knowledge.append(sentence)

    def update_knowledge(self):
        for sentence in self.knowledge:

            modified_sentence = False

            for mine in self.mines:
                if mine in sentence.cells:
                    self.mines.add(mine)
                    sentence.mark_mine(mine)
                    modified_sentence = True

            for safe in self.safes:
                if safe in sentence.cells:
                    self.safes.add(safe)
                    sentence.mark_safe(safe)
                    modified_sentence = True
            
            if self.check_sentence(sentence):
                return self.update_knowledge()

            for subsentence in self.knowledge:
                if subsentence == sentence:
                    continue
                if subsentence.cells.issubset(sentence.cells) and len(subsentence.cells) > 0:
                    sentence.cells = sentence.cells - subsentence.cells
                    sentence.count = sentence.count - subsentence.count
                    modified_sentence = True

            if self.check_sentence(sentence):
                modified_sentence = True

            if modified_sentence:
                return self.update_knowledge()

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.safes.add(cell)
        nearby_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell or (i, j) in self.safes:
                    continue
                if (i, j) in self.mines:
                    count -= 1
                    continue
                # Add to set of nearby cells if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    nearby_cells.add((i, j))
        
        # Create new sentence with the number of nearby cells which are mines
        new_sentence = Sentence(nearby_cells, count)

        # Add new sentence to knowledge
        self.add_sentence(new_sentence)

        # Update previous knowledge based on new knowledge
        self.update_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        counter = len(self.moves_made) + len(self.mines)
        while counter >= 0:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            cell = (i, j)
            if cell not in self.moves_made and cell not in self.mines:
                return cell
            counter -= 1
        return None
