from typing import Literal
import copy
import tqdm


class HashList():
    def __init__(self):
        """ list elements hashed and placed in dict[list[<type e>]]
        """
        self.d = {}
        self.len = 0
    
    def add(self, e):
        h = hash(e)
        if h not in self.d:
            self.d[h] = [e]
        else:
            self.d[h].append(e)
        self.len += 1

    def member(self, e):
        h = hash(e)
        if h in self.d and e in self.d[h]:
            return True
        else:
            return False
    def __len__(self):
        return self.len

class MoonSpinner():
    """ represents a puzzle state
    """
    def __init__(self, sails, pents, tris):
        # represents pieces on the outside of the rim starting from top large piece, clockwise around the circle
        # big middle pieces are called sails
        # pentagon pieces are called pentagons
        # triangles are called triangles
        # top center, top right, bottom right, bottom left, bottom left, top left, center
        self.sails = sails
        #top right, bottom right, bottom, bottom left, top left, center 'left', center 'right'
        self.pents = pents
        # top left, and around cockwise, middle left middle right
        self.tris = tris
        self.trail = []

    def __str__(self):
        return ''.join(self.sails) + ''.join(self.pents) + ''.join(self.tris)

    def eq_rotation(self, other):
        """ rotationally equal
        """
        found = False
        r = -1
        other_str = str(other)
        for rotation in range(5):
            self.rotate()
            if str(self) == other_str:
                found = True
                r = rotation
        return found, r

    def move(self, ind: Literal[0,1,2,3,4]):
        """ turn at the specified index

        1 = top
        2 = top right
        etc.
        """
        # set a trail to follow
        self.trail.append(ind)

        # sails is easy. swap the end with the spin index
        tmp = self.sails[ind]
        self.sails[ind] = self.sails[-1]
        self.sails[-1] = tmp

        # pents
        ind_m1 = (ind-1)%5
        tmp_m1 = self.pents[ind_m1]
        tmp = self.pents[ind]

        self.pents[ind_m1] = self.pents[-1]
        self.pents[ind] = self.pents[-2]

        self.pents[-1] = tmp_m1
        self.pents[-2] = tmp

        #tris
        #center right tri is ind*2
        i = ind*2
        i_m2 = (i-2)%10
        i_m1 = (i-1)%10
        i_p1 = (i+1)%10
        tmp_m2 = self.tris[i_m2]
        tmp_m1 = self.tris[i_m1]
        tmp = self.tris[i]

        self.tris[i_m2] = self.tris[i+1]        
        self.tris[i_m1] = self.tris[-1]
        self.tris[i] = self.tris[-2]
        self.tris[i_p1] = tmp_m2

        self.tris[-2] = tmp
        self.tris[-1] = tmp_m1

    def rotate(self):
        """ rotate the whole things counter clockwise by one
        """
        tmp = self.sails[0]
        for i in range(4):
            self.sails[i] = self.sails[i+1]
        self.sails[4] = tmp

        tmp = self.pents[0]
        for i in range(4):
            self.pents[i] = self.pents[i+1]
        self.pents[4] = tmp

        tmp = self.tris[0]
        tmp_p1 = self.tris[1]
        for i in range(8):
            self.tris[i] = self.tris[i+2]
        self.tris[8] = tmp
        self.tris[9] = tmp_p1

    def in_list(self, l):
        """ check if this spinner is represented in a list of strings
        """
        found = False
        for rotation in range(5):
            self.rotate()
            if l.member(str(self)):
                found = True
        return found


