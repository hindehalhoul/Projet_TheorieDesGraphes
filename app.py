import os
import numpy as np
import networkx as nx
from networkx import from_numpy_array
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from bfs import bfs
from dfs import dfs
from dijkstra import dijkstra
from warshall import warshall


app = Flask(__name__, static_folder='static')
@app.route('/')
def home1():
    return render_template('home.html')


@app.route('/dijkstra_page')
def dijkstra_page():
    return render_template('Dijkstrapage.html')
@app.route('/warshall_page')
def warshall_page():
    return render_template('Warshallpage.html')

@app.route('/dfs_page')
def dfs_page():
    return render_template('DFSpage.html')

@app.route('/bfs_page')
def bfs_page():
    return render_template('BFSpage.html')

@app.route('/BFS', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_nodes = int(request.form['num_nodes'])
        adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

        for i in range(num_nodes):
            for j in range(num_nodes):
                adj_matrix[i][j] = int(request.form[f'adj_matrix_{i}_{j}'])

        graph = nx.DiGraph(adj_matrix)

        bfs_result = list(map(str, bfs(graph, 0))) if bfs(graph, 0) else None

        img_folder = "C:\\Users\\ASUS\\Desktop\\LSI S2\\Theorie des graphes\\flask_project\\graph_theory_GUI\\static\\img"
        # delete existing images in folder
        for filename in os.listdir(img_folder):
            file_path = os.path.join(img_folder, filename)
            os.unlink(file_path)

        fig = plt.figure()
        fig.clf()
        plt.title('Graph')
        nx.draw(graph, with_labels=True)
        plt.savefig('static/img/graph.png', format='png')

        return render_template('result.html', bfs_result=bfs_result)
    else:
        return render_template('index.html')
    
 
@app.route('/DFS', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        num_nodes = int(request.form['num_nodes'])
        adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

        for i in range(num_nodes):
            for j in range(num_nodes):
                adj_matrix[i][j] = int(request.form[f'adj_matrix_{i}_{j}'])

        graph = nx.DiGraph(adj_matrix)

        dfs_result = list(map(str, dfs(graph, 0))) if dfs(graph, 0) else None

        img_folder = "C:\\Users\\ASUS\\Desktop\\LSI S2\\Theorie des graphes\\flask_project\\graph_theory_GUI\\static\\img"
        # delete existing images in folder
        for filename in os.listdir(img_folder):
            file_path = os.path.join(img_folder, filename)
            os.unlink(file_path)

        fig = plt.figure()
        fig.clf()
        plt.title('Graph')
        nx.draw(graph, with_labels=True)
        plt.savefig(os.path.join(img_folder, 'graph.png'), format='png')

        return render_template('result2.html', dfs_result=dfs_result)
    else:
        return render_template('index.html')
    




    
@app.route('/war', methods=['GET', 'POST'])
def warshall_algorithm():
    if request.method == 'POST':
        adjacency_matrix = request.form['matrix']
        # Convertir la chaîne de la matrice en une liste de listes
        matrix = [list(map(int, row.split())) for row in adjacency_matrix.strip().split('\n')]
        result_matrix = warshall(matrix)

        # Générer le graphe final à partir de la matrice résultante
        G = nx.from_numpy_array(np.array(result_matrix), create_using=nx.DiGraph)

        img_folder = os.path.join(app.static_folder, 'img')

        # Supprimer les images existantes dans le dossier
        for filename in os.listdir(img_folder):
            file_path = os.path.join(img_folder, filename)
            os.unlink(file_path)

        fig = plt.figure()
        fig.clf()
        plt.title('Graph')
        nx.draw(G, with_labels=True)
        plt.savefig(os.path.join(img_folder, 'graph.png'), format='png')

        # Afficher le graphe dans le template result.html
        return render_template('resultat3.html', result_matrix=result_matrix)

    return render_template('index3.html')


@app.route('/dijkstra', methods=['GET', 'POST'])
def index1():
    if request.method == 'POST':
        num_nodes = int(request.form['num_nodes'])
        adjacency_matrix = []
        for i in range(num_nodes):
            row = []
            for j in range(num_nodes):
                value = int(request.form[f'adj_matrix_{i}_{j}'])
                row.append(value)
            adjacency_matrix.append(row)

        start_node = int(request.form['start_node'])  # Récupérer le nœud de départ choisi par l'utilisateur

        distances, predecessors = dijkstra(adjacency_matrix, start_node)

        # Générer le graphe à partir de la matrice d'adjacence
        graph = from_numpy_array(np.array(adjacency_matrix), create_using=nx.DiGraph)

        # Dessiner le graphe et le sauvegarder en tant qu'image
        img_folder = "C:\\Users\\ASUS\\Desktop\\LSI S2\\Theorie des graphes\\flask_project\\graph_theory_GUI\\static\\img"
        plt.figure()
        plt.title('Graph from Adjacency Matrix')
        nx.draw(graph, with_labels=True)
        plt.savefig(os.path.join(img_folder, 'adjacency_graph.png'))

        # Générer le graphe des prédécesseurs
        pred_graph = nx.DiGraph()
        for node, predecessor in enumerate(predecessors):
            if predecessor is not None:
                pred_graph.add_edge(predecessor, node)

        # Dessiner le graphe des prédécesseurs et le sauvegarder en tant qu'image
        plt.figure()
        plt.title('Predecessor Graph')
        nx.draw(pred_graph, with_labels=True)
        plt.savefig(os.path.join(img_folder, 'predecessor_graph.png'))

        return render_template('result1.html', distances=distances, predecessors=predecessors)

    return render_template('index1.html')


if __name__ == '__main__':
    app.run(debug=True)
