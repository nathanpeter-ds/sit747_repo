import gymnasium as gym
import numpy as np
import pandas as pd 
import random 

class SingleStockTraderKFohlcvCuilogr(gym.Env):
    def __init__(self, data, cash = 500000, transaction = 0.001, lookback = 30):
        super().__init__()
        self.data = data
        self.initial_cash = cash
        self.cash = cash
        self.portfolio = cash
        self.transaction = transaction
        self.lookback = lookback
        self.current_step = self.lookback -1
        self.current_price = self.data['Close'].iloc[self.current_step]
        self.kalman_close = self.data['kalman_Close'].iloc[self.current_step]

        self.kalman_High = self.data['kalman_High'].iloc[self.current_step]
        self.kalman_Low = self.data['kalman_Low'].iloc[self.current_step]
        self.kalman_Open = self.data['kalman_Open'].iloc[self.current_step]
        self.kalman_Volume = self.data['kalman_Volume'].iloc[self.current_step]

        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low = -np.inf, high = np.inf, shape = (5*self.lookback,), dtype = np.float32)
        
        self.holdings = 0
        self.done = False
       
    def get_state(self):
        price_history = self.data['kalman_Close'].iloc[self.current_step-self.lookback+1:self.current_step+1]
        high_history = self.data['kalman_High'].iloc[self.current_step-self.lookback+1:self.current_step+1]
        low_history = self.data['kalman_Low'].iloc[self.current_step-self.lookback+1:self.current_step+1]
        open_history = self.data['kalman_Open'].iloc[self.current_step-self.lookback+1:self.current_step+1]
        vol_history = self.data['kalman_Volume'].iloc[self.current_step-self.lookback+1:self.current_step+1]

    
        state = np.stack([price_history,high_history,low_history,open_history,vol_history], axis=1)
        return state

    def reset(self, seed=None, random_start=False, steps =252):
        self.cash = self.initial_cash
        self.portfolio = self.cash
        self.holdings = 0
        if random_start == False:
            self.current_step = self.lookback-1
        elif random_start == True:
            self.current_step = random.randint(self.lookback ,len(self.data)-self.lookback - steps) #enforce min of 1 year
        self.current_price = self.data['Close'].iloc[self.current_step]
        self.kalman_close = self.data['kalman_Close'].iloc[self.current_step]
        self.kalman_High = self.data['kalman_High'].iloc[self.current_step]
        self.kalman_Low = self.data['kalman_Low'].iloc[self.current_step]
        self.kalman_Open = self.data['kalman_Open'].iloc[self.current_step]
        self.kalman_Volume = self.data['kalman_Volume'].iloc[self.current_step]

        self.done = False
        self.last_trade_step = self.current_step
        self.portfolio_history = []
        state = self.get_state()
        info = {'Date': self.data.index[self.current_step], 'Price': self.current_price, 'Holdings':self.holdings, 'Portfolio': self.portfolio}
        return state, info

    def step(self,action):
        if self.done:
            return self.get_state(), 0, self.done, True, {}

        
        current_portfolio = self.portfolio
        
        self.current_step += 1
        
        if self.current_step >= len(self.data)-1:
            self.done = True
            trunc = True
        else:
            trunc = False
            
        reward = 0 #intilialize at 0
        self.current_price = self.data['Close'].iloc[self.current_step] #price at end of lookback

        if action == 0 and self.holdings==0:
            self.holdings = self.cash // (self.current_price*(1+self.transaction))
            self.cash -= self.holdings * self.current_price*(1+self.transaction)
            self.portfolio = self.cash + self.holdings*self.current_price
        elif action == 1 and self.holdings>0:
            self.cash += self.holdings*self.current_price*(1-self.transaction)
            self.holdings = 0
            self.portfolio = self.cash
        elif action == 2:
            pass
        
        self.portfolio = self.cash + self.holdings*self.current_price
            
        self.portfolio_history.append(self.portfolio)

        reward += 100* np.log(self.portfolio/current_portfolio)

        info = {'Date':self.data.index[self.current_step], 'Price':self.current_price, 'Holdings':self.holdings, 'Portfolio':self.portfolio}
        state = self.get_state()
        return state, reward, self.done, trunc, info

    def render(self, mode = None):
        print(f"Step: {self.current_step}, Price: {self.current_price}, Holdings: {self.holdings}, Portfolio: {self.portfolio}")

