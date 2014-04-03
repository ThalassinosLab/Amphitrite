#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.4 on Sun Dec  9 09:55:02 2012

"""Program for calculating calibration curves for travelling wave ion
mobility mass spectrometry"""

__author__ = "Ganesh N. Sivalingam <g.n.sivalingam@gmail.com"

import wx, os

# begin wxGlade: extracode
# end wxGlade
import CalibrantGuiGrids
import CalibrationGuiPlotting as CGPlotting
import imClasses.Calibration as Calibration
import imClasses.Calibrant as Calibrant
import matplotlib.pyplot as plt
import lib.utils as utils
import collections, CalibrationGuiSettings
import cPickle as pickle
import paths as p


class CalibrationGui(wx.Frame):
    def __init__(self, *args, **kwds):
        # change directory to where the pickles are
        os.chdir('..')
        self.calibrants = collections.OrderedDict()
        self.calibrantCharges = collections.OrderedDict()
        self.calibration = Calibration()
        self.settings = CalibrationGuiSettings.CalibrationGuiSettings()
        
        # begin wxGlade: CalibrationGui.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D | wx.SP_BORDER)
        self.paneLeft = wx.Panel(self.window_1, -1, style=wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)
        self.textCtrlPath = wx.TextCtrl(self.paneLeft, -1, "")
        self.buttonOpenCalibrant = wx.Button(self.paneLeft, -1, "Open")
        self.choiceCalibrant = wx.Choice(self.paneLeft, -1, choices=["Myoglobin (denatured)", "Bovine Serum Albumin", "Alcohol Dehydrogenase", "Pyruvate Kinase", "Serum Amyloid P (5-mer)", "Serum Amyloid P (10-mer)", "Concanavalin A", "Avidin", "Cytochrome c (denatured)", "Cytochrome c (native)", "Bradykinin", "Beta-lactoglobulin Monomer", "Beta-lactoglobulin Dimer"])
        self.buttonAddCalibrant = wx.Button(self.paneLeft, -1, "Add")
        self.panelCalibrantListCtrl = wx.Panel(self.paneLeft, -1)
        self.label_3 = wx.StaticText(self.paneLeft, -1, "Edit Peak ")
        self.text_ctrl_peak = wx.TextCtrl(self.paneLeft, -1, "")
        self.buttonPick = wx.Button(self.paneLeft, -1, "Pick")
        self.sizer_2_staticbox = wx.StaticBox(self.paneLeft, -1, "Calibrant(s)")
        self.label_1 = wx.StaticText(self.paneLeft, -1, "Wave Velocity")
        self.textCtrlWaveVelocity = wx.TextCtrl(self.paneLeft, -1, "")
        self.label_2 = wx.StaticText(self.paneLeft, -1, "Mobility Gas")
        self.choiceGas = wx.Choice(self.paneLeft, -1, choices=["Nitrogen", "Helium"])
        self.buttonSaveCalibration = wx.Button(self.paneLeft, -1, "Save Calibration")
        self.sizer_3_staticbox = wx.StaticBox(self.paneLeft, -1, "Calibration")
        self.paneRight = wx.Panel(self.window_1, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.eventOpenCalibrant, self.buttonOpenCalibrant)
        self.Bind(wx.EVT_CHOICE, self.eventCalibrantChoice, self.choiceCalibrant)
        self.Bind(wx.EVT_BUTTON, self.eventAddCalibrant, self.buttonAddCalibrant)
        self.Bind(wx.EVT_TEXT_ENTER, self.eventWaveVelocity, self.textCtrlWaveVelocity)
        self.Bind(wx.EVT_TEXT, self.eventWaveVelocityTyping, self.textCtrlWaveVelocity)
        self.Bind(wx.EVT_CHOICE, self.eventGasChoice, self.choiceGas)
        self.Bind(wx.EVT_BUTTON, self.eventSaveCalibration, self.buttonSaveCalibration)
        # end wxGlade
        
    def __set_properties(self):
        # begin wxGlade: CalibrationGui.__set_properties
        self.SetTitle("Amphitrite - Calibration Beta")
        self.SetSize((772, 527))
        self.buttonOpenCalibrant.SetMinSize((70, 28))
        self.choiceCalibrant.SetSelection(0)
        self.buttonAddCalibrant.SetMinSize((70, 28))
        self.buttonPick.SetMinSize((60, 28))
        self.choiceGas.SetSelection(0)
        # end wxGlade
        self.figure = CGPlotting.CalGuiFigure(self.paneRight,self.calibrants,self.settings,self)
        self.panelCalibrantListCtrl.Hide()
        self.panelCalibrantListCtrl = CalibrantGuiGrids.CalibrantGrid(self.paneLeft,self.calibrants,self.settings,self.figure,self.text_ctrl_peak)
        self.settings.list_ctrl = self.panelCalibrantListCtrl
        
        # settings object
        self.settings.setCalNameCurrent(self.choiceCalibrant.GetStringSelection())
        #self.settings.setCalPath(r'C:\Users\ganesh\Desktop\121108_bsa_005.raw')
        self.settings.setWaveVelocity("350")
        
        # properties
        self.textCtrlPath.SetValue(self.settings.getCalPath())
        self.textCtrlWaveVelocity.SetValue(self.settings.getWaveVelocityString())
        

    def __do_layout(self):
        # begin wxGlade: CalibrationGui.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        self.sizer_3_staticbox.Lower()
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(3, 1, 0, 0)
        grid_sizer_4 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_3 = wx.FlexGridSizer(2, 2, 0, 0)
        self.sizer_2_staticbox.Lower()
        sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.HORIZONTAL)
        grid_sizer_5 = wx.FlexGridSizer(3, 1, 0, 0)
        grid_sizer_7 = wx.FlexGridSizer(1, 3, 0, 0)
        grid_sizer_6 = wx.FlexGridSizer(2, 2, 0, 0)
        grid_sizer_6.Add(self.textCtrlPath, 0, wx.EXPAND, 0)
        grid_sizer_6.Add(self.buttonOpenCalibrant, 0, 0, 0)
        grid_sizer_6.Add(self.choiceCalibrant, 0, wx.EXPAND, 0)
        grid_sizer_6.Add(self.buttonAddCalibrant, 0, 0, 0)
        grid_sizer_6.AddGrowableCol(0)
        grid_sizer_5.Add(grid_sizer_6, 1, wx.EXPAND, 0)
        grid_sizer_5.Add(self.panelCalibrantListCtrl, 1, wx.EXPAND, 0)
        grid_sizer_7.Add(self.label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_7.Add(self.text_ctrl_peak, 0, wx.EXPAND, 0)
        grid_sizer_7.Add(self.buttonPick, 0, 0, 0)
        grid_sizer_7.AddGrowableCol(1)
        grid_sizer_5.Add(grid_sizer_7, 1, wx.EXPAND, 0)
        grid_sizer_5.AddGrowableRow(1)
        grid_sizer_5.AddGrowableCol(0)
        sizer_2.Add(grid_sizer_5, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_2, 3, wx.EXPAND | wx.ALIGN_BOTTOM, 0)
        grid_sizer_3.Add(self.label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.textCtrlWaveVelocity, 0, wx.EXPAND, 0)
        grid_sizer_3.Add(self.label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.choiceGas, 0, wx.EXPAND, 0)
        grid_sizer_3.AddGrowableRow(0)
        grid_sizer_3.AddGrowableCol(1)
        grid_sizer_2.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_2.Add((1, 30), 0, wx.EXPAND, 0)
        grid_sizer_4.Add(self.buttonSaveCalibration, 0, wx.EXPAND, 0)
        grid_sizer_4.AddGrowableCol(0)
        grid_sizer_2.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_2.AddGrowableCol(0)
        sizer_3.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        self.paneLeft.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(0)
        grid_sizer_1.AddGrowableCol(0)
        self.window_1.SplitVertically(self.paneLeft, self.paneRight, 300)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def eventOpenCalibrant(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Open a calibration amphitrite file (FileDialog).
        """
        dlg = wx.FileDialog(self, message="Choose an Amphitrite file",
                            wildcard="Amphitrite IM file (*.a)|*.a",
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.settings.setCalPath(str(dlg.GetPath()))
            self.textCtrlPath.SetValue(self.settings.getCalPath())        
        dlg.Destroy()
        

    def eventCreateCalibation(self, event):  # wxGlade: CalibrationGui.<event_handler>
        # TODO(gns) - deleted this function. Needs to be removed from wxglade
        event.Skip()
    
    def createCalibration(self):
        """Calculate the calibration curve.
        """
        self.figure.createCalibration()      


    def eventSaveCalibration(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Save calibration and supporting figures (FileDialog).
        """
        dlg = wx.FileDialog(self, message="Save Amphitrite Calibration",
                            defaultFile="",wildcard="Amphitrite Calibration File (*.acal)|*.acal",
                            style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            p = dlg.GetPath()  
            if not p.endswith('.acal'):
                p += '.acal'
            self.settings.saveFilePath = p   
            
            dlg.Destroy()
            if not os.path.isdir(self.settings.saveFilePath):
                folderPath = self.settings.saveFilePath
                folderName = os.path.basename(folderPath)[:-5] # remove file extension

                os.mkdir(folderPath)
                calibrantsFolder = os.path.join(folderPath,'calibrants')
                os.mkdir(calibrantsFolder)
                
                # Calibration
                self.figure.calibration.pickle(os.path.join(folderPath,folderName+'.calibration'))
                
                # Calibration figure
                fig = plt.figure(figsize=[6,4])
                ax = fig.add_subplot(111)
                self.figure.calibration.plotCalibrationCurve(ax)
                fig.savefig(os.path.join(folderPath,folderName+'_calibration.png'))
                
                # Calibrants
                figure = plt.figure(figsize=[8,6])
                axMs = figure.add_subplot(211)
                axTd = figure.add_subplot(212)
                
                for name,calibrant in self.calibrants.items():
                    # plotting
                    calibrant.plotMsAndExtractionLimits(axMs)
                    calibrant.plotChargeStateAtds(axTd)
                    calibrant.plotCalibrantTdPeaks(axTd)
                    # set xlims
                    axMs.set_xlim(self.settings.xlimsMs[name])
                    axTd.set_xlim(self.settings.xlimsTds[name])
                    # save
                    figure.savefig(os.path.join(calibrantsFolder,folderName+'_%s.png' %calibrant.name))
                    # clear                
                    axMs.cla(); axTd.cla()
            


    def eventWaveVelocity(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Function is called when new wave velocity is entered. This should be removed
        from the gui (using wxglade). Also see self.eventWaveVelocityTyping().
        """
        # TODO(gns) - Delete this, think I used to have a button to press after entering the value
        event.Skip()

    def eventAddCalibrant(self, event,autoAxesLimits=1):  # wxGlade: CalibrationGui.<event_handler>
        """Add a calibrant to the calibration. Opens calibrant using path textbox,
        processes it and recalculates the calibration curve.
        """
        # please wait dialog
        bi = wx.BusyInfo("Working, please wait", self)
        wx.Yield() 
        
        if self.textCtrlPath.GetValue() != "":
            self.settings.setCalPath(self.textCtrlPath.GetValue())
        
        calibrantName = self.settings.getCalNameCurrent()
        
        # Mass Spectrum panel
        calibrant = Calibrant.Calibrant(calibrantName,self.settings.calPath)
        calibrant.plotMsAndExtractionLimits(self.getAxMS())
        if autoAxesLimits:
            mzs = [utils.get_mz(calibrant.approxMass, z) for z in calibrant.charges]
            self.settings.xlimsMs[calibrantName] = [min(mzs)*0.5,max(mzs)*2]
            self.figure.axMs.set_xlim(self.settings.xlimsMs[calibrantName])

            self.settings.ylimsMs[calibrantName] = self.figure.axMs.get_ylim()
            self.figure.axMs.set_xlim(self.settings.xlimsMs[calibrantName])
            self.figure.axMs.set_yticks([])
        
        # Tds panel
        calibrant.plotChargeStateAtds(self.getAxTds())
        calibrant.plotCalibrantTdPeaks(self.getAxTds(clear=0))
        if autoAxesLimits:
            tds = [calibrant.tds[z] for z in calibrant.charges][:]
            self.settings.xlimsTds[calibrantName] = [min(tds)*0.5,max(tds)*2.0]
            self.settings.ylimsTds[calibrantName] = self.figure.axTds.get_ylim()
            self.figure.axTds.set_xlim(self.settings.xlimsTds[calibrantName])
        
        # Fill in the grid
        self.panelCalibrantListCtrl.setData(calibrant)
        self.calibrants[calibrantName] = calibrant
        self.calibrantCharges[calibrantName] = calibrant.charges[:]
        
        self.createCalibration()
        self.draw()
        bi.Destroy()

    def eventWaveVelocityTyping(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Update the wave velocity and recalculate (and plot) the calibration as
        the user types.
        """
        self.settings.setWaveVelocity(self.textCtrlWaveVelocity.GetValue())
        self.createCalibration()
        self.draw()

    def eventGasChoice(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Record choice for gas setting (helium|nitrogen).
        """
        # TODO(gns) - This doesn't need to happen. When the calibration is calculated it
        # should just get this value from the gui element
        self.settings.setGas(self.choiceGas.GetStringSelection())
        self.createCalibration()
        self.draw()
    
    def eventCalibrantChoice(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Set the type of calibrant (protein and oligomeric state) in self.settings.
        """
        # TODO(gns) - This doesn't need to happen. When the calibration is calculated it
        # should just get this value from the gui element
        self.settings.setCalNameCurrent(self.choiceCalibrant.GetStringSelection())
    
    # getters for axes
    def getAxMS(self,clear=1):
        ":returns: Top panel matplotlib Axes object."
        if clear:
            self.figure.axMs.cla()
        return self.figure.axMs
    def getAxTds(self,clear=1):
        ":returns: Middle panel matplotlib Axes object."
        if clear:
            self.figure.axTds.cla()
        return self.figure.axTds
    def getAxCal(self,clear=1):
        ":returns: Lower panel matplotlib Axes object."
        if clear:
            self.figure.axCal.cla()
        return self.figure.axCal
    def draw(self):
        """Convenience function. Redraw the graphs (update with any changes made).
        """
        self.figure.canvas.draw()
        

    def eventEditPeakTyping(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Gets the value when the edit peak text box is updated and fills in
        the the associated cell in the calibrant ListCtrl (table). If a non numeric
        value is entered, nothing happens.
        """
        list_ctrl = self.panelCalibrantListCtrl.list_ctrl
        i = list_ctrl.selectedRow
        if i != None:
            try:
                td = float(self.text_ctrl_peak.GetValue())
                list_ctrl.setTdValue(td)
            except:
                pass

    def eventEditPeakToggle(self, event):  # wxGlade: CalibrationGui.<event_handler>
        """Allows the user to select the position of the peak top themselves by clicking
        on the arrival time (middle) matplotlib axis panel.
        """
        if self.buttonPickToggle.GetValue() == True:
            self.figure.pickingActive = True
            fail = self.panelCalibrantListCtrl.list_ctrl.pickPeak()
            if fail:
                self.buttonPickToggle.SetValue(False)
        elif self.buttonPickToggle.GetValue() == False:
            self.figure.axTds.set_picker(False)
            
            proName = self.panelCalibrantListCtrl.list_ctrl.displayedProtein
            if self.figure.pickedValue:
                self.calibrants[proName].setTdValue(self.figure.pickedValue,self.panelCalibrantListCtrl.list_ctrl.getCharge())
                self.calibrants[proName]._updateSpecies(updateApex=0)
                self.panelCalibrantListCtrl.list_ctrl.setTdValue(self.figure.pickedValue)
                self.text_ctrl_peak.SetValue("%.2f" %self.figure.pickedValue)
            self.panelCalibrantListCtrl.list_ctrl._plotTds(proName)
            self.figure.createCalibration()
            self.figure.pickedValue = False
            self.figure.pickingActive = False
            


# end of class CalibrationGui
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = CalibrationGui(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
