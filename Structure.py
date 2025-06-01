# Creer le back d'une application qui permet de générer une trajectoire d'un actif basé sur le modèle de Black-Scholes 
# Puis de modéliser le prix d'une option européenne basé sur Black-Scholes
# Puis delta hedger la position optionnelle selon les variations du sous-jacent

from numpy import random, sqrt, log, exp, ndarray, insert, cumprod, round, zeros
from math import pi, erf
from typing import Literal

def phi(x):

    '''Cumulative distribution function for the standard normal distribution'''

    return (1.0 + erf(x / sqrt(2.0))) / 2.0

def Cost_Function(Cout_Hedge:float, Quantite:float) -> float:

    """
    Fonction de coût de la couverture delta
    Cout_Hedge: Coût de la couverture
    Quantite: Quantité d'actif sous-jacent
    """

    if Quantite > 0:
        return Quantite * (1 + Cout_Hedge)  # Coût de la couverture pour une position longue
    elif Quantite <= 0:
        return Quantite * (1 - Cout_Hedge)  
    else:
        raise ValueError("Quantité must be non-zero")  # Pas de coût si pas de position

class Environnement_Modelisation:
    def __init__(self, T:float, Steps:int, Cout_Hedge:float, Periodicite_Hedge:float) -> None:
        self.Residual_Maturity = T # Maturité résiduelle de l'option
        self.Steps = Steps # Nombre de pas de temps
        self.dt = T / Steps # Pas de temps
        self.Cout_Hedge = Cout_Hedge #Coût de la couverture
        self.Periodicite_Hedge = Periodicite_Hedge  #Périodicité de la couverture
        

class BlackSchole_Modele:

    @staticmethod
    def Option_Price(OptionType:Literal["Call", "Put"],S0:float, K:float, T:float, r:float, q:float, sigma:float, round_nb:int=2) -> float:
        
        """
        Calcule le prix de l'option selon le modèle de Black-Scholes
        """

        d1:float = log(S0 / K) + (r - q + 0.5 * (sigma ** 2)) * T
        d1 /= sigma * sqrt(T)
        d2:float = d1 - sigma * sqrt(T)

        if OptionType == "Call":
            Price:float = S0 * exp(-q * T) * phi(d1) - K * exp(-r * T) * phi(d2)
            Price = round(Price, round_nb)
            return Price
        elif OptionType == "Put":
            Price = - S0 * exp(-q * T) * phi(-d1) + K * exp(-r * T) * phi(-d2)
            Price = round(Price, round_nb)
            return Price
        else:
            raise ValueError("OptionType must be 'Call' or 'Put'")
        
    @staticmethod
    def Option_Delta(OptionType:Literal["Call", "Put"],Spot:float, K:float, T:float, r:float, q:float, sigma:float, round_nb:int=2) -> float:

        """ Calcule le delta de l'option selon le modèle de Black-Scholes """

        d1:float = log(Spot / K) + (r - q + 0.5 * (sigma ** 2)) * T
        d1 /= sigma * sqrt(T)

        if OptionType == "Call":
            return round(exp(-q * T) * phi(d1), round_nb)
        elif OptionType == "Put":
            return round(-exp(-q * T) * (phi(-d1)), round_nb)
        else:
            raise ValueError("OptionType must be 'Call' or 'Put'")

    def __init__(self, OptionType:Literal["Call", "Put"],S0:float, K:float, T:float, r:float, q:float, sigma:float, round:int=2) -> None:
        self.OptionType:Literal["Call", "Put"] = OptionType
        self.S0:float = S0  # Prix initial de l'actif
        self.K:float = K    # Prix d'exercice de l'option
        self.T:float = T    # Temps jusqu'à l'échéance (en années)
        self.q:float = q    # Taux de dividende de l'actif
        self.r:float = r    # Taux d'intérêt sans risque
        self.sigma:float = sigma  # Volatilité de l'actif
        self.Price:float = self.Option_Price(OptionType, S0, K, T, r, q, sigma)  # Prix de l'option
        self.Delta:float = self.Option_Delta(OptionType, S0, K, T, r, q, sigma)  # Delta de l'option
        self.round:int = round

    
class Trajectoire:
    def __init__(self, ENV: Environnement_Modelisation, Option: BlackSchole_Modele, seed:int=10) -> None:
        self.ENV:Environnement_Modelisation = ENV
        self.Option:BlackSchole_Modele = Option
        self.Random:ndarray
        self.Trajectoire:ndarray
        self.Delta_Trajectoire:ndarray
        self.Prime_Trajectoire:ndarray
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

        """
        Calcule le delta de l'option pour chaque étape de la trajectoire
        """

        self.Delta_Trajectoire = zeros((self.ENV.Steps + 1, 2))
        for step in range(0, self.ENV.Steps + 1):
            delta_tmp:float = self.Option.Option_Delta(OptionType = self.Option.OptionType, Spot = self.Trajectoire[step],
                                                       K = self.Option.K, T = self.ENV.Residual_Maturity - (step * self.ENV.dt),
                                                       r = self.Option.r, q = self.Option.q, 
                                                       sigma = self.Option.sigma,round_nb = self.Option.round)
            self.Delta_Trajectoire[step,0] = step * self.ENV.dt
            self.Delta_Trajectoire[step,1] = round(delta_tmp,self.Option.round)
            del delta_tmp
        
    def GeneratioPrime_Trajectoire(self) -> None:

        """
        Calcule la prime de l'option pour chaque étape de la trajectoire
        """

        self.Prime_Trajectoire = zeros((self.ENV.Steps + 1, 2))
        for step in range(0, self.ENV.Steps + 1):
            prime_tmp:float = self.Option.Option_Price(OptionType = self.Option.OptionType, S0 = self.Trajectoire[step],
                                                       K = self.Option.K, T = self.ENV.Residual_Maturity - (step * self.ENV.dt),
                                                       r = self.Option.r, q = self.Option.q, 
                                                       sigma = self.Option.sigma, round_nb = self.Option.round)
            self.Prime_Trajectoire[step,0] = step * self.ENV.dt
            self.Prime_Trajectoire[step,1] = round(prime_tmp,self.Option.round)
            del prime_tmp

    def DeltaHedge(self) -> None:

        """
        Calcule la couverture delta de la position optionnelle selon les variations du sous-jacent
        """

        PTF = zeros((self.ENV.Steps + 1, 4))

        
        for step in range(1, self.ENV.Steps + 1, 1):
            pass
            
        