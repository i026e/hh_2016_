#! /usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Created on Thu Sep 22 2016

@author: pavel
"""
# Надеюсь, кириллица в комментариях проблем не вызовет

# Оставляю минимум зависимостей
import sys
import heapq



# создает из матрицы граф в ввиде списка (словаря) смежности
# 
def create_graph(matrix):
    height, width = len(matrix), len(matrix[0])
        
    graph = {-1 : set()} # в виде списка смежности    
    # добавляю виртуальный узел -1 (море)
    
    def safe_add(src, dest, cost):
        if src not in graph:
            graph[src] = set()
        graph[src].add((dest, cost))
        
    def flat_index(row, col):
        return row*width + col #отсчет от 0
        
    # добавляем ИСХОДЯЩИЕ ребра
    # стоимость ребра равна значению вершины из которой ребро ИСХОДИТ
    # если рядом море то ребро ВХОДЯЩЕЕ с 0 стоимостью    
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            
            index = flat_index(i, j)
            
            # вверх
            if i == 0: # море 
                safe_add(-1, index, 0)
            else:
                safe_add(index, flat_index(i-1, j), val)
                
            #вниз
            if i == height - 1:
                safe_add(-1, index, 0)
            else:
                safe_add(index, flat_index(i+1, j), val)
            
            #влево
            if j == 0:
                safe_add(-1, index, 0)
            else:
                safe_add(index, flat_index(i, j-1), val)
                
            #вправо
            if j == width-1:
                safe_add(-1, index, 0)
            else:
                safe_add(index, flat_index(i, j+1), val)    
                
    
    return graph
    
def shortest_path(graph, src):
    # вычисляем стоимость пути от источника до каждого узла графа
    # модификация алгоритма кратчайшего пути Dijkstr'ы
    # отличие в том, что стоимости не складываются
    costs = {}
    queue = [(0, src)]
    
    heapq.heapify(queue) # heap где стоимость пути - первый элемент тапла
    
    while len(queue) > 0:
        cost, node = heapq.heappop(queue) # pop smallest 
        
        if node not in costs:
            costs[node] = cost
            
            for dest, jump_cost in graph[node]:
                
                if dest not in costs: # если еще не посещали                    
                    heapq.heappush(queue, (max(cost, jump_cost), dest)) 
                    # здесь разница с оригинальным алгоритмом:
                    # MAX вместо суммы
    return costs
        
def volume(matrix, fullness) :
    # находим окончательный ответ
    height, width = len(matrix), len(matrix[0])
    
    def flat_index(row, col):
        return row*width + col #отсчет от 0
        
    v = 0    
        
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            index = flat_index(i, j)
            
            # разница между уровнем наполнения и высотой
            level = fullness[index] - val
            
            # имеет смысл только если уровень воды выше высоты местности
            if level > 0:
                v += level
    return v
    
def _read_matrix(src):
    height, width = [int(i) for i in src.readline().strip().split()]
    
    matrix = []
    
    for line in range(height):
        row = [int(i) for i in src.readline().strip().split()]
        
        assert len(row) == width
        
        matrix.append(row)
        
    return matrix
    
    
def read_data(src = sys.stdin):
    num_graphs = int(src.readline().strip())
    
    matrices = []
    for i in range(num_graphs):
        matrices.append(_read_matrix(src))
        
    return matrices

def solve(matrix):
    graph = create_graph(matrix)
    fullness = shortest_path(graph, -1)
    vol = volume(matrix, fullness)
        
    return vol


def test():
    test_files = {"pr1_ex1.txt" : (2, 7, 0)}
    
    for fname, answer in test_files.items():
        with open(fname, "r") as f:
            matrices = read_data(f)
            
            for i, m in enumerate(matrices):
                vol = solve(m)
                
                print(m, vol)
                assert vol == answer[i]



def main(*args):
    matrices = read_data()
    for m in matrices:
        print(solve(m)) 



if __name__ == "__main__":
    main()
    #test()
