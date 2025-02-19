@echo off
echo Activating virtual environment...
call ..\venv\Scripts\activate

echo Running database population script...
python manage.py shell -c "from recipes.scripts import populate_recipes_db; populate_recipes_db()"

echo Script execution completed.
pause