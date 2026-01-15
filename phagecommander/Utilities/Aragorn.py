from typing import List
from phagecommander import Gene
from Bio import SeqIO
import pyaragorn

URL = 'http://130.235.244.92/bcgi/aragorn.cgi'

TYPES = {'tRNA', 'tmRNA', 'both'}
SEQ_TOPOS = {'linear', 'circular'}
STRAND_TYPE = {'single', 'both'}


def aragorn_query(file_path: str, rna_type: str = 'tRNA', use_introns: bool = False, seq_topology: str = 'linear',
                  strand: str = 'both') -> List['Gene.TRNA']:
    """
    Calls Aragorn to analyze TRNA sequences in the DNA sequence
    :param file_path: fasta file path
    :param rna_type: {'tRNA', 'tmRNA', 'both'}
    :param use_introns:
    :param seq_topology: {'linear', 'circular'}
    :param strand: {'single', 'both'}
    :return: List[TRNA]
    """
    # check for valid parameters
    if rna_type not in TYPES:
        raise TypeError(f'{rna_type} is not a valid type {TYPES}')

    if use_introns:
        introns = 'yes'
    else:
        introns = 'no'

    if seq_topology not in SEQ_TOPOS:
        raise TypeError(f'{seq_topology} is not a valid sequence topology {SEQ_TOPOS}')

    try:
            record = SeqIO.read(file_path, "fasta")
    except ValueError:
        records = list(SeqIO.parse(file_path, "fasta"))
        if not records:
            raise ValueError("No sequence found in file.")
        record = records[0]

    finder = pyaragorn.RNAFinder(translation_table=11)

    try:
        predictions = finder.find_rna(bytes(record.seq))
    except TypeError:
        predictions = finder.find_rna(str(record.seq))

    filtered_predictions = []
    for rna in predictions:
        if rna_type == 'both':
            filtered_predictions.append(rna)
        elif rna.type == rna_type:
            filtered_predictions.append(rna)
            
    return filtered_predictions


# (GRyde) Updated to include totalLength parameter, original parameter list was aragorn_parse(aragorn_data: str, id=None)
def aragorn_parse(aragorn_data: List, totalLength, id=None):
    genes: List['Gene.TRNA'] = []

    for rna in aragorn_data:
        start = rna.begin
        stop = rna.end
        
        if rna.strand >= 0:
            direction = '+'
        else:
            direction = '-'

        if rna.type == 'tRNA':
            seq_type = f"{rna.type}-{rna.amino_acid}"
            if hasattr(rna, 'anticodon') and rna.anticodon:
                 seq_type += f"({rna.anticodon})"
        else:
            seq_type = rna.type
            if hasattr(rna, 'tag_peptide') and rna.tag_peptide:
                seq_type += f" peptide:{rna.tag_peptide}"

        gene = Gene.TRNA(start, stop, direction, seq_type, totalLength, identity=id)
        genes.append(gene)

    return genes