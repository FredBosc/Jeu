import random
import time

class cCite:
    def __init__(self,dict_Mortalite):
        self.m_ListBatiments = []
        self.m_ListPopulation=[]
        self.dict_Mortalite=dict_Mortalite
        self.m_FertiliteCite=15     #fertilite de base des habitants de la cite.
    

class cBatiment:
    def __init__(self):
        self.m_ListOccupants=[]
        self.m_ProductionOr=0
        self.m_ProductionVivre=0
        self.m_ProductionArmes=0

    def affichage(self):
        #Affichage du batiment
        m=0

    def vieillir(self):
        #On parcourt la liste des habitants
        for hab in self.m_ListOccupants:
            if hab.sante==0:
                self.ListOccupants.remove(hab)


class cHabitation (cBatiment):
    def __init__(self):
        pass
        
class cPersonne:
    def __init__(self,prenom, nom, cite, genre):
        self.m_Prenom= prenom
        self.m_Nom=nom
        self.m_Age=0                  #indique l'age                               
        self.m_Profession= AUCUNE     #Indique la profession
        self.m_Sante=100              #0-100: indique le niveau de santé. 0=Mort.
        self.m_CatAge = AGE_ENFANT
        self.m_Argent=0
        self.m_Bonheur=100
        self.m_StatutMarital = CELIBATAIRE
        self.m_Cite=cite
        self.m_Genre=genre
        self.m_Fertilite=self.m_Cite.m_FertiliteCite #l'enfant hérite de la fertilite de sa cité d'origine
        
        self.m_Cite.m_ListPopulation.append(self)
        self.m_ListEnfants=[]

    def calcul_CatAge(self):
        #calcul de la categorie d'age
        if self.m_Age<SEUIL_ADOLESCENT:
            self.m_CatAge=AGE_ENFANT
        elif self.m_Age<SEUIL_ADULTE:
            self.m_CatAge=AGE_ADOLESCENT
        elif self.m_Age<SEUIL_ANCIEN:
            self.m_CatAge=AGE_ADULTE
        else: 
            self.m_CatAge = AGE_ANCIEN
        

    
    #SCENARIO: GETTING OLDER
    #GIVEN a person
    #WHEN 
    #   he get older of one year
    #THEN
    #   his age is incremented
    #   the age category is updated if necessary
    #   we check if he get married
    #   we check if he has a baby
    #   we check if he die.
    def vieillit(self):
        #on incrmente l'age
        self.m_Age=self.m_Age+1
        #on met à jour éventuellement la catégorie d'age
        self.calcul_CatAge()
        #on vérifie le statut marital

        #on vérifie la naissance d'enfant
        self.naissance()

        #on vérifie si la personne meurt (en fonction du risque de décès lié à son statut)
        self.meurt()

    #Calcul si une naissance a lieu
    #SCENARIO: BIRTH
    #GIVEN
    #   An Adult and married woman
    #WHEN
    #   She's in a good health and his husband is in good health too
    #THEN
    #   there's a chance depending of the fertility of the woman that there's a baby
    #   this baby is added to the list of people living in the city and in the list of the woman children
    #   and to the list of the husband children list  
    def naissance(self):
        #si la personne est marié et adulte et une femme
        if self.est_marrie() and self.m_CatAge==AGE_ADULTE and self.m_Genre==FEMME:
            #si la personne est en relative bonne santé
            if self.m_Sante >30 and self.m_Conjoint.m_Sante>30 :
                if random.randint(0,100)<self.m_Fertilite:
                    n=cPersonne("x"+str(len(self.m_Cite.m_ListPopulation)),self.m_Nom,self.m_Cite,random.randint(0,1))
                    self.m_ListEnfants.append(n)                 #on ajoute l'enfant à la liste des enfants de la mère.
                    self.m_Conjoint.m_ListEnfants.append(n)      #on ajoute l'enfant à la liste des enfants du père.

    def est_marrie(self):
        return self.m_StatutMarital==MARIE

    #sCENARIO: DEATH
    # GIVEN 
    #   a person
    # WHEN
    #   a random number is greater than the mortality risk of the person
    # THEN
    #   The person die (Sante=0)
    # 
    # Note: For the moment,for mortality risk of the person is the same than the city one
    #regarding his age category.
    #NEED TO BE IMPROVED (profession - income - hapyness...)
    def meurt(self):
        i=random.randint(1,100)
        if i<dict_Mortalite[self.m_CatAge]:
            print("MORT")
            self.m_Sante=0
            self.m_Cite.m_ListPopulation.remove(self)

    #SCENARIO: FAMILY MEMBER
    #GIVEN a person A and a person B
    #WHEN 
    #     the person B is not a brother/sister or an direct ascendant or a direct descendant of A
    #Then 
    #   return True
    # #Verifie si une personne est dans la famille proche: enfant - frere/soeur - parents - grands parents
    def estFamilleProche(self,p):
        #A definir
        return False
    
    #SCENARIO: Getting married
    #GIVEN
    #  a cPersonn P who can be married
    #WHEN 
    #   There is a personn from the other sex who is marriable in the same city and who are not in the same family
    #THEN 
    #   the two personns become married and they change their marrital status
    #Note: this marriage is automatic and don't depend from other factors. NEED TO BE IMPROVED
    def se_marrie(self):
        #Si la personne n'est pas marriée si elle est adulte et en bonne santé alors elle peut se marrier    
        if self.est_marriable(): 
            for p in self.m_Cite.m_ListPopulation:
                if p.m_Genre!=self.m_Genre and p.est_marriable() and self.estFamilleProche(p)==False:
                    self.m_Conjoint=p
                    self.m_StatutMarital=MARIE
                    p.m_StatutMarital=MARIE
                    p.m_Conjoint=self
                    break

    def est_marriable(self):
        return self.est_marrie()==False and self.m_CatAge==AGE_ADULTE and self.m_Sante>50
     
    #retourne False si la personne est en vie(Santé > 0), True sinon
    def est_mort(self):
        return self.m_Sante==0

    #Affiche la catégorie d'age et l'age
    def print_CatAge(self):
        print (self.m_Nom+" est un "+ dict_CatAge[self.m_CatAge])            
        print ("il a "+ str(self.m_Age)+" an(s)")      

    def print_StatutMarital(self):
        print ("Il/elle est "+dict_StatutMarital[self.m_StatutMarital])

    def print_Genre(self):
        print(dict_Genre[self.m_Genre])

    def print_nbEnfants(self):
        print(len(self.m_ListEnfants))

    def fiche(self):
        self.print_CatAge()
        self.print_Genre()
        self.print_StatutMarital()
        self.print_nbEnfants()
        print("--------------------------")
        print("")

    def fiche_synthese(self):
        print (self.m_Prenom+" "+self.m_Nom+"-"+str(self.m_Age)+" ans - "+dict_Genre[self.m_Genre]+" - "+dict_StatutMarital[self.m_StatutMarital]+" - " +str(len(self.m_ListEnfants))+" enfants")

