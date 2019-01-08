# source daily.sh
source $FUNCIONARIOS_ENV
cd $PROJECT_DIR
cd funcionarios_tribunal_de_cuentas_provincia

echo "DETECTANDO CAMBIOS"
python3 detect-changes.py > post-process/chg.txt

HOY=`date +%Y-%m-%d`
DEST="post-process/data/${HOY}.csv"

git add $DEST
git commit -am 'update datos tribunal de cuentas provincia'
git push

CHANGES="post-process/chg.txt"
tail -30 $CHANGES
