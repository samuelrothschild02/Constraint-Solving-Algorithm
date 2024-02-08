#### CS76 Assignment 5: Sudoku
##### Sam Rothschild 23/10/23
### Implementation Discussion:
This assignment saw us implement solvers for propositional logic satisfiability problems. All modifications to the base code were made in the files: `SAT.py` and `solve_sudoku.py`. In order to test the code, please either use the lines: `result = sat.walkSAT(THRESHOLD, MAX_ITS)` to test walkSAT or `result = sat.GSAT(THRESHOLD, MAX_ITS)` to test GSAT. I attach print outs of the sudoku boards outputted further down in the report and the `.sol` files are created as advised in the spec in the zip file. (I have set a relatively arbitrary threshold and number of max_iterations because I found they worked well for me, feel free to change them if you'd like to play around with them though I'd encourage testers to just use those.)

In order to run the code please use: `python3 <path>/solve_sudoku.py <path>/test_case.cnf`

##### `SAT.py`
This file contains the class `sat` which we use to solve the problems. The class is generic as required by the homework spec. Every sat object is initialised with a filename, containing the data to be read in necessary for the problem and a solution, which will be updated in the main body of the code. The solution is naturally automatically instantiated to None when a new sat is created.

Following the pseudocode given in the homework spec and attached wikipage, I implemented the `GSAT` and `walkSAT` methods.

###### `parse_cnf(self)`
This function parses the `.cnf` files we were given. This function takes in a file and goes through it line by line checking to see if a line is negated with the '-' operator. If it is, it assigns a 0 to the relevant clause in our list of dictionaries so we can easily tell later, otherwise it just assigns a 1. We return the variables themselves as a list and the clauses as a list of dictionaries where the key:value pairs are the rules and whether or not they are negated.

###### `satisfied_clause(self, assignment, clause)`
This function takes an assignment and a clause as input and iterates through the variables in the clause and checks if they are satisfied. It returns True if any variable in the clause is satisfied, otherwise False.

###### `is_valid(self, assignment, clauses)`
This function iterates through all clauses and ensures they are all satisfied using the previous function. If any of them are not it returns False and the process is terminated. Otherwise if all are satisfied then it returns True.

##### `choose_next(self, assignment, clauses, variables)`
This function takes an assignment, a list of clauses, and a list of variables as input. It evaluates the impact of flipping each variable and chooses the one that maximizes the number of satisfied clauses. If multiple variables result in the same number of satisfied clauses, it selects one randomly from a list of those which give equally good results.

##### `GSAT(self, threshold, max_its)`
This function is the GSAT algo and follows the pseudocode. It parses the .cnf and then carries out the meat of the process while we are under the set maximum number of iterations. First, we generate a random assignment and flip variables in order to improve it, leveraging the previous function. If it finds a solution it reports it immediately, otherwise if we reach the maximum number of iterations before a solution is found it will report that accordingly. 

##### `find_unsatisfied_clauses(self, assignment, clauses)`
This function takes an assignment and a list of clauses as an input. It iterates through all clauses, and if any of them are not satisfied it appends them to a list which is returned. We can then take a selection from this list later to get an unsatisfied clause.

##### `walkSAT(self, threshold, max_its)`
This function is the walkSAT algo and also follows from the pseudocode info given on the spec and the wiki. It parses the .cnf file and adheres to the max number of iterations set. Here though, we leverage the previous helper function we wrote `find_unsatisfied_clauses`. We get our unsatisfied clauses as a list, and if it has length 0 (ie everything is satisfied) then we return our solution. Otherwise we pick one out from the unsatisfied list at random and grab a random number to see if it exceeds our threshold, if it does then we choose a variable at random and flip. Otherwise we use the `choose_next` function already discussed and flip that variable. If a solution cannot be found within the maximum number of iterations then that information is reported.

##### `write_solution(self, fname)`
This function outputs the solution in cnf format to a file. This just follows from the recommendation in the homework spec.

