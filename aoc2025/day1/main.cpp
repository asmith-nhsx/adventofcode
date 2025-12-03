#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

void debugOutput(const string& message, bool debugFlag = false) {
    if (debugFlag) {
        cout << message << endl;
    }
    return;
}

int getData(vector<string> &data, string fileName = "data.txt") {
    ifstream file(fileName); // Open the file
    string line;
    data = {};
    
    if (!file.is_open()) { // Check if the file opened successfully
        cerr << "Error opening the file!" << endl;
        return 1;
    }

    while (getline(file, line)) { // Read each line
        data.push_back(line);
    }

    file.close(); // Close the file
    return 0;
}

int solution1(vector<string> &data, bool debugFlag = false) {
    int dial = 50;
    int start = dial;    
    int incr = 0;
    int result = 0;
    
    for (const auto& datum : data) {
        incr = stoi(datum.substr(1));
        if (datum[0] == 'L') {
            dial -= incr;
        }
        else
        {
            dial += incr;
        }
        
        if (dial < 0) {
            dial = 100 + dial;
        }

        dial %= 100;
        if (dial == 0) {
            result++;
        }
        debugOutput(datum + " " + to_string(start) + " " + to_string(dial) + " " + to_string(result), debugFlag);
        start = dial;
    }
    return result;
}

int solution2(vector<string> &data, bool debugFlag = false) {
    int dial = 50;
    int start = dial;
    int incr = 0;
    int result = 0;

    for (const auto& datum : data) {
        incr = stoi(datum.substr(1));
        for (int i = 0; i < abs(incr); i++) {
            if (datum[0] == 'L') {
                dial--;
            }
            else
            {
                dial++;
            }
            if (dial > 99) {
                dial = 0;
            }
            if (dial < 0) {
                dial = 99;
            }
            if (dial == 0) {
                result++;
            }
        }
        debugOutput(datum + " " + to_string(start) + " " + to_string(dial) + " " + to_string(result), debugFlag);
        start = dial;
    }
    return result;
}

int main()
{
    int result;
    vector<string> data = {};
    
    cout << "AdventOfCode25 Day 1\n\n"; 
    
    if(getData(data) == 0) {
        result = solution1(data, false);
        cout << "The answer is " << result << endl;
        
        result = solution2(data, false);
        cout << "The answer is " << result << endl;       
    }

    return 0;
}





