#include <iostream>
#include <fstream>
#include <cmath>
#include <set>
#include <random>
#include <chrono>
#include <thread>

using namespace std;

void get_force(set<pair<int, int>>& A, float (&x)[18659], float (&y)[18659], float (&f)[18659]) {
    for (int i = 0; i < 18659; ++i) {
        f[i] = -0.000000001 * x[i];
    }
    for (int i = 0; i < 18658; ++i) {
        //cerr << i << endl;
        for (int j = i + 1; j < 18659; ++j) {
            float f_temp = 0;
            float dx = x[i] - x[j];
            if (A.find(make_pair(i, j)) != A.end())
                f_temp -= dx;
            float dy = y[i] - y[j];
            float div = (dx*dx + dy*dy);
            if (div == 0.0)
                div = 0.00001;
            div = div * sqrt(div);
            f_temp += 1000 * dx/div;
            f[i] += f_temp;
            f[j] -= f_temp;
        }
    }
}

int main() {
    std::ifstream infile("A.mat");
    int a, b;
    set<pair<int, int>> A;
    while (infile >> a >> b) {
        A.insert(make_pair(a, b));
    }
    float x[18659], y[18659], F_x[18659], F_y[18659], sum_fx(18659), sum_fy(18659);
    default_random_engine generator;
    uniform_real_distribution<float> distribution(0.0,2*3.1415926);
    uniform_real_distribution<float> distribution2(0.01,5000);
    /*for (int i = 0; i < 18659; ++i) {
        float number_x = distribution(generator);
        float number_y = distribution2(generator);
        x[i] = number_y*cos(number_x);
        y[i] = number_y*sin(number_x);
    }*/
    int i = 0;
    std::ifstream x_file("x.vec");
    std::ifstream y_file("y.vec");
    float z;
    while (x_file >> z) {
        x[i] = z;
        ++i;
    }
    i = 0;
    while (y_file >> z) {
        y[i] = z;
        ++i;
    }
    float alpha = 0.01;//0.00001;
    float tmp_sum_fx(0), tmp_sum_fy(0);
    for (int i = 0; i < 100000; ++i) {
        tmp_sum_fx = 0;
        tmp_sum_fy = 0;
        cerr << "Step " << i << endl << endl;
        get_force(A, x, y, F_x);
        get_force(A, y, x, F_y);
        for (int j = 0; j < 18659; ++j) {
            if (rand() % 2 == 0) {
                float ds = sqrt(F_x[j]*F_x[j] + F_y[j]*F_y[j]);
                float new_ds = 10000;
                if (ds < 10000)
                    new_ds = ds;
                x[j] += alpha*F_x[j]*new_ds/ds;
                y[j] += alpha*F_y[j]*new_ds/ds;
            }
            tmp_sum_fx += fabs(F_x[j]);
            tmp_sum_fy += fabs(F_y[j]);
        }
        cerr << tmp_sum_fx/sum_fx << " " << tmp_sum_fy/sum_fy << endl;
        sum_fx = tmp_sum_fx;
        sum_fy = tmp_sum_fy;
        cerr << "writing..." << endl;
        ofstream x_file, y_file;
        x_file.open("x.vec");
        y_file.open("y.vec");
        for (int i = 0; i < 18659; ++i) {
            x_file << x[i] << "\n";
            y_file << y[i] << "\n";
        }
        x_file.close();
        y_file.close();
    }
    return 0;
}
