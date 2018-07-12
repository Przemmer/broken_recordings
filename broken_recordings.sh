#!/bin/bash

echo
echo "Method 1 (gradient log):"
echo
for f in *.wav; do 
    python broken_recordings.py ${f} method_1; 
done;
echo
echo
echo "Method 2 (sudden change):"
echo
for f in *.wav; do 
    python broken_recordings.py ${f} method_2; 
done;
echo