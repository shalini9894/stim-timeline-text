#include <pybind11/pybind11.h>

#include <stdexcept>

#include "render_timeline_text.h"

namespace py = pybind11;

PYBIND11_MODULE(_native, m) {
    m.doc() = "Tag-aware ASCII timeline diagrams for Stim circuits.";
    m.def(
        "render_timeline_text",
        [](const std::string &stim_program) -> std::string {
            try {
                return stim_timeline_text::render_timeline_text(stim_program);
            } catch (const std::invalid_argument &e) {
                throw py::value_error(e.what());
            }
        },
        py::arg("stim_program"),
        "Render a Stim circuit program as an ASCII timeline diagram.");
}
