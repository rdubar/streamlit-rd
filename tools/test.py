from tools.plex import connect_to_plex
import pprint
import warnings

warnings.filterwarnings("ignore")
pp = pprint.PrettyPrinter(indent=4)
plex = connect_to_plex()

"""
Attempt to show all attributes in an object recirsively.
"""

obj = plex.search('alien')[0]

def process(x, indent=0):
    print(' '*indent, end='')
    if type(x)==list:
        print(x)
        for y in x:
            process(y)
    elif hasattr(x, '__dict__'):
        print('  ', end='')
        for v in vars(x):
            if v[0] == '_' or v == 'chapters':
                continue
            a = getattr(x, v)
            t = type(a)
            print(v, t, a)
            if t == list:
                process(a, indent=indent+1)
    else:
        print(x, type(x))

process(obj)
