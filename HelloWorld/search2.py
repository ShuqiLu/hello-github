# -*- coding: utf-8 -*-
from django.http import HttpResponse 
from django.shortcuts import render
from django.views.decorators import csrf
from neo4j.v1 import GraphDatabase
from django.core import serializers
import json
from TestModel.models import Test
from TestModel.models import news
def hello(request):
	url="bolt://10.48.150.47:7687"
	drive=GraphDatabase.driver(url,auth=("neo4j",123456))
	context = {}
	with drive.session()as session:
		with session.begin_transaction() as tx:
			mylist=[]
			for record in tx.run("match(a) where a.person1=\"习近平\" return a.person2"):
				mylist.append(record["a.person2"])
			context['hello'] = mylist[1]
			return render(request, 'hello.html', context) 
# 接收POST请求数据
def search_post(request):
    ctx ={}
    return render(request, "post.html", ctx)
def getpath(request):
    data2=[]
    if request.GET:
        url="bolt://10.48.150.47:7687"
        drive=GraphDatabase.driver(url,auth=("neo4j",'lushuqi'))
        start=request.GET['fname']
        print(str(start))
        with drive.session()as session:
            with session.begin_transaction() as tx:
                i=1
                data={}
                relation={}
                
                relation['0']=0
                flag=0
                for record in tx.run("MATCH p=(p1:person{name:'"+start+"'})-[r:friend]-(p2:person)with p2,r,p1 order by r.value DESC RETURN p2.name,p2.pagerank,p2.groupv,p1.name,p1.pagerank,p1.groupv,r.value limit 10"):
                    if flag==0:
                        mydic={}
                        mydic['name']=record["p1.name"]
                        mydic['pagerank']=record["p1.pagerank"]
                        mydic['group']=record["p1.groupv"]
                        data['0']=mydic
                        flag=1
                    mydic={}
                    mydic['name']=record["p2.name"]
                    mydic['pagerank']=record["p2.pagerank"]
                    mydic['group']=record["p2.groupv"]
                    data[str(i)]=mydic
                    #print(str(data[str(i)]))
                    relation[str(i)]=record["r.value"]
                    i=i+1
                if len(data)==0:
                    for record in tx.run("MATCH p=(p1:person{name:'"+start+"'}) return p1.name,p1.pagerank,p1.groupv"):
                        mydic={}
                        mydic['name']=record["p1.name"]
                        mydic['pagerank']=record["p1.pagerank"]
                        mydic['group']=record["p1.groupv"]
                        data[str(i)]=mydic  
                print(data)
                data2.append(data)
                data2.append(relation)
    return HttpResponse(json.dumps(data2),content_type="application/json")
def getpathten(request):
    data2=[]
    if request.GET:
        url="bolt://10.48.150.47:7687"
        drive=GraphDatabase.driver(url,auth=("neo4j",'lushuqi'))
        start=request.GET['fname']
        end=request.GET['tname']
        print(str(start))
        with drive.session()as session:
            with session.begin_transaction() as tx:
                i=0
                k=0
                t=0
                p_t=0
                nodes={}
                relation={}
                index={}
                path={}
                #MATCH (fromNodes:person) where fromNodes.name='李克强' MATCH (toNodes:person) where toNodes.name='扎克伯格' CALL apoc.algo.allSimplePaths(fromNodes, toNodes, 'friend',4) yield path RETURN path,reduce(a=1, r in rels(path) | a+r.value) as orders
