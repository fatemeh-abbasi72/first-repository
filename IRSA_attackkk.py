# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:01:27 2019

@author: Fateme
"""

import IRSA
import attack
import matplotlib.pyplot as plt
import math
import time
import numpy as np 


def main():
    n=1000
    count_avg=100
    distribution=[0,.5,.28,0,0,0,0,.22]  #G*=0.93

#    attacker_distribution_1=[0,0,0,0,0,0,0,0,1]
#    attacker_distribution_2=[0,0,1,0,0,0,0,0,0]
#    attacker_distribution_3=[0,.45,.17,0,0,0,0,.1,.28]

#    attacker_distribution_1=[0,0,1,0,0,0,0,0,0]
#    attacker_distribution_2=[.5,0,0,0,.5,0,0,0,0]
#    attacker_distribution_3=[.75,0,0,0,0,0,0,0,.25]
#    attacker_distribution_4=[.75,0,0,0,0,0,0,0,.25]        

    # attacker_distribution_1=[0,0,0,0,1,0,0,0,0]
    # attacker_distribution_2=[.25,0,0,0,.5,0,0,0,.25]
    # attacker_distribution_3=[0,0,.5,0,.25,0,0,0,.25]
    # attacker_distribution_4=[.5,0,0,0,0,0,0,0,.5]

    # attacker_distribution_1=[0,0,1,0,0,0,0,0,0]
    # attacker_distribution_2=[0,0,0,0,1,0,0,0,0]
    # attacker_distribution_3=[0,0,0,0,0,0,1,0,0]
    # attacker_distribution_4=[0,0,0,0,0,0,0,0,1]

    # attacker_distribution_1=[0.109, 0.062, 0.119, 0.232, 0.199, 0.015, 0.18, 0.002, 0.082] #E=3.6 
    # attacker_distribution_2=[0.158, 0.217, 0.0, 0.022, 0.284, 0.026, 0.018, 0.239, 0.036] #E=3.6 
    # attacker_distribution_3=[0.198, 0.047, 0.134, 0.175, 0.092, 0.087, 0.009, 0.145, 0.113] #E=3.6
    # attacker_distribution_4=[0.299, 0.004, 0.154, 0.037, 0.032, 0.014, 0.245, 0.194, 0.021] #E=3.6

    attacker_distribution_1=[0.299, 0.004, 0.154, 0.037, 0.032, 0.014, 0.245, 0.194, 0.021] #E=3.6  
    # attacker_distribution_2=[0.22, 0.10, 0.003, 0.18, 0.005, 0.23, 0.13, 0.006, 0.126] #E=3.57
    attacker_distribution_2=[0,0,.5,.28,0,0,0,0,.22] #E=3.6

    G=[];
    # PL_without=[];T_without=[]
    PL1_with=[];T1_with=[]
    PL2_with=[];T2_with=[]
    # PL3_with=[];T3_with=[]
    # PL4_with=[];T4_with=[]

    for m in range(50,n+1,50):  #m :number of users
        attacker_num=math.ceil(0.05*m)
        print('simulating graph with',n,'slots and',m,'users...')
        # loss_prob_without=[];throughput_without=[]
        loss_prob1_with=[];throughput1_with=[]
        loss_prob2_with=[];throughput2_with=[]
        # loss_prob3_with=[];throughput3_with=[]
        # loss_prob4_with=[];throughput4_with=[]


        for j in range(count_avg):
            bursts,sums,edges,g=IRSA.bipartite_graph(n,m,distribution)
            g1_copy=g.copy()
            g2_copy=g.copy()
            # g3_copy=g.copy()
            # g4_copy=g.copy()

            # lost_without,decode_without=IRSA.SIC(g,bursts,sums)
            # loss_prob_without.append(len(lost_without)/int(m))
            # throughput_without.append(len(decode_without)/int(n))

            edges,g1_copy=attack.attacker(n,m,sums,edges,g1_copy,attacker_num,attacker_distribution_1)
            lost1_with,decode1_with=attack.SIC(g1_copy,bursts,sums)
            loss_prob1_with.append(len(lost1_with)/int(m))
            throughput1_with.append(len(decode1_with)/int(n))

            edges,g2_copy=attack.attacker(n,m,sums,edges,g2_copy,attacker_num,attacker_distribution_2)
            lost2_with,decode2_with=attack.SIC(g2_copy,bursts,sums)
            loss_prob2_with.append(len(lost2_with)/int(m))
            throughput2_with.append(len(decode2_with)/int(n))

            # edges,g3_copy=attack.attacker(n,m,sums,edges,g3_copy,attacker_num,attacker_distribution_3)
            # lost3_with,decode3_with=attack.SIC(g3_copy,bursts,sums)
            # loss_prob3_with.append(len(lost3_with)/int(m))
            # throughput3_with.append(len(decode3_with)/int(n))

            # edges,g4_copy=attack.attacker(n,m,sums,edges,g4_copy,attacker_num,attacker_distribution_4)
            # lost4_with,decode4_with=attack.SIC(g4_copy,bursts,sums)
            # loss_prob4_with.append(len(lost4_with)/int(m))
            # throughput4_with.append(len(decode4_with)/int(n))
           
        G.append(m/n)
        # PL_without.append(sum(loss_prob_without)/count_avg)
        # T_without.append(sum(throughput_without)/count_avg)
        PL1_with.append(sum(loss_prob1_with)/count_avg)
        T1_with.append(sum(throughput1_with)/count_avg)
        PL2_with.append(sum(loss_prob2_with)/count_avg)
        T2_with.append(sum(throughput2_with)/count_avg)
        # PL3_with.append(sum(loss_prob3_with)/count_avg)
        # T3_with.append(sum(throughput3_with)/count_avg)
        # PL4_with.append(sum(loss_prob4_with)/count_avg)
        # T4_with.append(sum(throughput4_with)/count_avg)

        print('T1:',max(T1_with),T1_with.index(max(T1_with)))
        print('T2:',max(T2_with),T2_with.index(max(T2_with)))

    
    def lambda_func(x,vector,D,LAMBDA_prime_1):
        lambda_=[]
        for i in range(D):
            lambda_.append(vector[i]*(i+1)/LAMBDA_prime_1)
        Sum=0
        for i in range(D):
            Sum+=lambda_[i]*(x**i)
        return Sum
    def LAMBDA_fun(x,vector,D):
        Sum=0
        for i in range(D):
            Sum+=vector[i]*(x**(i+1))
        return Sum
    def p_func(i,G,vector,D,LAMBDA_prime_1):
        if i==0:
            return 1
        else:
            return (1-np.exp(-G*LAMBDA_prime_1*lambda_func(p_func(i-1,G,vector,D,LAMBDA_prime_1),vector,D,LAMBDA_prime_1)))  
    Imax=1000
    LAMBDA_prime_1=0; D=8; PL_asymptotic=[]; T_asymptotic=[]
    for i in range(D):
        LAMBDA_prime_1+=(i+1)*distribution[i]
    for i in G:
        PL_asymptotic.append(LAMBDA_fun( p_func(Imax,i,distribution,D,LAMBDA_prime_1),distribution,D))
    for i in range(len(G)):
        T_asymptotic.append(G[i]*(1-PL_asymptotic[i]))

    plt.figure(1)  
    plt.plot(G,T_asymptotic,':',label='asymptotic IRSA without attacker')
    # plt.plot(G,T_without,'',label='simulation IRSA without attacker')
    plt.plot(G,T1_with,'--',label='simulation IRSA with attacker $\Lambda_1$(x)')
    plt.plot(G,T2_with,'-.',label='simulation IRSA with attacker $\Lambda_2$(x)')
    # plt.plot(G,T3_with,marker='.',label='simulation IRSA with attacker $\Lambda_3$(x)')
    # plt.plot(G,T4_with,marker='x',label='simulation IRSA with attacker $\Lambda_4$(x)')
    plt.xlabel('Normalized Offered Traffic,G')
    plt.ylabel('Normalized Throughput,T')
    plt.grid()
    plt.legend(fontsize=8)
    plt.savefig('throughput.jpeg')
    plt.figure(2)
    plt.plot(G,PL_asymptotic,':',label='asymptotic IRSA without attacker')
    # plt.plot(G,PL_without,'',label='simulation IRSA without attacker')
    plt.plot(G,PL1_with,'--',label='simulation IRSA with attacker $\Lambda_1$(x)')
    plt.plot(G,PL2_with,'-.',label='simulation IRSA with attacker $\Lambda_2$(x)')
    # plt.plot(G,PL3_with,marker='.',label='simulation IRSA with attacker $\Lambda_3$(x)')
    # plt.plot(G,PL4_with,marker='x',label='simulation IRSA with attacker $\Lambda_4$(x)')
    plt.xlabel('Normalized Offered Traffic,G')
    plt.ylabel('Packet Loss,PL')
    plt.grid()
    plt.legend(fontsize=9)
    plt.savefig('packet loss.jpeg')    
    plt.show()
    print('user_distribution:',distribution)
    print('attacker_distribution_1:',attacker_distribution_1)
    print('attacker_distribution_2:',attacker_distribution_2)
    # print('attacker_distribution_3:',attacker_distribution_3)
    # print('attacker_distribution_4:',attacker_distribution_4)

start_time=time.time()
if __name__ == "__main__":main()
end_time=time.time()
print('run time=',end_time-start_time)