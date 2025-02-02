"""Class for holding additional functions for IesGui()."""

__author__ = "Ganesh N. Sivalingam <g.n.sivalingam@gmail.com"

import wx,os,re
import cPickle as pickle
from collections import OrderedDict
from msClasses import MassSpectrum
from imClasses import Im
import gui.guiFunctions as gf
import IesCheckboxStates
import ListCtrlConformationsIes
from lib import utils
class IesSettings():

    def __init__(self,plotPanel):
        self.species = []
        self.speciesCharges = OrderedDict()
        
        self.atrOb = None
        self.calibrationOb = None
        
        self.plotPanel = plotPanel

        self.checkboxStates = IesCheckboxStates.IesCheckboxStates()
        self.listCtrlConformations = None

        self.loadedFiles = OrderedDict()
        self.massSpectra = OrderedDict() # filename as key
        self.filenames = []              # should be set by listctrlfiles

        self.widthL = 1.0
        self.widthR = 1.0

        self.speciesSelected = None
        self.chargeSelected = None

        self.units = ''
        self.values = []

        self.conformations = []

        self.displayPeaks = True

    #====================
    # Adding other components
    def setListCtrlConformations(self,listCtrl):
        """Add the conformations table to this class.
        :parameter listCtrl: ListCtrlConformationsIes() object
        """
        self.listCtrlConformations = listCtrl

    def setPlotPanel(self,plotPanel):
        """Add the Matplotlib plot panel object to this class.
        :parameter plotPanel: IesPlotPanel() object
        """
        self.plotPanel = plotPanel

    #====================

    def setDisplayPeaks(self,bool):
        """Display user selected peaks.
        :parameter bool: Boolean for display peaks or not
        """
        self.displayPeaks = bool

    def addConformation(self,ccs):
        """Add a CCS conformation to user defined peaks.
        :parameter ccs: CCS value for the peak
        """
        self.listCtrlConformations.addConformation(ccs)
    def removeConformation(self,ccs):
        """Remove one of the user selected peaks.
        :parameter ccs: CCS value of the peak to remove
        """
        # TODO(gns) - Don't think this has been implemented yet
        self.listCtrlConformations.removeConformation(ccs)
        
    def setSpeciesAndCharge(self,species,charge):
        """Set the species and charge values (selected in the dropdown
        lists).
        :parameter species: Species name (string)
        :parameter charge: Charge state (int)
        """
        self.speciesSelected = species
        self.chargeSelected = charge
        
    def getSpeciesAndCharge(self):
        """Return the currently selected species and charge state (set by
        gui dropdown lists).
        :returns: [speciesName,chargeState]
        """
        return self.speciesSelected,self.chargeSelected
    
    def setUnits(self,units):
        """Set the units for labelling different data. e.g. 'eV'
        for unfolding experiments.
        :parameter units: (string)
        """
        self.units = units
        self.plotPanel.refresh_plot()
        
    def setValues(self,values):
        # TODO(gns) - do the comment
        self.values = []
        for value in values:
            if utils.isNumber(value):
                self.values.append(float(value))
            else:
                self.values.append(None)
                                   

    def setCalibration(self,filename):
        """Open the amphitrite IM calibration object.
        :parameter filename: Absolute path to pickled imClasses.Calibration() object
        """
        import imClasses.Calibration
        try:
            self.calibrationOb = pickle.load(open(filename,'rb'))
        except:
            message = 'Something wrong with calibration file!'
            gf.warningDialog(message)
        
    def loadAtroposSpeciesAndCharges(self,path):
        """Open amphitrite mass spectrum fit and load the species and
        charge information.
        :parameter path: Absolute path to pickled msClasses.MassSpectrum() object
        """
        self.atrOb = pickle.load(open(path,'rb'))
        # reset variables
        self.species = []
        self.speciesCharges = OrderedDict()
        
        for sp in sorted(self.atrOb.simulatedSpecies.keys()):
            self.species.append(sp)
            self.speciesCharges[sp] = self.atrOb.simulatedSpecies[sp].charges
        self.setImObsAtropos()
        
    def setImObsAtropos(self):
        """Load the mass spectrum fit into the imClasses.Im() objects.
        """
        if self.atrOb:
            for fn,imOb in self.loadedFiles.items():
                imOb.setMsFit(self.atrOb)
            
    def setFilenames(self,filenames):
        """Set the filenames for the data (Amphitrite .a files)
        :parameter filenames: List of absolute paths
        """
        self.filenames = filenames
        
    def _forPlotMassSpectra(self,ax,lift):
        """Load data from self.filenames and display in the plot panel.
        :parameter ax: Matplotlib Axes instance for plotting
        :parameter lift: Spacing between mass spectrum traces
        """
        self._loadData(self.filenames)
        self._removeExcessLoadedData(self.filenames)
        self._plottingStackedSpectra(ax,lift)
                
    def _loadData(self,filenames):
        """Open all the data files and load the files into
        imClasses.Im() objects.
        :parameter filenames: List of absolute paths
        """
        for fn in filenames:
            if not fn in self.loadedFiles.keys():
                imOb = Im()
                imOb.loadFolderAuto(fn)              
                ms = imOb.getMassSpectrum()
                self.massSpectra[fn] = ms
                imOb.massSpectrum.normalisationBpi()
                self.loadedFiles[os.path.basename(fn)] = imOb
        self.setImObsAtropos()
                
    def _removeExcessLoadedData(self,filenames):
        """Remove data files which have already been loaded.
        :parameter filenames: List of absolute paths
        """
        fns = [os.path.basename(x) for x in filenames]
        toRemove = []
        for fn in self.loadedFiles.keys():
            if not fn in fns:
                toRemove.append(fn)
        for fn in toRemove:
            print 'Deleting: %s' %fn
            del self.loadedFiles[fn]
            
    def _plottingStackedSpectra(self,ax,lift):
        """Plot all of the loaded mass spectra, with lift spacing between them.
        :parameter ax: Matplotlib Axes instance for plotting
        :parameter lift: Spacing between mass spectrum traces
        """
        for i,msOb in enumerate(self.massSpectra.values()):
            msOb.yvals += lift*i
            msOb.plot(ax)
            msOb.yvals -= lift*i
            
    def _getMzLimits(self,species,charge):
        """Get the m/z value upper and lower limits for extracting arrival
        time data.
        :parameter species: Name of molecular species (species)
        :parameter charge: Charge state (int)
        """
        mz = utils.get_mz(self.atrOb.simulatedSpecies[species].mass,charge)
        fwhm = self.atrOb.simulatedSpecies[species].peakFwhm
        left = (self.widthL*fwhm)/2.
        right = (self.widthR*fwhm)/2.
        return [mz-left,mz+right]

    def setWidthL(self,val):
        """Set the left peak FWHM multiplier for extracting arrival times.
        """        
        self.widthL = val
        self.plotPanel.refresh_plot()
    def setWidthR(self,val):
        """Set the right peak FWHM multiplier for extracting arrival times.
        """        
        self.widthR = val
        self.plotPanel.refresh_plot()

    def _getDataSlice(self,imOb):
        """Get the data slice associated with the currently selected
        species and charge state (from dropdowns).
        :parameter imOb: imClasses.Im() object
        """
        sp = self.speciesSelected
        z = self.chargeSelected
        return imOb.dataSlices[sp][z]
    
    def _updateExtractedSlices(self):
        """Regenerate the data slices using the currently entered
        width multipliers.
        """
        for fn,imOb in self.loadedFiles.items():
            imOb.generateSpeciesSlicesFwhm(
                self.speciesSelected,self.widthL,self.widthR)
            
    def getCcsLines(self):
        """Get the CCS distributions from the loaded data.
        :returns: ccsAxes, lines (intensity axis)
        """
        lines = []
        ccsAxes = []
        self._updateExtractedSlices()
        for fn,imOb in self.loadedFiles.items():
            dataSlice = self._getDataSlice(imOb)
            dataSlice.generateCcsAxisAndGrid(self.calibrationOb,
                                             ccsInterval=1)
            ccsAxes.append(dataSlice.ccsAxis)
            line = dataSlice.getCcsDistribution(self.calibrationOb)
            lines.append(line/line.max()*100)
        return ccsAxes, lines

    def getAtdLines(self):
        """Get the arrival time distributions from the loaded data.
        :returns: xaxes (arrival time axis), lines (intensity axis)
        """
        lines = []
        xaxes = []
        self._updateExtractedSlices()
        for fn,imOb in self.loadedFiles.items():
            dataSlice = self._getDataSlice(imOb)
            xaxes.append(dataSlice.atd.xvals)
            lines.append(dataSlice.atd.yvals)
        return xaxes,lines
        

    def getCcsAxisAndGrid(self):
        """Extract and return the CCS data for a contour plot.
        :returns: ccsAxis (Grid of CCS values associated with..), matrices (intensity matrix)
        """
        matrices = []
        self._updateExtractedSlices()
        for i,(fn, imOb) in enumerate(self.loadedFiles.items()):
            ds = imOb.getDataSlice(self.speciesSelected,
                                    self.chargeSelected)
            ccsMatrix,xaxis,ccsAxis = ds.getCcsMatrix(self.calibrationOb)
            ccsMatrix = ccsMatrix.transpose()
            matrices.append(ccsMatrix)
        return ccsAxis,matrices
            
    def getAtdAxisAndGrid(self):
        """Extract and return the arrival time data for a contour plot.
        :returns: ccsAxis (Grid of td values associated with..), matrices (intensity matrix)
        """
        matrices = []
        for i,(fn, imOb) in enumerate(self.loadedFiles.items()):
            ds = imOb.getDataSlice(self.speciesSelected,
                                    self.chargeSelected)
            matrix,xaxis,tdAxis = ds.getData()
            matrix = matrix.transpose()
            matrices.append(matrix)
        return tdAxis,matrices
