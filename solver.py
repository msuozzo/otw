"""Tools to automate collecting the passwords for OTW levels."""
import solutions

import pexpect


HOSTNAME = 'leviathan.labs.overthewire.org'
PORT = 2223
USERNAME_FUNC = lambda lvl: 'leviathan{}'.format(lvl)


def solve(level_to_solve, entry_password):
    """Solve an IO level given the password for access."""
    if level_to_solve == 0:
        return solutions.leviathan_minus_1(None)

    username = USERNAME_FUNC(level_to_solve - 1)

    try:
        solution_func = getattr(solutions, username)
    except AttributeError:
        return 'UNKNOWN'

    # Setup session with IO server
    proc = pexpect.spawn(
            'ssh -o StrictHostKeyChecking=no '
            '-p{port} {uname}@{hostname}'.format(
                port=PORT,
                uname=username,
                hostname=HOSTNAME,
            )
        )

    proc.expect('password: ')
    proc.sendline(entry_password)
    proc.expect(r'\$ ')

    # Run solution routine to pop the set uid shell
    password = solution_func(proc)

    # Tear down
    proc.sendeof()
    proc.terminate()

    return password


def solve_until(max_lvl=1):
    """Solve all levels up to and including `max_lvl`."""
    if max_lvl <= 0:
        raise ValueError('Invalid level number: %d' % max_lvl)
    password = 'leviathan0'
    for lvl in range(max_lvl + 1):
        password = solve(lvl, password)
        print('Level %d: %s' % (lvl, password))


if __name__ == '__main__':
    import sys

    solve_until(int(sys.argv[1]))
