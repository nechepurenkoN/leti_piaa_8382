#include <bits/stdc++.h>
using namespace std;

typedef tuple<int, int, int> luPoint; // Тип для хранения верхнего левого угла (y, x, size)

bool noIntersections(const luPoint& lu1, const luPoint& lu2){
    //Проверяем, пересекаются ли два квадрата, заданные двумя точками.
    auto [y1, x1, n1] = lu1;
    auto [y2, x2, n2] = lu2;
    //  int y1 = std::get<0>(lu1);
    //  int x1 = std::get<1>(lu1);
    //  int n1 = std::get<2>(lu1);
    //  int y2 = std::get<0>(lu2); // for stepik
    //  int x2 = std::get<1>(lu2);
    //  int n2 = std::get<2>(lu2);
    if (x1 == x2 && y1 == y2) return false;
    if (x1 == x2) {
        return (y1 > y2) ? \
        abs(y1-y2) >= n2 : abs(y1-y2) >= n1;
    }
    if (y1 == y2) {
        return abs(x1-x2) >= (x1 < x2 ? n1 : n2);
    }
    if (x1 < x2){
        if (y1 < y2){
            return abs(x1-x2) >= n1 || abs(y1-y2) >= n1;
        }
        return abs(x1-x2) >= n1 || abs(y1-y2) >= n2;
    } else {
        if (y1 < y2){
            return abs(x1-x2) >= n2 || abs(y1-y2) >= n1;
        }
        return abs(x1-x2) >= n2 || abs(y1-y2) >= n2;
    }
}

void log(const vector<luPoint>& v, int n) {
    for (int i = 0; i < n; i++) cout << "-";
    cout << endl;
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            bool flag = false;
            for (auto element : v){
                if (!noIntersections(element, {i,j,1})){
                    cout << get<2>(element) << " ";
                    flag = true;
                    break;
                }
            }
            if (!flag)
                cout << 0 << " ";
        }
        cout << endl;
    }
    for (int i = 0; i < n; i++) cout << "-";
    cout << endl;
}

bool pass(const vector<luPoint>& v, const luPoint& p){
    //Проверяем пересечение точки кандидата с уже имеющимися точками в решении.
    bool res = true;
    for (auto el : v){
        res &= noIntersections(el, p);
    }
    return res;
}

