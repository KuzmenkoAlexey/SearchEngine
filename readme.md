# SearchEngine

Данный проект является реализацией поисковой системы по статьям [хабра](https://habr.com).
Любая поисковая система состоит из двух основых этапов:
1. Сбор информации и построение индекса – веб-краулер;
2. Поиск информации в индексе по запросу пользователя – реализовано в виде клиент-серверного
 приложения.

Для запуска понадобится интерпретатор python 3 версии.
Понадобятся библиотеки: Flask, BeautifulSoup и Pickle 

Как ни странно, для того чтобы что-то найти сначала нужно это что-то
проиндексировать (и только в таком порядке). 

## Веб-краулер
Для запуска веб-краулера необходимо выполнить файл Crawler.py в
папке crawler.

Все настройки краулера находятся в settings.py:
* CRAWL_DELAY – задержка между запросами к хабру, по правилам 
сайта должна быть не меньше 10 секунд, иначе есть шанс получить бан, но мы ведь те еще хулиганы;
* MAX_PAGE_COUNTER – количество страниц которые Вы хотите проиндексировать;
* START_PAGE_INDEX – индекс статьи на с которой необходимо начать.

Результатом работы краулера будет файл hashindex.pkl в папке Data, в котором будет хранится индекс с
целью дальнейшего поиска в нем.
 
## Серверная часть 
Для запуска необходимо выполнить файл SearchServer.py в папке searchServer.
Настрой также хранятся в settings.py:
* HOST – ip-адрес, на котором Вы хотите запустить сервер,
по умолчанию localhost
* PORT – номер порта, по умолчанию стоит None – приложение выберет его за Вас

При старте серверной части сначала загрузятся все необходимые модули (словарь, индекс), потом сам сервер.
Когда он будет готов, на экране Вы увидете адрес по которому можно перейти в браузере и начать что-то искать.

## Этапы выполнения
* [первый](https://docs.google.com/document/d/17RWpdan5VpLP9T40lzYhYkF-p3gwDS8X2UEBAjkmXkk/edit?usp=sharing)
* [второй](https://docs.google.com/document/d/1Pa2SAddKFnZkFumCC4Iott09tPMCzzzJ23H8zC6qms8/edit?usp=sharing)
* [третий](https://docs.google.com/document/d/1fsq1YLwKKagtgxK1kFxTZ-qMsssB3UweSZWNapOcXz8/edit?usp=sharing)

Наша замечательная [презентация](https://docs.google.com/presentation/d/1wfJBOFwuTvOzoaR2bKwI6K_WCo9hB137NaOYsuklFFA/edit?usp=sharing)


  




