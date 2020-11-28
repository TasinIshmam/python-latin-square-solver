
class Config:

    variable_ordering_choices = ["brelaz", "smallest domain", "max dynamic degree", "min dynamic degree"]
    algorithm_choices = ["backtracking", "forward checking"]

    variable_ordering = variable_ordering_choices[3]
    algorithm = algorithm_choices[0]