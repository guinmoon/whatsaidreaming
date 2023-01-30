

def fix_abc(in_abc):
    abc=in_abc.replace('L1','L:1')
    abc = abc.replace(':1/4','L:1/4')
    abc = abc.replace('LL:','L:')
    abc = abc.replace('41K:','4\nK:')
    abc = abc.replace('#K:','\nK:')
    abc = abc.replace('minK','\nK:')
    abc = abc.replace('Dmin','D')
    abc = abc.replace('4/42','4/4')
    abc = abc.replace('::',':')
    return abc


if __name__ == '__main__':
    import os,sys
    __dir=os.path.dirname(os.path.realpath(__file__)) 
    abc=''
    with open(sys.argv[1],'r') as f:
        abc = f.read()
    fixed_abc = fix_abc(abc)
    print(fixed_abc)
