CXX      = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic

biblioteca: main.cpp biblioteca.hpp
	$(CXX) $(CXXFLAGS) -o biblioteca main.cpp

run: biblioteca
	./biblioteca

clean:
	rm -f biblioteca