AUCUNE=0

AGE_ENFANT     = 0
AGE_ADOLESCENT = 1
AGE_ADULTE     = 2
AGE_ANCIEN     = 3

SEUIL_ADOLESCENT = 10
SEUIL_ADULTE     = 16
SEUIL_ANCIEN     = 50

CELIBATAIRE     = 0
MARIE           = 1
VEUF            = 2

HOMME = 0
FEMME = 1    

#dictionnaires
dict_CatAge        = {AGE_ENFANT:"ENFANT",AGE_ADOLESCENT:"ADOLESCENT",AGE_ADULTE:"ADULTE",AGE_ANCIEN:"ANCIEN"}
dict_Mortalite     = {AGE_ENFANT:2,AGE_ADOLESCENT:1,AGE_ADULTE:1,AGE_ANCIEN:20}
dict_StatutMarital = {CELIBATAIRE:"CELIBATAIRE",MARIE:"MARIE(E)",VEUF:"VEUF(VE)"}
dict_Genre         = {HOMME:"Homme",FEMME:"Femme"}


Rome=cCite(dict_Mortalite)
Pierre = cPersonne("Pierre","DUPONT",Rome,HOMME)
Marie  = cPersonne("Marie","ROUX",Rome,FEMME)
Jean = cPersonne("Jean","ALIBERT",Rome,HOMME)
Aline= cPersonne("Aline","PEITPONT",Rome,FEMME)

while True:
    for i in Rome.m_ListPopulation:
        i.vieillit()
        i.se_marrie()
        i.fiche_synthese()
    print("")
    time.sleep(1)
