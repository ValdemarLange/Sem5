#ifndef BINARY_SEARCH_TREE_H
#define BINARY_SEARCH_TREE_H
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

class BinaryNode
{
public:
	int element;
	BinaryNode *left;
	BinaryNode *right;

	BinaryNode(const int & theElement, BinaryNode *lt, BinaryNode *rt)
		: element{ theElement }, left{ lt }, right{ rt } { }

	BinaryNode(int && theElement, BinaryNode *lt, BinaryNode *rt)
		: element{ std::move(theElement) }, left{ lt }, right{ rt } { }
};


class BinarySearchTree
{
public:
	BinarySearchTree(); 
	BinarySearchTree(const BinarySearchTree & rhs); 
	BinarySearchTree(BinarySearchTree && rhs); 
	~BinarySearchTree();
	
	const int & findMin() const;
	const int & findMax() const;
	bool contains(const int & x) const;
	bool isEmpty() const;
	void printTree() const;
	
	void makeEmpty();
	void insert(const int & x);
	void insert(int && x);
	void remove(const int & x);
	void preorder() const;
	void inorder() const;
	void postorder() const;
	void levelorder() const;
	int numberOfNodes() const;
	int numberOfLeaves() const;
	int numberOfFull() const;
	int internalPathLength() const;

	void createPerfect(vector<int> vec, int h);

	int numberOfBranches() const;

	std::string findRoute(int value) const;

	
private:
	BinaryNode *root;

	void insert(const int & x, BinaryNode * & t);
	void insert(int && x, BinaryNode * & t);
	void remove(const int & x, BinaryNode * & t);
	BinaryNode * findMin(BinaryNode *t) const;
	BinaryNode * findMax(BinaryNode *t) const;
	
	bool contains(const int & x, BinaryNode *t) const;
	
	void makeEmpty(BinaryNode * & t);
	void printTree(BinaryNode *t) const;
	BinaryNode * clone(BinaryNode *t) const;

	void preorder(BinaryNode *t) const;
	void inorder(BinaryNode *t) const;
	void postorder(BinaryNode *t) const;
	void levelorder(BinaryNode *t) const;

	int numberOfNodes(BinaryNode *t) const;
	int numberOfLeaves(BinaryNode *t) const;
	int numberOfFull(BinaryNode *t) const;

	int internalPathLength(BinaryNode *t, int N) const;

	int numberOfBranches(BinaryNode *t) const;
	BinaryNode* getOnlyChild(BinaryNode *node) const;

	std::string findRoute(BinaryNode *root, int value) const;
	
};

#endif