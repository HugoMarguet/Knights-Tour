import random


class CavalierEuler:

    def __init__(self, n, m, case_init):

        self.n = n
        self.m = m
        self.case_init = case_init
        self.borne_inf = 10
        self.echiquier = [1] * (m * n)
        for k in range(m):
            for i in range(n):
                self.echiquier[n * k + i] = [k, i]

    def __init__(self):

        self.n = 8
        self.m = 8
        self.case_init = 0
        self.borne_inf = 10
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

    def liste_adj(m_adj):
        """la liste d'adjacence est une liste ou liste[i] est une liste constituée des voisin de la case i selon
        notre numérotation. """
        list_adj = [0] * len(m_adj)
        for k in range(len(m_adj)):
            list_adj[k] = []
            for i, j in enumerate(m_adj):
                if j[k] == 1:
                    list_adj[k].append(i)
        return list_adj

    def affichage_mat(self, mat):
        """affiche une matrice bien ordonnée"""
        for k in mat:
            print(k)

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

    def suivant_alea(self, suivant):
        """renvoie aléatoirement une case parmi celle presente dans la liste suivante"""
        a = random.randint(0, len(suivant)) - 1
        return suivant[a]

    def vue(self, parcours):
        ech = [0] * self.n * self.m
        for i,val in enumerate(parcours):
            ech[val] = i + 1
        for i in range(self.n):
            print(ech[i*self.n:i*self.n+self.m])


    def alea_euler(self):
        """parcours aléatoire de taille borne_inf"""
        parcours = [self.case_init]
        max = len(parcours)
        while len(parcours) < self.borne_inf:
            if not self.suivant(parcours):
                if max < len(parcours):
                    max = len(parcours)
                    print(max)
                parcours = [self.case_init]
            else:
                parcours.append(self.suivant_alea(self.suivant(parcours)))
        print(len(parcours))
        self.vue(parcours)
        return parcours


test = CavalierEuler()
print(test.alea_euler())
