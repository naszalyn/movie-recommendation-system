# movie-recommendation-system
A szakdolgozatomban egy filmajánló rendszer kialakítása volt a célom.

Ehhez be kellett szereznem adatokat, azokat átalakítani, adatbázisban tárolni. Alapvető funkciókkal láttam el, mint például keresés cím alapján, értékelés leadása/módosítása/törlése, ajánlások megtekintése.

Az adatokat relációs adatbázisban tároltam, a filmadatokat a Cinemagoer segítségével az IMDb oldaláról szereztem be. A felhasználói értékelésekhez a MovieLens adatait használtam.

Az ajánlást mátrixok segítségével valósítottam meg, ezek alapján kerestem hasonlóságokat a filmek közt.

A tesztelés és a felhasználói felület kialakítása érdekében egy egyszerű weboldalt is készítettem.

### Továbbfejlesztési lehetőségek
Ajánlómotor:
- a kapott ajánlásokra milyen visszajelzések érkeztek &#8594; hatékonyság növelése

Weboldal:
- keresési, szűrési lehetőségek hozzáadása (jelenleg csak cím alapján lehet megtalálni a filmeket)
- személyek adatlapjai, filmeknél a szerepek feltüntetése a színészek mellett
- felhasználói fórumok kialakítása

### Források

Cinemagoer: https://cinemagoer.github.io/

MovieLens értékelések: https://grouplens.org/datasets/movielens/latest/
