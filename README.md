# pra1_tipologia
Pràctica 1 de l'assignatura Tipologia i Cicle de vida de les dades

Autors: Pau Bernabé i Sergi Crespi

Enllaç a l'arxiu a Zenodo: https://zenodo.org/record/7832930#.ZDupRC9j5qs

## Arxius presents al repositori


- steam_scraper.py: codi principal de l'scraper, on es duen a terme la gran majoria d'accions
- textUtils.py: codi accessori per a tractar alguns camps una vegada s'han extret
- item.py: format de l'Item, camps extrets en el web scraping.
- requirements.txt: Llistat dels mòduls de Python necessaris per executar el codi
- Directori */dataset*: conté el fitxer de sortida del scraper amb totes les dades recollides
- Memòria de la pràctica amb el nom d'arxiu pauconstans_screspia_PRA1.pdf

## Execució del crawler

Per tal d'executar el crawler, cal situar-se al directori */source* del projecte i executar la següent comanda:
```python
scrapy runspider steam_scraper.py
```
