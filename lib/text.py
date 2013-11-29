__author__ = 'Yovanni'

from operator import itemgetter
#from evospace import *
from lib.evospace import *
import random
import numpy
import sys

def current_fitness(fitness):
    return sum([fitness[k] for k in fitness])

def few_views(pop, views = 2, count = 2):
    return sum([1 for i in pop["sample"] if i["views"]>=views]) < count

def calc_fitness(pop):
    for ind in pop["sample"]:
        if ind['views'] > 0:
            ind['currentFitness'] = ( int(current_fitness(ind['fitness'])) + 1 ) / (float(ind['views'])+1)
        else:
            ind['currentFitness'] = None
    return pop

def init_pop(populationSize):
    #populationSize = 5 #esta variable se recibe como parametro
    listSize = 15 #esta variable se recibe como parametro
    chrome = [] #variable local
    limitmax = [150,80,1,1,1,1,4,1,1,1,3,1,1,2,3] #variable local
    limitmin = [10,5,0,0,0,0,0,0,0,0,0,0,0,0,0]#variable local
    server = Population()
    server.initialize()
    for individual in range(populationSize):
        for indice in range(listSize):
            aux = random.randint(limitmin[indice],limitmax[indice])
            chrome.insert(indice,aux)
        individual = {"id":None,"fitness":{"DefaultContext":0.0 },"chromosome":chrome,"views":0}
        server.put_individual(**individual)
        print chrome
        for x in chrome[:]: #inicializa la lista
            chrome.remove(x)

def get_sample(sample_size, popName= "pop" ):
    server = Population(popName)
    sample = server.get_sample(sample_size)
    return sample

def put_sample(sample_id, sample, popName="pop"):
    result = {'sample_id':sample_id , 'sample': sample}
    server = Population(popName)
    #   server.put_sample(json.dumps(result))
    server.put_sample(result)


def cross_simple(papa,mama):
    listSize = len(papa["chromosome"])

    #convertir a arreglos papa y mama
    papa["chromosome"] = numpy.array(papa["chromosome"])
    mama["chromosome"] = numpy.array(mama["chromosome"])

    cut = random.randint(0,listSize)
    if cut == 0: #Si la dimension es 1
        papa_cut1 = papa["chromosome"][cut]
        mama_cut1 = mama["chromosome"][cut]
        papa_cut2 = papa["chromosome"][cut+1:]
        mama_cut2 = mama["chromosome"][cut+1:]
        child1 = numpy.hstack((papa_cut1,mama_cut2))
        child2 = numpy.hstack((mama_cut1,papa_cut2))
    else:
        papa_cut1 = papa["chromosome"][:cut]
        mama_cut1 = mama["chromosome"][:cut]
        papa_cut2 = papa["chromosome"][cut:]
        mama_cut2 = mama["chromosome"][cut:]
        child1 = numpy.hstack((papa_cut1,mama_cut2))
        child2 = numpy.hstack((mama_cut1,papa_cut2))

    papa["chromosome"] = list(papa["chromosome"])
    mama["chromosome"] = list(mama["chromosome"])
    child1 = list(child1)
    child2 = list(child2)
    child1 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child1,
              'papa': papa["id"], 'mama':mama["id"] ,
              'crossover':'crossHorizontal:'+str(cut) }
    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2,
              'papa': papa["id"], 'mama':mama["id"],
              'crossover':'crossHorizontal:'+str(cut) }

    print (papa["chromosome"])
    print (mama["chromosome"])
    print cut
    print ("hijo 1 ",child1["chromosome"])
    print ("hijo 2 ",child2["chromosome"])
    return child1,child2

