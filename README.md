# The `D`ice `I`ntegrated `P`rogramming `La`nguage - `DIPLA`
A programming language that provides an integrated way to generate an array of random numbers (dice). The language is built around the evaluation and arithmetic of dice. For example, the language evaluates "2d20" and generates an array of size two with random numbers between 1-20 (inclusively).    

The language conforms to these [Grammer Rules](grammar.md)

## Requirements:
- MongoDB database

## Steps:

1. Setup "config.js" according to your environment
2. Run an interactive prompt 
    > node shell.py

## Examples

```
let attack = 2d20;
let att_wth_advt = 2{2d20} 
```