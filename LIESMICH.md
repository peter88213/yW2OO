# yW2OO (yWriter-zu-LibreOffice-Konvertierer)

Einen Roman aus [yWriter 7](http://www.spacejock.com/yWriter7.html) in eine OpenDocument-Textdatei exportieren.

![Screenshot: Automatisch erzeugtes ODT](https://raw.githubusercontent.com/peter88213/yW2OO/master/docs/Screenshots/Writer-de.png)

Mehr Informationen finden Sie im [Wiki (deutsch)](https://github.com/peter88213/yW2OO/wiki/Deutsch). 

## Voraussetzungen

* Windows.

* yWriter 7.

* Eine reguläre LibreOffice 5 oder 6-Installation (nicht "portable").

## Download

Die yW2OO Software kommt als ZIP-Archiv `yW2OO_Versionsnummer.zip`. 

[Download-Seite](https://github.com/peter88213/yW2OO/releases)

## yW2OO installieren

1. Falls Sie bereits eine frühere Version von yW2OO installiert haben, führen Sie bitte das Deinstallationsprogramm dafür aus. 

2. Entpacken Sie das Archiv `yW2OO_<Versionsnummer>.zip` irgendwo in Ihrem Benutzerbereich.  

3. Öffnen Sie den Ordner `yW2OO_<Versionsnummer>` und führen Sie `Install.bat` aus (Doppelklick). Dadurch werden alle Programmdateien an den richtigen Ort kopiert.

4. __Optional:__ ffnen Sie den Ordner `yW2OO_<Versionsnummer>\fonts` und entpacken Sie das Archiv `CourierPrime.zip`. Installieren Sie die `.ttf`-Dateien (Rechtsklick -> Installieren).


## yW2OO benutzen

1. Verfassen Sie Ihren Roman mit yWriter 7. Schauen Sie nach, ob der Ordner `<Ihr yWriter Projekt>.yw` eine Datei namens `writer.bat` enthält. Falls nicht, kopieren Sie sie von `yW2OO_<Versionsnummer>\setup` hierher.

2. Schließen Sie yWriter und öffnen Sie den Ordner `<Ihr yWriter Projekt>.yw7` und führen Sie `writer.bat` aus (Doppelklick). Wenn alles klappt, wird LibreOffice Writer automatisch starten und das Dokument im OpenDocument-Format als `<Ihr yWriter Projekt>.odt` mit hierarchischer Struktur und mit den richtigen Absatz-/Zeichenvorlagen anzeigen.

3. Bringen Sie Ihr Manuskript mit Hilfe von [OOTyW](https://github.com/peter88213/OOTyW/wiki/Deutsch) typographisch auf Vordermann.

## yW2OO deinstallieren

1. Öffnen Sie den Ordner `yW2OO_<Versionsnummer>` und führen Sie `Uninstall.bat` aus (Doppelklick).

