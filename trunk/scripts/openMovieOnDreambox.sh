#!/bin/bash

cd `dirname $0`
settingsFile=~/.openMovieOnDreambox.conf


# load settings
if [ -e $settingsFile ]; then
  source $settingsFile
else
  echo """dreamboxHost=dm8000
dreamboxMoviePath=/mnt/diskstation/Spielfilme
dreamboxMountPath=/mnt/diskstation
  """ >$settingsFile
  echo "Configuration file \"$settingsFile\" created."
  echo "Check the configuration and start openMoveOnDreambox.sh again."
  exit 5
fi


# mount diretory on dreambox
if [[ "$dreamboxMountPath" != "" ]]; then
  ssh $dreamboxHost "mount $dreamboxMountPath"
fi


# get video name via argument or ask user to enter one
movie=$1
if [[ "$movie" == "" ]]; then
  movie=`kdialog --inputbox "Filmname"` || exit 1
  #movie="Inside Man"
fi


# find movie diretory on dreambox
movieDir=`ssh $dreamboxHost "ls \"$dreamboxMoviePath\" | grep -i \"$movie\" -m 1"` || exit 2

if [[ "$movieDir" == "" ]]; then
  kdialog --error "Film nicht gefunden"
  exit 1
fi

kdialog --passivepopup "Found $movieDir"


# find ts file on dreambox
movieTs=`ssh $dreamboxHost "ls \"$dreamboxMoviePath/$movieDir\" | grep -i \"$movie\" | grep .ts -m 1"` || exit 3

if [[ "$movieTs" == "" ]]; then
  kdialog --error "ts-Datei nicht gefunden"
  exit 1
fi

fullMoviePath="$dreamboxMoviePath/$movieDir/$movieTs"
echo $fullMoviePath


# play movie on dreambox
curl -F "sRef=1:0:0:0:0:0:0:0:0:0:$fullMoviePath" "http://dm8000/web/zap"