def cross_doble(papa,mama):
    listSize = len(papa["chromosome"])

    #convertir a arreglos papa y mama
    papa["chromosome"] = numpy.array(papa["chromosome"])
    mama["chromosome"] = numpy.array(mama["chromosome"])

    cut = random.randint(0,listSize - 1)
    cut2 = random.randint(cut + 1,listSize)
    if cut == 0: #Si la dimension es 1
        papa_cut1 = papa["chromosome"][cut]
        mama_cut1 = mama["chromosome"][cut]
        papa_cut2 = papa["chromosome"][cut+1:cut2 - 1]
        mama_cut2 = mama["chromosome"][cut+1:cut2 - 1]
        papa_cut3 = papa["chromosome"][cut2:]
        mama_cut3 = mama["chromosome"][cut2:]
        child1 = numpy.hstack((papa_cut1,mama_cut2,papa_cut3))
        child2 = numpy.hstack((mama_cut1,papa_cut2,mama_cut3))
    else:
        papa_cut1 = papa["chromosome"][:cut + 1]
        mama_cut1 = mama["chromosome"][:cut + 1]
        papa_cut2 = papa["chromosome"][cut:cut2 - 1]
        mama_cut2 = mama["chromosome"][cut:cut2 - 1]
        papa_cut3 = papa["chromosome"][cut2:]
        mama_cut3 = mama["chromosome"][cut2:]
        child1 = numpy.hstack((papa_cut1,mama_cut2,papa_cut3))
        child2 = numpy.hstack((mama_cut1,papa_cut2,mama_cut3))

    papa["chromosome"] = list(papa["chromosome"])
    mama["chromosome"] = list(mama["chromosome"])
    child1 = list(child1)
    child2 = list(child2)
    child1 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child1,
              'papa': papa["id"], 'mama':mama["id"] ,
              'crossover':'crossHorizontal:'+str(cut) }
    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2,
              'papa': papa["id"], 'mama':mama["id"],
              'crossover':'crossHorizontal:'+str(cut) }
    print (papa)
    print (mama)
    print ("hijos")
    print (child1)
    print (child2)

    return child1,child2


def mutacion_ran(individual):
    limit = [200,80,1,1,1,1,4,1,1,1,3,1,1,2,3]
    #print individual #este print solo es de control, no es necesario
    indice = 2#random.randint(0,14)
    print indice #este print solo es de control, no es necesario
    individual["chromosome"][indice] = random.randint(0,limit[indice])
    print individual #este print solo es de control, no es necesario
    return individual

def mutacion_aprox(individual):
    limit = [200,80,1,1,1,1,4,1,1,1,3,1,1,2,3]
    #print individual #este print solo es de control, no es necesario
    indice = random.randint(0,13)
    if (indice == 0) and (individual["chromosome"][indice] >= 195):
        individual["chromosome"][indice] = individual["chromosome"][indice] - 5
    elif(indice == 0):
        individual["chromosome"][indice] = individual["chromosome"][indice] + 5
    elif(indice == 1)and (individual["chromosome"][indice] >= 75):
        individual["chromosome"][indice] = individual["chromosome"][indice] - 5
    elif(indice == 1):
         individual["chromosome"][indice] = individual["chromosome"][indice] + 5
    elif(indice == 6)and (individual["chromosome"][indice] >= 4):
        individual["chromosome"][indice] = 0
    elif(indice == 6):
         individual["chromosome"][indice] = individual["chromosome"][indice] + 1
    elif(indice == 10)and (individual["chromosome"][indice] >= 3):
        individual["chromosome"][indice] = 0
    elif(indice == 10):
         individual["chromosome"][indice] = individual["chromosome"][indice] + 1
    elif(indice == 13)and (individual["chromosome"][indice] >= 3):
        individual["chromosome"][indice] = 0
    elif(indice == 13):
         individual["chromosome"][indice] = individual["chromosome"][indice] + 1
    else:
        if(individual["chromosome"][indice] == 0):
            individual["chromosome"][indice] = 1
        else:
            individual["chromosome"][indice] = 0
    print indice #este print solo es de control, no es necesario
    print individual #este print solo es de control, no es necesario
    return individual

def reprieve(individual):
    if len(individual["fitness"]) <= 2:
        return True
    else:
        return False

