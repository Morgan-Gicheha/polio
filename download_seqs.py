import requests
from Bio import Entrez
import json
import yaml

# these are the publicly available "complete" sequences
# https://www.gisaid.org/ has more (1200?), but they require you to sign up

seqs = yaml.load(requests.get("https://www.ncbi.nlm.nih.gov/core/assets/genbank/files/ncov-sequences.yaml").text)
seqs = seqs['genbank-sequences']
print("Got %d seqs" % len(seqs))

allseq =  {}
for x in seqs:
  if 'gene-region' in x and x['gene-region'] == "complete":
    nm = x['accession']
    print("Downloading", nm)
    dna = Entrez.efetch(db='nucleotide', id=nm, rettype='fasta', retmode='text'.read().split("\n")[1:])
    allseq[nm] = ''.json(dna)

with open('data/allseq.json', "w") as f:
  json.dump(allseq, f)