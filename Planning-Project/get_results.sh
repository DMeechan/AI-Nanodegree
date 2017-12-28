echo '=> Getting results:'
echo '=>   Running P1 Uninformed'
python run_search.py -p 1 -s 1 3 5 7 >> results/uninformed_p1.txt
echo '=>   Running P2 Uninformed'
python run_search.py -p 2 -s 1 3 5 7 >> results/uninformed_p2.txt
echo '=>   Running P3 Uninformed'
python run_search.py -p 3 -s 1 3 5 7 >> results/uninformed_p3.txt
echo '=>   Running P1 Informed'
python run_search.py -p 1 -s 8 9 10 >> results/informed_p1.txt
echo '=>   Running P2 Informed'
python run_search.py -p 2 -s 8 9 10 >> results/informed_p2.txt
echo '=>   Running P3 Informed'
python run_search.py -p 3 -s 8 9 10 >> results/informed_p3.txt
echo '=> Complete!'