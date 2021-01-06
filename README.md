**Anpassungen:**
Es ist wichtig in der “config.py” die Credentials des Benutzeraccounts sowie die Geckodriver-Version entsprechend anzupassen. Ebenfalls muss auch der Pfad des Video Thumbnails angepasst werden(aktuell noch im “instagram_object.py”).

Dieses Python-Script lädt alle Unterseiten einer Instagram Benutzerseite herunter und überprüft ob es seit der letzten Überprüfung eine Veränderung gab. Je nach Granularität(fein oder grob) werden dabei entweder nur die einzelnen Beiträge und Stories des Benutzers überprüft oder aber auch die Anzahl der Followers, Followings, Likes,Videoaufrufe sowie die Kommentare auf seiner Benutzerseite.
Das Script teilt sich in zwei Phasen auf: Die **Download-Phase** und die **Monitor-Phase**.

In der Download-Phase wird eine neue Version von allen Unterseiten einer Benutzerseite heruntergeladen(Posts, IGTVs, Tagged, …). Es werden maximal zwei Kopien der Seite archiviert(“new.html”, “old.html”). Gibt es keine vorherige Version (das Verzeichnis ist leer), so wird die neu heruntergeladene Version direkt als “new.html” gespeichert. Gibt es bereits eine “new.html” im Verzeichnis, so wird sie in “old.html” umbenannt und die neue heruntergeladene Version als “new.html” gespeichert. Gibt es sowohl eine “old.html” als auch eine “new.html” im Verzeichnis, so wird die “old.html” gelöscht und “new.html” wird in “old.html” umbenannt. Die neue heruntergeladene Version wird als “new.html” gepeichert.

Dynamische Informationen durch z.B. Javascript sammeln wir und speichern sie in der “profile_data.py” geordnet ab, um später darauf zugreifen zu können (z.B. Um zu erkennen ob ein Post ein Video oder Bild ist).

In der “instagram_object.py” speichern wir die Informationen ab, die wir später in der Monitor-Phase brauchen, um Unterschiede zu erkennen. So verhindern wir ein doppeltes Iterien über die .html Dateien. Z.B sind das Followers und Followings Anzahl, aber auch LXML-Objekte, die Posts beinhalten.

Es werden zusätzlich in der Download-Phase alle relativen Links zu absoluten Links umgewandelt und Video Thumbnails mit einem Standard Thumbnail ersetzt, da die Video Thumbnails nur für 24 Stunden gültig sind.

In der Monitor-Phase vergleichen wir jeweils zwei Versionen einer Unterseite oder Story und schauen, wo Unterschiede auftreten. Gibt es Unterschiede, so wird das jeweilige Objekt mit grüner Farbe hervorgehoben.