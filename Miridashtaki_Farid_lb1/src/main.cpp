#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
using namespace std;
using namespace std::chrono;

// global variables for problem size and solution tracking
int n;
int best = 999999;


long long recursiveCalls = 0;      // number of times go() is called
long long placementAttempts = 0;    // number of squares we try to place


struct Box {
    int x, y, size;  // row, column, and side length 
};


vector<Box> current;
vector<Box> answer;  //best 

// true = occupied, false = free
vector<vector<bool>> field;  

// square of size s can be placed at 
bool canPlace(int row, int col, int s) {
    // check if square fits in the big square 
    if (row + s > n || col + s > n) {
        return false;
    }
    // ells in the square area are free ? 
    for (int i = row; i < row + s; i++) {
        for (int j = col; j < col + s; j++) {
            if (field[i][j] == true) {
                return false;
            }
        }
    }
    return true;
}

// value = true to place, false to remove , remove or place
void placeSquare(int row, int col, int s, bool value) {
    for (int i = row; i < row + s; i++) {
        for (int j = col; j < col + s; j++) {
            field[i][j] = value;
        }
    }
}

// find the first empty cell 
bool findFirstEmpty(int& fx, int& fy) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (field[i][j] == false) {
                fx = i;  
                fy = j;  
                return true;
            }
        }
    }
    return false;  // square is full
}

// recursive backtracking function
void go(int used) {
    recursiveCalls++;  
    
    // if more than best , stop 
    if (used >= best) {
        return;
    }
    
    // find first empty position to place next square
    int row, col;
    if (findFirstEmpty(row, col) == false) {
        // found a complete solution - we save that one
        if (used < best) {
            best = used;
            answer = current; 
        }
        return;
    }
    
    // determine maximum possible square size at this position
    int maxSize = n - row;
    if (n - col < maxSize) {
        maxSize = n - col;
    }
    
    // max size must be 1 to n-1
    if (maxSize > n - 1) {
        maxSize = n - 1;
    }
    
    // try all possible sizes from largest to smallest for opt
    for (int s = maxSize; s >= 1; s--) {
        placementAttempts++;  
        
        if (canPlace(row, col, s) == true) {
            
            placeSquare(row, col, s, true);
            
            
            Box b;
            b.x = row;
            b.y = col;
            b.size = s;
            current.push_back(b);
            
            go(used + 1);
            
            // backtrack: remove the square
            current.pop_back();
            placeSquare(row, col, s, false);
        }
    }
}

// research function to test multiple n values and save to csv
void runResearch(int maxN) {
    ofstream file("research.csv");
    file << "N,MinSquares,RecursiveCalls,PlacementAttempts,Time_ms\n";
    
    cout << "\nN\tSquares\tCalls\tAttempts\tTime(ms)\n";
    cout << "----------------------------------------\n";
    
    for (int testN = 2; testN <= maxN; testN++) {
        n = testN;
        best = 999999;
        recursiveCalls = 0;
        placementAttempts = 0;
        current.clear();
        answer.clear();
        
        // even n :4 squares
        if (n % 2 == 0) {
            // start timer for even case
            auto start = high_resolution_clock::now();
            
            best = 4;
            recursiveCalls = 1;
            placementAttempts = 0;
            
            // create the four equal squares
            answer.clear();
            int half = n / 2;
            Box b1, b2, b3, b4;
            b1.x = 0; b1.y = 0; b1.size = half;
            b2.x = 0; b2.y = half; b2.size = half;
            b3.x = half; b3.y = 0; b3.size = half;
            b4.x = half; b4.y = half; b4.size = half;
            answer.push_back(b1);
            answer.push_back(b2);
            answer.push_back(b3);
            answer.push_back(b4);
            
            auto end = high_resolution_clock::now();
            auto ms = duration_cast<milliseconds>(end - start).count();
            
            // save to csv and print to console
            file << n << "," << best << "," << recursiveCalls << "," 
                 << placementAttempts << "," << ms << "\n";
            
            cout << n << "\t" << best << "\t" << recursiveCalls << "\t" 
                 << placementAttempts << "\t\t" << ms << "\n";
            continue;
        }
        
        // for odd n, run backtracking with full setup
        // start timer including field initialization
        auto start = high_resolution_clock::now();
        
        // initialize empty field
        field.clear();
        field.resize(n);
        for (int i = 0; i < n; i++) {
            field[i].resize(n, false);
        }
        
        go(0);
        
        auto end = high_resolution_clock::now();
        auto ms = duration_cast<milliseconds>(end - start).count();
        
        // save to csv and print to console
        file << n << "," << best << "," << recursiveCalls << "," 
             << placementAttempts << "," << ms << "\n";
        
        cout << n << "\t" << best << "\t" << recursiveCalls << "\t" 
             << placementAttempts << "\t\t" << ms << "\n";
    }
    
    file.close();
    cout << "\nData saved to research.csv\n";
}

int main(int argc, char* argv[]) {
    // check if research mode is activated
    if (argc > 1) {
        string arg = argv[1];
        if (arg == "--research") {
            int maxN = 15;
            if (argc > 2) {
                maxN = atoi(argv[2]);
            }
            runResearch(maxN);
            return 0;
        }
    }
    
    // normal mode - solve for a single n
    cin >> n;
    
    // handle even n case directly
    if (n % 2 == 0) {
        auto start = high_resolution_clock::now();  
        
        // output in required format
        cout << 4 << endl;
        int half = n / 2;
        cout << "1 1 " << half << endl;
        cout << "1 " << half + 1 << " " << half << endl;
        cout << half + 1 << " 1 " << half << endl;
        cout << half + 1 << " " << half + 1 << " " << half << endl;
        
        auto end = high_resolution_clock::now();    
        auto duration = duration_cast<microseconds>(end - start);
        
        // research data for single run
        cout << "\nResearch Data:\n";
        cout << "Recursive calls: 1\n";
        cout << "Placement attempts: 0\n";
        cout << "Time: " << duration.count() / 1000.0 << " ms\n";
        return 0;
    }
    
    // odd n case - run backtracking
    // start timer including all setup
    auto start = high_resolution_clock::now();
    
    // initialize empty field
    field.clear();
    field.resize(n);
    for (int i = 0; i < n; i++) {
        field[i].resize(n, false);
    }
    
    go(0);
    
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    
    cout << best << endl;
    for (int i = 0; i < answer.size(); i++) {
        cout << answer[i].x + 1 << " " 
             << answer[i].y + 1 << " " 
             << answer[i].size << endl;
    }
    
    cout << "Recursive calls: " << recursiveCalls << endl;
    cout << "attempts: " << placementAttempts << endl;
    cout << duration.count() / 1000.0 << " ms\n";
    
    return 0;
}