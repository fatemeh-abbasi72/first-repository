# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 22:52:15 2019

@author: Fateme
"""
import igraph as ig
import random
import matplotlib.pyplot as plt
import cProfile
import pstats
import statistics
import os

def bipartite_graph(n,m,distribution):
    sums=[i for i in range(n)]
    bursts=[i+n for i in range(m)]
    edges=[]
    for i in bursts:
        x=random.random()
        if x>=0 and x<distribution[0]:
            burst_num=1
        elif x>=distribution[0] and x<sum(distribution[:2]):
            burst_num=2
        elif x>=sum(distribution[:2]) and x<sum(distribution[:3]):
            burst_num=3
        elif x>=sum(distribution[:3]) and x<sum(distribution[:4]):
            burst_num=4
        elif x>=sum(distribution[:4]) and x<sum(distribution[:5]):
            burst_num=5
        elif x>=sum(distribution[:5]) and x<sum(distribution[:6]):
            burst_num=6
        elif x>=sum(distribution[:6]) and x<sum(distribution[:7]):
            burst_num=7
        else:
            burst_num=8
            
        for item in random.sample(sums,burst_num): 
            edges.append((i,item))

    bipartite_type=[0 for i in range(n)]
    for i in range(m):bipartite_type.append(1)
    g=ig.Graph.Bipartite(bipartite_type,edges)
    # if not os.path.exists('result'):
    #     os.mkdir('result')
    # else:
    #     os.chdir('C:/Users/Fateme/.spyder-py3/tez/result')
    #     for filename in os.listdir():
    #         os.remove(filename)
    # layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
    # g.vs[:n]['label']=['s{}'.format(i) for i in range(n)]
    # g.vs[n:]['label']=['b{}'.format(i) for i in range(m)]
    # g.vs[:n]['color']=['blue'] ; g.vs[n:]['color']=['orange']
    # # ig.plot(g,'graph{} without attacker.png'.format(m+n),layout=layout)
    return bursts,sums,edges,g

def get_first_one_degree_node(g,sums):
    try: 
        return sums[g.degree(sums).index(1)]
    except: 
        return "Finish"
    
    # for i in sums:
    #     if g.degree(i)==1:
    #         return i
    # else:
    #     return 'Finish'
    
'''
SIC_model_(perfect): if now_degree=1 : decode
'''
def SIC(g,bursts,sums):
    decode=[] ; lost=[]
    # itr=0
    one_degree_node = get_first_one_degree_node(g,sums)
    while one_degree_node != "Finish":
        # itr+=1
        neighbor=g.neighbors(one_degree_node)
        neighbor_neighbor=g.neighbors(neighbor[0])
        for y in neighbor_neighbor:
            g.delete_edges((neighbor[0],y))
        decode.append(neighbor[0])
        one_degree_node = get_first_one_degree_node(g,sums)
        # layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
        # ig.plot(g,'SIC{} without attacker.png'.format(itr),layout=layout)        
    lost=list(set(bursts)-set(decode))
    return lost,decode
    
'''
SIC_model_(imperfect-1): if now_degree=1 and first_degree<5 : decode
'''
#def SIC(g,bursts,sums):    
#    first_degree=[g.degree(i) for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    decodable_nodes=[i for i in sums if g.degree(i)==1]
#    while len(decodable_nodes)!=0:
#        itr=itr+1
#        x=decodable_nodes[0]
#        neighbor=g.neighbors(x)
#        neighbor_neighbor=g.neighbors(neighbor[0])
#        for y in neighbor_neighbor:
#            g.delete_edges((neighbor[0],y))
#        decode.append(neighbor[0])
#        decodable_nodes=[i for i in sums if g.degree(i)==1 and first_degree[i] in [1,2,3,4]]
##        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##        ig.plot(g,'SIC{} without attacker.png'.format(itr),layout=layout)        
#    lost=list(set(bursts)-set(decode))
#    return lost,decode
    
'''
SIC_model_(imperfect-2): if now_degree=1 and ... : decode
'''
#def SIC(g,bursts,sums):
#    first_degree=[g.degree(i) for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    one_degree_nodes=[i for i in sums if g.degree(i)==1]
#    while len(one_degree_nodes)!=0:
#        itr+=1
#        x=one_degree_nodes[0]
#        g.vs[x]['check']='true'
#        neighbor=g.neighbors(x)
#        neighbor_neighbor=g.neighbors(neighbor[0])
#        r=random.random()
#        if first_degree[x]==1 or (first_degree[x]==2 and r<0.9) or (first_degree[x]==3 and r<0.8) or (first_degree[x]==4 and r<0.7) or (first_degree[x]==5 and r<0.6) or (first_degree[x]==6 and r<0.5) or (first_degree[x]==7 and r<0.4) or (first_degree[x]==8 and r<0.3) or (first_degree[x]==9 and r<0.2) or (first_degree[x]==10 and r<0.1):
#            for y in neighbor_neighbor:
#                g.delete_edges((y,neighbor[0]))
#            decode.append(neighbor[0])
#        one_degree_nodes=[i for i in sums if g.degree(i)==1 and g.vs[i]['check']!='true']
##        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##        ig.plot(g,'SIC{} without attacker.png'.format(itr),layout=layout)        
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-3): if now_degree=1 and SINR > threshold... : decode
'''
#def SIC(g,bursts,sums):
#    user_power=1.5
#    threshold=1
#    white_noise=1
#    
#    first_degree=[g.degree(i) for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    one_degree_nodes=[i for i in sums if g.degree(i)==1]
#    while len(one_degree_nodes)!=0:
#        itr+=1
#        x=one_degree_nodes[0]
#        neighbor=g.neighbors(x)
#        neighbor_neighbor=g.neighbors(neighbor[0])
#        g.vs[x]['check']='true'
#        residual_interference=(first_degree[x]-1)*0.05*user_power
#        if user_power/(white_noise+residual_interference)>=threshold: 
#            for y in neighbor_neighbor:
#                g.delete_edges((y,neighbor[0]))
#            decode.append(neighbor[0])
#        one_degree_nodes=[i for i in sums if g.degree(i)==1 and g.vs[i]['check']!='true']
##        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##        ig.plot(g,'SIC{} without attacker.png'.format(itr),layout=layout)        
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-4-5-6-7): if SINR > threshold... : decode
'''
#def SIC(g,bursts,sums):
#    user_power=2
#    threshold=1
#    white_noise=1
#    first_degree=[g.degree(i) for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    MAX_ITERATION=20
#    while MAX_ITERATION!=0:
#        for x in sums:
#            decoded_num=first_degree[x]-g.degree(x)
#            undecod_num=first_degree[x]-decoded_num
#            if g.degree(x)!=0: 
#                residual_interference=(decoded_num*0.05*user_power)+((undecod_num-1)*user_power)
#                if user_power/(white_noise+residual_interference)>=threshold:
#                    itr+=1     
#                    neighbor=g.neighbors(x)                                    
#                    for y in neighbor:
#                        neighbor_neighbor=g.neighbors(y)                   
#                        for z in neighbor_neighbor:
#                            g.delete_edges((z,y))
#                        decode.append(y)   
##                        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##                        ig.plot(g,'SIC{} without attacker.png'.format(itr),layout=layout)
#        MAX_ITERATION-=1
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(perfect SINR): if SINR > threshold... : decode
'''
#def SIC(g,bursts,sums):
#    user_power=1.75
#    threshold=1
#    white_noise=1
#    first_degree=[g.degree(i) for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    MAX_ITERATION=20
#    while MAX_ITERATION!=0:
#        for x in sums:
#            decoded_num=first_degree[x]-g.degree(x)
#            undecod_num=first_degree[x]-decoded_num
#            if g.degree(x)!=0: 
#                others_interference=(undecod_num-1)*user_power
#                if user_power/(white_noise+others_interference)>=threshold:
#                    itr+=1     
#                    neighbor=g.neighbors(x)                                    
#                    for y in neighbor:
#                        neighbor_neighbor=g.neighbors(y)                   
#                        for z in neighbor_neighbor:
#                            g.delete_edges((z,y))
#                        decode.append(y)   
##                        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##                        ig.plot(g,'SIC{} without attacker.png'.format(itr),layout=layout)
#        MAX_ITERATION-=1
#    lost=list(set(bursts)-set(decode))
#    return lost,decode


def main(n):
    profile = cProfile.Profile()
    profile.enable()

#    n=500 #size of frame
    count_avg=100
    # distribution=[0,.5,.28,0,0,0,0,.22]  #G*=0.93
    distribution=[0.22817564739737126, 0.07377107213151146, 0.024715850146525484, 0.1325074867649615, 0.0460650660145079, 0.12474837905515526, 0.06062671042946558, 0.09278765838533587, 0.21660212967516554] 
    # distribution=[0.4468768706695535, 0.17094188201999724, 0.0, 0.007274161475789276, 
            # 0.012665143306364136, 0.0, 0.08341146719564764, 0.2788304753326484]
    # distribution=[0.7385524342439916, 0.00318720287777708, 0.0, 0.0,
            # 0.04798662267998596, 0.0, 0.18830535959975858, 0.021968380598486627]
    # distribution=[0.6809380520732157, 0.019461935305703004, 0.0, 0.031482589406470765, 
            # 0.1000327258251083, 0.0, 0.0553092287080224, 0.1127754686814798]
    # distribution=[0.37421399387530097, 0.18131625922658298, 0.03879328288274909, 0.10186555667457194, 
            # 0.011279509256265877, 0.026381026196874102, 0.0678127390995006, 0.19833763278815464]
    G=[] ; PL=[] ; T=[]
#    ethroughput=[];eloss_prob=[]
    for m in range(50,n+1,50):  #number of users
        print('simulating graph with',n,'slots and',m,'users...')
        loss_prob=[] ; throughput=[]
        for j in range(count_avg):
            bursts,sums,edges,g=bipartite_graph(n,m,distribution)
            lost,decode=SIC(g,bursts,sums)
            loss_prob.append(len(lost)/int(m))
            throughput.append(len(decode)/int(n))
#        ethroughput.append(statistics.stdev(throughput))
#        eloss_prob.append(statistics.stdev(loss_prob))
        G.append(m/n)
        T.append(sum(throughput)/count_avg)
        PL.append(sum(loss_prob)/count_avg)        
    print(max(T))  
#    Gstar=0
#    for i in range(len(G)-3):
##        if T[i]>T[i+1] and T[i+1]>T[i+2] and T[i+2]>T[i+3]:
#        if T[i]>T[i+1] and T[i+1]>T[i+2]:
#            Gstar=G[i]
#            break
    plt.figure(1)
    plt.plot(G,T,marker='o')
#    plt.errorbar(G,T, ethroughput, linestyle='-', marker='o' ,capsize=5)
    plt.xlabel('Normalized Offered Traffic,G')
    plt.ylabel('Normalized Throughput,T')
    plt.grid()
#    plt.legend()
    plt.figure(2)
    plt.plot(G,PL,marker='*')
#    plt.errorbar(G,PL, eloss_prob, linestyle='-', marker='*' ,capsize=5)
    plt.xlabel('Normalized Offered Traffic,G')
    plt.ylabel('Packet Loss Probability,PL')
#    plt.yscale('log')
    plt.grid()
#    plt.legend()
    plt.show()
#    print(distribution)    
#    print('G*=',Gstar)
    
    ps = pstats.Stats(profile)
    ps.sort_stats('cumtime') 
    ps.print_stats(10)
    profile.disable()
    
if __name__ == "__main__":main(1000)
#if __name__ == "__main__":main(200,1)
#if __name__ == "__main__":main(200,1.5)
#if __name__ == "__main__":main(200,2)
