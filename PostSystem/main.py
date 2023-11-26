class Solution:
    def __init__(self):
        self.error = False
        self.ok = False
        self.replacements = []  # List of Replacement objects to track variable replacements

class Replacement:
    def __init__(self, variable, replacement, count):
        self.variable = variable  # Variable to be replaced
        self.replacement = replacement  # Value to replace the variable with
        self.count = count  # Number of times the replacement should be applied

class Rule:
    def __init__(self, source, target):
        self.source = source  # Original form of the rule
        self.target = target  # Transformed form of the rule

    def print_rule(self):
        print("{} -> {}".format(self.source, self.target))

def check_simple_rule(axioms, revealed_rule):
    """
    Check if the revealed rule is present in the axioms list.

    Args:
    axioms: List of current axioms
    revealed_rule: Rule to check

    Returns:
    Solution object indicating if the rule is present or not
    """
    result = revealed_rule in axioms
    solution = Solution()
    solution.ok = result
    return solution

def is_hard_rule(rule, variables):
    """
    Check if the rule contains any variables.

    Args:
    rule: Rule to check
    variables: List of variables

    Returns:
    True if rule contains any variables, False otherwise
    """
    for variable in variables:
        if variable in rule:
            return True
    return False

def find_first_variable(rule, variables):
    """
    Find the first variable in the rule.

    Args:
    rule: Rule to search in
    variables: List of variables

    Returns:
    The first variable found in the rule, or None if no variable is found
    """
    for variable in variables:
        if variable in rule:
            return variable

def check_revealed_rule(rule, axioms, alphabet, variables, replacement):
    """
    Check if the rule with the variable replaced with the replacement value is valid.

    Args:
    rule: Rule to check
    axioms: List of current axioms
    alphabet: List of valid replacement values
    variables: List of variables
    replacement: Replacement value

    Returns:
    Solution object indicating if the rule is valid or not
    """
    solution = Solution()

    for i in range(1, len(axioms)):
        variable = find_first_variable(rule, variables)

        new_rule = rule.replace(variable, replacement * i)

        check_result = check_rule(new_rule, axioms, alphabet, variables)

        if check_result.error:
            check_result.replacements.append(Replacement(variable, replacement, i))
            return check_result
        if check_result.ok:
            solution = check_result
            solution.replacements.append(Replacement(variable, replacement, i))

    return solution

def check_rule(rule, axioms, alphabet, variables):
    """
    Check if the rule is valid and can be applied.

    Args:
    rule: Rule to check
    axioms: List of current axioms
    alphabet: List of valid replacement values
    variables: List of variables

    Returns:
    Solution object indicating if the rule is valid or not
    """
    if not is_hard_rule(rule, variables):
        return check_simple_rule(axioms, rule)

    solution = Solution()

    for replacement in alphabet:
        check_result = check_revealed_rule(rule, axioms, alphabet, variables, replacement)

        if check_result.error:
            return check_result
        if check_result.ok:
            if not solution.ok:
                solution = check_result
            else:
                solution.ok = False
                solution.error = True
                solution.replacements.extend(check_result.replacements)
                return solution

    return solution

def apply_rule(axioms, rule_from, rule_to):
    """
    Apply a rule to the axioms list by replacing the 'rule_from' part with 'rule_to'.

    Args:
    axioms: List of current axioms
    rule_from: Rule part to be replaced
    rule_to: Rule part to replace with
    """
    axioms[0] = axioms[0].replace(rule_from, rule_to)

def one_step(axioms, rules, alphabet, variables):
    """
    Apply one step of rule transformation to the axioms list.

    Args:
    axioms: List of current axioms
    rules: List of rules
    alphabet: List of valid replacement values
    variables: List of variables

    Returns:
    True if a rule is successfully applied, False otherwise
    """
    solution = Solution()
    rule_id = 0

    for rule_index, rule in enumerate(rules):
        check_result = check_rule(rule.source, axioms[0], alphabet, variables)

        if check_result.error:
            print(axioms[0])
            rule.print_rule()
            print("Error: ambiguous application of the rule")
            return False
        if check_result.ok:
            if not solution.ok:
                solution = check_result
                rule_id = rule_index
            else:
                print(axioms[0])
                rules[rule_id].print_rule()
                rule.print_rule()
                print("Error: multiple rules can be applied")
                return False

    if solution.ok:
        rule_from = rules[rule_id].source
        rule_to = rules[rule_id].target

        for rep in solution.replacements:
            replacer = rep.replacement * rep.count
            rule_from = rule_from.replace(rep.variable, replacer)
            rule_to = rule_to.replace(rep.variable, replacer)

        print(axioms[0])
        apply_rule(axioms, rule_from, rule_to)
        rules[rule_id].print_rule()
        print(axioms[0] + "\n")
        return True

    return False

def apply_rules_until_converge(axioms, rules, alphabet, variables):
    """
    Apply rules until the axioms list no longer changes.

    Args:
    axioms: List of current axioms
    rules: List of rules
    alphabet: List of valid replacement values
    variables: List of variables

    Returns:
    The final axioms list after all rules have been applied
    """
    axioms_list = [axioms]
    while one_step(axioms_list, rules, alphabet, variables):
        pass
    return axioms_list[0]
    
def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() != '':
                equal_sign_pos = line.find(" = ")
                if equal_sign_pos == -1:
                    continue  # Пропустить строки без знака " = "
                key = line[:equal_sign_pos].strip()
                value = line[equal_sign_pos + 3:].strip()
                if key.strip() == 'A':
                    alphabet = set(value.strip()[1:-1].split(','))
                elif key.strip() == 'X':
                    variables = set(value.strip()[1:-1].split(','))
                elif key.strip() == 'A1':
                    axiom = value.strip()
                elif key.strip() == 'R':
                    rules = []
                    rules_text = value.strip()[1:-1]
                    lines = rules_text.split(',')
                    for line in lines:
                        rule_parts = line.split('->')
                        if len(rule_parts) == 2:
                            pattern = rule_parts[0].strip()
                            replacement = rule_parts[1].strip()
                            if pattern and replacement:
                                rules.append(Rule(pattern, replacement))
    return(axiom, alphabet, variables, rules)

def check_symbols_in_string(string, symbols):
    string = str(string)
    symbols = str(symbols)
    for char in string:
        if char not in symbols:
            return False
    return True


def main():
    axioms,  alphabet, variables, rules =  read_data("input.txt")
    
    # Continue the program if the data is correct
    # Is axiom valid? 
    if not (check_symbols_in_string(axioms, alphabet)):
        print("There is a simbol not from Alphabet")
        return 0

    # Is variables valid?
    if not (all(check_symbols_in_string(rules.source + rules.target, alphabet | variables) for rules in rules)):
        print("There is a wrong variable")
        return 0

    apply_rules_until_converge(axioms, rules, alphabet, variables)
    print("Calculations completed successfully")
    
   

if __name__ == "__main__":
    main()

