# yW2OO (yWriter-zu-OpenOffice/LibreOffice-Konvertierer)

HTML-Exportdatei von [yWriter](http://www.spacejock.com/yWriter5.html) in eine saubere OpenDocument-Textdatei umwandeln, um Dokument- und Formatvorlagen anwenden zu können.

![Screenshot: Automatisch erzeugtes ODT](https://raw.githubusercontent.com/peter88213/yW2OO/master/docs/Screenshots/Writer-de.png)

Mehr Informationen finden Sie im [Wiki (deutsch)](https://github.com/peter88213/yW2OO/wiki/Deutsch). 

## Download

Die yW2OO Software kommt als ZIP-Archiv `yW2OO_Versionsnummer.zip`. 

[Download-Seite](https://github.com/peter88213/yW2OO/releases)

## yW2OO installieren

1. Entpacken Sie das Archiv `yW2OO_<Versionsnummer>.zip` irgendwo in Ihrem Benutzerbereich.  

2. Öffnen Sie den Ordner `yW2OO_<Versionsnummer>` und führen Sie `Install.bat` aus (Doppelklick). Dadurch werden alle Programmdateien an den richtigen Ort kopiert und es wird die Office-Erweiterung installiert.

3. __Optional:__ Öffnen Sie den Ordner `yW2OO_<Versionsnummer>\template\StandardPages_<gewünschtes Papierformat>` und führen Sie `Install.bat` aus (Doppelklick), um die mitgelieferte Normseiten-Vorlage zu installieren.

4. __Optional:__ Öffnen Sie den Ordner `yW2OO_<Versionsnummer>\fonts` und entpacken Sie das Archiv `CourierPrime.zip`. Installieren Sie die `.ttf`-Dateien (Rechtsklick -> Installieren).


## yW2OO benutzen

1. Verfassen Sie Ihren Roman mit yWriter. Schauen Sie nach, ob der Ordner `<Ihr yWriter Projekt>\Export` eine Datei namens `writer.bat` enthält. Falls nicht, kopieren Sie sie von `yW2OO_<Versionsnummer>\setup` hierher.

2. __Optional:__ Lassen Sie yWriter die Szenenbeschreibungen an den vorgeschlagenen Ort exportieren, wenn Sie die Szenentitel als navigierbare Kommentare haben wollen. Befehl: __Project > Export Project > Scene descriptions__.

3. Lassen Sie yWriter Ihr Projekt als `<Ihr yWriter Projekt>\Export\Exported Project.html` exportieren. Befehl: __Project > Export Project > to html__.

4. Das Browserfenster, das "Exported Project.html" anzeigt, können Sie schließen.

5. Öffnen Sie den Ordner `<Ihr yWriter Projekt>\Export` und führen Sie `writer.bat` aus (Doppelklick). Wenn alles klappt, wird OpenOffice/LibreOffice Writer automatisch starten und das Dokument im OpenDocument-Format als "Exported Project.odt" mit hierarchischer Struktur und mit den richtigen Absatz-/Zeichenvorlagen anzeigen.

6. Bringen Sie Ihr Manuskript mit Hilfe von [OOTyW](https://github.com/peter88213/OOTyW/wiki/Deutsch) typographisch auf Vordermann.

## yW2OO deinstallieren

1. Öffnen Sie den Ordner `yW2OO_<Versionsnummer>` und führen Sie `Uninstall.bat` aus (Doppelklick).

