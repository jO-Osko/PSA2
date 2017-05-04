# 1. domača naloga pri PSA2: Implementacija drevesa

Na predavanjih bomo še spoznali različna iskalna drevesa, vaša naloga je da ta drevesa implementirate in med seboj 
primerjate prednosti in slabosti posameznih algoritmov.

## Orodja

Za izdelavo naloge boste uporabili git repozitorij, ki bo kopija (*fork*) repozitorija predmeta na 
[GitHub](https://github.com/jO-Osko/PSA2)u. Toplo priporočam, da 
si naredite novo vejo (*branch*) ter vse delo v zvezi z nalogo poteka v tej veji (seveda lahko po potrebi naredite še 
več vej). Vse vaše spremembe naj bodo v mapi `naloge/dn1/tree/ImePriimek`, kjer `ImePriimek` nadomestite s 
svojim imenom in priimkom. Po potrebi lahko vključite tudi teste, ki naj bodo v mapi `naloge/dn1/tree/ImePriimek`. 
Ko boste z nalogo zaključili, boste naredili *pull request* svoje veje na originalni repozitorij, potem pa bom vaše 
spremembe potegnil vanj.


## Implementacija

Priložen je modul `tree` z razredom `AbstractTree`, ki implementira osnovno drevo in škrbine potrebnih metod. 
Natančnejša dokumentacija je na voljo v programu.

## Naloga

Vaša naloga je za posamezno drevo implementirati nekatere metode na iskalnih drevesih:

+ `__init__` Metoda, ki konstruira novo drevo z začetnimi podatki.
+ `insert` Metoda, ki v drevo vstavi nov element
+ `remove` Metoda, ki iz drevesa odstrani element, če ga ni, naj sproži izjemo
+ `search` Metoda, ki vrne ali se element nahaja v drevesu



Svojo implementacijo postavite v eno ali več Pythonovih programov znotraj mape `naloge/dn1/tree/ImePriimek`, kjer 
`ImePriimek` nadomestite s svojim imenom in priimkom. V tej mapi naj bo tudi program `__init__.py`, kjer uvozite 
svoje razrede (glej [vzorec](tree/vzorec/__init__.py)). Potem bo ob poganjanju Pythonove konzole iz 
mape `naloge/dn1/` možno uvoziti vaše razrede.

Poskrbite, da bo koda berljiva in komentirana.

### Vso srečo!

## Analiza

![Prikaz časov][plot]

[plot]: plot.png