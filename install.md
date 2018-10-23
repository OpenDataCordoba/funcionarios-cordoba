## Instalación

```
python3 -m venv /path/to/ven
source /path/to/ven/bin/activate

pip install -r requirements.txt

# si no lo creaste
# scrapy startproject funcionarios_prov_cba

cd funcionarios_prov_cba/
scrapy crawl funcionarios -o post-process/data/funcionarios-2018-NN-NN.csv -t csv

# o con logs
scrapy crawl funcionarios -o post-process/data/funcionarios-2018-09-21.csv -t csv --logfile all.log --loglevel INFO

```