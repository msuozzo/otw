"""A tool to automate collecting passwords for OTW levels."""
import argparse
import itertools

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Automatically collect passwords for OTW levels.')
    parser.add_argument('wargame', type=str, choices=['leviathan'])
    parser.add_argument('max_level', type=int, help='The max level to retrieve')

    args = parser.parse_args()

    wargame = __import__(args.wargame)
    solver = wargame.Solver()
    solutions = itertools.chain((solver.default_password,),
                                solver.solve_until(args.max_level))
    for lvl, password in enumerate(solutions):
        print('Level %d: %s' % (lvl, password))
