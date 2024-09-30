/*
Write a program that reads N points in a plane and outputs any group of four
or more colinear points (i.e., points on the same line). The obvious brute-force
algorithm requires O(N4 ) time. However, there is a better algorithm that makes use
of sorting and runs in O(N2 log N) time.
*/



// -------------------------------- DIREKTE FRA CHATGPT --- IKKE Testet

#include <iostream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
using namespace std;

// Define a Point structure
struct Point {
    int x, y;
};

// Function to compute the slope between two points
// To avoid floating-point precision issues, we'll return a pair of integers
// representing the slope as a fraction (dy/dx).
pair<int, int> getSlope(const Point& p1, const Point& p2) {
    int dx = p2.x - p1.x;
    int dy = p2.y - p1.y;

    // Handle the case where the line is vertical (dx = 0)
    if (dx == 0) return {1, 0}; // Infinite slope (vertical line)
    if (dy == 0) return {0, 1}; // Horizontal line
    
    // Reduce the slope by the greatest common divisor (GCD)
    int gcd = __gcd(dx, dy);
    return {dy / gcd, dx / gcd};
}

void findCollinearPoints(const vector<Point>& points) {
    int n = points.size();
    
    // Loop over each point as a reference point
    for (int i = 0; i < n; ++i) {
        map<pair<int, int>, vector<Point>> slopeMap; // To store points with the same slope

        // Compare the current point (points[i]) with every other point
        for (int j = 0; j < n; ++j) {
            if (i == j) continue; // Skip if it's the same point
            
            // Calculate the slope between points[i] and points[j]
            pair<int, int> slope = getSlope(points[i], points[j]);
            
            // Store the point with the same slope
            slopeMap[slope].push_back(points[j]);
        }

        // Check for groups of 4 or more points with the same slope
        for (const auto& entry : slopeMap) {
            const vector<Point>& collinearPoints = entry.second;
            
            if (collinearPoints.size() >= 3) { // 3 + reference point = 4 or more collinear points
                // Output the group of collinear points
                cout << "Collinear points: (" << points[i].x << ", " << points[i].y << ")";
                for (const auto& p : collinearPoints) {
                    cout << " -> (" << p.x << ", " << p.y << ")";
                }
                cout << endl;
            }
        }
    }
}

int main() {
    int N;
    cout << "Enter the number of points: ";
    cin >> N;

    vector<Point> points(N);
    cout << "Enter the points as x y pairs:\n";
    for (int i = 0; i < N; ++i) {
        cin >> points[i].x >> points[i].y;
    }

    findCollinearPoints(points);

    return 0;
}
