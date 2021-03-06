from __future__ import print_function
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
from glob import glob

filenames = sorted(glob("./MOLs/*"))

canonical_SMILES = [Chem.MolToSmiles(Chem.MolFromMolFile(fn)) for fn in filenames]

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# sort canonical SMILES by similarity
print("\n".join(f7(canonical_SMILES)), end="")
import sys
sys.exit()
canonical_SMILES = sorted(set(canonical_SMILES))   # remove duplicates
N = len(canonical_SMILES)
matrice = [[0 for __ in range(N)] for _ in range(N)]
fingerprints = [
    FingerprintMols.FingerprintMol(Chem.MolFromSmiles(s)) for s in canonical_SMILES
]
for i in range(N):
    for j in range(N):
        if i == j:
            matrice[i][j] = -1
        else:
            matrice[i][j] = DataStructs.FingerprintSimilarity(
                fingerprints[i],
                fingerprints[j]
            )

result = []
current = N - 1     # start with a last one, for no reason
for i in range(N):
    result.append(canonical_SMILES[current])
    next_index = matrice[current].index(max(matrice[current]))
    for j in range(N):
        matrice[j][current] = -1
    current = next_index

print("\n".join(result), end="")
