/*A feldarabolt ratings (értékelések) fájl beolvasása. Összesen 28 fájl (ratings_1...._28.csv).*/
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ratings_1.csv' 
INTO TABLE ratings 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n';