#include <iostream>
#include <tuple>
#include <fstream>

using namespace std;

int sz, x, y, z, n;

tuple<int,int,int> info[1000];

int main() {
	ifstream F;
	F.open("info.txt");
	F >> sz;
	for (int i = 0; i < sz; ++i) {
		F >> x >> y >> z;
		info[i] = tuple<int,int,int>(x, y, z);
	}
	F.close();

	cin >> n;
	cout << n << endl;
	for (int i = 0; i < n; ++i) {
		cin >> x;
		auto t = info[x];
		cout << get<0>(t) << " " << get<1>(t) << " " << get<2>(t) << endl;
	}

	return 0;
}

