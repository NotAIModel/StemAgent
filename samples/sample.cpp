// Sample C++ code with intentional issues for the agent to review

#include <iostream>
#include <stdexcept>
#include <string>

// Issue: missing virtual destructor — deleting a Derived via a Base* leaks Derived's resources
class Base {
public:
    Base() {}
    ~Base() {}              // should be virtual ~Base()
    virtual void process() = 0;
};

class Derived : public Base {
public:
    int* data;

    Derived(int size) {
        data = new int[size];   // Issue: raw new — ownership is unclear, no RAII
    }

    ~Derived() {
        delete[] data;          // never reached if deleted through Base*
    }

    void process() override {
        std::cout << "processing" << std::endl;
    }
};


// Issue: buffer overflow — no bounds check before writing into fixed-size buffer
void copy_input(const std::string& input) {
    char buf[16];
    for (size_t i = 0; i < input.size(); i++) {  // writes past buf if input.size() > 16
        buf[i] = input[i];
    }
    std::cout << buf << std::endl;
}


// Issue: raw pointer parameter — caller and callee share no ownership contract
void print_value(int* ptr) {
    std::cout << *ptr << std::endl;   // no null check, no indication of who owns ptr
}


// Issue: unhandled exception — risky_operation can throw but caller ignores it
void risky_operation() {
    throw std::runtime_error("something went wrong");
}

void run_pipeline() {
    risky_operation();   // exception propagates uncaught; program will terminate
}


int main() {
    // Issue: memory leak — Derived allocated on heap, Base* used for deletion,
    // but ~Base() is not virtual so ~Derived() is never called
    Base* obj = new Derived(64);
    obj->process();
    delete obj;          // calls ~Base(), skips ~Derived() — data[] is leaked

    copy_input("this string is definitely longer than sixteen characters");

    int x = 42;
    print_value(&x);

    run_pipeline();

    return 0;
}
