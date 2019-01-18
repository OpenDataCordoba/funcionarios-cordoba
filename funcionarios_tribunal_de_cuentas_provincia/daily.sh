echo "*******************************************************+"
echo "Cargando el entorno '$FUNCIONARIOS_ENV'"
source $FUNCIONARIOS_ENV

echo "*******************************************************+"
echo "Ingresando al directorio de trabajo '$PROJECT_DIR'"
cd $PROJECT_DIR
cd funcionarios_tribunal_de_cuentas_provincia

echo "Borrando logs"
rm all.log

echo "BUSCANDO NUEVOS DATOS"
python -m funcionarios_tribunal_de_cuentas_provincia.main

echo "DETECTANDO CAMBIOS"
python3 detect-changes.py > post-process/chg.txt

HOY=`date +%Y-%m-%d`
DEST="post-process/data/${HOY}.csv"

git add $DEST
git commit -am 'update datos tribunal de cuentas provincia'
git push

CHANGES="post-process/chg.txt"
tail -30 $CHANGES
