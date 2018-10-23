source ~/envs/scrapyfunc/bin/activate

echo "Borrando logs"
rm all.log

HOY=`date +%Y-%m-%d`
DEST="post-process/data/funcionarios-${HOY}.csv"

echo "Borrando $DEST"
rm $DEST

echo "Creando $DEST"
scrapy crawl funcionarios -o $DEST -t csv --logfile all.log --loglevel INFO

echo "DETECTANDO CAMBIOS $DEST"
cd post-process
python3 detect-changes.py > chg.txt

cd ..
git add $DEST
git commit -am 'update'
git push

CHANGES="post-process/chg.txt"
tail -30 $CHANGES
