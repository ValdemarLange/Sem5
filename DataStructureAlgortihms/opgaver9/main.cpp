#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <memory>

class Edge; // Forward declaration

// Vertex-klassen
class Vertex {
public:
    std::string name; // Navn på vertex
    std::vector<Edge*> edges; // Tilstødende kanter

    Vertex(const std::string& name) : name(name) {}

    void addEdge(Edge* edge) {
        edges.push_back(edge);
    }
};

// Edge-klassen
class Edge {
public:
    Vertex* from; // Start-vertex
    Vertex* to;   // Slut-vertex
    double weight; // Kantens vægt (valgfrit, kan bruges som 1 for uvægtet graf)

    Edge(Vertex* from, Vertex* to, double weight = 1.0) 
        : from(from), to(to), weight(weight) {}
};

// Graph-klassen
class Graph {
private:
    std::unordered_map<std::string, std::unique_ptr<Vertex>> vertices;

public:
    void addVertex(const std::string& name) {
        if (vertices.find(name) == vertices.end()) {
            vertices[name] = std::make_unique<Vertex>(name);
        }
    }

    void addEdge(const std::string& from, const std::string& to, double weight = 1.0) {
        if (vertices.find(from) == vertices.end() || vertices.find(to) == vertices.end()) {
            std::cerr << "Error: One or both vertices not found." << std::endl;
            return;
        }

        Vertex* fromVertex = vertices[from].get();
        Vertex* toVertex = vertices[to].get();
        Edge* edge = new Edge(fromVertex, toVertex, weight);
        fromVertex->addEdge(edge);
    }

    void printGraph() const {
        for (const auto& pair : vertices) {
            const Vertex* vertex = pair.second.get();
            std::cout << vertex->name << " -> ";
            for (const Edge* edge : vertex->edges) {
                std::cout << edge->to->name << "(" << edge->weight << ") ";
            }
            std::cout << std::endl;
        }
    }
};

int main() {
    Graph graph;

    // Tilføj vertexer
    graph.addVertex("A");
    graph.addVertex("B");
    graph.addVertex("C");

    // Tilføj kanter
    graph.addEdge("A", "B", 2.0);
    graph.addEdge("A", "C", 1.0);
    graph.addEdge("B", "C", 3.0);

    // Print grafen
    std::cout << "Graph:" << std::endl;
    graph.printGraph();

    return 0;
}
