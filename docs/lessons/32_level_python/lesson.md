# Wasserwaage in Python

## Einleitung

Bisher haben wir den micro:bit immer mit dem Makecode Block Editor programmiert. Man kann den micro:bit aber auch in Python programmieren. Python ist eine moderne Programmiersprache die auf fast allen Computern benutzt werden kann.

Im Gegensatz zu Makecode wird hier das Programm in Form von Text eingegeben. Das ist zwar im ersten Moment komplizierter, bietet dafür aber auch mehr Möglichkeiten.

Wenn du später mit Comptertechnik arbeitest wirst du sicher mit Python in Kontakt kommen. Wir wollen im folgenden die Wasserwaage nochmal in Python programmieren.

Wie die meisten Programmiersprachen liest sich Python auch wie Englisch. Es ist also von Vorteil wenn du schon einige Worte Englisch verstehst.


## Verwendete (neue) Technologien

*   Python Programmiersprache
*   Python Online Editor (Voraussetzung: English)


## Programmierung

### Schritt 1: Das erste Python Program schreiben

Der micro:bit verwendet eine vereinfachte Variante von Python, sie heisst MicroPython. Dies ist eine Version von Python die nicht alle Funktionen anbietet. Dafür passt sie selbst in kleinste Computer.

Es gibt verschiedene Möglichkeiten den micro:bit mit MicroPython zu programmieren. Wir nutzen den offiziellen Online Python Editor des micro:bit Projekts.

