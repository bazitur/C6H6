from __future__ import division, print_function
from math import ceil
from itertools import product
from tqdm import tqdm
import lxml.etree
import lxml.builder
from random import random
import os


def graph6_to_bytestring(graph6_string):
    if graph6_string.startswith(">>graph6<<:"):
        graph6_string = graph6_string[11:]
    if len(graph6_string) == 0:
        raise ValueError("Empty graph!")
    graph6_bytes = [ord(char) for char in graph6_string]
    graph_length, matrice_bytes = graph6_bytes[0], graph6_bytes[1:]
    assert graph_length < 126, "Graphs with n > 63 are not supported yet"
    graph_length -= 63
    for i in range(len(matrice_bytes)):
        matrice_bytes[i] -= 63
    n_bits = (graph_length * (graph_length - 1)) // 2
    matrice_bytes[-1] //= 2 ** (6 * int(ceil(n_bits/6)) - n_bits)
    matrice_str = "".join("{:0>6b}".format(b) for b in matrice_bytes[:-1]) + \
        "{:0>{amount}b}".format(matrice_bytes[-1], amount=n_bits - 6 * (n_bits // 6))
    return matrice_str


def _s(p, *idx):
    return sum(p[i] for i in idx)


def weight_graphs(graph_bytestrings):
    ans = []
    for d in tqdm(graph_bytestrings):
        total = 3 ** len(tuple(filter(lambda x: x == "1", d)))
        for p in tqdm(product(*[(range(1) if char == "0" else range(1, 4)) for char in d]), total=total):
            if sum(p) == 9:                          # TODO: rewrite below
                if all(map(lambda x: 1 < x < 5, (    # doing some magic w/ matrix (counting Hs)
                    _s(p, 0, 1, 3, 6, 10),
                    _s(p, 0, 2, 4, 7, 11),
                    _s(p, 1, 2, 5, 8, 12),
                    _s(p, 3, 4, 5, 9, 13),
                    _s(p, 6, 7, 8, 9, 14),
                    _s(p, 10, 11, 12, 13, 14)
                ))):
                    ans.append(p)
    return ans


def graph_vector_to_edge_list(v):
    result = [
        (0, 1, v[0]),
        (0, 2, v[1]),
        (0, 3, v[3]),
        (0, 4, v[6]),
        (0, 5, v[10]),
        (1, 2, v[2]),
        (1, 3, v[4]),
        (1, 4, v[7]),
        (1, 5, v[11]),
        (2, 3, v[5]),
        (2, 4, v[8]),
        (2, 5, v[12]),
        (3, 4, v[9]),
        (3, 5, v[13]),
        (4, 5, v[14])
    ]
    return tuple(filter(lambda x: x[2] > 0, result))


def bytestring_to_CML(graph_tuples):
    E = lxml.builder.ElementMaker()
    MOLECULE = E.molecule
    ATOM_ARRAY = E.atomArray
    BOND_ARRAY = E.bondArray
    ATOM = E.atom
    BOND = E.bond

    for idx, molecule in enumerate(graph_tuples):
        doc = MOLECULE(
            ATOM_ARRAY(
                *[ATOM(
                    id="a{}".format(i),
                    elementType="C",
                    x3=str(0 + 15 * (random() - 0.5)),
                    y3=str(-0 + 15 * (random() - 0.5)),
                    z3=str(0 + 15 * (random() - 0.5))
                ) for i in range(1, 7)]
            ),
            BOND_ARRAY(
                *[BOND(
                    atomRefs2="a{} a{}".format(a1 + 1, a2 + 1),
                    order=str(w)
                ) for a1, a2, w in graph_vector_to_edge_list(molecule)]
            )
        )
        yield lxml.etree.tostring(doc, pretty_print=True).decode()


def bytestring_to_MOL(graph_tuples):
    # TODO: make straightforward translation from tuple to CML
    raise NotImplemented


def main():
    # load Geng's output
    with open("all_connected_maxord4.g6", "r") as input_file:
        raw_data = tuple(filter(bool, input_file.read().split("\n")))
    byted_strings = [graph6_to_bytestring(i) for i in raw_data]
    print("There are {} initial graphs without weights".format(len(byted_strings)))
    weighted_graphs = weight_graphs(byted_strings)
    print("\nGot {} weighted graphs\n".format(len(weighted_graphs)))

    if not os.path.isdir("./CMLs/"):
        os.mkdir("./CMLs")
    for idx, CML_representation in enumerate(bytestring_to_CML(weighted_graphs)):
        with open("CMLs/{0:0>3}.cml".format(idx), "w") as out_file:
            out_file.write(CML_representation)


if __name__ == "__main__":
    main()
