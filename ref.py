#!/usr/bin/env python3

class foo:
    val: int

    def __init__(self: 'foo', val: int):
        self.val = val

    def setVal(self: 'foo', val: int) -> None:
        self.val = val

    def __str__(self: 'foo') -> str:
        return "(foo.v: " + str(self.val) + ")"

    def __repr__(self: 'foo') -> str:
        return str(self)

if __name__ == "__main__":
    lst = []
    lst.append(foo(2))
    lst.append(foo(3))
    lst.append(foo(4))

    print(lst)
    print()

    at_1 = lst[1]

    at_1.setVal(7)

    print(lst)
    print(at_1)
    print()


    lst[1].setVal(42)

    print(lst)
    print(at_1)
