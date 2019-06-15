#include <iostream>
#include <tuple>
#include <cstdio>
#include <fstream>

using namespace std;

const int n = 9, rn = 3, MAXN = 16;

string A[MAXN];
bool red[MAXN][MAXN], stupac[MAXN][MAXN], mjesto[MAXN][MAXN], regija[MAXN][MAXN];
int col[MAXN][MAXN][MAXN];
tuple<int,int,int> info[n*n*n];
string mat[n*n*n];
int sz, colcnt[4];

void read() {
	char x;
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j) {
			cin >> x;
			A[i] += x;
		}
	}
}

void create_column_by_rule(int ind, bool rule[][MAXN]) {
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
			col[ind][i][j] = rule[i][j] ? -1 : colcnt[ind]++;
}

void create_columns() {
	create_column_by_rule(0, mjesto);
	create_column_by_rule(1, red);
	create_column_by_rule(2, stupac);
	create_column_by_rule(3, regija);
}

int main() {
	read();
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j) {
			if (A[i][j] != '0') {
				mjesto[i][j] = 1;
				red[i][A[i][j]-'0'-1] = 1;
				stupac[A[i][j]-'0'-1][j] = 1;
				regija[A[i][j]-'0'-1][(i/rn)*rn+j/rn] = 1;
			}
		}
	}

	create_columns();
	for (int i = 0; i < n*n*n; ++i) {
		for (int j = 0; j < colcnt[0]+colcnt[1]+colcnt[2]+colcnt[3]; ++j) {
			mat[i] += "0";
		}
	}

	for (int i = 0; i < n; ++i) { // broj
		for (int j = 0; j < n; ++j) { // redak 
			for (int k = 0; k < n; ++k) { // stupac
				if (mjesto[j][k]) continue;
				if (red[j][i]) continue;
				if (stupac[i][k]) continue;
				if (regija[i][(j/rn)*rn+k/rn]) continue;
				info[sz] = tuple<int,int,int>(i, j, k);
				mat[sz][col[0][j][k]] = '1';
				mat[sz][colcnt[0]+col[1][j][i]] = '1';
				mat[sz][colcnt[0]+colcnt[1]+col[2][i][k]] = '1';
				mat[sz][colcnt[0]+colcnt[1]+colcnt[2]+col[3][i][(j/rn)*rn+k/rn]] = '1';
				sz++;
			}
		}
	}
	
	cout << sz << " " << colcnt[0]+colcnt[1]+colcnt[2]+colcnt[3] << endl;
	for (int i = 0; i < sz; ++i) {
		cout << mat[i] << endl;
	}
	
	ofstream F;
	F.open("info.txt");
	F << sz << endl;
	for (int i = 0; i < sz; ++i) {
		auto tmp = info[i];
		F << get<0>(tmp) << " " << get<1>(tmp) << " " << get<2>(tmp) << endl;
	}
	F.close();

	return 0;
}


