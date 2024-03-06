//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/HeaderInfo.hpp"

#include <chrono>
#include <iostream>

int main() {

    uint32_t psid = 0x32;
    auto now = std::chrono::time_point_cast<std::chrono::milliseconds>(std::chrono::system_clock::now());
    uint64_t currentTime = now.time_since_epoch().count();
    auto timeBytes = std::vector<std::byte>(currentTime);
    int a = 9;
    HeaderInfo headerInfo;
    std::cout << "Hello!!!" << std::endl;
}