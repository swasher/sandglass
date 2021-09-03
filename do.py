import sys
from pyinfra.api import deploy
from pyinfra.operations import deploy, server


@deploy('Test1')
def test1(state=None, host=None):
    server.shell(
        name='Test1',
        commands=[
            "echo Test",
        ]
    )


def arg_check():
    if len(sys.argv) != 1:
        print('Warning: No operation given.')
        print('Usage: do.py [ up | down | list | create ]')
        sys.exit(1)


if __name__ == '__main__':
    arg_check()
    op = sys.argv[1]
    if op == 'test1':
        test1(host='prod')
    elif op == 'test2':
        test1(host='docker')
    else:
        print('invalid args')