*   Oeffne mit dem Browser die [MicroPython Website](https://python-editor-2-0-0-beta-4.microbit.org/#). 
*   Es öffnet sich ein Fenster in wir den Python Code unseres Programms eingeben können.
*   Auch hier wollen wir mit einem einfachen **Hello World** Programm starten. Gib das folgende Program ein.

```
from microbit import *

display.scroll('Hello micro:bit')
```

*   Falls du den Chrome Browser benutzt kannst du deinen micro:bit **verbinden**. Dadurch wird der Download einfacher. Wähle **Connect** im Menü des Editors (hier grün eingerahmt).

![](image1.png)

*   Wähle deinen micro:bit im Fenster das sich öffnet und drücke den **Connect** Knopf.
*   Um das Program auszuführen muss es auf den micro:bit kopiert werden. Wenn du deinen micro:bit verbunden hast, drücke den Button **Flash**. Ansonsten drücke **Download** und speichere die Datei auf dem micro:bit.

Wenn alles geklappt hat siehst du nun einmal den Text ```Hello micro:bit``` auf dem Bildschirm. Danach passiert nichts mehr. Wir wollen das Programm nun so umschreiben, dass der Text immer wieder (endlos) angezeigt wird.

*   Ändere das Program wie unten gezeigt um.

```
from microbit import *
import time

while True:
    display.scroll('Hello micro:bit')
    time.sleep(1)   
```

*   Damit haben wir eine sogenannte Endlosschleife gebaut, die nie endet.
*   Um eine kleine Pause zu machen, nutzen wir die Funktion ```sleep``` aus dem Modul ```time```.
*   Achte darauf dass die Zeilen innerhalb des ```while``` Blocks wie gezeigt eingerückt sind. Python verlangt das so um zu wissen wo die Schleife beginnt, respektive endet.



### Schritt 2: Wasserwaage einfach

Das Python Programm misst den Winkel den der micro:bit zur Erdachse hat. Wenn er 0 ist (exakt gerade) zeigt er ein Pixel in der Mitte des Bildschirms an. Wenn der micro:bit geneigt ist wandert das Pixel nach links oder rechts. Das Pixel entspricht damit der Luftblase einer echten Wasserwaage.

Da das Program nun schon recht kompliziert ist, besprechen wir es zusammen. Die Hauptpunkte sind:
1.  Die Beschleunigung wird in zwei Achsen gemessen und daraus mit der Tangens Funktion der Winkel berechnet (Dreiecksrechnung, Trigonometrie).
1.  Der Winkel wird von der Einheit Radian welche Computer und Mathematiker nutzen (Kreisumfang = 2*Pi) in Grad (Kreisumfang = 360°) umgerechnet.
1.  Der Winkel wird auf +/-2° begrenzt damit er mit den fünf Pixel des micro:bit angezeigt werden kann (-2. -1. 0, +1, +2).
1.  Aus dem Winkel wird die Position des Pixels (0 bis 4) bestimmt. Der ganze Bildschirm wird gelöscht und ein Pixel an der berechneten Position eingeschaltet.
1.  Nach einer kurzen Pause beginnt die Schleife von neuem.

```
from microbit import *
import time
import math

while True:
    # Get acceleration in x and y axis, then compute
    # angle micro:bit has (0 = level).
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    angle = math.atan2(x,y) / math.pi * 180    
    
    # Limits angle to -2 .. +2 degrees
    limit = 2.0
    if angle > limit:
        angle = limit
    elif angle < -limit:
        angle = -limit

    # Show a pixel depending on micro:bit level
    pos = round(2.0 + angle * 1.0)
    display.clear()
    display.set_pixel(int(pos), 2, 9)

    time.sleep_ms(50)
```


### Schritt 2: Wasserwaage mit Kalibrierung

Ziemlich sicher ist das Pixel nicht in der Mitte des Bildschirms, auch wenn dein micro:bit exakt gerade liegt. Das liegt daran, dass der Sensor nicht exakt kalibriert ist. Anstelle des Winkels 0 wird eine kleinere odere grössere Zahl gemessen (z.B. -2).

Wir erweitern daher unser Programm um eine Kalibrierfunktion. Wenn die Taste **A** gedrückt ist, soll sich das Programm den aktuellen Messwert merken. Dieser Fehlerwert soll dann bei allen folgenden Messungen abgezogen werden, so dass der Fehler der Messung verschwindet.

1.  Die Variable ```calibration``` soll den Fehlerwert speichern. Ihr Startwert ist 0.
1.  Wenn Taste **A** gedrückt ist, wird der gemessene Wert nicht angezeigt, sondern als Fehlerwert gemerkt.
1.  Vor der Anzeige eines Messwerts wird immer der Fehlerwert vom gemessenen Wert abgezogen.

```
from microbit import *
import time
import math

calibration = 0.0

while True:
    # Get acceleration in x and y axis, then compute
    # angle micro:bit has.
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    angle = math.atan2(x,y) / math.pi * 180    
    
    if button_a.is_pressed():
        display.show(Image.ARROW_S)
        calibration = angle
    else:
        angle = angle - calibration

        # Limits angle to -2 .. +2 degrees
        limit = 2.0
        if angle > limit:
            angle = limit
        elif angle < -limit:
            angle = -limit
        
        # Show a pixel depending on micro:bit level
        pos = round(2.0 + angle * 1.0)
        display.clear()
        display.set_pixel(int(pos), 1, 9)

    time.sleep_ms(50)
```


## Ideen für Dich

*   Vermutlich hast du bemerkt, dass das Pixel etwas herumspringt. Das hängt mit der Ungenauigkeit (dem Rauschen) der Messung zusammen. Mit einem Filter kann man das verbessern. 
*   Verbessere das Program so, dass es mehrere Messungen macht und den Durchschnitt aller Werte berechnet. Dadurch wird das Rauschen gefiltert und die Messung wird genauer.
*   Verbessere die Anzeige. Zeige anstelle des Punktes z.B. eine Linie an, die gerade oder schräge ist, je nach Lage des micro:bit.


## Was haben wir gelernt

*   Programmieren mit MicroPython
*   Endlosschleifen (while), Bedingungen (if)
*   Tastenabfrage
*   Anzeige eines Pixels auf dem Bildschirm
*   Mathematische Berechnungen (Arcustangens, Runden)



## Programme

*   [Hello](./hello.py)
*   [Wasserwaage 1](./level_1.py)
*   [Wasserwaage 2](./level_2.py)
*   [Wasserwaage komplett](./level_final.py)
