#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <set>
#include <numeric>

std::vector<int> partial_shuffle(std::vector<int>& A, int n, int c) {
    std::srand(std::time(0));
    for (int i = 0; i < c; ++i) {
        int j = i + std::rand() % (n - i);
        std::swap(A[i], A[j]);
    }
    return std::vector<int>(A.begin(), A.begin() + c);
}

std::set<int> select_slots(std::vector<int>& y, int n) {
    double p = y[0] / std::accumulate(y.begin(), y.end(), 0.0);
    int c = static_cast<int>(std::ceil(p * n));
    std::vector<int> A(n);
    for (int i = 0; i < n; ++i) {
        A[i] = i + 1;
    }
    partial_shuffle(A, n, c);
    std::set<int> s;
    for (int i = 0; i < c; ++i) {
        s.insert(A[i]);
    }
    return s;
}

int main() {
    std::vector<int> y = {10, 6, 3, 2, 5};  // Example queue lengths including self node
    int n = y.size();
    std::set<int> selected_slots = select_slots(y, n);

    std::cout << "Selected transmission slots: ";
    for (int slot : selected_slots) {
        std::cout << slot << " ";
    }
    std::cout << std::endl;

    return 0;
}
