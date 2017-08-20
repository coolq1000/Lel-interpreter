# Lel-interpreter
A Pure-Python implementation of Lel

## Features
So far it only generates a AST.

## Starting code
So for our tests we'll use
```Lisp
(function cube (x)
  (* x x x)
)
 
(let threeCubed (cube 3))
 
(print threeCubed)
```

## Lexing
Now we need to split this code into a bunch of tokens so it's easier to parse.
```python
[<Token, LPAREN, (>, <Token, KEYWORD, function>, <Token, KEYWORD, cube>, <Token, LPAREN, (>, <Token, KEYWORD, x>, <Token, RPAREN, )>, <Token, LPAREN, (>, <Token, KEYWORD, *>, <Token, KEYWORD, x>, <Token, KEYWORD, x>, <Token, KEYWORD, x>, <Token, RPAREN, )>, <Token, RPAREN, )>, <Token, LPAREN, (>, <Token, KEYWORD, let>, <Token, KEYWORD, threeCubed>, <Token, LPAREN, (>, <Token, KEYWORD, cube>, <Token, NUMBER, 3>, <Token, RPAREN, )>, <Token, RPAREN, )>, <Token, LPAREN, (>, <Token, KEYWORD, print>, <Token, KEYWORD, threeCubed>, <Token, RPAREN, )>]
```

## AST
Then we need to generate the AST.

```python
[
  [
    <Token, KEYWORD, function>,
    <Token, KEYWORD, cube>,
    [
      <Token, KEYWORD, x>
    ],
    [
      <Token, KEYWORD, *>,
      <Token, KEYWORD, x>,
      <Token, KEYWORD, x>,
      <Token, KEYWORD, x>
    ]
  ],
  [
    <Token, KEYWORD, let>,
    <Token, KEYWORD, threeCubed>,
    [
      <Token, KEYWORD, cube>,
      <Token, NUMBER, 3>
    ]
  ],
  [
    <Token, KEYWORD, print>,
    <Token, KEYWORD, threeCubed>
  ]
]
```

## Evaluator
This is the next step for my language.

### Resources
Heavily inspired from: https://francisstokes.wordpress.com/2017/08/16/programming-language-from-scratch/comment-page-1/#comment-44
