# Phage Commander 
Phage Commander is a software tool for identifying genes in phage genomes.


## Overview
Phage Commander runs a phage’s DNA sequence through multiple gene identification tools and outputs a list of potential genes. These tools include:

The following gene-encoding prediction tools are currently supported:
* Glimmer
* Genemark
* Genemark Hmm
* GenemarkS
* GenemarkS2
* Genemark Heuristic
* Prodigal
* RAST
* Metagene
* Aragorn (for tRNA genes)

Supported exporting formats:
* Genbank
* Excel


## Getting Started
### Prerequisites
* Python 3.6+


## How to use Phage Commander
1. Open Phage Commander.
   a. On Windows, open a command window (cmd.exe). Navigate to the folder where you
   have downloaded Phage Commander. Navigate to the phagecommander/bin directory.
   Type phagecom-windows.exe in the command window. 
   
   b. On Linux, open a shell. Navigate to the folder where you have downloaded Phage
   Commander. Type py phagecom.py in the shell.
   **Note:** The pip "Scripts" directory should be included in your PATH variable.
   
2. See the included PDF (Phage Commander User Guide.pdf) for how to enter 
   information into the query window.
   

## Manuscript about Phage Commander
Also see the following draft manuscript describing Phage Commander in detail:
https://www.biorxiv.org/content/10.1101/2020.11.11.378802v1


## Author
* **Matthew Lazeroff
* **Geordie Ryder
* **Philippos Tsourkas
* **Sarah Harris


## License
This project is licensed under the GNU GPLv3
