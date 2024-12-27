#include "BinarySearchTree.h"
#include <queue>
#include <vector>
#include <cmath>
using namespace std;

BinarySearchTree::BinarySearchTree() : root{ nullptr }
{
}


BinarySearchTree::BinarySearchTree(const BinarySearchTree & rhs) : root{ nullptr }
{
	root = clone(rhs.root);
}


BinarySearchTree::BinarySearchTree(BinarySearchTree && rhs) : root{ rhs.root }
{
	rhs.root = nullptr;
}

BinarySearchTree::~BinarySearchTree()
{
	makeEmpty();
}

const int & BinarySearchTree::findMin() const
{
	if (isEmpty())
		return -1;
	return findMin(root)->element;
}


const int & BinarySearchTree::findMax() const
{
	if (isEmpty())
		return -1;
	return findMax(root)->element;
}

bool BinarySearchTree::contains(const int & x) const
{
	return contains(x, root);
}

bool BinarySearchTree::isEmpty() const
{
	return root == nullptr;
}

void BinarySearchTree::printTree() const
{
	if (isEmpty())
		cout << "Empty tree" << endl;
	else
		printTree(root);
}

void BinarySearchTree::makeEmpty()
{
	makeEmpty(root);
}


void BinarySearchTree::insert(const int & x)
{
	insert(x, root);
}

void BinarySearchTree::insert(int && x)
{
	insert(std::move(x), root);
}

void BinarySearchTree::remove(const int & x)
{
	remove(x, root);
}

void BinarySearchTree::insert(const int & x, BinaryNode * & t)
{
	if (t == nullptr)
		t = new BinaryNode{ x, nullptr, nullptr };
	else if (x < t->element)
		insert(x, t->left);
	else if (t->element < x)
		insert(x, t->right);
	else
		;  // Duplicate; do nothing
}


void BinarySearchTree::insert(int && x, BinaryNode * & t)
{
	if (t == nullptr)
		t = new BinaryNode{ std::move(x), nullptr, nullptr };
	else if (x < t->element)
		insert(std::move(x), t->left);
	else if (t->element < x)
		insert(std::move(x), t->right);
	else
		;  // Duplicate; do nothing
}

void BinarySearchTree::remove(const int & x, BinaryNode * & t)
{
	if (t == nullptr)
		return;   // Item not found; do nothing
	if (x < t->element)
		remove(x, t->left);
	else if (t->element < x)
		remove(x, t->right);
	else if (t->left != nullptr && t->right != nullptr) // Two children
	{
		t->element = findMin(t->right)->element;
		remove(t->element, t->right);
	}
	else
	{
		BinaryNode *oldNode = t;
		t = (t->left != nullptr) ? t->left : t->right;
		delete oldNode;
	}
}

BinaryNode * BinarySearchTree::findMin(BinaryNode *t) const
{
	if (t == nullptr)
		return nullptr;
	if (t->left == nullptr)
		return t;
	return findMin(t->left);
}

BinaryNode * BinarySearchTree::findMax(BinaryNode *t) const
{
	if (t != nullptr)
		while (t->right != nullptr)
			t = t->right;
	return t;
}

bool BinarySearchTree::contains(const int & x, BinaryNode *t) const
{
	if (t == nullptr)
		return false;
	else if (x < t->element)
		return contains(x, t->left);
	else if (t->element < x)
		return contains(x, t->right);
	else
		return true;    // Match
}

void BinarySearchTree::makeEmpty(BinaryNode * & t)
{
	if (t != nullptr)
	{
		makeEmpty(t->left);
		makeEmpty(t->right);
		delete t;
	}
	t = nullptr;
}


void BinarySearchTree::printTree(BinaryNode *t) const
{
	if (t != nullptr)
	{
		printTree(t->left);
		cout << t->element << endl;
		printTree(t->right);
	}
}

BinaryNode * BinarySearchTree::clone(BinaryNode *t) const
{
	if (t == nullptr)
		return nullptr;
	else
		return new BinaryNode{ t->element, clone(t->left), clone(t->right) };
}

void BinarySearchTree::preorder() const
{
	preorder(root);
}


void BinarySearchTree::preorder(BinaryNode *t) const
{
	if (t != nullptr){
		cout << t->element << endl;
		preorder(t->left);
		preorder(t->right);
	}
}

void BinarySearchTree::inorder() const
{
	if (isEmpty())
		cout << "Empty tree" << endl;
	else
		inorder(root);
}

void BinarySearchTree::inorder(BinaryNode *t) const
{
	if (t != nullptr)
	{
		inorder(t->left);
		cout << t->element << endl;
		inorder(t->right);
	}
}

void BinarySearchTree::postorder() const
{
	if (isEmpty())
		cout << "Empty tree" << endl;
	else
		postorder(root);
}

void BinarySearchTree::postorder(BinaryNode *t) const
{
	if (t != nullptr)
	{
		postorder(t->left);
		postorder(t->right);
		cout << t->element << endl;
		return;
	}
}

void BinarySearchTree::levelorder() const
{
	if (isEmpty())
		cout << "Empty tree" << endl;
	else
		levelorder(root);
}

void BinarySearchTree::levelorder(BinaryNode *t) const
{
	queue<BinaryNode*> q;
	q.push(t);
	while(!q.empty())
	{
		BinaryNode* curr = q.front();
		q.pop();	
		cout << curr->element << endl;
		if(curr->left){q.push(curr->left);};
		if(curr->right){q.push(curr->right);};
	};
}

int BinarySearchTree::numberOfNodes() const
{
	if (isEmpty())
		return 0;
	else
		return numberOfNodes(root);
}

int BinarySearchTree::numberOfNodes(BinaryNode *t) const
{
	if (t != nullptr)
	{
		return numberOfNodes(t->left) + numberOfNodes(t->right) +1;
	}
	return 0;
}

int BinarySearchTree::numberOfLeaves() const
{
	if (isEmpty())
		return 0;
	else
		return numberOfLeaves(root);
}

int BinarySearchTree::numberOfLeaves(BinaryNode *t) const
{
	if(t == nullptr){
		return 0;
	}
	if ((t->left == nullptr) && (t->right == nullptr))
	{
		return 1;
	}
	return numberOfLeaves(t->left) + numberOfLeaves(t->right);
}


int BinarySearchTree::numberOfFull() const
{
	if (isEmpty())
		return 0;
	else
		return numberOfFull(root);
}

int BinarySearchTree::numberOfFull(BinaryNode *t) const
{
	if(t == nullptr){
		return 0;
	}
	if ((t->left != nullptr) && (t->right != nullptr))
	{
		return numberOfFull(t->left) + numberOfFull(t->right) + 1;
	}
	return numberOfFull(t->left) + numberOfFull(t->right);
}


int BinarySearchTree::internalPathLength() const
{
	if (isEmpty())
		return 0;
	else
		return internalPathLength(root, 0);
}

int BinarySearchTree::internalPathLength(BinaryNode *t, int N) const
{
	if(t == nullptr){
		return 0;
	}
	return internalPathLength(t->left, N+1) + internalPathLength(t->right, N+1) + N;
}

void BinarySearchTree::createPerfect(vector<int> vec, int h)
{
	for (int i = 0; i < pow(2,h+1)-1; i++)
	{
		insert(vec[i]);
	}
}

