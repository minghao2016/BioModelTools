import sys
import logging 
import os


class BfactorMapper:
    def __init__(self, reference_pdb, dataframe, outdir=None, column=None):
        '''
        Map calculated B-Factors onto pdb structure.

        Args:
            reference_pdb (str): '/path/to/pdb/structure.pdb',
                The output will be written to the same directory.

            dataframe (pd.DataFrame): Contains the CA B-factors.
                Rows are residue numbers (crystal numbering). 
                    	Classical 	Accelerated
                    1 	NaN 	NaN
                    ...
                    9 	NaN 	NaN
                    10 	197.212250 	828.368475
                    11 	61.747075 	447.767075
                    ...

            outdir (str): Defaults to path where reference_pdb is located:

        Usage:
        >>> with BfactorMapper("./results/bfactors/rluc8_b.pdb",
                               bfactors_rluc8,
                               outdir='/path/to/results',
                               column='Classical') as b:
                    b.fix_bfactors()
        '''

        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger()
        self._bfac_data = dataframe
        self._ref_pdb = reference_pdb
        self.column = column
        self.outdir = outdir or reference_pdb.split('/')[:-1]
        self._new_pdb_filename = self._create_results_filename(reference_pdb)

        self.name = reference_pdb.split('/')[-1].split('.')[0]


    def __enter__(self):
        self.logger.debug("Opening files for reading/writing")

        try:
            self._pdb = open(self._ref_pdb, 'r')
            self._new_pdb = open(self._new_pdb_filename, 'w')
            return self
        except IOError as e:
            self.logger.debug("Couldnt open pdb. {}".format(e))
            sys.exit(1)

    def __exit__(self, exception_type, exception_value, traceback):
        self.logger.debug("Closing files")

        self._pdb.close()
        self._new_pdb.close()

    def _create_results_filename(self,fname):
        '''Create pdb file with outdir in mind! '''

        *path, file_ = fname.split('/')
        file_ = file_.replace('.pdb',"_bfactors_{}.pdb".format(self.column))
        if self.outdir:
            return os.path.join(self.outdir, file_)
        else:
            path.append(file)
            return '/'.join(path)

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self,col):
        possible_columns = self._bfac_data.columns.tolist()
        if not col or (col not in possible_columns):
            raise TypeError("please choose which column out of {} contains bfactors.".format(possible_columns))
        else:
            self._column = col

    def __repr__(self):
        return "I represent {}".format(self._ref_pdb)

    def _is_atom(self,line):
        if line.startswith('ATOM'):
            self.logger.debug("{} is atom".format(line))
            return True
        else:
            return False

    def _fix_bfactor(self,line):
        self.logger.debug("Fixing bfactors in line \n{}".format(line))
        self.logger.debug("Identified resid {}".format(self._resid(line)))
        bfactor = str(self._bfac_data.ix[self._resid(line),self.column])[:5]
        newline = line[:61] + bfactor + line[65:]
        self.logger.debug("New line is\n{}".format(newline))
        return newline

    def _resid(self,line):
        self.logger.debug("Trying to get resid {}".format(line.split()[5]))

        #nekdy to vyjde tak, ze mezi ATOM_TYPE a RESNAME neni mezera
        try:
            return int(line.split()[5])
        except ValueError as e:
            return int(line.split()[4])

    def _process_line(self,line):
        if self._is_atom(line):
            line = self._fix_bfactor(line)
        self._new_pdb.write(line)

    def parse_pdb(self):
        for line in self._pdb:
            self._process_line(line)
        self.logger.debug("pdb sucesfully parsed")
