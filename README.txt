Platform for listening and posting songs

to start, write in terminal(windows):

python -m venv venv
venv/Scripts/activate
pip install Django, psycopg2, Pillow
cd soundline
python manage.py createsuperuser
// go to admin page and log in
python manage.py runserver
