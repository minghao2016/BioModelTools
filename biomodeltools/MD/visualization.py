from IPython.display import Image, display_png
import glob
import os

DEFAULT_PLOTS_TO_SKIP = ['bfactors_plot_backbone.png',
                        'plot_Dens.png',
                        'plot_Energies.png',
                        'plot_Pres.png',
                        'plot_Temp.png',
                        'plot_Vol.png',
                        'RMSD_plot_backbone_cut.png',
                        'RMSD_plot_backbone.png'
                        ]

def plot_md_info(directory=None, run_list=None, plots_to_skip=DEFAULT_PLOTS_TO_SKIP):
    '''Find run folders of given enzyme and show plots.

    Use in jupyter notebook.


    Args:
        directory (str): path to enzymeA ie. ~/MD/enzymeA/
            The folder ~/MD/enzymeA must contain folers in format runX/analyze where x
            is number 1+. and analyze contains results from cpptraj analysis and plots
    plotted in gnuplot by Sergio's script.
        run_list (list): a list of runs which to analyze.
                       defaults to all runs found in directory kwarg
        plots_to_skip (list): a list of filenames (.png) you do not want to plot
    '''

    if not directory or not os.path.isdir(directory):
        raise FileNotFoundError("Please specify existing folder containing MD runs!")
    if not run_list:
        run_list = sorted(glob.glob(os.path.join(directory,"run?")))
    if not plots_to_skip:
        plots_to_skip=[]

    print('''Plotting MD info from folder {}\n
    about runs {}\n
    excluding plots: {}'''.format(directory, list(map(lambda x: x.split("/")[-1], run_list)), plots_to_skip))
    os.chdir(directory)
    print()
    for run in run_list:
        images = glob.glob(run.split('.')[0]+"/analyze/*png")
        images = [img for img in images if img.split('/')[-1] not in plots_to_skip]
        print("#"*80)
        print("-"*35,run.split('/')[-1],"-"*35)
        print("#"*80)
        for image in images:
            display_png(Image(filename=image))