int main(){
    int n = 0;
    cin >> n;
    auto start = chrono::steady_clock::now();
    

    // Находим наименьший делитель числа n
    int currentDivisor = 2;
    int divisor = 1;
    while (currentDivisor*currentDivisor <= n) {
        if (n % currentDivisor == 0){
            divisor = currentDivisor;
            break;
        }
        currentDivisor++;
    }

    int scalar = 1;
    if (divisor != 1) {
        scalar = n / divisor;
        n = divisor;
    }

    // Самый тривиальный случай -- просто выводим ответ
    /*
    _______
    |  |  |
    -------
    |  |  |
    -------

    */
    if (n == 2){
        cout << 4 << endl;
        cout << 1 << " " << 1 << " " << (scalar*n>>1) << endl;
        cout << 1+(scalar*n>>1) << " " << 1 << " " << (scalar*n>>1) << endl;
        cout << 1 << " " << 1+(scalar*n>>1) << " " << (scalar*n>>1) << endl;
        cout << 1+(scalar*n>>1) << " " << 1+(scalar*n>>1) << " " << (scalar*n>>1) << endl;
        return 0;
    }

    // Добавляем 3 квадрата, уменьшая общее пространство решений. Эмпирическим путем было выяснено,
    // что в наилучшем решении есть эти три квадрата
    vector<luPoint> currentSolution;
    currentSolution.push_back({0, 0, (n >> 1) + 1});
    currentSolution.push_back({0, (n >> 1) + 1, n >> 1});
    currentSolution.push_back({(n >> 1) + 1, 0, n >> 1});

    if (divisor == 1 && n % 10 == 9) {
        // Если число простое и с девяткой на конце, то можно добавить еще три квадрата, тем самым ускорив
        // выполнение программы
        int anotherBigSize = ((n - (n >> 1)) >> 1) + 1;
        int smallerSize = n - anotherBigSize - (n>>1);
        currentSolution.push_back({n - anotherBigSize, n - anotherBigSize, anotherBigSize});
        currentSolution.push_back({n - smallerSize, n - smallerSize - anotherBigSize, smallerSize});
        currentSolution.push_back({n - smallerSize - anotherBigSize, n - smallerSize, smallerSize});
    }

    int maxCount = 2*n;
    vector<luPoint> answer;

    int currentSquare = 0;
    for (auto element : currentSolution){
        auto [y, x, size] = element;
        // int y = std::get<0>(element);
        // int x = std::get<1>(element); // for stepik
        // int size = std::get<2>(element);
        currentSquare += size*size;
    }
    
    for (int size = n >> 1; size > 0; size--){
        // Перебираем по размеру, пытаясь начать с квадрата размером size
        stack<tuple<int,int,int>> rStack; // эмуляция рекурсивного поведения
        rStack.push({size, 0, n >> 1});
        do {

            tuple<int,int,int> stack_top = rStack.top();
            auto [cursz, visited, itsz] = stack_top;
            //  int cursz = std::get<0>(stack_top);
            //  int visited = std::get<1>(stack_top); // for stepik
            //  int itsz = std::get<2>(stack_top);
            if ((int)currentSolution.size() == maxCount && n*n - currentSquare > cursz*cursz) {
                // Если неполное решение уже нелучшее
                rStack.pop();
                continue;
            }
            auto flag = false;
            for (int i = n >> 1; i < n && !visited; i++){
                for (int j = n >> 1; j < n && !visited; j++){
                    if (pass(currentSolution, {i, j, 1})){ // Пустая клетка
                        if (i + cursz <= n && j + cursz <= n && pass(currentSolution, {i, j, cursz})){
                            // Квадрат кандидат помещается
                            currentSolution.push_back({i, j, cursz});
                            log(currentSolution, n);
                            visited = 1; // Если в этой итерации уже ставили, то больше не ставим
                            currentSquare += cursz*cursz;
                            rStack.pop();
                            rStack.push({cursz, visited, itsz});
                        } else {
                            flag = true;
                            break;
                        }
                    }
                    
                }
                if (flag) break;
            }

            if (flag) {
                // Есть пустая клетка, мы в нее не поставили, нужно продолжать перебор в родительском вызове.
                rStack.pop();
                continue;
            }

            if (currentSquare == n*n && (int) currentSolution.size() <= maxCount){
                // Нашли решение
                maxCount = (int) currentSolution.size();
                answer = currentSolution;
                auto point = currentSolution.back();
                auto topPointSize = std::get<2>(point);
                currentSquare -= topPointSize * topPointSize;
                currentSolution.pop_back();
                log(currentSolution, n);
                rStack.pop();
                continue;
            }

            if (maxCount == (int) currentSolution.size()){
                // Нет необходимой площади, уже нелучшее решение
                auto point = currentSolution.back();
                auto topPointSize = std::get<2>(point);
                currentSquare -= topPointSize * topPointSize;
                currentSolution.pop_back();
                log(currentSolution, n);
                rStack.pop();
                continue;
            }

            auto cont = false;
            for (int i = itsz; i > 0; i--){
                // Вызываем перебор для размеров меньше
                if (n*n - currentSquare >= i*i){
                    rStack.pop();
                    rStack.push({cursz, visited, i-1});
                    rStack.push({i, 0, n >> 1});
                    cont = true;
                    break;
                }
            }
            if (cont) continue;

            // Удаляем поставленный квадрат
            rStack.pop();
            auto p = currentSolution.back();
            auto point = currentSolution.back();
            auto topPointSize = std::get<2>(point);
            currentSquare -= topPointSize * topPointSize;
            currentSolution.pop_back();
            log(currentSolution, n);
        } while (!rStack.empty());
    }

    // Выводим ответ
    cout << (int) answer.size() << endl;
    for (auto element : answer) {
        auto [y, x, size] = element;
        // int y = std::get<0>(element);
        // int x = std::get<1>(element); // for stepik
        // int size = std::get<2>(element);
        cout << scalar*y + 1 << " " << scalar*x + 1 << " " << scalar*size << endl;
    }
    auto end = chrono::steady_clock::now();
    cout << chrono::duration_cast<chrono::milliseconds>(end - start).count() << "ms";
    return 0;
}