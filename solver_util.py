"""Utilities to automate collecting the passwords for OTW levels."""

import abc

import pexpect


class AbstractSolver(abc.ABC):
  """An abstract class for solving OTW puzzles.

  This provides the framework for level solutions for wargames. Each level
  function should accept a `pexpect.spawn` instance argument and return the
  "flag" for that level (i.e. password string for the next level). By default,
  the solver looks for level solutions with names of the format
  "level{level_num}" e.g. "level0", "level1", etc.
  """

  @classmethod
  @abc.abstractmethod
  def username(cls, level):
    pass

  @property
  @abc.abstractmethod
  def host(cls):
    pass

  @property
  def port(self):
    return 22

  def get_solution_func(self, level):
    try:
      return getattr(self, 'level{}'.format(level))
    except AttributeError:
      raise ValueError('No solution found for level {}'.format(level))

  @property
  def default_password(self):
    return self.username(0)

  def solve(self, level, entry_password=None):
    """Solve the provided level number.

    Args:
      level: Int, the number of the level to solve.
      entry_password: Optional[Str], if provided, the password to use to log
        into the level. Otherwise, `self.default_password` will be used.

    Returns: Str, The password to the next level.
    """
    if entry_password is None:
      entry_password = self.default_password
    proc = pexpect.spawn('ssh -o StrictHostKeyChecking=no '
                         '-p{port} {user}@{host}'.format(
                             port=self.port,
                             user=self.username(level),
                             host=self.host,
                         ))

    proc.expect('password: ')
    proc.sendline(entry_password)
    proc.expect(r'\$ ')

    # Run solution routine to pop the set uid shell
    password = self.get_solution_func(level)(proc)

    # Tear down
    proc.sendeof()
    proc.terminate()

    return password.decode('utf8')

  def solve_range(self, min_lvl, max_lvl, min_lvl_password=None):
    """Solve all levels from `min_lvl` up to and including `max_lvl`."""
    if max_lvl <= 0:
      raise ValueError('Invalid level number: %d' % max_lvl)
    if min_lvl < 0:
      raise ValueError('Invalid level number: %d' % min_lvl)
    password = min_lvl_password
    for lvl in range(min_lvl, max_lvl + 1):
      password = self.solve(lvl, password)
      yield password
