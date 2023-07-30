# import pytest
from solver import *

def get_solved_spinner():
    end_sails = ['r','b','p','o','r','g']
    end_pents = ['b','b','o','o','r','g','g']
    end_tris =  ['g','b','b','g','o','o','o','o','r','r','g','g']

    return MoonSpinner(end_sails, end_pents, end_tris)


def test_rotation_repitition():
    """ test that 5 rotations gives the same item
    """
    spinner = get_solved_spinner()
    start_state = str(spinner)
    for rotation in range(5):
        spinner.rotate()
    end_state = str(spinner)
    assert start_state == end_state, f"{start_state} != {end_state}"
    

if __name__ == "__main__":

    test_rotation_repitition()
