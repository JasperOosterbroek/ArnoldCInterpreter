# ArnoldC interpreter

Deze ArnoldC interpreter is geschreven voor het ATP vak en voldoet aan de must have's van de opdracht.
Informatie over het gebruik van de taal is hier te vinden:
https://github.com/lhartikk/ArnoldC

# Instructies
Het gebruik van de interpreter is vrij simpel. Nadat de repo is gedownload en uitgepakt kan je in de map een console openen.
In deze console kan je het volgende typen:
```
main.py -f "bestandsnaam"
```
De bestandsnaam moet de ArnoldC code bevatten die je wilt interpeteren.
Binnen de command line kan je de volgende argumenten meegeven
`-d ` of `--debug` om de programstate per stap uit te laten draaien
`-t` of `--test` om de tests geschreven in unittest voor het interpeteren uit te laten voeren

# Tests
De officiele ArnoldC repository heeft tests geschreven om aan te geven hoe de code zou moeten werken.
De logica tests, operator tests en branch tests zijn overgenomen om aan te geven dat de interpreter werkt zoals het volgens de maker van de taal bedoelt was. Deze tests zijn in het bestand `unittests.py` te vinden en zijn gemaakt met de python unittest library.

## Must have's:
- Classes worden gebruikt als data objecten
- Er vindt binnen de error classen overerving plaats
- Objecten kunnen via `__str__` en `__repr__` worden geprint
- Tijdens het programeren had ik geen punt gevonden waarop "private" variabelen van toepassing waren
- Er is een decorator geschreven die ervoor zorgt dat de programstate tijdens het uitvoeren van de code informatie print met `-d` of `--debug` is meegegeven
- Zover ik functioneel programmeren begrijp is het zo geprogrammeert
- Alle functies zijn conform aan python typing type-annotated
- Er is meer dan drie keer gebruik gemaakt van hogere order functies\

## Should have's
De volgende should have's zijn in de opdracht verwerkt
- Error-messaging (syntax, parser en runtime)
- advanced language features (while, Macros, if else & methods meer over methods hieronder)
- instruction-and-show-off-video (https://youtu.be/YEGhVjXrs-8)
## Extras
Extras buiten de opdracht must en should have's om:
- Unittests (overgenomen van de ArnoldC bedenker om de interpreter zo correct mogelijk aan de taal te krijgen)
- commandline arguments (om makkelijk te kunnen debuggen of de taal te kunnen testen zonder in de code te werken)

## Methods
De advanced feature methods is op het laatste pas gemaakt. Omdat dit zo'n grootte feature is om te implementeren is dat nog niet volledig gedaan.

Je hebt nu maar 1 manier om methods te gebruiken die echt werkt zoals bedoelt, al het andere om methods heen werkt nog niet goed en is nog niet goed getest.

### Method gebruik
Je kan de output van een method naar een variable schrijven.
In dit geval wordt de method modulo aangeroepen met als variabellen 4795 en 87
```
GET YOUR ASS TO MARS result2
DO IT NOW modulo 4795 87
```
De modulo functie zal er als volgt uitzien.
```
LISTEN TO ME VERY CAREFULLY modulo
I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE dividend
I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE divisor
GIVE THESE PEOPLE AIR
[method code]
I'LL BE BACK remainder
HASTA LA VISTA, BABY
```
`LISTEN TO ME VERY CAREFULLY` geeft de method naam aan
`I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE` is om een method variable aan te geven
`GIVE THESE PEOPLE AIR` geeft aan dat het gaat om een non-void method
`I'LL BE BACK` is de return statement
`HASTA LA VISTA,BABY` geeft het einde van de method aan

# Wat wordt niet ondersteund
De volgende dingen worden niet ondersteund die de officiele taal wel ondersteund:
- Methods die void returnen en daarmee meteen ook method calls die niet aan variabelen worden assigned
- ParseError `WHAT THE FUCK DID I DO WRONG`
- ReadInteger `I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM ANSWERED IMMEDIATELY`

Voor de andere method opties had ik geen tijd om te maken
De ParseError vondt ik niet nodig, om dit wel toe tevoegen is simpel, de parse error class zou aangepast moeten worden (geval van tekst vervangen)
De ReadInteger was Input wat ik niet wilde ondersteunen.

