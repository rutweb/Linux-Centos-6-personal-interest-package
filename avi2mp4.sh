ffmpeg -y -sameq -i $1 -acodec libmp3lame -ar 44100 -ab 96k -vcodec libx264 -aspect 16:9 -r 24 -s 426x240 -b 600k -threads 2 -f flv $2
