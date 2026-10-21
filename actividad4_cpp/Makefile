CXX      = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic

personal: main.cpp personal_unap.hpp
	$(CXX) $(CXXFLAGS) -o personal main.cpp

run: personal
	./personal

clean:
	rm -f personal
