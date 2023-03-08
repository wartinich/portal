run:
	uvicorn main:app --reload

db:
	python create_db.py
