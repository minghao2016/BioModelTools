==========
Basic info
==========
Use conda to install all packages and dependencies with
``conda env create -f environment.yml``

To comfortably import in your scripts, make sure to clone the repo and add

``export PYTHONPATH="/home/pocin/projects/BioModelTools:$PYTHONPATH" #path/to/git/repo``
to your ~/.bashrc
This will do just fine before the collection of scripts grows into larger scale. 
If needed pip package might be created

Use with caution :)
