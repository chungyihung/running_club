## Running Club Member System

Draft version

### Environment
* Python 3.6.1
* PyQt5 (V5.8.1)

### Installation

### Windows
1. Python 3.6.1 - Download release binary from website:

	```bash
   https://www.python.org/downloads/release/python-361/
   ```
2. PyQt5 - After install Python 3.6.1, run the below commands:

   ```bash
   pip3 install pyqt5
   One could check PyQt5 version with following code:
     from PyQt5.QtCore import QT_VERSION_STR
     from PyQt5.Qt import PYQT_VERSION_STR
     from sip import SIP_VERSION_STR

     print( "QT Ver: ", QT_VERSION_STR )
     print("SIP Version: ", SIP_VERSION_STR )
     print( "PyQt Version: ", PYQT_VERSION_STR )

   The results are as follows,
        >>> print( "QT Ver: ", QT_VERSION_STR )
        QT Ver:  5.8.0
        >>> print("SIP Version: ", SIP_VERSION_STR )
        SIP Version:  4.19.1
        >>> print( "PyQt Version: ", PYQT_VERSION_STR )
        PyQt Version:  5.8.1
   ```

###TODO
1. Redesign the data type of each items in database. In this draft version I just implemented a toy without mature design.
2. Learn how to manipulate QtTableWidget to implement more user friendly interface.
3. Think/discuss a way with user to implement functions/pages for each running activity.


