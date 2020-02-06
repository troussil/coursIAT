#Cours: optimisation (exacte)

##Introduction

### énoncé du problème

- fonction/énergie : source -> but (=R)
- +contraintes
- objectif : trouver un élément x de la source tel que
 - x vérifie les contraintes,
 - f(x) est min/max

Différentes variantes : 
- ensemble source peut être
 - discret, continu
 - 1d, 2d, ..., nd,
- fonction peut-être linéaire, convexe/concave, "compliquée"
- contraintes peuvent être
 - égalités, inégalités
 - linéaires, non-linéaires

### convexité, déférentiabilité

- convexité/concavité (sur support convexe) => existence minimum/maximum global
- 1d: dérivée seconde, nd: hessienne, valeurs propres

## Optimisation continue

### 1d

- méthodes utilisant les dérivées
 - Méthode de Newton
 - Dichotomie avec dérivées (bisecting search method)
- méthodes sans dérivées
 - 4 intervalles égaux,
 - Fibonacci
 - nombre d'or

### nd (n >= 2)

#### sans contrainte

- Méthode de Newton
- Descente de gradient à pas déterminé (fixé ou diminuant à mesure des itérations)
- Descente de gradient à pas optimal (steepest descent)
- Méthode des directions conjugués (Fletcher et Reeves)

#### avec contraintes

- contraintes d'inégalités linéaires 
 - et fonction linéaire (PL): simplexe (p. 43-61 [1])
 - et fonction continument différentiable: méthode de Frank et Wolf (p. 242-243 [1])
- contraintes d'inégalités
 - conditions de Kuhn et Tucker, etc. (p. 204 et après [1])
- contraintes d'égalités
 - multiplicateur de Lagrange, etc. (p. 209 et après [1])

## Optimisation combinatoire

### rappel complexité (cf. algo)

### Problèmes "faciles" (rappels cf. algo)

- arbre couvrant de poids minimal (Kruskal, Prim), 
- plus court chemin (Dijkstra, Bellman-Ford-Moore, Algorithme de Floyd-Warshall)
- flot maximum (Algorithme de Ford-Fulkerson) 

### Problèmes "difficiles"

- modélisation/exemples
 - problème d'affectation
 - problème du sac à dos (knapsack problem)
 - problème du voyageur de commerce
 - problème d'ordonnancement de tâches
 - problème des surveillants de musée
 - problème de coloration
 - PLNE
 ...

- résolution : 
 - Algorithme glouton (non exact)
 - Principle de la programmation dynamique (p. 527 et après [1])
 - Méthodes arborescentes par séparation-évaluation (branch and bound) (p. 338-349 [1]) (ex. Algorithme de Little)
 - Programmation par contraintes (p. 420-424 [1])

- non traité : 
 - heuristiques (...), méta-heuristiques (tabou, recuit-simulé, alg génétique, colonie de fourmis, ...) -> cf. cours Olivier
 - optimisation stochastique (méthode de Monte-Carlo)

##Références

[1] Programmation mathématique, Théorie et algorithmes, Michel Minoux, Lavoisier, 2eme édition, 2008, 711 pp. 

#3 TDs

3 approches: 
- optimisation continue: simplexe et/ou Franck et Wolf
- optimisation combinatoire: 
   - branch and bound
   - programmation par contrainte

organisation, 2 alternatives: 
- 1 TD modélisation sur papier, 2 TDs machines où "on trouve des solutions optimales"
- 3 TDs, chacun consacré à une approche. Dans chacun, modélisation puis expérimentation sur machine. 

