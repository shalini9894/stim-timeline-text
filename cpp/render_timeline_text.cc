#include "render_timeline_text.h"

#include <sstream>

#include "stim/circuit/circuit.h"
#include "stim/diagram/ascii_diagram.h"
#include "stim/diagram/timeline/timeline_ascii_drawer.h"

namespace stim_timeline_text {

std::string render_timeline_text(const std::string &stim_program) {
    stim::Circuit circuit(stim_program.c_str());
    auto diagram = stim_draw_internal::DiagramTimelineAsciiDrawer::make_diagram(circuit);
    std::stringstream out;
    out << diagram;
    return out.str();
}

}  // namespace stim_timeline_text
