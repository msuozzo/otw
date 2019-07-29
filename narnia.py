"""Implementations of solutions for Narnia OTW levels."""
import functools
import textwrap

import solver_util

_get_password_from_shell = functools.partial(solver_util.get_password_from_shell,
        password_file_cbk=lambda lvl: '/etc/narnia_pass/narnia%d' % lvl)


class Solver(solver_util.AbstractSolver):
  """Solver for the Narnia OTW levels."""

  @classmethod
  def username(cls, level):
    return 'narnia{}'.format(level)

  @property
  def host(cls):
    return 'narnia.labs.overthewire.org'

  @property
  def port(self):
    return 2226
