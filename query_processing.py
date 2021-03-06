def postfix(infix_tokens):
    precedence = {}
    precedence["NOT"] = 3
    precedence["AND"] = 2
    precedence["OR"] = 1
    precedence["("] = 0
    precedence[")"] = 0

    output = []
    operator_stack = []

    # create postfix expression
    for token in infix_tokens:
        if token == "(":
            operator_stack.append(token)
        elif token == ")":
            operator = operator_stack.pop()
            while operator != "(":
                output.append(operator)
                operator = operator_stack.pop()
        elif token in precedence:
            if operator_stack:
                current_operator = operator_stack[-1]
                while (
                    operator_stack and precedence[current_operator] > precedence[token]
                ):
                    output.append(operator_stack.pop())
                    if operator_stack:
                        current_operator = operator_stack[-1]
            operator_stack.append(token)
        else:
            output.append(token.lower())

    # while stack is not empty appending
    while operator_stack:
        output.append(operator_stack.pop())
    return output


def and_operator(word1, word2):
    if (word1) and (word2):
        return set(word1).intersection(word2)
    else:
        return set()


def or_operator(word1, word2):
    return set(word1).union(word2)


def not_operator(a, doc_ids):
    return set(doc_ids).symmetric_difference(a)


doc_ids = []
for i in range(0, 2008):
    doc_ids.append(i)


def process_query(q, dictionary):
    q = q.replace("$", "")
    q = q.replace("(", "( ")
    q = q.replace(")", " )")
    q = q.split(" ")
    query = []

    for i in q:
        query.append(i)
    for i in range(0, len(query)):
        if query[i] == "and" or query[i] == "or" or query[i] == "not":
            query[i] = query[i].upper()
    results_stack = []
    postfix_queue = postfix(query)

    # evaluating postfix query expression
    for i in postfix_queue:
        if i != "AND" and i != "OR" and i != "NOT":
            i = i.replace("(", " ")
            i = i.replace(")", " ")
            i = i.lower()
            i = dictionary.get(i)
            results_stack.append(i)
        elif i == "AND":
            a = results_stack.pop()
            b = results_stack.pop()
            results_stack.append(and_operator(a, b))
        elif i == "OR":
            a = results_stack.pop()
            b = results_stack.pop()
            results_stack.append(or_operator(a, b))
        elif i == "NOT":
            a = results_stack.pop()
            results_stack.append(not_operator(a, doc_ids))
    return results_stack.pop()
