# Small experiment: generate all C<sub>6</sub>H<sub>6</sub> structural isomers.
## Requirements
> Please note that this project uses Python 2!

1. Install required packages via apt:
```bash
$ sudo apt-get install python-rdkit librdkit1 rdkit-data openbabel
```
2. Install requirements from Pipfile (via Pipenv preferably) into virtual environment:
```bash
$ pipenv --two && pipenv shell   # or pip install -r requirements.txt
```

## Current Workflow
1. Generate all matching graphs with [Nauty](http://pallini.di.uniroma1.it/)'s `geng` (sample file for C<sub>6</sub>H<sub>6</sub> case is already there):
```bash
# -c for connected, -q for quiet, -D4 is for 4 Carbon's maximum valence of 4
$ geng -c -D4 -q 6 > all_connected_maxord4.g6
```
2. Run `compose.sh`:
```bash
$ sh compose.sh
```
3. The program outputs to `molecules.pdf`

## Results

## TODO
 - [ ] generalize the program for C<sub>x</sub>H<sub>y</sub> case
 - [x] join all subprograms into a single bash script

## License
This project is distributed under BSD 3-clause license. See LICENSE.md for the full license.