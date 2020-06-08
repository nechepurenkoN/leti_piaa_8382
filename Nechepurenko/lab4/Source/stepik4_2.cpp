#include <vector>
#include <string>
#include <iostream>

int main(){
    std::string needle, haystack;
    std::cin >> needle;
    std::cin >> haystack;
    std::swap(needle, haystack);
    int needleSize = (int) needle.size();
    int haystackSize = (int) haystack.size();
    std::string str = needle + "@" + haystack;
    int expLen = needleSize+1+2*haystackSize;
    needle.clear();
    haystack.clear();
    std::vector<int> prefixFunction(expLen, 0);
    for (int i = 1; i < expLen; i++){
        int idx = (i >= needleSize + 1 + haystackSize) ? i - haystackSize : i;
        int k = prefixFunction[i-1];
        while (k > 0 && str[k] != str[idx]){
            k = prefixFunction[k-1];
        }
        if (str[idx] == str[k])
            k++;
        prefixFunction[i] = k;
    }
    std::cout << "Prefix function for merged string is:" << std::endl;
    for (auto el : prefixFunction) {
        std::cout << el << " ";
    }std::cout << std::endl;
    for (int i = needleSize; i < expLen; i++){
        if (prefixFunction[i] == needleSize){
            std::cout << "Rotated on: " << i - needleSize - haystackSize << std::endl;
            return 0;
        }
    }
    std::cout << "No rotation: " << -1 << std::endl;

    return 0;
}
