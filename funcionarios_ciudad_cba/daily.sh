#!/usr/bin/env bash
echo "*******************************************************+"
echo "Cargando el entorno '$FUNCIONARIOS_ENV'"
source $FUNCIONARIOS_ENV

echo "*******************************************************+"
echo "Ingresando al directorio de trabajo '$PROJECT_DIR'"
cd $PROJECT_DIR

cd funcionarios_ciudad_cba

echo "Borrando logs"
rm all.log

echo "BUSCANDO NUEVOS DATOS"
python -m funcionarios_ciudad_cba.main

echo "DETECTANDO CAMBIOS $DEST"
cd post_process
python detect-changes.py > chg.txt

HOY=`date +%Y-%m-%d`
DEST="data/${HOY}.csv"

git add $DEST
git commit -am 'update datos ciudad de Córdoba'
git push

CHANGES="chg.txt"
tail -30 $CHANGES
