
# delete toontown.apworld 
rm -f toontown.apworld
# delete toontown.zip
rm -f toontown.zip
# archive up the toontown folder with tar with unix equivalent of tar -a -c -f toontown.zip toontown
tar -acf toontown.zip toontown
# rename toontown.zip to toontown.apworld
mv toontown.zip toontown.apworld
