import Switch

#
SWITCH_LIST = [
    # Switch
    # number, name, code_on, code_off, is_multiswitch (optional)
    # Brennstuhl elro_800_switch Switches Codes with groupcode 11111
    # A 1361  1364
    #B 4433  4436
    #C 5201  5204
    #D 5393  5396 

    [
        Switch.Switch(1, "LED Schreibtisch", '7145473', '7145475'),
        Switch.Switch(2, "Ecklampe", "1361", "1364"),
        Switch.Switch(3, "Tischlampe", "4433", "4436")
    ],
    [
        Switch.Switch(4, "Stehlampe", '11742167 4 355', '11559223 4 355'),
        Switch.Switch(5, "Leuchtkugel", '11940012 4 355', '12494204 4 355'),
        Switch.Switch(6, "Deckenfluter", '12494206 4 355', '11940014 4 355'),
        Switch.Switch(7, "Alles", '11735922 4 355', '12052066 4 355', True)
    ]
]
