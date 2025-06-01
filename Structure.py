# Creer le back d'une application qui permet de générer une trajectoire d'un actif basé sur le modèle de Black-Scholes 
# Puis de modéliser le prix d'une option européenne basé sur Black-Scholes
# Puis delta hedger la position optionnelle selon les variations du sous-jacent

from numpy import random, sqrt, log, exp, ndarray, insert, cumprod, round, zeros
from math import pi, erf
from typing import Literal

def phi(x):

    '''Cumulative distribution function for the standard normal distribution'''

    return (1.0 + erf(x / sqrt(2.0))) / 2.0

class Environnement_Modelisation:
    def __init__(self, T:float, Steps:int, Cout_Hedge:float, Periodicite_Hedge:float) -> None:
        self.Residual_Maturity = T # Maturité résiduelle de l'option
        self.Steps = Steps # Nombre de pas de temps
        self.dt = T / Steps # Pas de temps
        self.Cout_Hedge = Cout_Hedge #Coût de la couverture
        self.Periodicite_Hedge = Periodicite_Hedge  #Périodicité de la couverture
        

class BlackSchole_Modele:
    def __init__(self, OptionType:Literal["Call", "Put"],S0:float, K:float, T:float, r:float, q:float, sigma:float, round:int=2) -> None:
        self.OptionType:Literal["Call", "Put"] = OptionType
        self.S0:float = S0  # Prix initial de l'actif
        self.K:float = K    # Prix d'exercice de l'option
        self.T:float = T    # Temps jusqu'à l'échéance (en années)
        self.q:float = q    # Taux de dividende de l'actif
        self.r:float = r    # Taux d'intérêt sans risque
        self.sigma:float = sigma  # Volatilité de l'actif
        self.Price:float
        self.round:int = round

    def Option_Price(self) -> None:
        
        """
        Calcule le prix de l'option selon le modèle de Black-Scholes
        """

        d1:float = log(self.S0 / self.K) + (self.r - self.q + 0.5 * (self.sigma ** 2)) * self.T
        d1 /= self.sigma * sqrt(self.T)
        d2:float = d1 - self.sigma * sqrt(self.T)

        if self.OptionType == "Call":
            self.Price = self.S0 * exp(-self.q * self.T) * phi(d1) - self.K * exp(-self.r * self.T) * phi(d2)
            self.Price = round(self.Price, self.round)
        elif self.OptionType == "Put":
            self.Price = - self.S0 * exp(-self.q * self.T) * phi(-d1) + self.K * exp(-self.r * self.T) * phi(-d2)
            self.Price = round(self.Price, self.round)
        else:
            raise ValueError("OptionType must be 'Call' or 'Put'")


    def Option_Delta(self, Spot:float, T_residuel:float) -> float:

        """ Calcule le delta de l'option selon le modèle de Black-Scholes """

        d1:float = log(Spot / self.K) + (self.r - self.q + 0.5 * (self.sigma ** 2)) * T_residuel
        d1 /= self.sigma * sqrt(T_residuel)

        if self.OptionType == "Call":
            return round(exp(-self.q * T_residuel) * phi(d1), self.round)
        elif self.OptionType == "Put":
            return round(-exp(-self.q * T_residuel) * (phi(-d1)), self.round)
        else:
            raise ValueError("OptionType must be 'Call' or 'Put'")
        
class Trajectoire:
    def __init__(self, ENV: Environnement_Modelisation, Option: BlackSchole_Modele, seed:int=10) -> None:
        self.ENV:Environnement_Modelisation = ENV
        self.Option:BlackSchole_Modele = Option
        self.Random:ndarray
        self.Trajectoire:ndarray
        self.Delta_Trajectoire:ndarray
        self.seed = seed
        self.DetlaHedging_Matrice:ndarray
        self.GenerationRandom(self.seed)
        self.GenerationTrajectoire()
        self.GenerationDelta_Trajectoire()

    def GenerationRandom(self, seed:int = 10) -> None:
        random.seed(seed)
        self.Random = random.normal(0, 1, self.ENV.Steps)

    def GenerationTrajectoire(self) -> None:
        self.Trajectoire = self.Random * sqrt(self.ENV.dt) * self.Option.sigma
        self.Trajectoire = exp((self.Option.r - self.Option.q - (self.Option.sigma **2) * 0.5) * (self.ENV.dt) + self.Trajectoire)
        self.Trajectoire = cumprod(self.Trajectoire,0) * self.Option.S0
        self.Trajectoire = insert(self.Trajectoire, 0, self.Option.S0)
        self.Trajectoire = round(self.Trajectoire, self.Option.round)

    def GenerationDelta_Trajectoire(self) -> None:
        self.Delta_Trajectoire = zeros((self.ENV.Steps + 1, 2))
        for step in range(0, self.ENV.Steps + 1):
            delta_tmp:float = self.Option.Option_Delta(self.Trajectoire[step], self.ENV.Residual_Maturity - (step * self.ENV.dt))
            self.Delta_Trajectoire[step,0] = step * self.ENV.dt
            self.Delta_Trajectoire[step,1] = round(delta_tmp,self.Option.round)
            del delta_tmp
        
    def DeltaHedge(self) -> None:

        """
        Calcule la couverture delta de la position optionnelle selon les variations du sous-jacent
        """

        PTF = zeros((self.ENV.Steps + 1, 4))

        PTF[0, 0] = 0 # Col0 = Temps
        PTF[0, 1] = -self.Option.Option_Delta(self.Option.S0, self.ENV.Residual_Maturity) # Col1 = Quantité actif sous-jacent
        PTF[0, 2] = - self.Option.Price - PTF[0, 1] * self.Option.S0 # Col2 = Valeur du portefeuille
        PTF[0, 3] = self.Option.Option_Delta(self.Option.S0, self.ENV.Residual_Maturity) + PTF[0, 1] # Col3 = Delta du portefeuille

        print(f'En période {0} \n delta option {self.Delta_Trajectoire[0, 1]} \n quantité sous-jacent {PTF[0, 1]} \n valeur du portefeuille {PTF[0, 2]} \n delta portefeuille {PTF[0, 3]}')

        for step in range(1, self.ENV.Steps + 1, 1):

            PTF[step, 0] = step * self.ENV.dt
            Var_Delta = self.Delta_Trajectoire[step, 1] - self.Delta_Trajectoire[step - 1, 1] 

            if step % self.ENV.Periodicite_Hedge * self.ENV.Steps != 0 or True: # Si on ne hedge pas à cette période
                
                PTF[step, 1] = PTF[step - 1, 1] # Quantité sous-jacent inchangée
                PTF[step, 2] = PTF[step - 1, 2] +  PTF[step - 1, 1] * (self.Trajectoire[step] - self.Trajectoire[step - 1]) # Valeur du portefeuille 
                PTF[step, 3] = PTF[step - 1, 3] + Var_Delta
                
            
            print(f'En période {step} \n delta option {self.Delta_Trajectoire[step, 1]} \n quantité sous-jacent {PTF[step, 1]} | Prix action {self.Trajectoire[step] } \n valeur du portefeuille {PTF[step, 2]} \n delta portefeuille {PTF[step, 3]}')
            
        self.DetlaHedging_Matrice = PTF
