#!/bin/sh

echo "" > log.txt
echo "" > brief_results.txt
for dir in ./tests/parser/*; do
    rm -rf ./input.txt ./parse_tree.txt ./syntax_errors.txt
    cp "${dir}/input.txt" ./input.txt
    python3 ./compiler.py
    printf "\n\n\n\n=====================================>>>>> Running Test ${dir}...\n" >> log.txt
    printf "\n\n=====================================>>>>> Running Test ${dir}...\n" >> brief_results.txt
    printf "\n\n              *** syntax_errors.txt diffrences ***\n" >> log.txt
    diff -s -y -B -W 250 -w ./syntax_errors.txt "${dir}/syntax_errors.txt" >> log.txt
    diff -y -B -W 250 -w -q ./syntax_errors.txt "${dir}/syntax_errors.txt" >> brief_results.txt
    printf "\n\n              *** parse_tree.txt diffrences ***\n" >> log.txt
    diff -s -y -B -W 250 -w ./parse_tree.txt "${dir}/parse_tree.txt" >> log.txt
    diff -y -B -W 250 -w -q ./parse_tree.txt "${dir}/parse_tree.txt" >> brief_results.txt

done
cat ./brief_results.txt
rm -rf *.txt