### Results:
As you can see, there is full functionality as per the spec and using walkSAT instead of GSAT significantly improves performance.
*NB as the spec suggests, GSAT is only really feasible for the first few problems, so I only attach GSAT solutions up to and including `rows.cnf`, in addition please not all .sol files are in the zip so can be examined in .cnf format if you prefer to look at that than the outputted board*
`one_cell.cnf`: rules that ensure that the upper left cell has exactly one value between 1 and 9.  
*GSAT solution:*
Solution found after 4 flips  
1 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
++++++++++++++  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
++++++++++++++  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
*walkSAT solution:*  
Solution found after 4 flips  
8 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
++++++++++++++  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
++++++++++++++  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
0 0 0 | 0 0 0 | 0 0 0  
`all_cells.cnf`: rules that ensure that all cells have exactly one value between 1 and 9.  
*GSAT solution:*  
Solution found after 401 flips  
3 6 7 | 9 1 5 | 5 1 3  
1 2 2 | 2 3 7 | 9 1 2  
2 6 8 | 6 3 6 | 2 9 1  
++++++++++++++  
8 3 3 | 2 3 1 | 1 7 6  
2 6 3 | 2 2 1 | 8 3 7  
4 7 4 | 6 4 7 | 4 1 8  
++++++++++++++  
3 5 3 | 2 8 2 | 4 9 9  
6 9 7 | 1 9 4 | 2 5 2  
8 2 4 | 6 8 2 | 6 8 1  
*walkSAT solution:*  
Solution found after 281 flips  
7 3 1 | 9 1 3 | 7 7 4  
2 3 4 | 2 1 4 | 6 6 8  
7 5 5 | 8 6 9 | 9 7 1  
++++++++++++++  
1 2 5 | 4 7 9 | 1 5 2  
6 3 1 | 4 8 5 | 2 4 9  
1 4 5 | 6 4 9 | 6 6 6  
++++++++++++++  
4 2 1 | 9 7 5 | 9 9 8  
1 8 5 | 2 1 2 | 8 5 5  
6 5 1 | 1 7 1 | 5 7 5  
`rows.cnf`: rules that ensure that all cells have a value, and every row has nine unique values.  
*GSAT solution:*  
Solution found after 551 flips  
6 4 9 | 1 8 5 | 2 3 7  
2 1 4 | 5 3 8 | 6 9 7  
5 6 8 | 9 4 1 | 3 2 7  
++++++++++++++  
2 1 9 | 4 8 5 | 6 3 7  
9 6 5 | 1 8 2 | 7 3 4  
1 5 2 | 8 9 7 | 6 3 4  
++++++++++++++  
3 8 1 | 9 6 7 | 4 5 2  
7 5 3 | 6 9 4 | 2 1 8  
3 1 7 | 9 5 2 | 6 4 8  
*walkSAT solution:*  
Solution found after 355 flips  
6 5 9 | 7 8 3 | 1 2 4  
1 2 8 | 6 7 4 | 5 9 3  
3 2 1 | 4 7 6 | 9 5 8  
++++++++++++++  
6 1 9 | 8 2 3 | 7 5 4  
8 4 7 | 1 3 9 | 5 2 6  
2 6 8 | 1 4 9 | 3 5 7  
++++++++++++++  
3 1 5 | 8 7 9 | 6 4 2  
8 2 7 | 3 5 9 | 6 4 1  
1 9 3 | 8 5 4 | 6 2 7  
`rows_and_cols.cnf`: rules that ensure that all cells have a value, every row has nine unique values, and every column has nine unique values.  
*walkSAT solution:*  
Solution found after 1941 flips  
2 8 7 | 4 5 1 | 6 9 3  
4 7 2 | 9 8 3 | 5 6 1  
7 5 9 | 3 4 6 | 1 2 8  
++++++++++++++  
8 1 6 | 2 3 5 | 7 4 9  
9 4 3 | 6 1 2 | 8 5 7  
3 9 8 | 5 6 7 | 2 1 4  
++++++++++++++  
1 6 5 | 8 7 9 | 4 3 2  
5 3 4 | 1 2 8 | 9 7 6  
6 2 1 | 7 9 4 | 3 8 5  
`rules.cnf`: adds block constraints, so each block has nine unique values. (The complete rules for an empty sudoku board.)  
*walkSAT solution:*  
Solution found after 8895 flips  
2 8 7 | 6 1 5 | 3 9 4  
4 6 1 | 9 3 7 | 2 5 8  
3 5 9 | 8 2 4 | 7 1 6  
++++++++++++++  
9 4 3 | 1 7 8 | 6 2 5  
1 2 6 | 3 5 9 | 8 4 7  
8 7 5 | 2 4 6 | 9 3 1  
++++++++++++++  
5 3 4 | 7 6 2 | 1 8 9  
7 9 2 | 5 8 1 | 4 6 3  
6 1 8 | 4 9 3 | 5 7 2  
`puzzle1.cnf`: Adds a few starting values to the game to make a puzzle.  
*walkSAT solution:*  
Solution found after 4967 flips  
5 8 9 | 6 7 4 | 1 3 2  
2 6 1 | 3 9 8 | 4 5 7   
3 4 7 | 1 2 5 | 8 6 9  
++++++++++++++  
8 9 3 | 2 6 7 | 5 1 4  
1 5 6 | 8 4 9 | 7 2 3  
7 2 4 | 5 3 1 | 6 9 8  
++++++++++++++  
4 1 8 | 9 5 3 | 2 7 6  
9 7 2 | 4 1 6 | 3 8 5  
6 3 5 | 7 8 2 | 9 4 1   
`puzzle2.cnf`: Some different starting values.   
*walkSAT solution:*  
Solution found after 221441 flips  
1 3 4 | 6 5 2 | 7 9 8  
5 7 2 | 1 9 8 | 6 3 4  
6 9 8 | 4 3 7 | 5 2 1  
++++++++++++++  
8 4 9 | 7 6 1 | 2 5 3  
3 2 6 | 8 4 5 | 1 7 9  
7 5 1 | 9 2 3 | 4 8 6  
++++++++++++++  
4 8 3 | 5 7 6 | 9 1 2  
2 6 7 | 3 1 9 | 8 4 5  
9 1 5 | 2 8 4 | 3 6 7   
`puzzle_bonus.cnf`: Several starting values. Difficult; solution welcome but not required.
*walkSAT solution:*  
Solution found after 342855 flips  
5 3 4 | 6 7 8 | 9 1 2  
6 7 2 | 1 9 5 | 3 4 8  
1 9 8 | 3 4 2 | 5 6 7  
++++++++++++++  
8 5 9 | 7 6 1 | 4 2 3  
4 2 6 | 8 5 3 | 7 9 1  
7 1 3 | 9 2 4 | 8 5 6  
++++++++++++++  
9 6 1 | 5 3 7 | 2 8 4  
2 8 7 | 4 1 9 | 6 3 5  
3 4 5 | 2 8 6 | 1 7 9  

