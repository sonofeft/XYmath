#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
XY_Job holds all data related to one XYmath task.

This object reads, writes, and administrates XYmath task
"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import next
from builtins import map
from builtins import object

#
# import statements here. (built-in first, then 3rd party, then yours)
from numpy import array, double
import os
from itertools import combinations

from .dataset import DataSet
from .linfit import LinCurveFit
from .nonlinfit import NonLinCurveFit
from .eqn_defs import common_eqn_defL
from .helper_funcs import INFINITY, is_number
from .exhaustive import build_xterms

here = os.path.abspath(os.path.dirname(__file__))

__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2013 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "charlietaylor@users.sourceforge.net"
__status__ = "4 - Beta" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"


class XY_Job(object):
    """XY_Job holds all data related to one XYmath task.

       This object reads, writes, and administrates XYmath task
    """

    def __init__(self, job_name='XYmath Task', file_prefix=None):
        """Inits XY_Job."""
        self.job_name = job_name
        self.file_prefix = file_prefix
        if file_prefix is None:
            self.file_name = None
        else:
            self.file_name = file_prefix + '.x_y'
        
        self.dataset = None
        self.linfit = None # saved linear curve fit
        self.nonlin_fit =  None # save non-linear curve fit

    def define_dataset(self, xArr, yArr, wtArr=None, xName='', yName='',
        xUnits='', yUnits='', timeStamp=None):
        """Create DataSet object for XY_Job."""
        self.dataset = DataSet(xArr, yArr, wtArr=wtArr, xName=xName, yName=yName,
        xUnits=xUnits, yUnits=yUnits, timeStamp=timeStamp)
        
        #print 'New dataset defined with wtArr=',wtArr
    
    def make_linear_fit(self, xtranL=None, ytran='y', fit_best_pcent=0, cArr=None,
        pcent_std=None, std=None): # pcent_std and std are dummy inputs
        '''Do a linear sum of terms fit, possibly followed by a refinement(for ytran!='y')
           If cArr is input, simply save the c values and recalc pcent_std and std
        '''
        Lfit = LinCurveFit( self.dataset, xtranL=xtranL, ytran=ytran, \
            fit_best_pcent=fit_best_pcent, cArrInp=cArr)
        return Lfit
        
    def save_linear_fit(self, Lfit):
        self.linfit = Lfit
    
    def basenameWithExt(self, fname):
        '''returns the file name "fname" with a new extension (if provided)'''
        if fname.lower().endswith('.x_y'):
            return fname
        else:
            return fname + '.x_y'

    def set_file_name(self, fname):
        """Sets values of file_name and file_prefix"""
        if fname:
            self.file_name = self.basenameWithExt( fname )
            self.file_prefix = self.file_name[:-4]

    def write_job_to_file(self, fname=None):
        """Write XY_Job to disk."""
        
        self.set_file_name( fname )
            
        if not self.file_name:
            print('ERROR... no file name specified in "write_job_to_file".')
            return
        
        fOut = open( self.file_name, 'w' )
        def write_property(obj, header, propL ):
            fOut.write( '[%s]\n'%header )
            for pname in propL:
                if pname.endswith(b'Arr'):
                    try:
                        valL = ['%s'%val for val in getattr(obj, pname)]
                        fOut.write( '%s = %s\n'%(pname, ', '.join(valL)) )
                    except:
                        fOut.write( '%s = %s\n'%(pname, getattr(obj, pname)) )
                else:
                    fOut.write( '%s = %s\n'%(pname, getattr(obj, pname)) )
            
        write_property(self, 'XY_Job', ['job_name'] )
        
        if self.dataset:
            write_property(self.dataset, 'DataSet', 
                ['xArr', 'yArr', 'wtArr', 'xName', 'yName', 'xUnits', 'yUnits','timeStamp'])
                        
        fOut.close()

    def read_job_from_file(self, fname=None, fileObj=None):
        """Read XY_Job from disk."""
        
        if fileObj:
            self.set_file_name( fileObj.name )
        else:
            self.set_file_name( fname )        
            if not os.path.isfile( self.file_name ):
                print('ERROR... file does not exist in "read_job_from_file".')
                return
            fileObj = open( self.file_name, 'r' )
        
        def strip_square_brackets( s ):
            if s.startswith(b'[') and s.endswith(b']'):
                return s[1:-1]
            else:
                return s
        
        def build_header_dicts():
            allD = {} # dict of dict.  Each header will have a dict
            header = ''
            for line in fileObj: # Headers look like [HeaderName]
                line = line.strip()
                if line.startswith(b'[') and line.endswith(b']'):
                    header = line[1:-1]
                    allD[header] = {} # dict for header
                else:
                    # data lines within a Header look like: param = all the param data
                    # split at the 1st equal sign for name/data pairs
                    sL = line.split(b' = ', 1)
                    if len(sL) == 2:
                        pname = sL[0].strip()
                        # strip any enclosing square brackets from data 
                        val = strip_square_brackets( sL[1].strip() )
                        
                        # Maybe change val for special circumstances
                        if val!=b'None':
                            if pname.endswith(b'Arr'):
                                # arrays should be space delimited numbers
                                val = val.replace(b',',b' ') # if comma delimited, change
                                vL = val.split()
                                print( '---> %10s'%pname,'val=',val )
                                val = array( list(map(float, vL)), dtype=double)
                            else:
                                if is_number(val):
                                    val = float(val)
                                    #print '%10s'%pname,'val=',val
                        else:
                            val = None
                                
                        if header:
                            allD[header][pname] = val
            return allD
        
        allD = build_header_dicts()
        
        D = allD.get('XY_Job', {'job_name':'XYmath Task'})
        self.job_name = D['job_name']
        
        D = allD.get('DataSet', {})
        if D:
            self.define_dataset(**D)
            print('xArr =',self.dataset.xArr)
            print('yArr =',self.dataset.yArr)
            
                    
        fileObj.close()
        

        
    def fit_dataset_to_common_eqns(self, run_both=1, sort_by_pcent=1, max_terms=9):
        ordered_resultL = [] # list of LinCurveFit objects
        for ytran, xtranL in common_eqn_defL:
            # skip equations with too many terms
            if len(xtranL) > max_terms:
                continue
                
            if run_both or not sort_by_pcent:
                try:
                    #print '\nfitting',ytran,'=',xtranL
                    linfit = self.make_linear_fit(xtranL, ytran, fit_best_pcent=0)
                    if linfit.std < INFINITY:
                        ordered_resultL.append( linfit )
                        #print linfit.get_eqn_str_w_consts()
                        #print linfit.get_eqn_str_w_numbs()
                except:
                    pass
            if run_both or sort_by_pcent:
                try:
                    #print '\nfitting',ytran,'=',xtranL
                    linfit = self.make_linear_fit(xtranL, ytran, fit_best_pcent=1)
                    if linfit.pcent_std < INFINITY:
                        ordered_resultL.append( linfit )
                        #print linfit.get_eqn_str_w_consts()
                        #print linfit.get_eqn_str_w_numbs()
                except:
                    pass
                
        if sort_by_pcent:
            ordered_resultL.sort( key=lambda lf: lf.pcent_std)
        else:
            ordered_resultL.sort( key=lambda lf: lf.std)
                
        if ordered_resultL:
            self.linfit = ordered_resultL[0]
                
        return ordered_resultL


    # make exhaustive search a generator so it can be interupted
    def fit_dataset_to_exhaustive_search(self, run_best_pcent=0, 
        num_terms=3, funcL=None, xtranL=None,  ytranL=None):
            
        self.linfit = None
        
        # default to a simple search
        if funcL is None:
            funcL = ['const','x','x**2']
        if xtranL is None:
            xtranL=['x','(1/x)','exp(x)']
        if ytranL is None:
            ytranL=['y','1/y','y**2']
        
        # build a list of all possible terms
        termL = build_xterms( funcL=funcL, xtranL=xtranL )
        
        for ytran in ytranL:
            for i,rhs in enumerate(combinations(termL, num_terms)):

                # skip equations with too many terms
                if len(rhs) > num_terms:
                    continue
                    
                if run_best_pcent:
                    try:
                        #print '\nfitting',ytran,'=',rhs
                        linfit = self.make_linear_fit(rhs, ytran, fit_best_pcent=1)
                        if linfit.pcent_std < INFINITY:
                            #print linfit.get_eqn_str_w_consts()
                            if self.linfit:
                                if linfit.pcent_std < self.linfit.pcent_std:
                                    self.linfit = linfit
                            else:
                                self.linfit = linfit
                            yield linfit
                    except:
                        pass
                        
                else: # best total error
                    try:
                        #print '\nfitting',ytran,'=',rhs
                        linfit = self.make_linear_fit(rhs, ytran, fit_best_pcent=0)
                        if linfit.std < INFINITY:
                            #print linfit.get_eqn_str_w_consts()
                            if self.linfit:
                                if linfit.std < self.linfit.std:
                                    self.linfit = linfit
                            else:
                                self.linfit = linfit
                            yield linfit
                    except:
                        pass


    # make exhaustive search a generator so it can be interupted
    def fit_dataset_to_nonlinear_eqn(self, run_best_pcent=0, rhs_eqnStr='A*x**b', 
                                         constDinp=None):
        
        self.nonlin_fit =  NonLinCurveFit(self.dataset, rhs_eqnStr=rhs_eqnStr, 
                                          fit_best_pcent=run_best_pcent, 
                                          constDinp=constDinp)        


