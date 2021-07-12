# The `D`ice `I`ntegrated `P`rogramming `La`nguage - `DIPLA`
A programming language that provides an integrated way to generate an array of random numbers (dice). The language is built around the evaluation and arithmetic of dice. For example, the language evaluates "2d20" and generates an array of size two with random numbers between 1-20 (inclusively).    

### RUN
usage: shell.py [-h] [-i] [-s] [FILE [FILE ...]]

Run an interactive prompt
>python shell.py -i

Run a file
>python shell.py ./Example.dicelang

Run a file and then enter the interactive prompt
>python shell.py ./Example.dicelang -i
