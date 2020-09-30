#!/bin/bash


POSITIONAL=()
dbname="itemmanagerdb"
username="postgres"
pass="postgres"
filename="poblacion_bd.sql"
port="5432"
gitclone="false"
proc="false"
branch="master"

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
	-d|--dbname)
	    dbname="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-u|--username)
	    username="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-dp|--dbpass)
	    pass="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-bf|--backupfile)
	    filename="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-p|--dbport)
	    port="$2"
	    shift # past argument
	    shift # past value
	    ;;
	-c|--gitclone)
	    gitclone=true
	    shift # past argument
	    ;;
	--produc|--produccion|--pro)
	    proc=true
	    shift # past argument
	    ;;
	-b|--branch)
	    branch="$2"
	    shift # past argument
	    shift # past value
	    ;;
	--default)
	    DEFAULT=YES
	    shift # past argument
	    ;;
	*)    # unknown option
	    POSITIONAL+=("$1") # save it in an array for later
	    shift # past argument
	    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

#echo $dbname
#echo $username
#echo $pass
#echo $filename
#echo $port
#echo $gitclone
#echo $branch

if [[ $proc == "true" ]]; then
    ./produccion.bash $branch $filename
else
    ./desarrollo.bash $dbname $username $pass $filename $port $gitclone
fi

