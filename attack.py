# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 21:48:05 2019

@author: Fateme
"""
import IRSA
import random
import matplotlib.pyplot as plt
import igraph as ig
import math
import cProfile
import pstats

def attacker(n,m,sums,edges,g,attacker_num,attacker_distribution):
    for i in range(attacker_num):
        g.add_vertex(m+n+i,type=True,label='attacker')
        x=random.random()
        
        if x>=0 and x<attacker_distribution[0]:
            burst_num=0
        elif x>=attacker_distribution[0] and x<sum(attacker_distribution[:2]):
            burst_num=1
        elif x>=sum(attacker_distribution[:2]) and x<sum(attacker_distribution[:3]):
            burst_num=2
        elif x>=sum(attacker_distribution[:3]) and x<sum(attacker_distribution[:4]):
            burst_num=3
        elif x>=sum(attacker_distribution[:4]) and x<sum(attacker_distribution[:5]):
            burst_num=4
        elif x>=sum(attacker_distribution[:5]) and x<sum(attacker_distribution[:6]):
            burst_num=5
        elif x>=sum(attacker_distribution[:6]) and x<sum(attacker_distribution[:7]):
            burst_num=6
        elif x>=sum(attacker_distribution[:7]) and x<sum(attacker_distribution[:8]):
            burst_num=7
        elif x>=sum(attacker_distribution[:8]) and x<sum(attacker_distribution[:9]):
            burst_num=8
            
        if burst_num!=0:         
            for item in random.sample(sums,burst_num): 
                edges.append((m+n+i,item))
                g.add_edge(m+n+i,item,color='red')

    # layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
    # ig.plot(g,'graph{} with attacker.png'.format(m+n),layout=layout)      
    return edges,g

def get_first_one_degree_node(g,sums):    
            
    for i in sums:
        if g.degree(i)==1 and g.vs[g.neighbors(i)[0]]['label']!='attacker':
            return i
    else:
        return 'Finish'
    
    # i=-1
    # for deg in g.degree(sums):
    #     i+=1
    #     if deg==1 and g.vs[g.neighbors(i)[0]]['label'] != 'attacker' :
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
        # ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)        
    lost=list(set(bursts)-set(decode))
    return lost,decode

'''
SIC_model_(imperfect-1): if now_degree=1 and first_degree<5 : decode
'''
#def SIC(g,bursts,sums): 
#    first_degree=[g.degree(i) for i in sums]   
#    decode=[] ; lost=[]
#    itr=0
#    decodable_nodes=[i for i in sums if g.degree(i)==1 and g.vs[g.neighbors(i)[0]]['label']!='attacker']
#    while len(decodable_nodes)!=0:
#        itr=itr+1
#        x=decodable_nodes[0]
#        neighbor=g.neighbors(x)
#        neighbor_neighbor=g.neighbors(neighbor[0])
#        for y in neighbor_neighbor:
#            g.delete_edges((neighbor[0],y))
#        decode.append(neighbor[0])
#        decodable_nodes=[i for i in sums if g.degree(i)==1 and g.vs[g.neighbors(i)[0]]['label']!='attacker' and first_degree[i] in [1,2,3,4]] 
##        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##        ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)        
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-2): if now_degree=1 and ... : decode
'''
#def SIC(g,bursts,sums):
#    first_degree=[g.degree(i) for i in sums]   
#    decode=[] ; lost=[]
#    itr=0
#    one_degree_nodes=[i for i in sums if g.degree(i)==1 and g.vs[g.neighbors(i)[0]]['label']!='attacker']
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
#        one_degree_nodes=[i for i in sums if g.degree(i)==1 and g.vs[g.neighbors(i)[0]]['label']!='attacker' and g.vs[i]['check']!='true']
##        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##        ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)        
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-3): if now_degree=1 and SINR > threshold... : decode
'''
#def SIC(g,bursts,sums):
#    user_power=1.5
#    attacker_power=0.25
#    threshold=1
#    white_noise=1
#    attacker_list=[]
#    for i in sums:
#        attackers=0
#        for j in g.neighbors(i):
#            if g.vs[j]['label']=='attacker':
#                attackers+=1
#        attacker_list.append(attackers)
#    first_degree=[g.degree(i)-attacker_list[i] for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    one_degree_nodes=[i for i in sums if (g.degree(i)-attacker_list[i])==1]
#    while len(one_degree_nodes)!=0:
#        itr+=1
#        x=one_degree_nodes[0]
#        neighbor=g.neighbors(x)         
#        neighbor_neighbor=g.neighbors(neighbor[0])  #neighbor[0] always is only one user; because of its small ID than attacker(s) ID
#        g.vs[x]['check']='true'
#        residual_interference=(first_degree[x]-1)*0.05*user_power
#        if user_power/(white_noise+attacker_list[x]*attacker_power+residual_interference)>=threshold: 
#            for y in neighbor_neighbor:
#                g.delete_edges((y,neighbor[0]))
#            decode.append(neighbor[0])
#        one_degree_nodes=[i for i in sums if (g.degree(i)-attacker_list[i])==1 and g.vs[i]['check']!='true']
##        layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##        ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)        
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-4): if SINR > threshold... : decode
'''
#def SIC(g,bursts,sums):
#    user_power=2
#    attacker_power=1
#    threshold=1 
#    white_noise=1
#    attacker_list=[]
#    for i in sums:
#        attackers=0
#        for j in g.neighbors(i):
#            if g.vs[j]['label']=='attacker':
#                attackers+=1
#        attacker_list.append(attackers)
#    first_degree=[g.degree(i)-attacker_list[i] for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    MAX_ITERATION=20
#    while MAX_ITERATION!=0:
#        for x in sums:
#            decoded_num=first_degree[x]-(g.degree(x)-attacker_list[x])
#            undecod_num=first_degree[x]-decoded_num
#            if g.degree(x)!=0 and first_degree[x]!=0 and undecod_num!=0: 
#                residual_interference=(decoded_num*0.05*user_power)+((undecod_num-1)*user_power)
##                print(x,decoded_num,undecod_num,attacker_list[x])
#                if user_power/(white_noise+attacker_list[x]*attacker_power+residual_interference)>=threshold:
#                    itr+=1     
#                    neighbor=g.neighbors(x)                                    
#                    for y in neighbor:
#                        if g.vs[y]['label']!='attacker':                       
#                            neighbor_neighbor=g.neighbors(y)                   
#                            for z in neighbor_neighbor:
#                                g.delete_edges((z,y))
#                            decode.append(y)         
##                            layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##                            ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)
#        MAX_ITERATION-=1
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-5): if SINR > threshold... : decode , with different attacker power (ravesh ghalat)
'''
#def SIC(g,bursts,sums):
#    user_power=2
#    attacker_power=4
#    threshold=1
#    white_noise=1
#    
#    m=len(bursts) ; n=len(sums)
#    for i in range(m+n,len(g.vs),1):
#        if g.vs[i].degree()!=0:
#            g.vs[i]['power']=attacker_power/g.vs[i].degree()
#        else:
#            g.vs[i]['power']=0
##    print(g.vs[m+n:]['power'])
#
#    attackers_num_list=[]
#    attackers_index_list=[]
#    for i in sums:
#        attackers_num=0
#        attackers_index=[]
#        for j in g.neighbors(i):
#            if g.vs[j]['label']=='attacker':
#                attackers_num+=1
#                attackers_index.append(g.vs[j].index)
#        attackers_num_list.append(attackers_num)
#        attackers_index_list.append(attackers_index)
##    print(attackers_num_list,'\n')
##    print(attackers_index_list,'\n')
#    
#    first_degree=[g.degree(i)-attackers_num_list[i] for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    MAX_ITERATION=20
#    while MAX_ITERATION!=0:
#        for x in sums:
#            decoded_num=first_degree[x]-(g.degree(x)-attackers_num_list[x])
#            undecod_num=first_degree[x]-decoded_num
#            if g.degree(x)!=0 and first_degree[x]!=0 and undecod_num!=0: 
#                residual_interference=(decoded_num*0.05*user_power)+((undecod_num-1)*user_power)
#                
#                attacker_interference=0
#                if attackers_num_list[x]!=0:
#                    for i in attackers_index_list[x]:
#                        attacker_interference+=g.vs[i]['power']
##                print(attacker_interference,attackers_num_list[x],attackers_index_list[x])
#                if user_power/(white_noise+attacker_interference+residual_interference)>=threshold:
##                    print(user_power,white_noise+attacker_interference+residual_interference,white_noise,attacker_interference,residual_interference)
#                    itr+=1     
#                    neighbor=g.neighbors(x)                                    
#                    for y in neighbor:
#                        if g.vs[y]['label']!='attacker':                       
#                            neighbor_neighbor=g.neighbors(y)                   
#                            for z in neighbor_neighbor:
#                                g.delete_edges((z,y))
#                            decode.append(y)         
##                            layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##                            ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)
#        MAX_ITERATION-=1
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-6): if SINR > threshold... : decode , with different attacker power
                            2-floor: 2,4      with equal/non-equal probability
                            3-floor: 2,4,6    with equal/non-equal probability
'''
#def SIC(g,bursts,sums):
#    user_power=2
#    threshold=1
#    white_noise=1
#    
#    m=len(bursts) ; n=len(sums)
#    for i in range(m+n,len(g.vs),1):
#        x=random.random()
#        if x>=0 and x<0.33:
#            g.vs[i]['power']=2
#        elif x>=0.33 and x<0.66:
#            g.vs[i]['power']=4
#        else:
#            g.vs[i]['power']=6
##    print(g.vs[m+n:]['power'])
#
#    attackers_num_list=[]
#    attackers_index_list=[]
#    for i in sums:
#        attackers_num=0
#        attackers_index=[]
#        for j in g.neighbors(i):
#            if g.vs[j]['label']=='attacker':
#                attackers_num+=1
#                attackers_index.append(g.vs[j].index)
#        attackers_num_list.append(attackers_num)
#        attackers_index_list.append(attackers_index)
##    print(attackers_num_list,'\n')
##    print(attackers_index_list,'\n')
#    
#    first_degree=[g.degree(i)-attackers_num_list[i] for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    MAX_ITERATION=20
#    while MAX_ITERATION!=0:
#        for x in sums:
#            decoded_num=first_degree[x]-(g.degree(x)-attackers_num_list[x])
#            undecod_num=first_degree[x]-decoded_num
#            if g.degree(x)!=0 and first_degree[x]!=0 and undecod_num!=0: 
#                residual_interference=(decoded_num*0.05*user_power)+((undecod_num-1)*user_power)
#                
#                attacker_interference=0
#                if attackers_num_list[x]!=0:
#                    for i in attackers_index_list[x]:
#                        attacker_interference+=g.vs[i]['power']
##                print(attacker_interference,attackers_num_list[x],attackers_index_list[x])
#                if user_power/(white_noise+attacker_interference+residual_interference)>=threshold:
##                    print(user_power,white_noise+attacker_interference+residual_interference,white_noise,attacker_interference,residual_interference)
#                    itr+=1
#                    neighbor=g.neighbors(x)
#                    for y in neighbor:
#                        if g.vs[y]['label']!='attacker':                       
#                            neighbor_neighbor=g.neighbors(y)                   
#                            for z in neighbor_neighbor:
#                                g.delete_edges((z,y))
#                            decode.append(y)         
##                            layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##                            ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)
#        MAX_ITERATION-=1
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

'''
SIC_model_(imperfect-7): if SINR > threshold...: decode , with different attacker power (imperfect SINR)
'''
# def SIC(g,bursts,sums,attacker_power):
#     user_power=2
#     threshold=1
#     white_noise=1
    # 
#    m=len(bursts) ; n=len(sums)
#    for i in range(m+n,len(g.vs),1):
#        g.vs[i]['power']=attacker_power[g.vs[i].degree()]
##    print(g.vs[m+n:]['power'])
#
#    attackers_num_list=[]
#    attackers_index_list=[]
#    for i in sums:
#        attackers_num=0
#        attackers_index=[]
#        for j in g.neighbors(i):
#            if g.vs[j]['label']=='attacker':
#                attackers_num+=1
#                attackers_index.append(g.vs[j].index)
#        attackers_num_list.append(attackers_num)
#        attackers_index_list.append(attackers_index)
##    print(attackers_num_list,'\n')
##    print(attackers_index_list,'\n')
#    
#    first_degree=[g.degree(i)-attackers_num_list[i] for i in sums]
#    decode=[] ; lost=[]
#    itr=0
#    MAX_ITERATION=20
#    while MAX_ITERATION!=0:
#        for x in sums:
#            decoded_num=first_degree[x]-(g.degree(x)-attackers_num_list[x])
#            undecod_num=first_degree[x]-decoded_num
#            if g.degree(x)!=0 and first_degree[x]!=0 and undecod_num!=0: 
#                residual_interference=(decoded_num*0.05*user_power)+((undecod_num-1)*user_power)
#                
#                attacker_interference=0
#                if attackers_num_list[x]!=0:
#                    for i in attackers_index_list[x]:
#                        attacker_interference+=g.vs[i]['power']
##                print(attacker_interference,attackers_num_list[x],attackers_index_list[x])
#                if user_power/(white_noise+attacker_interference+residual_interference)>=threshold:
##                    print(user_power,white_noise+attacker_interference+residual_interference,white_noise,attacker_interference,residual_interference)
#                    itr+=1
#                    neighbor=g.neighbors(x)
#                    for y in neighbor:
#                        if g.vs[y]['label']!='attacker':                       
#                            neighbor_neighbor=g.neighbors(y)                   
#                            for z in neighbor_neighbor:
#                                g.delete_edges((z,y))
#                            decode.append(y)         
##                            layout=g.layout_bipartite(hgap=1,vgap=1,maxiter=1000)
##                            ig.plot(g,'SIC{} with attacker.png'.format(itr),layout=layout)
#        MAX_ITERATION-=1
#    lost=list(set(bursts)-set(decode))
#    return lost,decode

def main():
    profile = cProfile.Profile()
    profile.enable()
    
#    attacker_distribution=[0,0,.5,0,.25,0,0,0,.25]
    # attacker_distribution=[.25,0,0,0,.5,0,0,0,.25]
    # attacker_distribution=[0,0,.5,.28,0,0,0,0,.23]
    # attacker_distribution=[0,0,0,0,0,0,0,0,1]
    attacker_distribution=[0.10918568997389266, 0.06258929268902025, 0.11960422478815005, 0.23251135394403272, 0.19974643406900713, 0.01532550408221428, 0.18056060974012528, 0.002123844933730853, 0.07835304577982677]
    n=200 #size of frame
    count_avg=100
    distribution=[0,.5,.28,0,0,0,0,.22]  #G*=0.93
    G=[];PL=[];T=[]
    for m in range(10,n+1,10):  #number of users
        attacker_num=math.ceil(0.05*m)
        print('simulating graph with',n,'slots and',m,'users...')
        loss_prob=[];throughput=[]
        for j in range(count_avg):
            bursts,sums,edges,g=IRSA.bipartite_graph(n,m,distribution)
            edges,g=attacker(n,m,sums,edges,g,attacker_num,attacker_distribution)
            lost,decode=SIC(g,bursts,sums)
            loss_prob.append(len(lost)/int(m))
            throughput.append(len(decode)/int(n))
        G.append(m/n)
        PL.append(sum(loss_prob)/count_avg)
        T.append(sum(throughput)/count_avg)
    print(max(T),T.index(max(T)))

    plt.figure(1)
    plt.plot(G,T,marker='o')
    plt.xlabel('Normalized Offered Traffic,G')
    plt.ylabel('Normalized Throughput,T')
    plt.grid()
    plt.figure(2)
    plt.plot(G,PL,marker='*')
    plt.xlabel('Normalized Offered Traffic,G')
    plt.ylabel('PL')
    # plt.yscale('log')
    plt.grid()
    plt.show()
    # print('user_distribution:',distribution)
    # print('attacker_distribution',attacker_distribution)

    ps = pstats.Stats(profile)
    ps.sort_stats('cumtime') 
    ps.print_stats(10)
    profile.disable()

if __name__ == "__main__":main()