if __name__=='__main__':
    from numpy import array, double
    from .dataset import DataSet
    from pylab import *
    from .helper_funcs import nextColor # to make color iterator
    
    XY = XY_Job(file_prefix='tube_socks')

    XY.read_job_from_file()
    
    print('*'*60)
    for linfit in XY.fit_dataset_to_exhaustive_search( run_best_pcent=0, 
        num_terms=3, funcL=None, xtranL=None,  ytranL=None):
        print(linfit.get_eqn_str_w_consts())
        
    XY.write_job_to_file()
    print('Stop at sys.exit()')
    sys.exit()
    
    xArr = array( [1,2,3,4,5,6], dtype=double)
    yArr = array( [1.2, 3.1, 9.2, 15.8, 24.6, 36.5], dtype=double)
    wtArr = None # array( [1,1,1,1,1,1], dtype=double)
    
    XY.define_dataset(xArr, yArr, wtArr=wtArr, xName='LaDee', yName='Daa', xUnits='inches', yUnits='degF')
    Lfit = XY.make_linear_fit(['const','x'], ytran='log(y)', fit_best_pcent=1)
    XY.save_linear_fit( Lfit )
    print(Lfit.get_full_description())
    print()
    #Lfit.refine_the_fit_v2( min_pcent=0 )
    #print Lfit.get_full_description()
    #print
    
    ordered_resultL = []
    if 1:
        ordered_resultL = XY.fit_dataset_to_common_eqns(run_both=0, sort_by_pcent=0)
        for lf in ordered_resultL:
            #print lf.get_full_description()
            print('%-36s'%lf.get_eqn_str_w_consts(), '%10.3f'%lf.std, \
                '%10.5f'%lf.pcent_std, {0:'STD',1:'%std'}[lf.fit_best_pcent])
        print(ordered_resultL[0].get_full_description())
    
    XY.write_job_to_file()
    
    ncolor = nextColor() # make color iterator
    
    xPlotArr = XY.linfit.get_x_plot_array(Npoints=100, logScale=0)
    mfc=next(ncolor)
    plot(xPlotArr, XY.linfit.eval_xrange(xPlotArr), '-+', mfc=mfc,color=mfc,  
        label=XY.linfit.get_eqn_str_w_consts(), linewidth=3)
    #mfc=ncolor.next()
    plot(XY.dataset.xArr, XY.dataset.yArr, 'o',markersize=10, mfc=mfc,color=mfc, label='Data Points')
    
    for lf in ordered_resultL[1:4]:
        mfc=next(ncolor)
        plot(xPlotArr, lf.eval_xrange(xPlotArr), mfc=mfc,color=mfc, 
            label=lf.get_eqn_str_w_consts(), linewidth=1)
        
    
    legend(loc='best')
    grid(True)
    title( XY.linfit.get_eqn_str_w_numbs() )
    xlabel( XY.dataset.get_x_desc() )
    ylabel( XY.dataset.get_y_desc() )

    show()
    