if __name__ == "__main__":

    # top center, top right, bottom right, bottom left, bottom left, top left, center  
    start_sails = ['g','r','r','p','o','b']
    #top right, bottom right, bottom, bottom left, top left, center 'left', center 'right'
    start_pents = ['g','o','g','r','b','b','o']
    # top left, and around cockwise, middle left middle right
    start_tris = ['g','g','o','o','r','g','g','o','b','r','o','b']

    # start_sails = ['g','b','p','o','r','r']
    # start_pents = ['g','b','o','o','g','b','r']
    # start_tris = ['g','r','b','g','o','o','o','o','b','g','g','r']
    
    start_spinner = MoonSpinner(start_sails, start_pents, start_tris)


    end_sails = ['r','b','p','o','r','g']
    end_pents = ['b','b','o','o','r','g','g']
    end_tris =  ['g','b','b','g','o','o','o','o','r','r','g','g']
    
    end_spinner = MoonSpinner(end_sails, end_pents, end_tris)

    start_spinner = copy.deepcopy(end_spinner)
    start_spinner.move(2)
    start_spinner.move(1)
    start_spinner.move(0)
    start_spinner.move(4)
    start_spinner.move(3)
    start_spinner.move(0)
    start_spinner.move(2)
    start_spinner.move(4)
    start_spinner.move(1)
    start_spinner.move(3)
    start_spinner.move(0)
    start_spinner.move(2)
    start_spinner.move(4)
    start_spinner.move(1)
    start_spinner.move(2)
    start_spinner.move(3)
    start_spinner.move(0)
    start_spinner.move(2)
    start_spinner.move(4)
    start_spinner.move(1)
    start_spinner.move(2)
    start_spinner.trail = []

    # end_spinner.move(0)

    #print(str(end_spinner))
    # exit()

    start_spinners = []
    end_spinners = []

    start_spinners.append(start_spinner)
    end_spinners.append(end_spinner)

    start_explored = HashList()
    start_explored.add(str(start_spinner))
    end_explored = HashList()
    end_explored.add(str(end_spinner))

    depth = 0

    """ Doing an BFS of the state graph from the starting state and ending state

    Ensure that nodes are not visited twice. Consider all rotations of a state to be equal.
    The first state that appears in both the starting exploration and the ending exploration is the most efficient solution. 
    """
    while True:
        new_spinners = []
        pb = tqdm.tqdm(total = len(start_spinners) + len(end_spinners), leave=False)
        for spinner in start_spinners:
            pb.update(1)
            for i in range(5):
                spinner_new = copy.deepcopy(spinner)
                spinner_new.move(i)
                # breakpoint()
                if not spinner_new.in_list(start_explored):
                    new_spinners.append(spinner_new)
                    start_explored.add(str(spinner_new))
                if spinner_new.in_list(end_explored):
                    print("Found a path to the end!")
                    for sp in end_spinners:
                        eq, r = sp.eq_rotation(spinner_new)
                        if eq:
                            print(f"{len(spinner_new.trail + sp.trail[::-1])} moves: " + str(spinner_new.trail + [f'r{r}'] + sp.trail[::-1]))
                    print(f"Explored {len(start_explored) + len(end_explored)} states!")
                    file1 = open("solved_spinners.txt", "a")
                    file1.write(str(spinner_new.trail + [f'r{r}'] + sp.trail[::-1]))
                    file1.write("\n")
                    exit()
        start_spinners = new_spinners
        new_spinners = []
        for spinner in end_spinners:
            pb.update(1)
            for i in range(5):
                spinner_new = copy.deepcopy(spinner)
                spinner_new.move(i)
                if not spinner_new.in_list(end_explored):
                    new_spinners.append(spinner_new)
                    end_explored.add(str(spinner_new))
                if spinner_new.in_list(start_explored):
                    print("Found a path to the end!")
                    for sp in start_spinners:
                        eq, r = sp.eq_rotation(spinner_new)
                        if eq:
                            print(f"{len(sp.trail + spinner_new.trail[::-1])} moves: " + str(sp.trail + [f'r{r}'] +  spinner_new.trail[::-1]))
                    print(f"Explored {len(start_explored) + len(end_explored)} states!")
                    file1 = open("solved_spinners.txt", "a")
                    file1.write(str(spinner_new.trail + [f'r{r}'] + sp.trail[::-1]))
                    file1.write("\n")
                    exit()
        end_spinners = new_spinners
        pb.close()
        depth += 1
        print(f"Explored to depth: {str(depth)}\n\tnumber of states: {len(start_explored) + len(end_explored)}\n\tnumber of spinners: {len(start_spinners) + len(end_spinners)}")
        


