from typing import Literal
import copy


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


if __name__ == "__main__":

    # top center, top right, bottom right, bottom left, bottom left, top left, center  
    start_sails = ['g','b','o','r','p','r']
    #top right, bottom right, bottom, bottom left, top left, center 'left', center 'right'
    start_pents = ['o','b','r','o','g','g','b']
    # top left, and around cockwise, middle left middle right
    start_tris = ['g','o','g','g','o','b','o','b','r','g','o','r']

    # start_sails = ['g','b','p','o','r','r']
    # start_pents = ['g','b','o','o','g','b','r']
    # start_tris = ['g','r','b','g','o','o','o','o','b','g','g','r']
    
    start_spinner = MoonSpinner(start_sails, start_pents, start_tris)


    end_sails = ['r','b','p','o','r','g']
    end_pents = ['b','b','o','o','r','g','g']
    end_tris =  ['g','b','b','g','o','o','o','o','r','r','g','g']
    
    end_spinner = MoonSpinner(end_sails, end_pents, end_tris)

    start_spinner = copy.deepcopy(end_spinner)
    start_spinner.move(3)
    start_spinner.move(0)
    start_spinner.move(2)
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

    # print(str(end_spinner))
    # exit()

    start_spinners = []
    end_spinners = []

    start_explored = [str(start_spinner)]
    end_explored = [str(end_spinner)]

    start_spinners.append(start_spinner)
    end_spinners.append(end_spinner)

    found = False
    depth = 0

    while not found:
        new_spinners = []
        for spinner in start_spinners:
            for i in range(5):
                spinner_new = copy.deepcopy(spinner)
                spinner_new.move(i)
                # breakpoint()
                if str(spinner_new) not in start_explored:
                    new_spinners.append(spinner_new)
                    start_explored.append(str(spinner_new))
                if str(spinner_new) in end_explored:
                    print("Found a path to the end!")
                    for sp in end_spinners:
                        if str(sp) == str(spinner_new):
                            print(f"{len(spinner_new.trail + sp.trail[::-1])} moves: " + str(spinner_new.trail + sp.trail[::-1]))
                    print(f"Explored {len(start_explored) + len(end_explored)} states!")
                    exit()
        start_spinners = new_spinners
        new_spinners = []
        for spinner in end_spinners:
            for i in range(5):
                spinner_new = copy.deepcopy(spinner)
                spinner_new.move(i)
                if str(spinner_new) not in end_explored:
                    new_spinners.append(spinner_new)
                    end_explored.append(str(spinner_new))
                if str(spinner_new) in start_explored:
                    print("Found a path to the end!")
                    for sp in start_spinners:
                        if str(sp) == str(spinner_new):
                            print(f"{len(sp.trail + spinner_new.trail[::-1])} moves: " + str(sp.trail + spinner_new.trail[::-1]))
                    print(f"Explored {len(start_explored) + len(end_explored)} states!")
                    exit()
        end_spinners = new_spinners
        depth += 1
        print(f"Explored to depth: {str(depth)}\n\tnumber of states: {len(start_explored) + len(end_explored)}\n\tnumber of spinners: {len(start_spinners) + len(end_spinners)}")
        # breakpoint()


