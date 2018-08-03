run:
	cd client && yarn start &
	cd server && export FLASK_APP=server.py && flask run &
