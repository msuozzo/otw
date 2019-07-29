"""A tool to automate collecting passwords for OTW levels."""
import argparse
import itertools

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description='Automatically collect passwords for OTW levels.')
  parser.add_argument('wargame', type=str, choices=['leviathan', 'narnia'])
  parser.add_argument('max_level', type=int, help='The max level to solve')
  parser.add_argument('--min_level',
                      type=int,
                      default=0,
                      help='The min level to retrieve')
  parser.add_argument('--start_password',
                      type=str,
                      help='The password of the min level')

  args = parser.parse_args()

  wargame = __import__(args.wargame)
  solver = wargame.Solver()
  if (args.min_level == 0) ^ (args.start_password is None):
    raise Exception('--min_level must be accompanied with a --start_password')
  solutions = itertools.chain(
      (args.start_password or solver.default_password,),
      solver.solve_range(args.min_level,
                         args.max_level,
                         min_lvl_password=args.start_password))
  for lvl, password in enumerate(solutions, args.min_level):
    print('Level %d: %s' % (lvl, password))