#ORDER BY orders desc limit 10
                shortflag=0
                for record in tx.run("MATCH (martin:person { name:'"+start+"' }),(michael:person { name:'"+end+"'}), path = allShortestPaths((martin)-[*]-(michael)) RETURN path,nodes(path),relationships(path),reduce(a=1, r in rels(path) | a+r.value) as orders ORDER BY orders desc limit 10"):
                    shortflag=1
                    k=len(record["relationships(path)"])
                    if(len(record["nodes(path)"])!=0):
                        i+=1
                        print(i)
                    #print(type(record))
                    for j in range(len(record["nodes(path)"])):
                        if record["nodes(path)"][j]["id"] in nodes:
                            pass
                        else:
                            nodict={}
                            nodict['name']=record["nodes(path)"][j]["name"]
                            nodict['group']=record["nodes(path)"][j]["groupv"]
                            nodict['pagerank']=record["nodes(path)"][j]["pagerank"]
                            #nodes[record["nodes(path)"][j]["id"]]=record["nodes(path)"][j]["name"]
                            nodes[record["nodes(path)"][j]["id"]]=nodict
                            #index[str(i)]=record["nodes(path)"][j]["id"]
                    for j in range(len(record["nodes(path)"])-1):
                        mydic={}
                        flag=0
                        mypath={}
                        mypath['start']=record["nodes(path)"][j]["id"]
                        mypath['end']=record["nodes(path)"][j+1]["id"]
                        mypath['value']=record["relationships(path)"][j]["value"]
                        mypath['pathid']=i
                        path[str(p_t)]=mypath
                        #print('!!'+str(p_t)+' '+str(mypath))
                        p_t+=1
                        for x in relation:
                            if relation[x]['start']==record["nodes(path)"][j]["id"] and relation[x]['end']==record["nodes(path)"][j+1]["id"] and relation[x]['value']==record["relationships(path)"][j]["value"]:
                                flag=1
                                break
                        
                        if flag==0:
                            mydic['start']=record["nodes(path)"][j]["id"]
                            mydic['end']=record["nodes(path)"][j+1]["id"]
                            mydic['value']=record["relationships(path)"][j]["value"]
                            mydic['pathid']=i
                        
                            relation[str(t)]=mydic
                            t+=1
                    if i==10:
                        break
                front=0
                while i <10 and shortflag==1:
                    #front=i
                    k+=1
                    if k>5:
                        print(k)
                        break
                    for record in tx.run("MATCH (fromNodes:person) where fromNodes.name='"+start+"' MATCH (toNodes:person) where toNodes.name='"+end+"' CALL apoc.algo.allSimplePaths(fromNodes, toNodes, 'friend',"+str(k)+") yield path RETURN nodes(path),relationships(path),reduce(a=1, r in rels(path) | a+r.value) as orders ORDER BY orders desc limit 10"):
                        if len(record["relationships(path)"])==k:
                            if(len(record["nodes(path)"])!=0):
                                i+=1
                                print(i)
                            #print(type(record))
                            for j in range(len(record["nodes(path)"])):
                                if record["nodes(path)"][j]["id"] in nodes:
                                    pass
                                else:
                                    nodict={}
                                    nodict['name']=record["nodes(path)"][j]["name"]
                                    nodict['group']=record["nodes(path)"][j]["groupv"]
                                    nodict['pagerank']=record["nodes(path)"][j]["pagerank"]
                                    #nodes[record["nodes(path)"][j]["id"]]=record["nodes(path)"][j]["name"]
                                    nodes[record["nodes(path)"][j]["id"]]=nodict
                                    #index[str(i)]=record["nodes(path)"][j]["id"]
                            for j in range(len(record["nodes(path)"])-1):
                                mydic={}
                                flag=0
                                mypath={}
                                mypath['start']=record["nodes(path)"][j]["id"]
                                mypath['end']=record["nodes(path)"][j+1]["id"]
                                mypath['value']=record["relationships(path)"][j]["value"]
                                mypath['pathid']=i
                                path[str(p_t)]=mypath
                                #print(str(p_t)+' '+str(mypath))
                                p_t+=1
                                for x in relation:
                                    if relation[x]['start']==record["nodes(path)"][j]["id"] and relation[x]['end']==record["nodes(path)"][j+1]["id"] and relation[x]['value']==record["relationships(path)"][j]["value"]:
                                        flag=1
                                        break
                                
                                if flag==0:
                                    mydic['start']=record["nodes(path)"][j]["id"]
                                    mydic['end']=record["nodes(path)"][j+1]["id"]
                                    mydic['value']=record["relationships(path)"][j]["value"]
                                    mydic['pathid']=i
                                
                                    relation[str(t)]=mydic
                                    t+=1
                            if i==10:
                                break
                    '''
                    for j in range(len(record["relationships(path)"])):
                        relation[str(k)]=record["relationships(path)"][j]["value"]
                        k+=1
                    '''
                print(str(nodes))
                print(str(relation))
                print(path)
                data2.append(nodes)
                data2.append(relation)
                data2.append(path)
                '''
                list1 = Test.objects.filter(person1='习近平',person2='温家宝')
                for var in list1:
                    list2 = news.objects.filter(id=var.newid)
                    for var2 in list2:
                        print(str(var2.title))
                list1 = Test.objects.filter(person1='温家宝',person2='习近平')
                for var in list1:
                    list2 = news.objects.filter(id=var.newid)
                    for var2 in list2:
                        print(str(var2.title)) 
                '''  
                #data2.append(index)
    return HttpResponse(json.dumps(data2),content_type="application/json")
def getnews(request):
    data2=[]
    pnews={}
    #print('nbhn')
    if request.GET:
        print('jsdb')
        start=request.GET['fname']
        end=request.GET['tname']
        print(start)
        print(end)
        list1 = Test.objects.filter(person1=start,person2=end)
        i=0
        for var in list1:
            list2 = news.objects.filter(id=var.newid)
            for var2 in list2:
                mynews={}
                mynews['title']=var2.title
                mynews['context']=var2.context
                pnews[i]=mynews
                i+=1
        list1 = Test.objects.filter(person1=end,person2=start)
        for var in list1:
            list2 = news.objects.filter(id=var.newid)
            for var2 in list2:
                mynews={}
                mynews['title']=var2.title
                mynews['context']=var2.context
                pnews[i]=mynews
                i+=1
        print(i)
        #print(str(pnews))
        data2.append(pnews)
    return HttpResponse(json.dumps(data2),content_type="application/json")
'''
MATCH (fromNodes:person) where fromNodes.name='李克强' MATCH (toNodes:person) where toNodes.name='扎克伯格' CALL apoc.algo.allSimplePaths(fromNodes, toNodes, 'friend',4) yield path RETURN path,reduce(a=1, r in rels(path) | a+r.value) as orders
ORDER BY orders desc limit 10
'''