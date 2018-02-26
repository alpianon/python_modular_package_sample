
#    Copyright (C) 2018  Alberto Pianon <alberto@pianon.eu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pkgutil, sys, inspect

__all__ = []

for loader, module_name, is_pkg in  pkgutil.walk_packages(
    __path__, prefix=__name__+"."
):
    if not is_pkg:
        __all__.append(module_name)
        __import__(module_name)

# Set here the base class. Do not move this line above 
# otherwise you get a NameError, because modules must be loaded before this line
BASE_CLASS = basetask.BaseTask


def get_classes():
    """returns a list of tuples (ORDER, classname, classobject)"""
    classes = []
    classnames = [] # this list is just to check for duplicate classnames
    for modname, modobj in inspect.getmembers(
        sys.modules[__name__], inspect.ismodule
    ):
        for classname, classobj in inspect.getmembers(
            sys.modules[__name__+"."+modname], 
            lambda membercl: 
                inspect.isclass(membercl) 
                and 
                issubclass(membercl, basetask.BaseTask)
        ):
            if hasattr(classobj, 'ORDER') and classobj != BASE_CLASS:
                if classname in classnames:
                    raise Exception("Duplicate class name '%s'" % classname)
                else:
                    classnames.append(classname)
                    classes.append((classobj.ORDER, classname, classobj))
    classes.sort()            
    return classes

def get_class_list():
    classes = get_classes()
    return [ 
        (classname, classobj.__doc__)  
        for order, classname, classobj in classes
    ]
    
def get_class(name):
    classes = get_classes()
    for order, classname, classobj in classes:
        if classname == name:
            return classobj
    raise Exception("Task class '%s' does not exist" % name) 







            
                
        
