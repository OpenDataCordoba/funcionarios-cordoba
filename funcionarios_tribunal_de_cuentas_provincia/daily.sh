# source daily.sh

source ~/envs/funcionarios-cordoba/bin/activate

echo "DETECTANDO CAMBIOS"
python3 detect-changes.py > post-process/chg.txt

HOY=`date +%Y-%m-%d`
DEST="post-process/data/${HOY}.csv"

git add $DEST
git commit -am 'update datos tribunal de cuentas provincia'
git push

CHANGES="post-process/chg.txt"
tail -30 $CHANGES
