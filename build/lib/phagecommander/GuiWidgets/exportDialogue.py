import os
from abc import abstractmethod
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from phagecommander.Utilities.Tools import *
# (GRyde) May need this for vertical line
from PyQt5 import QtWidgets
from PyQt5 import QtCore
# (GRyde) ------------------------------------

class exportDialog(QDialog):
    """
    Abstract class for representing an export dialogue

    Must Implement:
    saveFile()

    accept() and reject() can be overloaded to change behavior when Export/Cancel are clicked respectively
    Default behavior is to call QDialog.accept()/QDialog.reject()
    """
    
    # (GRyde) Strings updated
    _EXACTLY_BUTTON_TEXT = 'Exactly'
    _LESS_THAN_EQUAL_BUTTON_TEXT = 'No more than'
    _GREATER_THAN_BUTTON_TEXT = 'At least'
    _ALL_BUTTON_TEXT = 'All programs'
    _ONE_BUTTON_TEXT = 'Any program (Export all genes)'
    _INVALID_SAVE_FILE_BORDER = 'border: 1px solid red'
    
    # (GRyde) ************************************************************************** start
    # Additional buttons text
    _MOST_OCCURRENCES_TEXT = 'Majority rule'
    _SPECIFIC_PROGRAM_TEXT = 'Specific program'
    _LONGEST_TEXT = 'Longest open reading frame (called by program)'
    # (GRyde) ************************************************************************** end

    def __init__(self, queryData, settings, parent=None):
        super(exportDialog, self).__init__(parent)

        self.queryData = queryData
        self.settings = settings

        # VARIABLES -----------------------------------------------------------------
        # currently selected radiobutton - defaults to ALL
        self.currentSelection = self._LESS_THAN_EQUAL_BUTTON_TEXT
        self.codonCurrentSelection = self._MOST_OCCURRENCES_TEXT
        self.exportTRNA = True
        self.specificProgram = ''
        self.toolCount = 0
        for tool in self.queryData.tools:
            if tool in GENE_TOOLS and self.queryData.tools[tool] is True:
                self.toolCount += 1
        self.saveFileName = ''
        
        # radio button font
        radioFont = QFont()
        radioFont.setPointSize(12)
        
        # label font
        exportLabelFont = QFont()
        exportLabelFont.setPointSize(12)
        exportLabelFont.setUnderline(True)
        
        exportCallsFont = QFont()
        exportCallsFont.setPointSize(12)

        # WIDGETS ------------------------------------------------------------------
        mainLayout = QVBoxLayout()
        spinBoxLayout = QGridLayout() # Previously QHBoxLayout()
        radioButtonLayout = QGridLayout()
        saveFileLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        # (GRyde) ********************************************************************** start
        # Box layouts for dividers
        threeBoxLayout = QGridLayout()
        dividerLineLayout = QVBoxLayout()
        codonMainLayout = QVBoxLayout()
        codonLabelLayout = QHBoxLayout()
        codonRadioButtonLayout = QGridLayout()
        # (GRyde) ********************************************************************** end

        selectionText = QLabel('Export genes chosen by:')
        selectionText.setFont(exportLabelFont)

        self.filterSpinBox = QSpinBox()
        self.filterSpinBox.setMaximumWidth(50)
        # set max possible value to total amount of tools
        self.filterSpinBox.setMaximum(self.toolCount)
        self.filterSpinBox.setMinimum(1)
        self.filterSpinBox.setValue(self.filterSpinBox.maximum())

        callsLabel = QLabel('programs')
        callsLabel.setFont(exportCallsFont)

        self.radioButtons = []
        exactlyRadioButton = QRadioButton(self._EXACTLY_BUTTON_TEXT)
        exactlyRadioButton.clicked.connect(lambda: self.buttonClicked(exactlyRadioButton))
        self.radioButtons.append(exactlyRadioButton)
        greaterThanRadioButton = QRadioButton(self._GREATER_THAN_BUTTON_TEXT)
        greaterThanRadioButton.clicked.connect(lambda: self.buttonClicked(greaterThanRadioButton))
        self.radioButtons.append(greaterThanRadioButton)
        lessThanEqualRadioButton = QRadioButton(self._LESS_THAN_EQUAL_BUTTON_TEXT)
        lessThanEqualRadioButton.clicked.connect(lambda: self.buttonClicked(lessThanEqualRadioButton))
        lessThanEqualRadioButton.setChecked(True)
        self.radioButtons.append(lessThanEqualRadioButton)
        allRadioButton = QRadioButton(self._ALL_BUTTON_TEXT)
        allRadioButton.clicked.connect(lambda: self.buttonClicked(allRadioButton))
        self.radioButtons.append(allRadioButton)
        oneRadioButton = QRadioButton(self._ONE_BUTTON_TEXT)
        oneRadioButton.clicked.connect(lambda: self.buttonClicked(oneRadioButton))
        self.radioButtons.append(oneRadioButton)
        
        # (GRyde) ********************************************************************** start
        # Testing button groups
        # Added font setting
        genesButtonGroup = QButtonGroup(self)
        for button in self.radioButtons:
            genesButtonGroup.addButton(button)
            button.setFont(radioFont)
        
        # (GRyde) ********************************************************************** end
        
        # (GRyde) ********************************************************************** start
        # Testing adding new items to export box
        dividerLine = QFrame(self)
        dividerLine.setFrameShape(QFrame.VLine)
        dividerLine.setFrameShadow(QFrame.Sunken)
        dividerLine.setLineWidth(1)
        
        codonSelectionText = QLabel('Export gene starts chosen by:')
        codonSelectionText.setFont(exportLabelFont)
        programSelectionText = QLabel('Program:')
        programSelectionText.setFont(exportLabelFont)
        tProgramSelectionText = QLabel('If either or both, favor:')
        tProgramSelectionText.setFont(exportLabelFont)
        
        self.codonRadioButtons = []
        mostOccurButton = QRadioButton(self._MOST_OCCURRENCES_TEXT)
        mostOccurButton.clicked.connect(lambda: self.codonButtonClicked(mostOccurButton))
        mostOccurButton.setChecked(True)
        self.codonRadioButtons.append(mostOccurButton)
        longestButton = QRadioButton(self._LONGEST_TEXT)
        longestButton.clicked.connect(lambda: self.codonButtonClicked(longestButton))
        self.codonRadioButtons.append(longestButton)
        specificButton = QRadioButton(self._SPECIFIC_PROGRAM_TEXT)
        specificButton.clicked.connect(lambda: self.codonButtonClicked(specificButton))
        self.codonRadioButtons.append(specificButton)
        self.programComboBox = QComboBox()
        self.programComboBox.setEnabled(False)
        
        
        # (GRyde) Need this check so that only programs actually used can be selected. But probably need an
        #         add'l list with cleaner, full names that cross references this and then populates list that way
        toolNames = []
        for tool in self.queryData.tools:
            if tool in GENE_TOOLS and self.queryData.tools[tool] is True:
                toolNames.append(tool)
                #self.programComboBox.addItem(tool)
        #self.programComboBox.setMinimumWidth(250)
        
        # (GRyde) Dictionary to hold zhuzhed up program names for combobox
        self.zhuzhedNames = {'rast': 'Rast', 'metagene': 'MetaGene', 'gm': 'GeneMark',
                        'hmm': 'HMM', 'heuristic': 'Heuristic', 'gms': 'GeneMarkS',
                        'gms2': 'GeneMarkS-2', 'glimmer': 'Glimmer', 'prodigal': 'Prodigal'}
                        
        for tool in toolNames:
            self.programComboBox.addItem(self.zhuzhedNames[tool])
        self.programComboBox.setMinimumWidth(250)
                        
        
        codonButtonGroup = QButtonGroup(self)
        for button in self.codonRadioButtons:
            codonButtonGroup.addButton(button)
            button.setFont(radioFont)
            
        tRNABox = QCheckBox('Export tRNA called by Aragorn')
        tRNABox.stateChanged.connect(lambda: self.toggleTRNA(tRNABox))
        tRNABox.setChecked(True)
        tRNABox.setFont(radioFont)
            
        dividerLineLayout.addWidget(dividerLine)
        codonLabelLayout.addWidget(codonSelectionText)
        # (GRyde) ********************************************************************** end

        exportButton = QPushButton('Export')
        exportButton.clicked.connect(self.exportPressed)
        exportButton.setDefault(True)

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.cancelPressed)

        self.saveLineEdit = QLineEdit()
        self.saveLineEdit.setMinimumWidth(150) # Originally 200, scaled up after changing grid layout
        self.saveLineEdit.textEdited.connect(self.saveLineEdited)
        saveButton = QPushButton('Save as...')
        saveButton.clicked.connect(self.saveFile)

        # LAYOUT -------------------------------------------------------------------
        # Old implementation of spin box. Needed to be added to radioButtonLayout to achieve aesthetic effect
        # requested.
        
        #spinBoxLayout.addWidget(self.filterSpinBox)
        #spinBoxLayout.addWidget(callsLabel)
        
        # Re-purposing spinBoxLayout to get intended aesthetic effect for program
        spinBoxLayout.addWidget(greaterThanRadioButton, 0, 0)
        spinBoxLayout.addWidget(self.filterSpinBox, 0, 1)
        spinBoxLayout.addWidget(callsLabel, 0, 2)
        # Since width of radio button is relevant to the layout mostly, adjusting width here instead of putting in the block of text
        # that creates all the radio buttons
        #greaterThanRadioButton.setMaximumWidth(140)

        mainLayout.addWidget(selectionText)
        #mainLayout.addLayout(spinBoxLayout)
        
        # Commented out buttons removed from final version but code remains in case needed again
        # or to allow for re-purposing later
        
        oneRadioButton.sizePolicy().setHorizontalStretch(1)
        #radioButtonLayout.addWidget(lessThanEqualRadioButton, 0, 0)
        radioButtonLayout.addWidget(oneRadioButton, 0, 0)
        #radioButtonLayout.addWidget(greaterThanRadioButton, 1, 0)
        radioButtonLayout.addLayout(spinBoxLayout, 1, 0)
        radioButtonLayout.addWidget(allRadioButton, 2, 0)
        #radioButtonLayout.addWidget(exactlyRadioButton, 2, 0)
        radioButtonLayout.addWidget(tRNABox, 3, 0)
        
        
        # (GRyde) ********************************************************************** start
        # Testing layouts for extra buttons
        codonRadioButtonLayout.addWidget(mostOccurButton, 0, 0)
        codonRadioButtonLayout.addWidget(longestButton, 1, 0)
        codonRadioButtonLayout.addWidget(specificButton, 2, 0)
        codonRadioButtonLayout.addWidget(programSelectionText, 3, 0)
        codonRadioButtonLayout.addWidget(self.programComboBox, 4, 0, 1, 2)
        
        
        # These .addStretch lines line up the second box perfectly with the first, very aesthetic
        codonMainLayout.addLayout(codonLabelLayout)
        #codonMainLayout.addStretch(1)
        codonMainLayout.addLayout(codonRadioButtonLayout)
        codonMainLayout.addStretch(2)
        
        
        # (GRyde) ********************************************************************** end

        mainLayout.addLayout(radioButtonLayout)
        #mainLayout.addLayout(spinBoxLayout)

        saveFileLayout.addWidget(self.saveLineEdit)
        saveFileLayout.addWidget(saveButton)
        

        buttonLayout.addWidget(exportButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout.addLayout(saveFileLayout)
        mainLayout.addLayout(buttonLayout)
                
        # (GRyde) ********************************************************************** start
        # Definitely a test 
        # Seems to work!
        threeBoxLayout.addLayout(mainLayout, 0, 0)
        threeBoxLayout.addLayout(dividerLineLayout, 0, 1)
        threeBoxLayout.addLayout(codonMainLayout, 0, 2)
        # (GRyde) ********************************************************************** end
        

        # WINDOW --------------------------------------------------------------------
        self.setWindowTitle('Export Dialogue')
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setLayout(threeBoxLayout) # (GRyde) Originally self.setLayout(mainLayout)

    def exportPressed(self):
        """
        Called when export is pressed
        :return:
        """
        if not self._checkValidSaveFile():
            return
        else:
            self.accept()

    def cancelPressed(self):
        """
        Called when cancel is pressed
        """
        self.reject()

    def accept(self):
        """
        Called by exportPressed
        """
        QDialog.accept(self)

    def reject(self):
        """
        Called by cancelPressed
        """
        QDialog.reject(self)

    @abstractmethod
    def saveFile(self):
        """
        TO BE IMPLEMENTED BY SUBCLASS
        """
        pass

    def buttonClicked(self, radioButton: QRadioButton):
        """
        Called when a radio button is toggled
        :param radioButton: QRadioButton which was toggled
        """

        # set the range of the spinbox
        self.setSpinBoxRange(radioButton)

        # set the currentSelection
        self.currentSelection = radioButton.text()
        
    # (GRyde) Additional method for codon radio buttons
    def codonButtonClicked(self, radioButton: QRadioButton):
        
        # set selection for codon button groups
        self.codonCurrentSelection = radioButton.text()
        
        # Determine if combobox should be enabled
        if self.codonCurrentSelection == self._SPECIFIC_PROGRAM_TEXT:
            self.programComboBox.setEnabled(True)
        else:
            self.programComboBox.setEnabled(False)
            # Clear out attribute if specific program isn't selected
            self.specificProgram = ''
            
    # (GRyde) Additional method for toggling TRNA checkbox
    def toggleTRNA(self, checkbox: QCheckBox):
        if checkbox.isChecked():
            self.exportTRNA = True
        else:
            self.exportTRNA = False
            

    def setSpinBoxRange(self, radioButton: QRadioButton):
        """
        Dynamically sets the range of spinboxes based upon the selected filter type
        :param radioButton: radioButton which was toggled
        """
        buttonText = radioButton.text()

        # enable the spinbox if it was disabled
        self.filterSpinBox.setEnabled(True)

        # set range from 1-max
        if buttonText == self._EXACTLY_BUTTON_TEXT or buttonText == self._LESS_THAN_EQUAL_BUTTON_TEXT:
            maxVal = self.toolCount
            self.filterSpinBox.setMaximum(maxVal)
            self.filterSpinBox.setMinimum(1)

        # (GRyde) Updating range to accommodate change from > comparison operator to >=
        # (Updated) set range from 1, max
        # Effectively same as exactly or LTE but will keep separate just in case for later
        # (Old) set range from 0, max - 1
        elif buttonText == self._GREATER_THAN_BUTTON_TEXT:
            maxVal = self.toolCount 
            self.filterSpinBox.setMaximum(maxVal)
            self.filterSpinBox.setMinimum(1)

        # (GRyde) Clarification on what "ALL" refers to
        # Doesn't export all genes, just exports genes called by all used programs
        # So if 8 programs used, set spin box value to 8 and use comparison operator of ==
        elif buttonText == self._ALL_BUTTON_TEXT:
            # set box to max and disable
            self.filterSpinBox.setValue(self.toolCount)
            self.filterSpinBox.setDisabled(True)

        # (GRyde) Currently this only pulls genes called by 1 program when it should be all genes called by AT LEAST 1 program (so all genes)
        #         Will just updated lambda to >=. Since this sets the value as 1, then >= 1 will pull everything    
        elif buttonText == self._ONE_BUTTON_TEXT:
            # set box to one and disable
            self.filterSpinBox.setValue(1)
            self.filterSpinBox.setDisabled(True)

    def getSelection(self):
        """
        :return: The currently selected button and filter amount in a tuple
                (<selected_button_text>, <filter_amount>)
        """
        return self.currentSelection, self.filterSpinBox.value()
        
    # (GRyde) Pull current program selection from combobox, only called if specific 
    #         program button selected when hitting export
    def getSpecificProgram(self):
    
        key_list = list(self.zhuzhedNames.keys())
        value_list = list(self.zhuzhedNames.values())
        
        position = value_list.index(self.programComboBox.currentText())
    
        return key_list[position]

    def getFilterFunction(self):
        """
        :return: A filter function based upon the current dialog selection
            * Filter function is of the following form:
                lambda x: x <= <filter_amount>
                lambda x: x == <filter_amount>
                lambda x: x > <filter_amount>
        """
        filterAmount = self.filterSpinBox.value()

        filterFunctions = {
            self._ALL_BUTTON_TEXT: lambda x: x == filterAmount,
            self._LESS_THAN_EQUAL_BUTTON_TEXT: lambda x: x <= filterAmount,
            self._GREATER_THAN_BUTTON_TEXT: lambda x: x >= filterAmount,
            self._EXACTLY_BUTTON_TEXT: lambda x: x == filterAmount,
            self._ONE_BUTTON_TEXT: lambda x: x >= filterAmount
        }

        return filterFunctions[self.currentSelection]

    def saveLineEdited(self):
        """
        Called when the save line edit is changed
        :return:
        """
        # reset border to default
        self.saveLineEdit.setStyleSheet('')

    def _checkValidSaveFile(self):
        """
        Checks if the file path given in the line edit is valid
        """

        invalid = False
        # if empty save file
        if self.saveLineEdit.text() == '':
            self.saveLineEdit.setStyleSheet(self._INVALID_SAVE_FILE_BORDER)
            QMessageBox.warning(self,
                                'File Not Given',
                                'Select a file to save to.')
            invalid = True

        # if the given directory exists
        elif not os.path.isdir(os.path.split(self.saveLineEdit.text())[0]):
            self.saveLineEdit.setStyleSheet(self._INVALID_SAVE_FILE_BORDER)
            QMessageBox.warning(self,
                                'Directory Does Not Exist',
                                'Selected directory does not exist.')
            invalid = True

        # check if a directory and file were given
        elif os.path.split(self.saveLineEdit.text())[1] == '':
            self.saveLineEdit.setStyleSheet(self._INVALID_SAVE_FILE_BORDER)
            QMessageBox.warning(self,
                                'Select a Save File',
                                'Please select a file to save to.')
            invalid = True

        if invalid:
            return False

        # save file is valid
        else:
            self.saveFileName = self.saveLineEdit.text()
            return True


if __name__ == '__main__':
    from phagecommander.phagecom import QueryData

    app = QApplication([])
    dig = exportDialog(QueryData(), QSettings())
    dig.show()
    app.exec_()
    print(dig.saveFileName)
