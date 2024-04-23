#!bin/bash
DJANGO_FOLDER=${DJANGO_FOLDER:-'jalodei'}
echo $DJANGO_FOLDER
source .env
PROD=${PRODUCTION:-0}

if [[ $PROD == 0 ]] ; then
	cd $DJANGO_FOLDER
fi;

if [ $# -eq 0 ]
then
	echo -e "\nIniciando servidor..."
	python manage.py runserver 0.0.0.0:8000
        exit 0
fi

while [ $# -gt 0 ] ; do
    case $1 in
	-i | --install)
	    echo -e "\nInstalando requerimientos..."
	    # pipenv sync
		# pipenv sync --dev
		cd ..
		pip install -r requirements.txt
	    exit 0
	    ;;

	-c | --cleandb)
		if [[ $PROD > 0 ]] ; then
			python manage.py collectstatic --noinput

			echo $GOOGLE_JSON > jalodei/jalodei-efdccda46100.json
			if [[ $DELETE_DB == true ]] ; then

				find . -type f -path '*migrations*/*' -name '*.py' \
					! -name '__init__.py' -delete
				find . -type f -path '*migrations*/*' -name '*.pyc' -delete

				echo "DELETING PSQL DB"
				python drop_db.py;
			fi;
		else
			if [[ $DELETE_DB == true ]] ; then
				find . -type f -path '*migrations*/*' -name '*.py' \
					! -name '__init__.py' -delete
				find . -type f -path '*migrations*/*' -name '*.pyc' -delete
			fi;

			echo -e "\nBorrando DB sqlite... ";
			rm -v db.sqlite3
		fi;

        echo -e "\nAplicando migraciones al ORM..."
        python manage.py makemigrations
        python manage.py migrate

        echo "Creating $DJANGO_SUPERUSER_USERNAME"
        echo -e "\n Creando dev users"
        python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME \
            --email $DJANGO_SUPERUSER_EMAIL --no-input

		if [[ $BRIAN_USER == 'brian' ]] ; then
		export DJANGO_SUPERUSER_PASSWORD=$BRIAN_PASSWORD
		python manage.py createsuperuser --username $BRIAN_USER \
            --email $DJANGO_SUPERUSER_EMAIL --no-input
		fi;
	    
		python manage.py check

		# echo -e "\n Cargando fixtures"
		# python manage.py shell < fixtures.py

	    exit 0
	    ;;
	-t | --test)
	    echo -e "\nTesting... "
	    cd $NAME
	    python manage.py test
	    exit 0
	    ;;
    esac
    shift
done