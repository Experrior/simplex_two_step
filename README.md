## Python implementation of two step version of simplex algorithm

This version is an 'expanded' version of the two step simplex algorithm, as it can handle cases with all 'less than', 'more than', 'equals' types of constrains present at the same time. For all possible RHS values including 0 (little approximation behind the scenes).

I provided example inputs in files: `input_max.txt` `input_min.txt`, with the results so that you can check and verify them yourself.

You should plug in the problem to `input.txt` in a following format:

MAX/MIN x<sub>1</sub> x<sub>2</sub> x<sub>3</sub> ...

y<sub>1</sub> y<sub>2</sub> y<sub>3</sub> ... </=/> z<sub>1</sub> 

y<sub>4</sub> y<sub>5</sub> y<sub>6</sub> ... </=/> z<sub>1</sub>
<br/><br/> ...

where 
$x \in R$, $y \in R$, $z \in N$
