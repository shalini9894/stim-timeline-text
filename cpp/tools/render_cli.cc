#include <iostream>
#include <sstream>

#include "render_timeline_text.h"

int main() {
    std::stringstream buf;
    buf << std::cin.rdbuf();
    std::cout << stim_timeline_text::render_timeline_text(buf.str());
    return 0;
}
