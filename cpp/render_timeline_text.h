#ifndef STIM_TIMELINE_TEXT_RENDER_H
#define STIM_TIMELINE_TEXT_RENDER_H

#include <string>

namespace stim_timeline_text {

/// Parses a Stim circuit program and renders it as an ASCII timeline diagram,
/// resolving tsim metadata tags to their logical gate names.
std::string render_timeline_text(const std::string &stim_program);

}  // namespace stim_timeline_text

#endif
