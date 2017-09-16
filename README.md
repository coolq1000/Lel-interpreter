# Lel interpreter written in python
This is a LEL interpreter, inspired and based off: https://francisstokes.wordpress.com/2017/08/16/programming-language-from-scratch/

## Basics
If you don't know what LISP is, then I highly recommend that you check out this: https://en.wikipedia.org/wiki/Lisp_(programming_language)

Lel is a variation of Lisp, here are some basics:
### Set a variable,
```lisp
(let a 10) ; Set's `a` to 10.
```

#### Output,
```lisp
(print "Hello, World!") ; Outputs `>>>: Hello, World!`
```

#### Iteration,

Because I used straight functions for recursion, it is easy to hit the stack limit in Python.
Because of this, I added a `loop` function.
```lisp
(loop (<EXPR>) 
    <CODE>
)
```

#### Comments,
```lisp
; This is a comment. There are no multi-line comments yet.
```

#### Functions,
```lisp
(function cube(x)
    ; Take X and multiply it be itself,
    (let a (* x x))
    ; Return x * a
    (* x a)
)
; Set `threeCubed` to cube(3),
(let threeCubed (cube 3))
; Lastly print the result,
(print threeCubed)
>>> 27.0
```

#### Lists,
```lisp
(print (list 1 2 3))
>>> [1, 2, 3]
```

#### Indexing list,
Note that lists also wrap with negative values.
```lisp
(let lst (list 1 2 3))
(print (index 0 lst))
>>> 1.0
(print (index (- 0 1) lst))
>>> 3.0
```

## REPL,
To use the REPL, simply run the program without any filename
```~$ python main.py
LEL> (function test(x y)
...>    (+ x y)
...>
LEL> (test 10 10)
20.0 ; Outputs correct value.
LEL>
```
