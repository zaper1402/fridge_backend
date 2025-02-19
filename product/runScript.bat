@echo off
echo Activating virtual environment...
call ..\venv\Scripts\activate

echo Running database population script...
python manage.py shell -c "from product.scripts import populate_db; populate_db()"

echo Script execution completed.
pause