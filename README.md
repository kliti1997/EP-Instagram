# EP-Instagram-1
## Kurzbeschreibung

Das Python-Modul `instagram` speichert Instagram-Benutzerseiten als HTML-Dateien ab und stellt Änderungen zu Vorgängerversionen grafisch dar.

Es werden pro Instagram-Profil und pro Kategorie (Posts, IGTV, Markiert) maximal 2 Versionen gespeichert. Es werden keine keine Bilder oder Videos gespeichert, sondern lediglich der statische Seitenquelltext.
# Developer Guide

## Schnittstelle

Das Hauptmodul `Instagram` wird über `instagram.src.instagram` erreicht. Bei dem Aufruf wird eine Liste defaultdict(list) mit den URLs übergeben.

Eine URL wie wie folgt definiert:
```python
url = {
    "id": "user_id",
    "href": "https://www.instagram.com/user_id",            # ggf. /user_id/channel *oder* /user_id/tagged
    "type": "posts" *oder* "igtv" *oder* "tagged",
    "mode": "1" *oder* "2",                                 # mode 1: change == notify *oder* mode 2: Likes und Views setzen notify nicht auf True
    "monitoring_folder": "ulferdowoff/tagged/",             # Pfad der html Dateien, wird kombiniert mit dem Pfad aus den Einstellungen
    "change": "", "notify": "", "err": ""                   # Rückgabewerte
}
```

## Rückgabewerte

Mögliche Veränderungen auf einer Instagram Seite: {Abonnenten, Abonnierte, Likes, Views, Kommentare, Stories, Beiträge (posts*oder* igtv *oder* tagged)}

*change:*   Wird bei jeder Veränderung zwischen der old.html und new.html auf True gesetzt, ansonsten False.
*notify:*   mode 1: Immer True, falls change True ist, ansonten False.
            mode 2: Identisch zu mode 1 außer, dass folgende Änderungen: {Likes, Views, Abonnenten, Abonnierte} ignoriert werden.
*err:*      Wird auf True gesetzt, falls ein Fehler bei der Verarbeitung auftritt, sonst False.

## Einstellungen

Die Einstellungen werden in instagram/data/config.py gespeichert.
Wichtige Variablen sind dabei:

*ig_credentials:*       Zugangsdaten für den Instagram Account, der zum Aufrufen der Seiten benutzt wird.
*monitoring_folder:*    Setzt in Kombination mit dem monitoring_folder der jeweiligen URL den Pfad, wo die html Dateien gespeichert werden.
*profile_folder:*       Pfad zu dem Firefox-Profil.

## Datenquellen
Die Daten zum Vergleich kommen aus zwei Quellen, die über die Klasse ProfileData (profile_data.py) zusammengetragen werden:
 * Zum Zeitpunkt des Seitenaufrufs wird lokal ein JSON-Objekt 'window._sharedData' angelegt, die neben Informationen zu Profilbild, Anzahl Follower etc. auch die Informationen zu den ersten 12 Posts / IGTV's beinhaltet.
 * Anschließend (und im Fall von der Kategorie 'Markiert' von Beginn an) werden weitere Daten via Requests von Instagram angefragt. Diese Requests können wir (zusammen mit den Antworten) mit dem Package 'selenium-wire' auslesen und so auch Daten zum 13.-24. Post hinterlegen.
 
 Die später benötigten Daten werden mit Hilfe von data-Tags in die HTML geschrieben (_'add_html_tags'_, download_methods.py).
  
## Download-Phase
In der Download-Phase (instagram_store.py) werden alle benötigten Informationen (DOM, Inhalt von 'window._sharedData', Requests) abgerufen.
Anschließend werden mit Hilfe der ProfileData- und InstagramObject-Klassen die extrahierten Daten im DOM hinterlegt.
Der fertige DOM wird abschließend in eine '_new.html_' geschrieben. Sollte diese schon existieren, wird sie zu '_old.html_' umbenannt und eine neue '_new.html_' wird angelegt ('_pre_download_', download_methods.py).   
Es werden zusätzlich in der Download-Phase alle relativen Links zu absoluten Links umgewandelt und Video Thumbnails mit einem Standard Thumbnail ersetzt, da die Video Thumbnails nur für 24 Stunden gültig sind.


## Monitoring/Modify-Phase
In der Monitoring- bzw Modify-Phase werden die zuvor erstellten HTML-Dateien miteinenander verglichen und änderungen entsprechend der Vorgaben grafisch dargestellt.  
Hierzu wird häufig auf die InstagramObject-Klasse zurückgegriffen, über die in den HTML-Dateien navigiert werden kann.