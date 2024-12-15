#include <cassert>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>
#include <array>
#include <map>
#include <string>

std::map<int, std::vector<int>> beforeAfter;
std::map<int, std::vector<int>> afterBefore;
std::vector<std::vector<int>> updates;
std::ifstream in { "input.txt"};
int sum1 { 0 };
int sum2 { 0 };

void readFile() {
    std::string s;
    bool end { false };
    while (!end and std::getline(in, s)) {
        auto pos = s.find('|');
        if(pos != std::string::npos) {
            auto split = s.substr(0, pos);
            int firstNum = std::stoi(split);
            split = s.substr(pos + 1, std::string::npos);
            int secondNum = std::stoi(split);
            beforeAfter[firstNum].push_back(secondNum);
            afterBefore[secondNum].push_back(firstNum);
        } else {
            end = true;
        }
    }
    while (std::getline(in, s) and s != "") {
        updates.push_back(std::vector<int>());
        auto updatesLast { std::rbegin(updates) };
        auto sub = s;
        auto pos = sub.find(',');
        end = false;
        while(!end) {
            sub = sub.substr(0, pos);
            int num { std::stoi(sub) };
            updatesLast->push_back(num);
            sub = s.substr(pos + 1, std::string::npos);
            s = sub;
            if(pos == std::string::npos)
                end = true;
            pos = sub.find(',');
        }
    }
}

void part1() {
    for(auto const& anU : updates) {
        bool correct { true };
        for(size_t i {0}; i < anU.size(); i++) {
            for(size_t j {i+1}; j < anU.size(); j++) {
                // get the numbers that should be before anU[i]
                for(auto befores : afterBefore[anU[i]]) {
                    // if any number after anU[i] should be before instead
                    if(befores == anU[j])
                        correct = false;
                }
            }
        }

        if(correct) {
            auto index {anU.size() / 2};
            sum1 += anU[index];
        }
    }
}

void part2() {
    size_t updateNum { 0 };
    while(updateNum < updates.size()) {
        auto &anU = updates[updateNum];
        bool correct { true };
        for(size_t i {0}; i < anU.size(); i++) {
            for(size_t j {i+1}; j < anU.size(); j++) {
                size_t it { 0 };
                // get the numbers that should be before anU[i]
                auto &befores = afterBefore[anU[i]];
                while(it < befores.size()) {
                    bool correctCheck { true };
                    // if any number after anU[i] should be before instead
                    if(befores[it] == anU[j]) {
                        correct = false;
                        correctCheck = false;
                        assert(i < anU.size() - 1);
                        auto swap { anU[j] };
                        anU[j] = anU[i];
                        anU[i] = swap;
                    }
                    // doesn't increment to be shure the change is ok
                    if(correctCheck)
                        it++;
                }
            }
        }
        // count++;
        if(!correct) {
            // std::cout << "Count " << count << " is not correct." << std::endl;
            auto index {anU.size() / 2};
            sum2 += anU[index];
        }
        updateNum++;
    }
}

auto main(int argc, char *argv[]) -> int {

    if(!in.is_open()) {
        std::cout << "Failed to open file.\n";
        return EXIT_FAILURE;
    }

    readFile();
    part1();
    part2();
    std::cout << "Part1: " << sum1 << std::endl;
    std::cout << "Part2: " << sum2 << std::endl;

    return 0;
}
