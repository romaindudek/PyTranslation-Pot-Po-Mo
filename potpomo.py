#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Simple instructions to generate Pot / po / mo files for translation
import sys
import os
from shutil import copyfile
from pathlib import Path
import subprocess


class PotPoMo:

    DIR_PATH = os.getcwd()

    def init(self, locale, my_file):
        self.locale = locale
        self.my_file = my_file
        if self.check_params_init():
            self.create_dir(os.path.join(self.DIR_PATH, 'locales'))
            self.create_the_locale_dirs()
            self.create_pot()
            self.copy_pot_to_po()
            print(f"Successfully initiated {self.locale} !")
        else:
            print(messages.WRONG_INIT)
            self.copy_pot_to_po()
    
    def add(self, locale):
        self.locale = locale
        if self.check_params_add():
            self.create_the_locale_dirs()
            self.copy_pot_to_po()
            print(f"Successfully added {self.locale} !")
        else:
            print(messages.WRONG_ADD)

    def check_params_add(self):
        return len(self.locale) == 5

    def create_the_locale_dirs(self):
        self.create_dir(os.path.join(self.DIR_PATH, 'locales', self.locale))
        self.create_dir(os.path.join(self.DIR_PATH, 'locales', self.locale, 'LC_MESSAGES'))

    def create_dir(self, dir_path):
        if not Path(dir_path).is_dir():
            print(f"Create {dir_path} directory")
            os.mkdir(dir_path)
        else:
            print(f"{dir_path} directory allready exists")

    def create_pot(self):
        try:
            subprocess.run(['xgettext', '-d', 'base', '-o', 'locales/base.pot', os.path.join(self.DIR_PATH, self.my_file)])
        except subprocess.CalledProcessError as e:
            print(e.output)
    
    def mo_generate(self):
        subs = [f.name for f in os.scandir(os.path.join(self.DIR_PATH, 'locales')) if f.is_dir()]
        print([x for x in subs])
        for subdir in subs:
            try:
                subprocess.run(['msgfmt', '-o', os.path.join(self.DIR_PATH, 'locales', subdir, 'LC_MESSAGES', 'base.mo'), os.path.join(self.DIR_PATH, 'locales', subdir, 'LC_MESSAGES', 'base') ])
            except subprocess.CalledProcessError as e:
                print(e.output)

    def copy_pot_to_po(self):
        copyfile(os.path.join(self.DIR_PATH, 'locales', 'base.pot'), os.path.join(self.DIR_PATH, 'locales', self.locale, 'LC_MESSAGES', 'base.po'))

    def check_params_init(self):
        return len(self.locale) == 5 and self.my_file[-3:] == '.py'


potpomo = PotPoMo()

class messages:

    HELP = """
* Usage : ./potpomo.py [option] [parameters]

* Available options :

    [-init]         :   [parameter1] = <current_locale (fr_FR, en_US, es_ES etc...)> [parameter2] = <file_to_translate (.py)>
                        Create transtation tree with the current_locale :

                        locale/
                            |__ <current_locale>/LC_MESSAGES
                            |                               |_ base.po
                            |_ base.pot

    [-add]    :   [parameter] = <new_locale> 
                        Create a new branch in the current tree for your new_locale :

                        locale/
                            |__ <new_locale>/LC_MESSAGES
                                                            |_ base.po

    [-build]        :   Create the .mo files 

    [-add_keys]     :   [parameter] = <file_to_translate (.py)>
                        Rebuild the .pot file, adding the new keys found in the file_to_translate
    
    [-code]         :   Generate the code to add in your .py file to be shure to translate correctly on the client side
"""

    WRONG_INIT = """
Something is wrong with the parameters :

[parameter1] = <current_locale (fr_FR, en_US, es_ES etc...)> [parameter2] = <file_to_translate (.py)>        
"""

    WRONG_ADD = """
Something is wrong with the parameter :

[parameter] = <current_locale (fr_FR, en_US, es_ES etc...)>
"""


def main(argv):

    if not argv :
        print(messages.HELP)
        sys.exit()

    if argv[0] == '-h':
        print(messages.HELP)
        sys.exit()

    if argv[0] == '-init' and argv[1] and argv[2]:
        potpomo.init(argv[1], argv[2])
    
    if argv[0] == '-add' and argv[1]:
        potpomo.add(argv[1])
    
    if argv[0] == '-build' and argv[1]:
        print("go for it")
        potpomo.add(argv[1])

if __name__ == "__main__":
    main(sys.argv[1:])