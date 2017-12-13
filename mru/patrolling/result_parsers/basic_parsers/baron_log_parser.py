def has_solution(content):
    """

    :param content:
    :return: true if baron computed a result, false otherwise
    """
    if len(content) > 2:
        return True

    return False

def get_baron_values(content):
    """

    :param content:
    :return: lower bound, objective, upper bound
    """
    # find stats in the log
    index = 0
    for l in content:
        index += 1
        if 'Objective' in l:
            break

    stats=content[index-1:]

    # all the values in the log are for the attacker
    # (1 - val) = payoff of the team
    obj = 1.0 -float(stats[0].split(' ',1)[1].strip())

    splitted = stats[1].split(',',1)
    lower_bound = float(splitted[0].split('=',1)[1].strip()) # NO (1-...) since we will use this info only to check baron performances
    upper_bound = float(splitted[1].split('=',1)[1].strip())

    return lower_bound, obj, upper_bound

def get_baron_time(content):
    """

    :param content:
    :return: time required to solve the instance
    """
    final_line = content[len(content) - 1]
    seconds = float(final_line.split('=',1)[1].strip().split(' ',1)[0].strip())

    return seconds

def get_file_path(targets,instance):
    """

    :param targets:
    :param instance:
    :return: the path to the baron log for the given instance
    """
    return './baron/baron/ntargets_' + str(targets) + '/baron_log_ntargets_' + str(targets) + \
           '_instance_' + str(instance) + '.log'


def is_fine(content):
    """

    :param content:
    :return: true iff the solution is meaningful (exclude those instances for which the computations did not start
    and those instances for which the bounds found are 0,inf)
    """
    if has_solution(content):

        if 'CPU time limit' in content[2]:

            lower_bound = float(content[4].split('=',1)[1].split(',',1)[0].strip())

            if lower_bound == 0.0:

                return False

        return True

    return False

