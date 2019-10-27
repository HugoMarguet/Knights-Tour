import random


class CavalierEuler:

    borne_inf_def = 5

    def __init__(self, n, m, case_init):

        self.n = n
        self.m = m
        self.case_init = case_init
        self.borne_inf = CavalierEuler.borne_inf_def
        self.echiquier = [1] * (m * n)
        for k in range(m):
            for i in range(n):
                self.echiquier[n * k + i] = [k, i]

    def __init__(self):

        self.n = 8
        self.m = 8
        self.case_init = 0
        self.borne_inf = CavalierEuler.borne_inf_def
        self.echiquier = [1] * (self.m * self.n)
        for k in range(self.m):
            for i in range(self.n):
                self.echiquier[self.n * k + i] = [k, i]

    def nv_echiquier(self):
        echiquier = [1] * (self.m * self.n)
        for k in range(self.m):
            for i in range(self.n):
                echiquier[self.n * k + i] = [k, i]
        return echiquier

    def translation(self, pos):
        """donne les coordonnées pos=[i,j] sous la forme de notre convention nommée ci-dessus. m est le nombre de ligne de l'échiquier."""
        i = pos[0]
        j = pos[1]
        return j + self.m * i

    def translation_inv(self, case):
        return self.echiquier[case]

    def dep_cav(self, case):
        """indique les positions possibles du cavalier. """
        pos_cav = []
        position = self.translation_inv(case)
        j = position[1]
        i = position[0]
        dep_pos = [[i - 1, j + 2], [i + 1, j + 2], [i + 2, j - 1], [i + 2, j + 1], [i - 1, j - 2], [i + 1, j - 2],
                   [i - 2, j - 1], [i - 2, j + 1]]
        for k in dep_pos:
            if 0 <= k[0] < self.m and 0 <= k[1] < self.n:
                k_conv = self.translation(k)
                pos_cav.append(k_conv)
        return pos_cav

    def sont_relies(self, c1, c2):
        """renvoie si les cases [i,j] et [k,l] sont reliés par le deplacement du cavalier. ci = case i """
        depcav = self.dep_cav(c1)
        for k in depcav:
            if k == c2:
                return True
        return False

    def mat_adj(self):
        """renvoie la matrice d'adjacence pour le parcours du cavalier """
        adj = [0] * self.m * self.n
        for k in range(self.m * self.n):
            adj[k] = [0] * self.n * self.m
        for i in range(len(adj)):
            for j in range(len(adj)):
                if self.sont_relies(i, j) or self.sont_relies(j, i):
                    adj[i][j] = 1
        return adj

    def liste_adj(self, m_adj):
        """la liste d'adjacence est une liste ou liste[i] est une liste constituée des voisin de la case i selon
        notre numérotation. """
        list_adj = [0] * len(m_adj)
        for k in range(len(m_adj)):
            list_adj[k] = []
            for i, j in enumerate(m_adj):
                if j[k] == 1:
                    list_adj[k].append(i)
        return list_adj

    def echange(self, l, i, j):
        """échange les éléments d'indice i et j dans la liste l. """
        a = l[i]
        l[i] = l[j]
        l[j] = a
        return l

    def suivant(self, parcours):
        """renvoie la liste des cases que pourra rejoindre le cavalier"""
        last_case = parcours[-1]
        relie = []
        for case in self.echiquier:
            case_conv = self.translation(case)
            if self.sont_relies(last_case, case_conv):
                relie.append(case_conv)
        for k in parcours:
            for i, val in enumerate(relie):
                if k == val:
                    self.echange(relie, i, -1)
                    relie.pop()
        return (relie)

    def cases_manquantes(self, parcours):
        l=[-1] * self.m * self.n
        r=[]
        for p in range(self.m * self.n):
            for q in parcours:
                if q == p:
                    l[p] = p
        for p,k in enumerate(l):
            if k == -1:
                r.append(p)
        return r

    def verification(parcours):
        """renvoie True si le parcours est correct ie chaque case est différente et deux cases sucessives sont reliées par le déplacement du cavalier, False sinon"""
        for k in range(len(parcours)-1):
            for l in range(k+1,len(parcours)):  # on verifie ici que le cavalier ne repasse jamais par une même case.
                if parcours[k] == parcours[l]:
                    print(k,l)
                    return False
            case_prec = parcours[k]
            case_suiv = parcours[k+1]
            if not sont_relies(case_prec,case_suiv): #on vérifie ici que les cases succédantes sont bien reliés selon le deplacement du cavalier.
                print(k)
                return False
        return True

    def euler(self, parcours):

        def prive_de(l1,l2):
            """Cette fonction retourne la liste l1 privé de l2"""
            prive = []
            for p in l1:
                bool = True
                for q in l2:
                    if p == q:
                        bool = False
                if bool:
                    prive.append(p)
            return prive

        def chemin_renv_bis(chemin,xi):
            """retourne la liste renversé de chemin[xi+1:] """
            nv_ch = []
            n = len(chemin)
            for k in range(xi,n):
                l= n - (k+1) + xi
                nv_ch.append(chemin[l])
            return nv_ch

        def voisin_derch(chemin):
            """renvoie la liste des voisins de la derniere case du chemin, sans l'avant derniere case du chemin."""
            derch = chemin[-1]
            intru = chemin[-2]
            matadj = self.mat_adj()
            adj = self.liste_adj(matadj)
            voisin = adj[derch]
            for k in range(0,len(voisin)):
                if voisin[k] == intru:
                    self.echange(voisin,k,-1)
                    voisin.pop()
                    return voisin
            return voisin

        def x_plus_1(parcours,x):
            for i,val in enumerate(parcours):
                if val == x:
                    return i+1
            return 0

        def indice_voisin_pif(voisin,parcours):
            x = voisin[random.randint(0,len(voisin)-1)]
            for i,val in enumerate(parcours): # i est l'indice et val la valeur
                if val == x:
                    return i + 1
            return 0 # cas jamais atteint, utilisé simplement pour éviter 'NoneType'

        def indice_voisin(voisin,parcours,case_manquante,):
            voisin = prive_de(voisin,case_manquante)
            for x in voisin:
                ixplus1 = x_plus_1(parcours,x)
                xplus1 = parcours[ixplus1]
                for case in case_manquante:
                    if self.sont_relies(xplus1,case,):
                        return ixplus1
            x = indice_voisin_pif(voisin,parcours)
            return x

        def cases_manquantes(chemin):
            """renvoie les cases manquantes au trajet partiel 'chemin'"""
            list_echiquier = [0] * self.m * self.n
            for k in range(1,len(list_echiquier)):
                list_echiquier[k] = k
            return prive_de(list_echiquier,chemin)

        def modif_parcours(chemin,case_manquante):
            """modifie le parcours selon la methode d'euler"""
            voisin = voisin_derch(chemin,)
            xiplus1 = indice_voisin(voisin,chemin,case_manquante,)
            m= chemin[-1]
            ch = chemin_renv_bis(chemin,xiplus1)
            return chemin[0:xiplus1]+ch

        derniere_case = parcours[-1]
        cases_manq = cases_manquantes(parcours)
        while len(parcours) < self.m * self.n:
            while len(prive_de(voisin_derch(parcours),parcours)) != 0 :
                case_manq_temp = cases_manq[:]
                k = 0
                for i,case in enumerate(case_manq_temp):
                    j = i - k
                    derniere_case = parcours[-1]
                    if self.sont_relies(case,derniere_case,) :
                        parcours.append(case)
                        del cases_manq[j]
                        k += 1
            parcours = modif_parcours(parcours,cases_manq)

        if len(parcours) != self.m * self.n:
            return false
        derniere_case = parcours[-1]
        premiere_case = parcours[0]
        while not self.sont_relies(derniere_case,premiere_case):
            parcours = modif_parcours(parcours,[])
            derniere_case = parcours[-1]
            premiere_case = parcours[0]
        return parcours

    def alea(self):
        """parcours aléatoire de taille borne_inf"""

        def suivant_alea(suivant):
            """renvoie aléatoirement une case parmi celle presente dans la liste suivante"""
            a = random.randint(0, len(suivant)) - 1
            return suivant[a]

        parcours = [self.case_init]
        max = 1
        while len(parcours) < self.borne_inf:
            if not self.suivant(parcours):
                if max < len(parcours):
                    max = len(parcours)
                print(max)  # Affiche le parcours le plus long (permet de conjectuerer sur la borne_inf car la terminaison n'est pas vérifiée)
                parcours = [self.case_init]
            else:
                parcours.append(suivant_alea(self.suivant(parcours)))
        return parcours

    def warnsdorff(self):
        """renvoie le parcours du cavalier avec la méthode des poids de Warnsdorff"""

        def poids(list_adj):
            """ renvoie le poids de chaque case ie le nombre de cases reliées a cette case"""
            poids = []
            for k in list_adj:
                poids.append(len(k))
            return poids

        def actualisation(case,adj,p):
            """supprime tous les éléments case de la liste d'adjacence et réduit le poids associé. """
            p[case] = 0
            adj[case] = []
            for i in range(len(adj)):
                j = 0
                length = len(adj[i])
                while j < length:
                    if adj[i][j] == case:
                        p[i] -= 1
                        self.echange(adj[i],j,-1)
                        adj[i].pop()
                        j = length # On supose ici que chaques sous listes de la liste d'adjacence ne peut contenir qu'un seul élément de valeur a.
                    j += 1
            return adj

        def i_poids(poids):
            """retourne une liste des indices des éléments de la liste poids triés par ordre croissant de poids"""
            list = []
            for m in range(1,9):
                for i,val in enumerate(poids): #val prend les valeurs de la liste et i l'indice des éléments de la liste
                    if val == m :
                        list.append(i)
            return list

        def prive(parcours,ipoids):
            """ retourne la liste des cases possibles du cavalier en conservant l'ordre croissant du poids. Cette fonction retourne la liste Poids privé de Parcours"""
            case = parcours[-1]
            prive = []
            for p in ipoids:
                bool = True
                for q in parcours:
                    if p == q:
                        bool = False
                if bool and self.sont_relies(case,p):
                    prive.append(p)
            return prive

        def det(cases_pos):
            """détermine la prochaine case du cavalier"""
            if cases_pos == [] :
                return -1
            return cases_pos[0]

        # Initialisation
        m_adj = self.mat_adj()
        adj = self.liste_adj(m_adj)
        parcours = []
        p = poids(adj)
        ip = i_poids(p)
        parcours.append(self.case_init)
        actualisation(self.case_init,adj,p)
        ip = i_poids(p)
        cases_pos = prive(parcours,ip)
        case = det(cases_pos)

        while case != -1:
            parcours.append(case)
            p = poids(adj)
            ip = i_poids(p)
            cases_pos = prive(parcours,ip)
            actualisation(case,adj,p)
            case = det(cases_pos)

        return parcours

    def alea_euler(self):
        parcours = self.alea()
        parcours = self.euler(parcours)
        return parcours

    def warnsdorff_euler(self):
        parcours = self.warnsdorff()
        parcours = self.euler(parcours)
        return parcours


def affichage_mat(mat):
    """affiche une matrice de dimension 2"""
    for k in mat:
        print(k)

def vue(parcours, n, m):
    ech = [0] * self.n * self.m
    for i,val in enumerate(parcours):
        ech[val] = i + 1
    for i in range(n):
        print(ech[i * n : i * n + m])

test1 = CavalierEuler()
print(test1.warnsdorff())
print(test1.alea())
print(test1.alea_euler())


