#include <vector>
#include <string>
#include <iostream>

int main(){
    /*
    Читаем подстроку и строим массив значений префикс функции для неё
    */
    std::string needle;
    std::cout << "Input pattern:" << std::endl;
    std::cin >> needle;
    int needleSize = (int) needle.size();
    std::vector<int> prefixFunction(needleSize, 0);
    for (int i = 1; i < needleSize; i++){
        int k = prefixFunction[i-1];
        while (k > 0 && needle[k] != needle[i]){
            k = prefixFunction[k-1];
        }
        if (needle[i] == needle[k])
            k++;
        prefixFunction[i] = k;
    }

    /*
    Вывод полученной префикс-функции
    */
    std::cout << "Prefix function for pattern is:" << std::endl;
    for (const auto& value : prefixFunction){
        std::cout << value << " ";
    } std::cout << std::endl;

    //std::cout << "Input length of string cmp search in:" << std::endl;
    //int haystackSize = 0;
    //std::cin >> haystackSize;
    std::cout << "Input string:" << std::endl;

    /*
    Считываем очередной символ из буффера, ищем максимальный префикс;
    оптимизированная часть практически не отличается от обычного кмп
    */
    std::vector<int> answer;
    char currentSymbol = 65;
    int k = 0;
    int iteration = 0;
    std::cin.get();
    while(std::cin.get(currentSymbol) && currentSymbol != ' ' && currentSymbol != '\n') {
        while (k > 0 && currentSymbol != needle[k]) // поиск
            k = prefixFunction[k-1];                // max. префикса
        if (currentSymbol == needle[k]) // префиксы равны, увеличиваем значение
            k++;
        if (k == needleSize) // нашли конец вхождения
            answer.push_back(iteration - needleSize + 1);
        iteration++;
    }

    /*
    Выводим ответ
    */
    int answerSize = (int) answer.size();
    if (answerSize == 0){
        std::cout << "-1" << std::endl;
        return 0;
    }
    for (int i = 0; i < answerSize; i++){
        std::cout << answer[i];
        if (i + 1 != answerSize)
            std::cout << ",";
    }
    std::cout << std::endl;

    return 0;
}