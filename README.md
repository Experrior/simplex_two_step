## Python implementation of two step version of simplex algorithm

This version is the broad version of simplex algorithm, as it covers cases with 'less than', 'more than', 'equals' types of constrains. For all possible RHS values including 0 (little approximation behind the scenes).

I provided example inputs in files: `input_max.txt` `input_min.txt`, with results so that you can check and verify the results.

You should plug in the problem to input.txt in a following format:

MAX/MIN x<sub>1</sub> x<sub>2</sub> ...

y<sub>1</sub> y<sub>2</sub> ... </=/> z<sub>1</sub>
...

where 
$x \in R$, $y \in R$, $z \in N$
