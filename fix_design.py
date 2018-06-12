#!/bin/bash

if [ "$#" -ge 1 ]; then
    design=$1
    ui=$(echo $1 | sed 's/\./_/').py
else
    design='main.ui'
    ui='main_ui.py'
fi

if [ "$#" -eq 2 ]; then
    baseclass=$2
else
    baseclass='QtGui.QWidget'
fi

echo "---------------------------"
echo "design=$design ui=$ui baseclass=$baseclass"
echo "---------------------------"

echo "> Converting design"
pyuic4 $design > $ui

# make self executable
if [[ ! $(head -n1 $ui | grep '#!/usr/bin/python' | wc -l) > 0 ]]; then
    echo "> adding header"
    echo '#!/usr/bin/python -OOtt' > _$ui
    cat $ui >> _$ui
    mv -f _$ui $ui
    chmod +x $ui
else
    echo "> has header"
fi

# fix inheritance
if [[ $(grep '^class .*(object):' $ui | wc -l) != '0' ]]; then
    echo "> fixing inheritance"
    sed -i "s/class \([^(]*\)(object):/class \1($baseclass):/" $ui
else
    echo "> has inheritance"
fi


if [[ $(grep "if __name__ == '__main__':" $ui | wc -l) == 0 ]]; then
    echo "> adding main"
    echo "if __name__ == '__main__':" >> $ui
    echo "    import sys" >> $ui
    echo "    app = QtGui.QApplication(sys.argv)" >> $ui

    # set class name
    obj=$(grep '^class ' $ui | sed 's/^class //' | sed 's/(.*//')
    echo "    win = ${obj}()" >> $ui

    echo "    win.setupUi(win)" >> $ui
    echo "    win.retranslateUi(win)" >> $ui
    echo "    win.show()" >> $ui
    echo "    sys.exit(app.exec_())" >> $ui
    echo "" >> $ui
else
    echo "> has main"
fi

