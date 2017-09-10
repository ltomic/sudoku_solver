class node {
	public:
		node *l, *r, *u, *d, *c;
		int rowid, columnid;
};

class column: public node {
	public:
		int sz, name;
};
