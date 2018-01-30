#!/bin/bash

rm -rf ./MOLs/ ./CMLs/
/usr/bin/python C6H6.py
mkdir MOLs
cd MOLs
for i in $(ls -1 ../CMLs | grep cml)
do
  obabel -icml ../CMLs/$i -omol -O ./${i%.*}.mol -h
  echo -en "\e[2A"
  echo -e "\e[0K\r $i"
done
echo ""
echo "Removing copies"
cd ..
/usr/bin/python remove_copies.py > final_molecules.smiles
echo "Rendering..."
rm -rf render/
mkdir render
mv final_molecules.smiles ./render/
cd render

echo "Got $(wc -l < final_molecules.smiles) different molecules"
echo ""
echo ""
split -d -l 20 final_molecules.smiles
for i in $(ls -1 | grep "x")
do
  echo -en "\e[2A"
  echo "Rendering page #$i"
  obabel -ismiles $i -opng -O $i.png -xw 2481 -xh 3510 -xr 5 -xc 4 -xs -h
done
echo "Converting to PDF, it might take some time..."
convert x*.png molecules.pdf
mv molecules.pdf ..
echo "Done."
