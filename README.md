"# Blog parser" 
Parser uses multiprocessing, proxy and changeable User-Agent header.

PostgreSQL Tables:
'Config', 'Parser'

'Config' columns: 
str column url = 'https://bikepost.ru/index/'
str column author_name
int column number_of_processes
int column task = 1 - 'is search for author posts throughout the site'/ task = 2 - 'search for new posts by the author'

'Parser' columns:
str columns author_name, post_name, post_date
