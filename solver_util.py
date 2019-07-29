"""Utilities to automate collecting the passwords for OTW levels."""

import abc

import pexpect


class AbstractSolver:

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
        if entry_password is None:
            entry_password = self.default_password
        proc = pexpect.spawn(
                'ssh -o StrictHostKeyChecking=no '
                '-p{port} {user}@{host}'.format(
                    port=self.port,
                    user=self.username(level),
                    host=self.host,
                )
            )

        proc.expect('password: ')
        proc.sendline(entry_password)
        proc.expect(r'\$ ')

        # Run solution routine to pop the set uid shell
        password = self.get_solution_func(level)(proc)

        # Tear down
        proc.sendeof()
        proc.terminate()

        return password.decode('utf8')

    def solve_until(self, max_lvl):
        """Solve all levels up to and including `max_lvl`."""
        if max_lvl <= 0:
            raise ValueError('Invalid level number: %d' % max_lvl)
        password = None
        for lvl in range(max_lvl + 1):
            password = self.solve(lvl, password)
            yield password
