from microbit import *
import make_radio

radio = make_radio.MakeRadio(group=1)
radio.off()
radio.on()

licht = False

lampe = Image("99999:"
              "99999:"
              "99999:"
              "99999:"
              "99999")

def schalte(licht):
    return not licht

while True:
    if licht:
        display.show(lampe)
    else:
        display.clear()

    if button_a.was_pressed():
        radio.send_number(0)

    if button_b.was_pressed():
        licht = schalte(licht)

    if radio.receive_packet() == 0:
        licht = schalte(licht)

    sleep(100)