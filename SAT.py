# Sam Rothschild 24/10/23
# sudoku assignment
# SAT class, instantiates and solves problems using sat algos
from random import *

class SAT:
    def __init__(self, fname):
        # Initialise filename and solution, solution should start as None and then be populated
        self.fname = fname
        self.solution = None

    # Function to parse the clauses of a cnf file, returns a list of variables and a list of dicionaries for clauses
    # Returning the list of dictionaries with key:value pairs gets around the indexing difficulties outlined in the spec
    # and simplified implementing the code for me
    def parse_cnf(self):
        # Initialise a list of clauses and a set for variables
        clauses = []
        variables = set()
        # Iterating through the file line by line
        with open(self.fname, 'r') as file:
            lines = file.readlines()

        for line in lines:
            clause = {}
            # Splitting the lines into tokens
            for token in line.split():
                # If it is negated add store a 0 and add token to variables
                if token[0] == '-':
                    # Knock off the leading operator, set to 0 and add to our list of dicts and variables
                    normalised = token[1:]
                    clause[normalised] = 0  
                    variables.add(normalised)
                # Otherwise, so if not negated then just add   
                else:
                    clause[token] = 1
                    variables.add(token)
            clauses.append(clause)
        
        # Convert back to a list so we can return
        variables = list(variables)

        # Return the variables and our clauses
        return variables, clauses
    
    # Helper function to check if a clause is satisfied
    def satisfied_clause(self, assignment, clause):
        # Iterate through the clause variable by variable
        for variable in clause:
            # If it is consistent across teh clause and the assignment then return True
            if clause[variable] == assignment[variable]:
                return True
        # Otherwise return false as the clause isn't satisfied
        return False

    # Check to see if an entire assignment is valid 
    def is_assignment_valid(self, assignment, clauses):
        # Iterate through all clauses
        for clause in clauses:
            # If any of them isn't satisfied, then return False
            if not self.satisfied_clause(assignment, clause):
                return False
        # Else return True as all have been satisfied
        return True
    
    # Helper function to choose next variable which we are going to flip
    def choose_next(self, assignment, clauses, variables):
        # Initialise list of potentials and start the maximum number of satisfied clauses as negative infinity
        potential = []
        max_satisfied_clauses = float("-inf")
        # Iterating through variables
        for variable in variables:
            # Start the number of clauses we have satisfied at 0 and flip variable
            satisfied_clauses = 0
            assignment[variable] = (assignment[variable] + 1) % 2 
            # Iterating through clauses if we have satisfied a clause then increment our counter
            for clause in clauses:
                if self.satisfied_clause(assignment, clause):
                    satisfied_clauses += 1

            # If the number of satisfied clauses equals the maximum we have satisfied then append variable
            if satisfied_clauses == max_satisfied_clauses:
                potential.append(variable)

            # If we exceed the maximum number then store that variable as potential and pudate maximum number of clauses satisfied
            elif satisfied_clauses > max_satisfied_clauses:
                potential = [variable]
                max_satisfied_clauses = satisfied_clauses

            # Flip 
            assignment[variable] = (assignment[variable] + 1) % 2

        return choice(potential)

    # GSAT algorithm, implemented closely following from the wiki page supplied on course website
    def GSAT(self, threshold, max_its):
        variables, clauses = self.parse_cnf()
        seed(1)
        flips = 0  # Initialise flips here
        # While we are under max iteraions
        for _ in range(max_its):
            # Generate an assignment
            assignment = {variable: randint(0, 1) for variable in variables}
            while True:
                # If we have found solution, then update the solution and print number of flips, then return
                if self.is_assignment_valid(assignment, clauses):
                    self.solution = assignment
                    print(f"Solution found after {flips} flips")
                    return assignment
                # If we cross the threshold then flip a variable
                if uniform(0, 1) >= threshold:
                    flip = choice(list(assignment.keys()))
                    assignment[flip] = (assignment[flip] + 1) % 2
                # Else, choose the next best variable, using our helper function and flip
                else:
                    flip = self.choose_next(assignment, clauses, variables)
                    assignment[flip] = (assignment[flip] + 1) % 2
                flips += 1  # Increment flips so we can track total

        # If no solution can be found then report as such and return None
        print("No solution found")
        self.solution = None
        return None

    # Helper function for walkSAT to find all clauses which are not yet satisfied
    def find_unsatisfied_clauses(self, assignment, clauses):
        # Initialise satisfied variable as true, and create an empty list of all unsatisfied clauses
        unsatisfied_clauses = []
        # Iterating through clauses
        for clause in clauses:
            # If a clause is not satisfied
            if not self.satisfied_clause(assignment, clause):
                # Set satisfied to false and append the unsatisfied clause to the list of unsatisfied clauses
                unsatisfied_clauses.append(clause)
        return unsatisfied_clauses

    # WalkSAT algo, following the pseudocode
    def walkSAT(self, threshold, max_its):
        # Get in variables and list of dictionaries for negation from cnf
        variables, clauses = self.parse_cnf()
        seed(1)
        flips = 0  # Initialise flips so we can track
        # While we are under the max number of iterations
        for _ in range(max_its):
            # Generate a random assignment
            assignment = {variable: randint(0, 1) for variable in variables}
            while True:
                # Find all unsatisfied clauses
                unsatisfied_clauses = self.find_unsatisfied_clauses(assignment, clauses)
                # If there are none, then update solution and return it
                if len(unsatisfied_clauses) == 0:
                    self.solution = assignment
                    print(f"Solution found after {flips} flips")
                    return assignment
                # Otherwise pick one of the unsatisfied clauses
                clause = choice(unsatisfied_clauses)
                # If we have crossed the threshold, then flip a varible
                if uniform(0, 1) >= threshold:
                    chosen_variable = choice(list(clause.keys()))
                    assignment[chosen_variable] = (assignment[chosen_variable] + 1) % 2
                else:
                    # Else pick the next variable to flip and flip it
                    next = self.choose_next(assignment, clauses, clause)
                    assignment[next] = (assignment[next] + 1) % 2
                flips += 1

        # If no solution can be found then report as such and return None
        print("Solution not found")
        return None


    # Helper function to write a solution in CNF format to .sol files as per spec
    def write_solution(self, fname):
        # OPen file
        with open(fname, 'w') as file:
            # Iterating through the solution by var
            for var in self.solution:
                # If we can, write the var separated by new line terminators
                if self.solution[var]:
                    file.write(var + "\n")
                # Handle negation case
                else:
                    file.write("-%s"% var +"\n")

    ################################################################################
    #    """                                                                       #
    #    Begin extra credit portion of the assignment, leveraging resolution:      #
    #    """                                                                       #
    ################################################################################

    # Helper function to find a resolution between two clauses
    def resolution(self, clause1, clause2):
        # Represent the resolved clause with an empty dictionary 
        resolved = {}
        
        # Copy the variables and their signs from clause1
        for variable, sign in clause1.items():
            resolved[variable] = sign
        
        # Add variables and their signs from clause2, checking for conflicts
        for variable, sign in clause2.items():
            if variable in resolved:
                # Check for a conflict
                if resolved[variable] != sign:
                    return {}  # If there is a conflict, return an empty clause
            else:
                # Else store appropriate and return
                resolved[variable] = sign
        
        return resolved

    # Helper function to determine if we have a tautology (ie the same thing said twice )
    def is_tautology(self, clause):
        # Create a set to store literals encountered
        literals = set()
        
        # iterate through variables
        for variable in clause:
            # Convert the variable to an integer so we can flip
            variable_int = int(variable)  
            negated_variable = (variable_int + 1) % 2
            
            # If we already have the negated variable then return True
            if negated_variable in literals:
                return True
            # Otherwise add the variable to literals
            literals.add(variable_int)
        
         # Return false if not a tautology
        return False 

    # Wrapper function to actually solve using resolution, to be called in solve_sudoku.py
    def solve_with_resolution(self):
        # Parse the CNF
        variables, clauses = self.parse_cnf()

        # Attempt to find a satisfying assignment using WalkSAT
        satisfying_assignment = self.walkSAT(0.3, 100000)

        # If there is a satisfying assignment using walksat
        if satisfying_assignment:
            print("Assignment found using WalkSAT...")

            # Check for additional clauses that can be derived using resolution
            resolution_possible = self.resolution_solver(clauses)

            if resolution_possible:
                print("Additional clauses derived using resolution:")
                for idx, clause in enumerate(clauses[len(variables):], 1):
                    print(f"Derived Clause {idx}: {clause}")
            else:
                print("No additional clauses derived using resolution.")
        else:
            print("No satisfying assignment found using WalkSAT")

    def resolution_solver(self, clauses):
        # Initialize an empty set of resolved clauses
        resolved_clauses = set()

        while True:
            # Check for unsatisfiability
            if any(len(clause) == 0 for clause in clauses):
                return False  # Unsatisfiable

            # Attempt resolution on all pairs of non-tautological clauses
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if not self.is_tautology(clauses[i]) and not self.is_tautology(clauses[j]):
                        resolvent = self.resolution(clauses[i], clauses[j])
                        if not resolvent:
                            return False  # Found an empty clause, indicating unsatisfiability
                        new_clauses.append(resolvent)

            # Check if there are any new clauses added
            if not new_clauses:
                return True  # No more resolution steps possible

            # Deduplicate the new clauses
            new_clauses = [tuple(clause) for clause in new_clauses]
            new_clauses = list(set(new_clauses))
            resolved_clauses.update(new_clauses)

            # Merge resolved clauses with the original clauses
            clauses += new_clauses
