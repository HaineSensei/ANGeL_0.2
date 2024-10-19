## parser.py

"""
This aims to be a parser for a language with similar syntax to that written in Fun_Language_Example.txt
For personal simplicity, I intend to adjust the language slightly so that every variable/function definition
has the let keyword before it. This allows for simple block parsing — blocks can easily be identified by
simply splitting the code into blocks separated by keywords, and then parsing the blocks separately with
parsing rules depending on the keyword prefixing the block. Early on, the only two keywords of this form
will be "let" and "type". This will probably be extended once something like a trait system is built and
potentially something similar for modules (though I don't mind simply requiring modules to be written in
separate module files, if I do this, the language would still need some form of statement to import the
appropriate modules.)
"""
from collections.abc import Generator

class UnreachableError(Exception):
    def __init__(self, message : str):
        self.message = message
        super().__init__(self.message)

# non-documentation comments will be handled separately
# documentation comments handled by this tree together with specific implementation added later.
tree_of_breakers = {"main" : ["type", "let"], 
                        "type" : [":="],
                        "let" : ["::=", ":=", ":"]}

text = """
let x : Int ::= 3
let y:Rat ::=(4/3)
let z: Rat:=y/x
let x : Indeterminate ::= 'x'
let p: Poly Int x ::= 3x + 3
let f (x: Int) : Int := 3 + x
"""

alpha_under = "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm_"
numeric = "0123456789"
alpha_under_numeric = alpha_under + numeric
bracket = "()[]{}"


def word_generator(text : str) -> Generator[tuple[str,str],str,None]:
    curr = ""
    curr_state_key = {
        0 : "empty",
        1 : "word",
        2 : "number",
        3 : "symbol string",
        4 : "bracket"
        }
    curr_state = 0

    def initialise(letter):
        nonlocal curr_state, curr
        if letter == " " or letter == '\n':
            curr_state = 0
            curr = ""
            return
        curr = letter
        if letter in alpha_under:
            curr_state = 1
        elif letter in numeric:
            curr_state = 2
        elif letter in bracket:
            curr_state = 4
        else:
            curr_state = 3

    for letter in text:
        match curr_state:
            case 0:
                initialise(letter)
                continue
            case 1:
                if letter in alpha_under_numeric:
                    curr += letter
                    continue
                yield (curr_state_key[curr_state],curr)
                initialise(letter)
            case 2:
                if letter in numeric:
                    curr += letter
                    continue
                yield (curr_state_key[curr_state],curr)
                initialise(letter)
            case 3:
                if letter in " \n" or letter in alpha_under_numeric or letter in bracket:
                    yield (curr_state_key[curr_state],curr)
                    initialise(letter)
                    continue
                curr += letter
            case 4:
                yield (curr_state_key[curr_state],curr)
                initialise(letter)

type leaf = tuple[()]

type tree = leaf | list[tuple[str, tree]]

tree_construction : tree = []

"""
()
let (0)(0,0) ... : (0,1) ... ::= (0,2) ...
let (1)(1,0) ... : (1,1) ... ::= (1,2) ...
let (2)(2,0) ... : (2,1) ... ::= (2,2) ...

()
|-let (0)
|  |-    (0,0) ...
|  |-:   (0,1) ...
|  |-::= (0,2) ...
|
|-let (1)
|  |-    (1,0) ...
|  |-:   (1,1) ...
|  |-::= (1,2) ...
|
|-let (2)
|  |-    (2,0) ...
|  |-:   (2,1) ...
|  |-:=  (2,2) ...
"""

super_scope = "none"
curr_scope = "main"
curr_index = []

def call_tree_at_index(t:tree,index:list[int]) -> tree:
    return call_tree_at_index(t[index[0]],index[1:])

for x in word_generator(text):
    print(x)

# TODO: make the curr_index follow the tree in the above comment.
for sort,word in word_generator(text):
    in_tree : tree = call_tree_at_index(tree_construction,curr_index)
    if word in tree_of_breakers[curr_scope]:
        curr_index += [call_tree_at_index(tree_construction,curr_index).len()]
        in_tree.append((word,[]))
    else:
        if super_scope != "none":
            if word in tree_of_breakers[super_scope]:
                curr_index[-1] += 1
        else:
            in_tree.append((word,()))


