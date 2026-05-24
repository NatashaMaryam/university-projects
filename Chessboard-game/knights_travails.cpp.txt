#include <iostream>
#include <queue>
#include <vector>
#include <utility> // for std::pair
#include <limits>  // for std::numeric_limits
#include <string>  // for std::string
#include <algorithm> // for std::reverse

using namespace std;

// Directions a knight can move on the chessboard
const int dx[] = {2, 1, -1, -2, -2, -1, 1, 2};
const int dy[] = {1, 2, 2, 1, -1, -2, -2, -1};

// Function to check if the position is within the chessboard
bool isValid(int x, int y, int N) {
    return (x >= 0 && x < N && y >= 0 && y < N);
}

// Function to convert chess notation to board coordinates
pair<int, int> chessToBoard(const string& position) {
    int x = position[0] - 'A'; // Convert column (A-H) to index (0-7)
    int y = position[1] - '1';  // Convert row (1-8) to index (0-7)
    return {x, y};
}

// Function to find the shortest path using BFS
vector<pair<int, int>> minStepsToReachTarget(int startX, int startY, int targetX, int targetY, int N) {
    if (startX == targetX && startY == targetY) return {{startX, startY}};

    vector<vector<bool>> visited(N, vector<bool>(N, false));
    vector<vector<pair<int, int>>> parent(N, vector<pair<int, int>>(N, {-1, -1}));
    queue<pair<int, int>> q;

    visited[startX][startY] = true;
    q.push({startX, startY});

    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop();

        for (int i = 0; i < 8; i++) {
            int newX = x + dx[i];
            int newY = y + dy[i];

            if (isValid(newX, newY, N) && !visited[newX][newY]) {
                visited[newX][newY] = true;
                parent[newX][newY] = {x, y};
                q.push({newX, newY});

                if (newX == targetX && newY == targetY) {
                    // Build the path
                    vector<pair<int, int>> path;
                    for (pair<int, int> v = {targetX, targetY}; v.first != -1; v = parent[v.first][v.second]) {
                        path.push_back(v);
                    }
                    reverse(path.begin(), path.end());
                    return path;
                }
            }
        }
    }
    return {}; // If not reachable
}

void printPath(const vector<pair<int, int>>& path) {
    for (const auto& [x, y] : path) {
        char col = 'A' + x;
        char row = '1' + y;
        cout << col << row << " ";
    }
    cout << endl;
}

int main() {
    cout << "Welcome to the Knight's Travails Game!" << endl;
    cout << "You will help a knight find the shortest path on a chessboard." << endl;

    int N = 8; // Size of the chessboard
    string startPos, targetPos;

    cout << "Enter the starting position of the knight (e.g., A1): ";
    cin >> startPos;
    cout << "Enter the target position (e.g., C5): ";
    cin >> targetPos;

    auto [startX, startY] = chessToBoard(startPos);
    auto [targetX, targetY] = chessToBoard(targetPos);

    // Check if the input is valid
    if (!isValid(startX, startY, N) || !isValid(targetX, targetY, N)) {
        cout << "Invalid positions. Please enter values between A1 and H8." << endl;
        return 1;
    }

    vector<pair<int, int>> path = minStepsToReachTarget(startX, startY, targetX, targetY, N);
    if (path.empty()) {
        cout << "The knight cannot reach the target position." << endl;
    } else {
        cout << "The knight can reach the target position in " << path.size() - 1 << " moves." << endl;
        cout << "Path: ";
        printPath(path);
    }

    return 0;
}