import os
import sys

#############################################################
# given a specific patrolling instance, it builds the ampl .run file
#   and solves the exact formulation (BARON solver)
#############################################################

def build_run(run_path, dat_path, mod_path, res_path, ntargets, instance):
    """
    builds and saves the .run file
    TIME LIMIT: 1h

    :param run_path:
    :param dat_path:
    :param mod_path:
    :param res_path: where to save BARON output
    :param ntargets:
    :param instance:
    :return:
    """
    # output file
    fout=open(os.path.join(os.getcwd(),run_path), "w")

    run_str=''
    run_str= run_str + 'model "' + mod_path + '";\n'
    run_str= run_str + 'data "' + dat_path + '";\n\n'

    run_str= run_str + 'option solver baron;\n'
    # TIME LIMIT!
    run_str= run_str + "option baron_options 'maxtime=3600 barstats';"
    run_str= run_str + '\n\n'

    run_str= run_str + 'solve;\n\n'

    run_str= run_str + 'display v>>' + res_path + 'baron_value_ntargets_'+str(ntargets)+'instance_'+str(instance)+'.dat;\n\n'

    fout.write(run_str)

    fout.close()

def baron(ntargets, instance):
    """
    given a patrolling instance computes the solution to the exact non-linear
    problem using ampl+baron

    HP: dat files have already been created (dat_builder.py)

    :param ntargets:
    :param instance:
    :return:
    """
    dat_path='./dat/ntargets_'+str(ntargets)+'/'+'ntargets_'+str(ntargets)+'_instance_'+str(instance)+'.dat'
    mod_path='./mod/tmaxmin_exact.mod'
    run_path='./run/ntargets_'+str(ntargets)+'/'+'ntargets_'+str(ntargets)+'_instance_'+str(instance)+'.run'
    res_path='./results/baron/ntargets_'+str(ntargets)+'/'
    log_path= res_path + 'baron_log_ntargets_'+str(ntargets)+'_instance_'+str(instance)+'.log'

    build_run(run_path,dat_path,mod_path,res_path,ntargets,instance)

    # runs the ampl .run file
    os.system('ampl ' + run_path + '>>' + log_path)

if __name__ == "__main__":
    # ntargets, instance
    baron(sys.argv[1],sys.argv[2])
