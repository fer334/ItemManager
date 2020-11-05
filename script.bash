#!/bin/bash

Help(){
     # Display Help
     echo "Script that initializes the project and the postgres database."
     echo
     echo "Usage: script [OPTIONS]"
     echo "Options:"
     echo "-D --dbname        Specify the postgres DB name"
     echo "-U --username      Specify the postgres username"
     echo "-P --dbpass        Specify the postgres password"
     echo "--port --dbport    Specify the postgres port"
     echo "-F --backupfile    File to use for initialize the DB"
     echo "-c --gitclone      Specify if it will be used the command git clone"
     echo "-p --production    Specify if is going to run in production mode"
     echo "-d --dev           Specify if is going to run in developer mode"
     echo "-h --help          Show this output and exit"
     echo "-b --branch        This is the heroku branch to use on pushing into heroku"
     exit
}

PrintDefault(){
    echo 'dbname=>"itemmanagerdb"'
    echo 'username=>"postgres"'
    echo 'pass=>"postgres"'
    echo 'filename=>"poblacion_bd.sql"'
    echo 'port=>"5432"'
    echo 'gitclone=>"false"'
    echo 'prod=>"false"'
    echo 'dev=>"false"'
    echo 'branch=>"master"'
    exit;
}

POSITIONAL=()
dbname="dbdesarrollo"
username="postgres"
pass="postgres"
filename="dbdesarrollo_bk.sql"
port="5432"
gitclone="false"
prod="false"
dev="false"
branch="master"
tag="master"

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
	-D|--dbname)
	    dbname="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-U|--username)
	    username="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-P|--dbpass)
	    pass="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-F|--backupfile)
	    filename="$2"
	    shift # past argument
	    shift # past value
	    ;;
	--port|--dbport)
	    port="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-c|--gitclone)
	    gitclone=true
	    shift # past argument
	    ;;
	-p|--produc|--produccion|--pro|--production)
	    prod=true
	    shift # past argument
	    ;;
	-d|--dev|--developer|--desarrollo)
	    dev=true
	    shift # past argument
	    ;;
	-h|--help|--ayuda)
	    Help; exit;
	    ;;
	-b|--branch)
	    branch="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-t|--tag)
	    tag="$2"
	    shift # past argument
	    shift # past value
	    ;;
	--default)
	    PrintDefault; exit;
	    ;;
	*)    # unknown option
	    POSITIONAL+=("$1") # save it in an array for later
	    shift # past argument
	    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


if [[ $prod == "true" ]]; then
    ./produccion.bash $branch $filename $tag $gitclone
elif [[ $dev == "true" ]]; then
    ./desarrollo.bash $dbname $username $pass $filename $port $gitclone
else
      echo "You need to specify the mode Developer or Production"
      Help
fi