# Comment trouver les gares connectées par des trajets direct, et la durée d'un trajet ?

Durée d'un trajet : durée moyenne sur un ensemble de trajets ? Considéré valide même si très peu de trajets, ou bien un niveau de fréquentation minimum est nécessaire ?

Déterminer le trajet le + court, le trajet le + long entre 2 gares données, à conditions qu'elles soient reliées par une ligne directe. Par exemple :

| start | stop | min_time | max_time |
|---|---|---|---|
| Clermont-ferrand | Vichy | 26 | 32 |
| Clermont-ferrand | Montluçon | 54 | 64 |

## Récupérer les stop cibles à partir d'un stop source ? (approche naïve)

1. Identifier un stop source
1. Sélectionner les stop_times pour ce stop, récupérer les trips correspondant
1. Sélectionner les trips, récupérer les routes distinctes
1. Sélectionner les trips pour ces routes distinctes
1. Sélectionner les stop_times pour ces trips, récupérer les stop distincts

=> On obtient la liste des stop cibles accessibles depuis notre stop source

## Récupérer directement le résultat attendu ? (approche brutale)

Sélectionner les stop_times (stop source), joindre avec tous les autres stop_times (stop cible) ayant un trip_id commun, et dont stop_time source < stop_time cible, récupérer stop source, stop cible, durée de trajet tq stop_time cible - stop_time source. Sur ce résultat, grouper par stop_id source et stop_id_cible, puis récupérer la durée max, ainsi que la durée min. 


Perfs / mémoire : 
* produit scalaire (hors filtre sur même trip) : 300K ² = 90Ma d'enreg 😱
* produit scalaire (avec filtre sur même trip) : 300K * 10 = 3M enreg (on considère 10 stops en moyenne sur un trip)
* total nb gares : 4400 * 10 * 2 = 44000 (on considère 10 stops en moyenne sur un trip, des trajets aller et retour)

Idée : filtrer sur les trip dont le service est actuel ou futur proche

NB : ça ne concerne que les trajets TER. Il faudrait ajouter Intercité et TGV.