# yW2OO (yWriter-zu-LibreOffice-Konvertierer)

Einen Roman aus [yWriter 6](http://www.spacejock.com/yWriter6.html) oder [yWriter 7](http://www.spacejock.com/yWriter7.html) in eine OpenDocument-Textdatei 
exportieren.

![Screenshot: Automatisch erzeugtes ODT](https://raw.githubusercontent.com/peter88213/yW2OO/master/docs/Screenshots/Writer-de.png)

Mehr Informationen finden Sie im [Wiki (deutsch)](https://github.com/peter88213/yW2OO/wiki/Deutsch). 



## Voraussetzungen

* Windows.

* yWriter 6 oder 7.

* Eine reguläre LibreOffice 5 oder 6-Installation (nicht "portable").



## Download

Die yW2OO Software kommt als ZIP-Archiv `yW2OO_Versionsnummer.zip`. 

[Download-Seite](https://github.com/peter88213/yW2OO/releases/latest)



## yW2OO installieren

1. Falls Sie bereits eine frühere Version von yW2OO installiert haben, führen Sie bitte das
   Deinstallationsprogramm dafür aus. 

2. Entpacken Sie das Archiv `yW2OO_<Versionsnummer>.zip` irgendwo in Ihrem Benutzerbereich.  

3. Öffnen Sie den Ordner `yW2OO_<Versionsnummer>` und führen Sie `Install.bat` aus (Doppelklick).
   Dadurch werden alle Programmdateien an den richtigen Ort kopiert. 
   Möglicherweise werden Sie  um Erlaubnis gebeten, die Windows-Registry zu ändern. 
   Bitte stimmen Sie zu, um für yWriter7-Dateien einen Explorer-Kontextmenüeintrag 
   "Export to LibreOffice" zu installieren.

4. __Optional:__  Laden Sie die Schriftart [Courier Prime](https://quoteunquoteapps.com/courierprime) herunter und installieren sie sie.



## yW2OO benutzen

1. Verfassen Sie Ihren Roman mit yWriter. Bitte beachten Sie die folgenden Konventionen:
   * Textauszeichung: Fettschrift (Bold) und Kursivschrift (Italics) werden unterstützt. Andere Hervorhebungen wie Unterstreichung (Underline) und Durchstreichung (Strikethrough) gehen verloren. 
   * Kapitel und Szenen, die als "Unused" (U) markiert sind, werden nicht exportiert.
   * Kapitel, die mit "Other" (I) markiert sind, werden nicht exportiert.
   * Wenn `This chapter begins a new section` in _Chapter/Details_ ausgewählt ist, ist die Überschrift auf der ersten Ebene. Andernfalls ist sie auf der zweiten Ebene.
   * Wenn `Suppress chapter title when exporting` in _Chapter/Details_ ausgewählt ist, entfernt yW2OO "Chapter" aus den automatisch nummerierten Kapitelüberschriften. Die Nummern bleiben erhalten, ebenso die anderen Kapitelüberschriften.
   * Wenn `Append to previous scene` in _Szene/Exporting_ ausgewählt ist, wird weder eine leere Zeile noch ein Szenentrenner zwischen den Szenen eingefügt. Andernfalls werden drei Sternchen eingefügt (Stil: Überschrift 4). 

   Machen Sie ein Backup des gesamten Projekts und schließen sie yWriter. 

2. Öffnen Sie den Ordner Ihres yWriter-Projekts und machen Sie einen Rechtsklick auf die .yw6 oder
   .yw7-Projektdatei. Im Kontextmenü wählen Sie `Export to LibreOffice`.

![Screenshot: Windows Explorer Kontextmenu](https://raw.githubusercontent.com/peter88213/yW2OO/master/docs/Screenshots/yw2oo_cm.png)

3. Wenn alles klappt, sehen Sie jetzt eine OpenDocument-Datei `<Ihr yWriter Projekt>.odt`. Zum Bearbeiten doppelklicken.

4. Bringen Sie Ihr Manuskript mit Hilfe von [OOTyW](https://github.com/peter88213/OOTyW/wiki/Deutsch) typographisch auf Vordermann.



## yW2OO deinstallieren

1. Öffnen Sie den Ordner `yW2OO_<Versionsnummer>` und führen Sie `Uninstall.bat` aus 
  (Doppelklick). Möglicherweise werden Sie  um Erlaubnis gebeten, die Windows-Registry zu ändern. 
  Bitte stimmen Sie zu, um den Explorer-Kontextmenüeintrag zu entfernen.

