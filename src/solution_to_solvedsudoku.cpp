#include <iostream>
#include <fstream>

using namespace std;

int n, br, r, c;

string A;

using namespace std;

int main() {
	ifstream F;
	F.open("sudoku.txt");
	F >> A;
	F.close();

	cin >> n;
	for (int i = 0; i < n; ++i) {
		cin >> br >> r >> c;
		A[r*9+c] = br+1+'0';
	}

	cout << A;
	return 0;
}