### Extra Credit:

##### Additional Resolution Coding: 
For extra credit I attempted to implement resolution. This was quite tricky done following information from wikipedia. I used the existing SAT class to implement it and you can see the code at the bottom of that file.

This report discusses a Python implementation of a resolution-based SAT solver. The SAT solver utilizes the resolution method to derive new clauses from a given set of clauses in Conjunctive Normal Form (CNF). The primary objective of this code is to find a satisfying assignment for a given CNF formula or determine that the formula is unsatisfiable.

Usage: please uncomment the line `result = sat.solve_with_resolution()` and comment the other usage lines from above in order to run this code.

## Functionality

I made several extra functions to implement resolution:

1. **`resolution(self, clause1, clause2)`**: This method combines two clauses, `clause1` and `clause2`. It detects conflicts between complementary literals and returns a new resolved clause or an empty clause if a conflict is detected between the two courses.

2. **`is_tautology(self, clause)`**: This method checks for tautological clauses within the CNF file passed in. It identifies pairs of complementary literals and returns `True` if any are found.

3. **`resolution_solver(self, clauses)`**: The `resolution_solver` is responsible for iteratively applying resolution to the provided clauses. It returns `False` if it encounters an unsatisfiable situation or if no further resolutions can be applied. If no more non-tautological clauses can be found, the method indicates that no additional resolution steps are possible.

4. **`solve_with_resolution(self)`**: This method is the wrapper for solving the CNF file, it is directly called in `solve_sudoku.py`. It attempts to find a satisfying assignment using the `walkSAT` algorithm and, if successful, checks if additional clauses can be derived using the `resolution_solver`.

## Bug Explanation

The `resolution_solver` method doesn't resolve any more clauses with any meaningful benefit. I am not sure how further to address this bug given the time constraints of the assignment, though offer the ideas in the code that was written for partial credit.