def evolve(sample_size=16 ):
    sample = get_sample(sample_size)
    pop = calc_fitness(sample)
    pop["sample"].sort(key=itemgetter('currentFitness'), reverse=True)

    for i in pop["sample"]:
        print i["id"], i["currentFitness"],
        if "views" in i.keys():
            print i["views"]

    offspring = pop["sample"][:sample_size/2]
    out = pop["sample"][sample_size/2:]

    #crossFunctions = [crossVertical]
    crossFunctions = [crossVertical,crossHorizontal,crossMirrorH,crossMirrorV,crossMirrorH,crossMirrorV]
    for papa, mama in zip(offspring[::2], offspring[1::2]):
        offspring1,offspring2 = random.choice(crossFunctions)(papa,mama)
        offspring1["views"] = 0
        offspring2["views"] = 0
        offspring.extend((offspring1, offspring1))

    #for individual in out:
    # if reprieve(individual):
    # offspring.append(individual)
    print '############################'
    print len(offspring), sample_size
    print '############################'


    print '############################'

    put_sample(sample["sample_id"], offspring )

def evolve_Tournament(sample_size=6 , mutation_rate = 0.5 ):

    #get two samples from evospace
    sample_papa = get_sample(sample_size)
    #if None evospace empty? just return
    if not sample_papa:
        return
    sample_mama = get_sample(sample_size)

    if not sample_mama:
        return

    #each must have a minimum of two individuals with at least 2 views each (DEFAULTS)
    # if not return both samples unchanged
    if few_views(sample_mama,1) or few_views(sample_papa,1):
        put_sample(sample_mama["sample_id"], sample_mama["sample"])
        put_sample(sample_papa["sample_id"], sample_papa["sample"])
        print "few",few_views(sample_mama),few_views(sample_papa)
        return

    #Add currentFitness to individuals
    sample_papa = calc_fitness(sample_papa)
    sample_mama = calc_fitness(sample_mama)
    #get the best, first_parent
    sample_papa["sample"].sort(key=itemgetter('currentFitness'), reverse=True)
    papa = sample_papa["sample"][0]

    #get the best, second_parent
    sample_mama["sample"].sort(key=itemgetter('currentFitness'), reverse=True)
    mama = sample_mama["sample"][0]
    #crossFunctions = [crossVertical]
    crossFunctions = [cross_simple,cross_doble]

    offspring1,offspring2 = random.choice(crossFunctions)(papa,mama)
    offspring1["views"] = 0
    offspring2["views"] = 0
    print offspring1

    if random.random() <= mutation_rate:
        if random.random() <= .20:
            mutacion_aprox(offspring1)
            mutacion_aprox(offspring2)
            offspring1["mutation"] ="aproximacion"
            offspring2["mutation"] ="aproximacion"
            print "aproximacion"

        else:
            #range random?
            for i in range(random.randint(1,4)):
                mutacion_ran(offspring1)
                mutacion_ran(offspring2)
                offspring1["mutation"] ="random"
                offspring2["mutation"] ="random"
            print "random"

    worst_mama = min( [a for a in sample_mama["sample"] if a["currentFitness"] is not None], key=itemgetter('currentFitness'))
    worst_papa = min( [a for a in sample_papa["sample"] if a["currentFitness"] is not None], key=itemgetter('currentFitness'))
    sample_mama["sample"].remove(worst_mama)
    sample_papa["sample"].remove(worst_papa)

    sample_mama["sample"].append(offspring1)
    sample_papa["sample"].append(offspring2)


    put_sample(sample_mama["sample_id"], sample_mama["sample"])
    put_sample(sample_papa["sample_id"], sample_papa["sample"])




if __name__ == "__main__":
#     #init_pop(32)
#     evolve()

    init_pop(100)

    
#mutacion_ran(papa)
#mutacion_aprox(papa)
#server = Population()
#sample = server.get_sample(2)
#papa = {'fitness': {'DefaultContext': 0.0}, 'views': 0, 'id': 'pop:individual:7', 'chromosome': [141, 37, 1, 0, 0, 1, 3, 1, 0, 0, 0, 1, 0, 3]}
#mama = sample["sample"][1]
#print papa
#print mama
#cross_simple(papa,mama)
#mutacion_ran(papa)


