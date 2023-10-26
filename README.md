# Bachelorarbeit

Dieses Repo enthält sämtlichen Code, den ich im Rahmen meiner Bachelorarbeit geschrieben habe.

## Gitterspektrometer -> gridspec.py

Im Code müssen die korrekten COM/Serial Ports für die Messgeräte eingetragen sein! Dazu in den Geräteeinstellungen des PCs nachschauen.


Bedienung:
- in Konsole python ausführen (mit 'python' oder 'python3') -> muss im Pfad passieren, in dem das Programm liegt!
- Programm importieren mit ('from gridspec import GridSpec)
- Instanz der Klasse erstellen über 'a = GridSpec()' (Bennenung 'a' ist beliebig)
- Messen mit 'a.measure()'
    - übergebe sv=False, falls länger als die Standardzeit im Detektor gemessen werden soll (Messwerte akkumulieren)
    - Programm für Nutzer durch Anwendung
- Gitterspektrometer steuern mit 'a.goto(<Wellenlänge in nm>)' zum Einstellen einer Wellenlänge und 'a.get()' um WL auszulesen
- Photosensor Output-Stream mit a.loop()
 
