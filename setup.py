import setuptools

# 7/31/22: added "encoding='utf-8' " to enable reading.
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

# 7/31/22: removed version number on pyqt5 to enable it to install.
setuptools.setup(
    name='phage-commander',
    license='GPL-3',
    version='0.4.5dev',
    author='Matthew Lazeroff',
    author_email='lazeroff@unlv.nevada.edu',
    description='A graphical tool for predicting genes on phage DNA sequences',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sarah-harris/PhageCommander',
    packages=['phagecommander'],
    package_data={'phagecommander': ['species.txt', 'GuiWidgets/*', 'Utilities/*']},
    install_requires=['wheel',
                      'requests',
                      'bs4',
                      'openpyxl',
                      'pyqt5',
                      'biopython',
                      'ruamel.yaml'],
    entry_points={'gui_scripts': 'phagecom = phagecommander.phagecom:main'},
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: MacOS",
                 "Operating System :: Unix"],
    include_package_data=True,
)
