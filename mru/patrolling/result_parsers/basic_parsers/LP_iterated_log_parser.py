def get_LP_values(content):
    """

    :param content:
    :return: dict <n_restart, (value, n_iter)>
    """
    values={}

    for l in content:

        if 'value =' in l:
            splitted_line=l.split('-',3)

            n_restart = int(splitted_line[1].split('=',1)[1].strip())
            value = float(splitted_line[2].split('=',1)[1].strip())
            n_iter=int(splitted_line[3].split('=',1)[1].strip())

            values[n_restart] = (value, n_iter)

    return values


def get_LP_time(content):
    """

    :param content:
    :return: time to compute the solution
    """
    ftr=[3600, 60, 1]

    seconds = 0.0

    for l in content:
        if 'Total time' in l:
            timestr = l.split(':',3)[3].strip()
            seconds=sum([a*b for a,b in zip(ftr, [float(i) for i in timestr.split(":")])])

    return seconds


def get_file_path(targets,instance):
    """

    :param targets:
    :param instance:
    :return: the path to the LP_iterated log for the given instance
    """
    return './LP_iterated/LP_iterated/ntargets_' + str(targets) + '/LP_iterated_log_ntargets_' + str(targets) +  \
           '_instance_' + str(instance) + '.log'

