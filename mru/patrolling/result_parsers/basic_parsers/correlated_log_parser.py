def get_all_correlated_values(content):
    """

    :param content:
    :return: dict <n_iter, value>
    """
    values={}

    for l in content:
        if 'partial' in l:
            splitted=l.split('-',3)

            value=float(splitted[3].split('=',1)[1].strip())
            n_iter=int(splitted[2].split('=',1)[1].strip())

            values[n_iter]=value

    return values


def get_correlated_time(content):
    """

    :param content:
    :return: time required to compute the solution
    """
    final_line = content[len(content) - 1]

    if 'Total time' in final_line:

        ftr = [3600, 60, 1]
        timestr = final_line.split(':',3)[3].strip()
        seconds = sum([a*b for a,b in zip(ftr, [float(i) for i in timestr.split(":")])])

    elif 'TIMEOUT' in final_line:

        seconds = 3600

    return seconds

def get_file_path(targets,instance,oracle_type):
    """

    :param targets:
    :param instance:
    :param oracle_type: 'ilp' or 'greedy' or 'ilp_unlimited'
    :return: the path to the correlated log for the given instance
    """
    folder = ''
    if oracle_type == 'ilp':
        folder = './correlated/correlated/'
    elif oracle_type == 'greedy':
        folder = './correlated_greedy/'
    elif oracle_type == 'ilp_unlimited':
        folder = './correlated/correlated_unlimited/'
    else:
        raise ValueError('The wrong oracle type was given to the correlated parser')


    if oracle_type == 'ilp_unlimited':

        return folder + 'ntargets_' + str(targets) + '/correlated_milp_ntargets_' + str(targets) + \
           '_instance_' + str(instance) + '.log'

    return folder + 'ntargets_' + str(targets) + '/correlated_ntargets_' + str(targets) + \
           '_instance_' + str(instance) + '.log'

def has_terminated(content):
    """

    :param content:
    :return: True if computations terminated within the time threshold
    """
    final_line = content[len(content) - 1]

    if 'TIMEOUT' in  final_line:
        return False

    return True
