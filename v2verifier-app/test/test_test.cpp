//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/test.hpp"

int main() {
    test T;
    return T.add_two_numbers(2,5) == 7 ? 0 : 1;
}