#!/bin/bash

cd `dirname $0`
settingsFile=~/.openMovieOnDreambox.conf

if [ -e $settingsFile ]; then
  source $settingsFile
else
  echo """dreamboxHost=dm8000
dreamboxMoviePath=/mnt/diskstation/Spielfilme
  """ >$settingsFile
  echo "Configuration file \"$settingsFile\" created."
  echo "Check the configuration and start openMoveOnDreambox.sh again."
  exit 5
fi

movie=$1

if [[ "$movie" == "" ]]; then
  movie=`kdialog --inputbox "Filmname"` || exit 1
  #movie="Inside Man"
fi

movieDir=`ssh $dreamboxHost "ls \"$dreamboxMoviePath\" | grep -i \"$movie\" -m 1"` || exit 2

if [[ "$movieDir" == "" ]]; then
  kdialog --error "Film nicht gefunden"
  exit 1
fi

kdialog --passivepopup "Found $movieDir"

movieTs=`ssh $dreamboxHost "ls \"$dreamboxMoviePath/$movieDir\" | grep -i \"$movie\" | grep .ts -m 1"` || exit 3

if [[ "$movieTs" == "" ]]; then
  kdialog --error "ts-Datei nicht gefunden"
  exit 1
fi

fullMoviePath="$dreamboxMoviePath/$movieDir/$movieTs"

echo $fullMoviePath

curl -F "sRef=1:0:0:0:0:0:0:0:0:0:$fullMoviePath" "http://dm8000/web/zap"
