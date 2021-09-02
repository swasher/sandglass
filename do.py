import sys

def arg_check():
    if len(sys.argv) < 2:
        print('Warning: No operation given.')
        print('Usage: do.py [ up | down | list | create ]')
        sys.exit(1)



if __name__ == '__main__':
    arg_check()
    op = sys.argv[1]
    if op == 'list':
        list()
    elif op == 'up':
        up()
    elif op == 'down':
        down()
    elif op == 'create':
        create_inventory()
    else:
        print('invalid args')