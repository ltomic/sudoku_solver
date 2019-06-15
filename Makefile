SRCDIR = src
BINDIR = bin

INCLUDE = -Iinclude -I.

SOURCES = $(wildcard $(SRCDIR)/*.cpp)
BINARIES = $(SOURCES:$(SRCDIR)/%.cpp=$(BINDIR)/%)

CXXFLAGS = -std=c++11
CPPFLAGS = $(INCLUDE)

dirs:
	mkdir -p $(BINDIR)


install: dirs $(BINARIES)

$(BINARIES): $(BINDIR)/%: $(SRCDIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) $^ -o $@


