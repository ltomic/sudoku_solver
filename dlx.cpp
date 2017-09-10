#include <cstdio>
#include <cstdlib>

#include "matrix.h"

const int MAXN = 1000, MAXM = 1000, INF = 1e9;

node node_buff[MAXN*MAXM];
node *node_alk = node_buff;

column col_buff[MAXM];

column master;

node *O[MAXN];

char A[MAXN][MAXM];

// makni stupac i redove u kojima su mu jedinice
void cover_column(column *c) {
	c->r->l = c->l;
	c->l->r = c->r;
	for (node *i = c->d; i != c; i = i->d) {
		for (node *j = i->r; j != i; j = j->r) {
			j->d->u = j->u;
			j->u->d = j->d;
			((column*)j->c)->sz = (int)((column*)j->c)->sz - 1;
		}
	}
}

void uncover_column(column *c) {
	printf("UNCOVERING: %d\n", c->name);
	for (node *i = c->u; i != c; i = i->u) {
		printf("VRTIM %d %d, %d %d\n", i->rowid, i->columnid, i->l->rowid, i->l->columnid);
		for (node *j = i->l; j != i; j = j->l) {
			printf("VRACAM U STUPCU: %d\n", ((column*)j->c)->name);
			((column*)j->c)->sz = ((column*)j->c)->sz + 1;
			j->d->u = j;
			j->u->d = j;
		}
	}
	c->r->l = c;
	c->l->r = c;
	printf("GOTOV UNCOVERING\n");
}

void print(int br) {
	FILE *sol;
	sol = fopen("rows.txt", "w");
	fprintf(sol, "%d\n", br);
	for (int i = 0; O[i] != NULL; ++i) {
		fprintf(sol, "%d ", O[i]->rowid);
	}
	fprintf(sol, "\n");
	fclose(sol);
}

void print_columns() {
	printf("ACTIVE COLUMNS: ");
	for (column *i = (column*)master.r; i != &master; i = (column*)i->r) {
		printf("%d ", i->name);
	}
	printf("\n");
}

void search(int k) {
	printf("USAO:%d\n", k);
	// rijeseni svi stupci
	if ((column*)master.r == &master) {
		printf("NASAO\n");
		print(k);
		exit(0);
	}
	// nadi stupac s najmanjim brojem jedinica
	print_columns();
	column *c = NULL;
	int mn = INF;
	for (column *i = (column*)master.r; i != &master; i = (column*)i->r) {
		if (i->sz < mn) {
			c = i;
			mn = i->sz;
		}
	}
	
	if (c == NULL) return;
	printf("\nCHOSE:%d %d\n", k, c->name);
	cover_column(c);
	print_columns();

	int cnt = 0;
	for (node *i = c->d; i != c; i = i->d) {
		printf("ROKA %d %d\n", ((column*)i->c)->name, cnt);
		cnt++;
		O[k] = i;
		for (node *j = i->r; j != i; j = j->r) {
			cover_column((column*)j->c); 
		}
		print_columns();
		search(k+1);
		for (node *j = i->l; j != i; j = j->l) {
			uncover_column((column*)j->c); 
		}
	}
	O[k] = NULL;
	uncover_column(c);
	print(k);
	print_columns();
	printf("IZASAO\n");
}

int main() {
	int n, m;
	scanf("%d%d", &n, &m);
	for (int i = 0; i < n; ++i) {
			scanf("%s", A[i]);
	}

	column *t = col_buff;
	t->name = 0;
	t->rowid = -1;
	t->columnid = 0;
	master.l = t;
	master.r = t;
	t->r = &master;
	t->l = &master;
	t->u = t;
	t->d = t;
	for (int i = 1; i < m; ++i) {
		t = col_buff+i;
		t->name = i;
		t->columnid = i;
		t->u = t;
		t->d = t;
		t->l = col_buff+i-1;
		t->r = col_buff[i-1].r;
		t->r->l = t;
		col_buff[i-1].r = t;
	}

	node *prev = node_alk++;
	prev->l = prev;
	prev->r = prev;
	for (int i = 0; i < n; ++i) {
		bool flag = 0;
		for (int j = 0; j < m; ++j) {
			if (A[i][j] == '1') {
				t = col_buff+j;
				t->sz = t->sz + 1;
				node *curr = flag ? node_alk++ : prev;
				curr->rowid = i;
				curr->columnid = j;
				curr->c = t;
				
				curr->u = t->u;
				t->u->d = curr;
				t->u = curr;
				curr->d = t;
				
				curr->l = prev;
				curr->r = prev->r;
				prev->r->l = curr;
				prev->r = curr;
				
				flag = 1;
			}
		}
		if (flag) prev = node_alk++;
		prev->l = prev;
		prev->r = prev;
	}
		
	search(0);
	print(-1);
	printf("NISAM NASAO\n");
	return 0;
}
